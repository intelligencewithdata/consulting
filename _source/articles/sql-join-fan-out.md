---
slug: insights-sql-join-fan-out
title: Why your SQL totals are too high: the join fan-out problem
dek: A single join can quietly double your revenue figures. Learn how to spot join fan-out in SQL, why DISTINCT doesn't fix it, and three reliable patterns that do.
category: SQL
author: thomas-forrester
audience: consulting
date: 2026-11-13
---

One of the most common reasons a report "doesn't match finance" has nothing to do with bad data. The data is fine. The query joined two tables in a way that **counted the same rows more than once**, and every total built on top of it is inflated.

This is called **join fan-out**. It produces no error and no warning. The query runs, the numbers look plausible, and they can be wrong by a factor of two or three. Because it often appears when someone adds "just one more column" to an existing query, it can creep into a report that used to be correct.

This article explains what fan-out is, how to check for it in a few seconds, and the patterns we use to make sure totals stay right.

## What fan-out looks like

Take three small tables that most businesses have in some form:

```sql
customers (customer_id, name, region)
orders    (order_id, customer_id, order_date, amount)
contacts  (contact_id, customer_id, email, is_primary, created_date)
```

Our sample has five orders worth **£1,700** in total. One customer has three contacts on file, another has two.

Now someone wants revenue alongside a contact email, so they join orders to contacts:

```sql
SELECT SUM(o.amount) AS revenue
FROM orders AS o
INNER JOIN contacts AS ct
        ON ct.customer_id = o.customer_id;
```

The result is **£3,800**, more than double the true figure.

The reason is simple once you see it. A join returns one row for **every matching pair**. An order for a customer with three contacts matches three contact rows, so that order appears three times and its amount is added three times. Nothing is broken; the query is doing exactly what it was asked to do.

The underlying problem is **grain**: the level of detail one row represents. The orders table has one row per order. The contacts table has one row per contact, and there can be several per customer. Joining them produces a result at neither grain, and summing it double counts.

## How to spot it in seconds

You don't need to stare at the output to catch fan-out. Two quick checks do the job.

**Check 1: compare row counts before and after the join.** If the number of rows grows but the number of distinct orders doesn't, rows are being duplicated:

```sql
SELECT COUNT(*) AS rows_after_join,
       COUNT(DISTINCT o.order_id) AS distinct_orders
FROM orders AS o
INNER JOIN contacts AS ct
        ON ct.customer_id = o.customer_id;
```

In our sample this returns 11 rows but only 5 distinct orders. That gap is the fan-out.

**Check 2: confirm the join key is unique on the side you're joining to.** If the table you're adding has more than one row per key, it will multiply the other side:

```sql
SELECT customer_id, COUNT(*) AS rows_per_customer
FROM contacts
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

Any rows returned here mean that joining on `customer_id` will repeat orders. It's worth running this check whenever you join to a table you didn't design yourself.

## Why DISTINCT doesn't fix it

The tempting fix is to add `DISTINCT`, or to write `SUM(DISTINCT amount)`. **Don't.** `SUM(DISTINCT ...)` removes duplicate *values*, not duplicate *rows*.

```sql
SELECT SUM(DISTINCT o.amount) AS revenue
FROM orders AS o
INNER JOIN contacts AS ct
        ON ct.customer_id = o.customer_id;
```

In our sample this returns £1,450, not £1,700, because two genuinely different orders both happen to be worth £250. One of them is thrown away. The figure is now too low instead of too high, and it will change unpredictably as new orders arrive.

`SELECT DISTINCT` on the detail rows has a similar weakness: it only works if the columns you select happen to make each row unique, and it hides the real problem rather than solving it. The fixes below deal with grain directly.

## Fix 1: join to exactly one row

If you only need one contact per customer, make sure the join can only ever find one. Where the data has a reliable flag, filter on it in the join:

```sql
SELECT o.order_id, o.amount, ct.email
FROM orders AS o
LEFT JOIN contacts AS ct
       ON ct.customer_id = o.customer_id
      AND ct.is_primary = 1
ORDER BY o.order_id;
```

That is only safe if the data guarantees **one primary contact per customer**. If it doesn't, rank the rows and keep the first. `ROW_NUMBER` numbers the rows within each customer, so `rn = 1` can only ever match once:

```sql
WITH ranked_contacts AS (
    SELECT customer_id, email,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY is_primary DESC, created_date
           ) AS rn
    FROM contacts
)
SELECT o.order_id, o.amount, rc.email
FROM orders AS o
LEFT JOIN ranked_contacts AS rc
       ON rc.customer_id = o.customer_id
      AND rc.rn = 1
ORDER BY o.order_id;
```

This prefers the primary contact, then the oldest one. Every order now appears exactly once, and the total is back to £1,700. Using `LEFT JOIN` also keeps orders for customers with no contact at all.

## Fix 2: use EXISTS when you're only filtering

Sometimes the second table is only there to filter, for example "revenue from customers who have a contact at a particular domain". You don't need any of its columns, so don't join to it. Use `EXISTS`, which checks for at least one match without repeating rows:

```sql
SELECT SUM(o.amount) AS revenue
FROM orders AS o
WHERE EXISTS (
    SELECT 1
    FROM contacts AS ct
    WHERE ct.customer_id = o.customer_id
      AND ct.email LIKE '%@acme.example'
);
```

However many matching contacts a customer has, each order is counted once.

## Fix 3: aggregate before you join

The most damaging version of fan-out happens when you join **two child tables** to the same parent, such as orders and refunds per customer:

```sql
SELECT c.name,
       SUM(o.amount) AS revenue,
       SUM(r.amount) AS refunded
FROM customers AS c
LEFT JOIN orders  AS o ON o.customer_id = c.customer_id
LEFT JOIN refunds AS r ON r.customer_id = c.customer_id
GROUP BY c.name
ORDER BY c.name;
```

A customer with two orders and two refunds produces four rows, so both figures are doubled. In our sample, one customer's £800 of revenue is reported as £1,600 and £80 of refunds as £160.

The fix is to **summarise each child table to one row per customer first**, then join the summaries:

```sql
WITH order_totals AS (
    SELECT customer_id, SUM(amount) AS revenue
    FROM orders
    GROUP BY customer_id
),
refund_totals AS (
    SELECT customer_id, SUM(amount) AS refunded
    FROM refunds
    GROUP BY customer_id
)
SELECT c.name,
       COALESCE(ot.revenue, 0)  AS revenue,
       COALESCE(rt.refunded, 0) AS refunded,
       COALESCE(ot.revenue, 0) - COALESCE(rt.refunded, 0) AS net_revenue
FROM customers AS c
LEFT JOIN order_totals  AS ot ON ot.customer_id = c.customer_id
LEFT JOIN refund_totals AS rt ON rt.customer_id = c.customer_id
ORDER BY c.name;
```

Each common table expression (CTE) has one row per customer, so the joins are one-to-one and nothing is repeated. `COALESCE` turns a missing summary into zero, so a customer with no refunds shows £0 rather than an empty value that would also make `net_revenue` empty.

These queries use standard SQL and run as written in SQL Server, PostgreSQL and SQLite.

## Build the habit into your reporting

Fan-out is easiest to prevent when it's part of how queries are written and reviewed, not something you hunt for after a board pack goes out. A few habits help:

- **State the grain** of every query in a comment: "one row per order", "one row per customer per month".
- **Know which side of each join is unique.** If neither side is, stop and aggregate first.
- **Reconcile a headline total** against a simple query on the base table, such as `SELECT SUM(amount) FROM orders`, whenever a query changes.
- **Treat a sudden jump** after a report change as a possible join problem before treating it as good news.

## The bottom line

When SQL totals come out too high, the cause is very often a join that matched one row to many. Check row counts before and after the join, confirm the key is unique on the side you're joining to, and resist the quick fix of `DISTINCT`.

Instead, join to exactly one row, use `EXISTS` when you're only filtering, and aggregate child tables before joining them together. Those three patterns keep each row counting once, so the figures in your reports match the figures in your finance system.
