---
slug: insights-sql-null-values
title: NULL in SQL: six mistakes that quietly skew your results
dek: NULL isn't zero and it isn't blank. Learn how it behaves in filters, joins, averages and groupings, and the simple fixes that keep your query results honest.
category: SQL
author: jayne-carter
audience: training
date: 2026-10-23
---

Most SQL mistakes announce themselves with an error message. Mistakes involving `NULL` don't. The query runs, the numbers look reasonable, and nobody notices that a handful of rows have silently dropped out of the result.

If you're learning SQL for a data role, understanding `NULL` is one of the quickest ways to make your work more reliable.

This article covers six common mistakes, why each one happens and how to fix it. Every example uses two small tables:

```sql
customers (customer_id, name, region)
orders    (order_id, customer_id, amount, discount, status)
```

Some customers have no `region`, some orders have no `discount` or `status`, and one order has no `customer_id`.

## What NULL actually means

`NULL` means **"no value is known"**. It is not zero, and it is not an empty piece of text. An order with a `NULL` discount hasn't been given a discount of zero; the database simply doesn't know what the discount was.

Because the value is unknown, SQL can't say whether a `NULL` equals anything, including another `NULL`. A comparison involving `NULL` doesn't come out as true or false. It comes out as **unknown**, and a `WHERE` clause only keeps rows where the condition is true. That one rule explains almost every mistake below.

## 1. Using = NULL instead of IS NULL

The most natural way to find orders with no status looks like this:

```sql
SELECT order_id
FROM orders
WHERE status = NULL;
```

It returns **no rows**, even when plenty of orders have no status. `status = NULL` is unknown for every row, so nothing passes the filter. Microsoft's documentation for SQL Server says the same: with the standard `ANSI_NULLS` behaviour, `WHERE column_name = NULL` returns zero rows. From SQL Server 2017 onwards that standard behaviour is always on.

Use the dedicated operators instead:

```sql
SELECT order_id
FROM orders
WHERE status IS NULL;
```

The opposite test is `IS NOT NULL`. Never write `<> NULL` either; it also returns nothing.

## 2. "Not equal" filters quietly drop NULLs

Suppose you want every order that wasn't cancelled:

```sql
SELECT order_id, status
FROM orders
WHERE status <> 'Cancelled';
```

This looks right, but orders with no status are missing from the result. For those rows, `status <> 'Cancelled'` is unknown, not true, so they are filtered out. If those orders were genuine sales still waiting for a status update, your revenue figure is now too low.

Decide what you want to happen to the unknowns and **say it explicitly**:

```sql
SELECT order_id, status
FROM orders
WHERE status <> 'Cancelled'
   OR status IS NULL;
```

This mistake is worth remembering whenever you use `<>`, `NOT LIKE` or `NOT BETWEEN` on a column that allows `NULL`.

## 3. NOT IN returns nothing when the list contains a NULL

A classic question: which customers have never placed an order? Many people reach for `NOT IN`:

```sql
SELECT name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```

In our sample data this returns **no rows at all**, even though one customer has never ordered. The reason is the order with a `NULL` customer ID. `NOT IN` checks that the value differs from every item in the list, and "differs from `NULL`" is unknown. One unknown is enough to stop any row qualifying.

`NOT EXISTS` doesn't have this problem, because it simply asks whether a matching row exists:

```sql
SELECT c.name
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
);
```

A `LEFT JOIN` with `WHERE o.order_id IS NULL` works too. Either way, make **`NOT EXISTS` your default** for "find what's missing" questions.

## 4. Averages ignore NULLs, which may not be what you want

Aggregate functions such as `SUM`, `AVG`, `MIN` and `MAX` skip `NULL` values. Microsoft's documentation puts it plainly: except for `COUNT(*)`, aggregate functions ignore `NULL` values.

That makes sense for totals, but it changes what an average means:

```sql
SELECT AVG(discount)              AS avg_ignoring_nulls,
       AVG(COALESCE(discount, 0)) AS avg_treating_null_as_zero,
       COUNT(discount)            AS orders_with_discount,
       COUNT(*)                   AS all_orders
FROM orders;
```

In our sample, three of five orders have a discount recorded (20, 0 and 10). The first average is **10**, the average of the known discounts. The second is **6**, because the two unknowns are counted as zero discount.

Neither answer is wrong. They answer different questions, and you need to know which one your stakeholder is asking. `COALESCE` returns the first value in its list that isn't `NULL`, so `COALESCE(discount, 0)` swaps unknowns for zero. Only do that when zero is a fair assumption.

One more surprise: if every value is `NULL`, `SUM` returns `NULL`, not 0. Wrap it in `COALESCE(SUM(discount), 0)` if a report needs a number.

## 5. One NULL turns a whole calculation into NULL

Arithmetic with an unknown value gives an unknown answer:

```sql
SELECT order_id,
       amount - discount              AS net_amount,
       amount - COALESCE(discount, 0) AS net_amount_fixed
FROM orders;
```

Every order with no discount gets a `NULL` net amount in the first column. If you then total that column, those orders vanish from the sum without warning. The second column treats a missing discount as no discount and gives a value for every row.

Text behaves the same way. In SQL Server, joining strings with `+` gives `NULL` if any part is `NULL`; Microsoft's documentation shows `'abc' + NULL` returning `NULL`. The `CONCAT` function is more forgiving, because it converts `NULL` arguments to empty strings. SQLite and PostgreSQL use `||` for joining text, which also returns `NULL` when a part is missing.

SQL Server also has `ISNULL(column, replacement)`, which takes exactly two arguments. `COALESCE` is part of standard SQL and accepts a longer list, so it's the more portable habit.

## 6. NULLs group together and sort to the top

When you `GROUP BY` a column, every `NULL` lands in **one group**. Microsoft's documentation for SQL Server confirms that all `NULL` values in a grouping column are treated as equal and collected into a single group.

```sql
SELECT region, COUNT(*) AS customers
FROM customers
GROUP BY region
ORDER BY region;
```

The result includes a row with a blank region. On a chart it often appears as "(Blank)" or an empty label, and people ask what it means. Give it a clear name instead:

```sql
SELECT COALESCE(region, 'Unknown') AS region,
       COUNT(*) AS customers
FROM customers
GROUP BY COALESCE(region, 'Unknown')
ORDER BY region;
```

Sorting matters too. In SQL Server and SQLite, `NULL` is treated as the lowest possible value, so it appears **first** in an ascending sort and last in a descending one. Other databases differ, so check before relying on the order.

## A quick NULL checklist

Before you share a query result, run through these questions:

- **Filters:** am I using `IS NULL` / `IS NOT NULL`, and do my `<>` filters handle unknowns deliberately?
- **Missing records:** have I used `NOT EXISTS` rather than `NOT IN` with a subquery?
- **Averages:** should unknown values be ignored or treated as zero?
- **Calculations:** could a single `NULL` blank out a derived column?
- **Groups:** does a "blank" group need a proper label?

A useful habit is to count the gaps before you start. `COUNT(*) - COUNT(column)` tells you how many `NULL` values a column holds, so you know how much each of these decisions matters.

## The bottom line

`NULL` means unknown, and SQL handles unknowns cautiously: comparisons with them are never true, aggregates skip them and calculations pass them along. None of that produces an error, which is exactly why it catches people out.

The fixes are small: `IS NULL` instead of `= NULL`, `NOT EXISTS` instead of `NOT IN`, and `COALESCE` when you have consciously decided what an unknown should become. Build those habits now and your results will hold up when someone checks them.
