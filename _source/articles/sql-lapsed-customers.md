---
slug: insights-sql-lapsed-customers
title: Find customers who've stopped buying with one SQL query
dek: A simple SQL query that sorts every customer into active, at risk, lapsed or never ordered, so you know who to contact before they're gone for good.
category: SQL
author: thomas-forrester
audience: consulting
date: 2026-11-27
---

Most businesses can tell you how many customers bought last month. Far fewer can tell you which regular customers **quietly stopped buying** three or six months ago. Those customers rarely announce that they've gone. They just stop appearing in the sales figures.

If your orders are stored in a database, you can answer that question with one query. It needs nothing more advanced than `GROUP BY`, a `LEFT JOIN` and a `CASE` expression.

This article builds the query step by step, points out the two mistakes that make the results look better than they are, and shows how to turn it into a short list your team can act on.

## In short

- Find each customer's **most recent completed order** with `MAX(order_date)` and `GROUP BY`.
- Start from the **customer list with a LEFT JOIN**, so customers who have never ordered aren't missed.
- Put the status filter in the **join condition, not WHERE**, or the never-ordered customers disappear.
- Use `CASE` to give every customer **one clear status**: active, at risk, lapsed or never ordered.

## The idea: one row per customer

Your order data has **one row per order**. To spot lapsed customers you need **one row per customer**, showing the date they last bought. Once you have that date, sorting customers into groups is simple.

The examples use two small tables:

```sql
customers (customer_id, name)
orders    (order_id, customer_id, order_date, amount, status)
```

Each order has a status of `Complete` or `Cancelled`. We'll pretend we are running the check on **1 December 2026** and use these groups:

[[fig:sql-lapsed-bands]]

The three-month and six-month windows are only a starting point. A café's regulars might buy every week, while a business customer might reorder twice a year. **Choose windows that match how often your customers normally buy**, and agree them with whoever will act on the list.

## Step 1: find each customer's last order

Start with the orders table on its own. `MAX` on a date column returns the latest date, and `GROUP BY` gives you one row for each customer:

```sql
SELECT customer_id,
       MAX(order_date) AS last_order_date,
       COUNT(*)        AS order_count,
       SUM(amount)     AS total_spend
FROM orders
WHERE status = 'Complete'
GROUP BY customer_id;
```

The `WHERE` clause matters. Without it, a cancelled order counts as recent activity. In our sample data, one customer placed an order in October and then cancelled it. Counting that order would label her **active** when she hasn't completed a purchase since April.

This query has a blind spot, though. It only sees customers who appear in the orders table. Anyone who signed up but **never completed an order** is missing entirely.

## Step 2: start from the customer list

To include every customer, start from the `customers` table and use a `LEFT JOIN` to bring in their orders. Customers with no matching orders are kept, with `NULL` in the order columns:

```sql
SELECT c.customer_id,
       c.name,
       MAX(o.order_date) AS last_order_date,
       COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
      AND o.status = 'Complete'
GROUP BY c.customer_id, c.name;
```

Two details make this work:

1. **`COUNT(o.order_id)` instead of `COUNT(*)`.** `COUNT(*)` counts rows, so a customer with no orders would still show 1. Counting a column from the orders table skips the `NULL` and correctly shows 0.
2. **The status filter is in the `ON` clause.** This is the mistake that catches most people, so it gets its own section.

## The mistake that hides your never-ordered customers

It feels natural to filter cancelled orders in a `WHERE` clause, as we did in step 1:

```sql
SELECT c.customer_id,
       c.name,
       MAX(o.order_date) AS last_order_date,
       COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
WHERE o.status = 'Complete'
GROUP BY c.customer_id, c.name;
```

This query runs without any error, but it quietly drops every customer who has never ordered. **`WHERE` runs after the join.** For those customers, `o.status` is `NULL`, and `NULL = 'Complete'` is not true, so the row is filtered out. Your `LEFT JOIN` now behaves like an `INNER JOIN`.

Moving the condition into `ON` changes its meaning. It now says "only join completed orders", and customers without any are still kept. When you filter the right-hand table of a `LEFT JOIN`, **the filter belongs in `ON`**.

## Step 3: give every customer a status

Now wrap the query in a common table expression (CTE) and add a `CASE` expression. `CASE` checks each condition in order and uses the first one that is true, so the order of the lines matters:

```sql
WITH last_orders AS (
    SELECT c.customer_id,
           c.name,
           MAX(o.order_date) AS last_order_date,
           COUNT(o.order_id) AS order_count
    FROM customers AS c
    LEFT JOIN orders AS o
           ON o.customer_id = c.customer_id
          AND o.status = 'Complete'
    GROUP BY c.customer_id, c.name
),
banded AS (
    SELECT name,
           last_order_date,
           order_count,
           CASE
               WHEN last_order_date IS NULL         THEN 'Never ordered'
               WHEN last_order_date >= '2026-09-01' THEN 'Active'
               WHEN last_order_date >= '2026-06-01' THEN 'At risk'
               ELSE 'Lapsed'
           END AS customer_status
    FROM last_orders
)
SELECT name, last_order_date, order_count, customer_status
FROM banded
ORDER BY last_order_date;
```

The `NULL` check comes first. If it came later, a missing date would fail every comparison and fall through to `ELSE`, and a never-ordered customer would be labelled **lapsed**. Those are two different conversations, so keep them apart.

[[fig:sql-lapsed-shape]]

## Make the dates move on their own

Typing cut-off dates by hand is fine for a one-off check, but a report you run every month should **work out the dates itself**.

In SQL Server, or a Microsoft Fabric warehouse, use `DATEADD`. Its arguments are the date part, the number to add and the starting date. Microsoft's documentation notes that `GETDATE()` returns the current date **and time**, so convert it to a `date` first:

```sql
DECLARE @run_date date = CAST(GETDATE() AS date);

-- inside the CASE expression:
WHEN last_order_date >= DATEADD(month, -3, @run_date) THEN 'Active'
WHEN last_order_date >= DATEADD(month, -6, @run_date) THEN 'At risk'
```

If you also want a "days since last order" column, SQL Server's `DATEDIFF(day, last_order_date, @run_date)` gives it. Be aware that `DATEDIFF` counts **boundaries crossed** rather than complete periods, so `DATEDIFF(month, ...)` between 31 January and 1 February returns 1. Day-level differences avoid that surprise.

Other databases use different date functions. SQLite, for example, uses `date('now', '-3 months')`. The structure of the query stays the same.

## Turn it into a list people can use

A one-line summary is useful for a management meeting. Replace the final `SELECT` with a count by status:

```sql
SELECT customer_status,
       COUNT(*) AS customers
FROM banded
GROUP BY customer_status
ORDER BY customers DESC;
```

For the team who will pick up the phone, the detailed list matters more. A few practical points:

1. **Add value to the list.** Include `total_spend` from step 1 so the team calls high-value at-risk customers first.
2. **Act on "at risk", not just "lapsed".** A customer who stopped buying four months ago is easier to win back than one who left a year ago.
3. **Track the counts over time.** If the at-risk group grows month after month, that is an early warning worth investigating.
4. **Feed it into your reporting.** The same query can sit behind a Power BI report, so the list refreshes without anyone rerunning it.

## The bottom line

Lapsed customers don't show up as a problem in a sales total. They show up as an absence. One query that finds **each customer's last completed order**, starting from the **full customer list**, and sorts the results with **`CASE`** turns that absence into a named list.

Watch the two traps: filter cancelled orders in the **`ON` clause**, and check for **`NULL` dates first**. Get those right and you'll have a dependable, repeatable view of who has stopped buying, while there is still time to do something about it.
