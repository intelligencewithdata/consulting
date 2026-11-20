---
slug: insights-sql-order-of-execution
title: SQL order of execution: why your query doesn't run top to bottom
dek: SQL reads your query in a different order from the one you type. Learn that order and you'll understand alias errors, WHERE vs HAVING and where LIMIT really applies.
category: SQL
author: jayne-carter
audience: training
date: 2026-11-20
---

You write a SQL query from the top down: `SELECT`, then `FROM`, then `WHERE`. It is natural to assume the database works through it in the same order. It doesn't, and that gap explains some of the most confusing errors beginners meet.

Once you know the order SQL actually uses, messages like "invalid column name" stop being a mystery. You also start to see why `WHERE` and `HAVING` both exist, and why sorting happens before the first few rows are kept.

This article walks through that order with one small table and shows the fixes for the mistakes it causes.

## In short

- SQL works out `FROM` first and `SELECT` almost last, so **aliases from SELECT aren't available in WHERE, GROUP BY or HAVING**.
- **WHERE filters rows before grouping; HAVING filters groups after grouping.**
- `ORDER BY` runs after `SELECT`, so it **can** use your aliases.
- `TOP` and `LIMIT` come last, so they keep the first rows **after** sorting.

## The order you write vs the order SQL reads

Microsoft's documentation for the `SELECT` statement in SQL Server sets out a **logical processing order**. It lists `FROM`, `ON`, `JOIN`, `WHERE`, `GROUP BY`, `WITH CUBE` or `WITH ROLLUP`, `HAVING`, `SELECT`, `DISTINCT`, `ORDER BY` and finally `TOP`.

The documentation explains why this matters: the order decides **when something defined in one step becomes available to later steps**. Tables named in `FROM` can be used everywhere after it. Column aliases defined in `SELECT` can't be used by the clauses that come before it, but they can be used by later ones such as `ORDER BY`.

[[fig:sql-logical-order]]

The examples below use one table of orders:

```sql
orders (order_id, customer_id, region, quantity, unit_price, status)
```

Each order has a region, a quantity, a unit price and a status of `Complete` or `Cancelled`.

## Why your alias doesn't work in WHERE

Say you want every order worth more than 100. You calculate the value, give it a friendly name, and filter on that name:

```sql
SELECT order_id, quantity * unit_price AS order_value
FROM orders
WHERE order_value > 100;
```

SQL Server rejects this query with an error. **`WHERE` is processed before `SELECT`**, so at the point SQL filters the rows, `order_value` hasn't been created yet.

Be aware that some databases are more relaxed. SQLite, for example, accepts this query. Don't rely on that: the same code will fail when you move it to SQL Server or a Fabric warehouse, and anyone reading it may assume it is portable.

There are two reliable fixes. The first is to **repeat the calculation** in the filter:

```sql
SELECT order_id, quantity * unit_price AS order_value
FROM orders
WHERE quantity * unit_price > 100;
```

The second, which is tidier when the calculation is long, is to **calculate it in a CTE** and filter in the next step. By the time the outer query runs, `order_value` is a real column:

```sql
WITH order_values AS (
    SELECT order_id, quantity * unit_price AS order_value
    FROM orders
)
SELECT order_id, order_value
FROM order_values
WHERE order_value > 100;
```

Both return the same four orders. Use whichever your team finds easier to read, and stick to it.

## WHERE vs HAVING: filtering before or after grouping

`WHERE` and `HAVING` both filter, so beginners often wonder why SQL needs two of them. The processing order gives the answer: **they run at different times**.

`WHERE` runs before `GROUP BY`, so it works on individual rows. `HAVING` runs after `GROUP BY`, so it works on whole groups and can use totals such as `SUM` or `COUNT`.

If you try to filter on a total in `WHERE`, the query fails, because the groups don't exist yet:

```sql
SELECT region, SUM(quantity * unit_price) AS sales
FROM orders
WHERE SUM(quantity * unit_price) > 200
GROUP BY region;
```

Put each filter where it belongs instead. Here, cancelled orders are removed row by row, and then regions with sales of 200 or less are removed as groups:

```sql
SELECT region, SUM(quantity * unit_price) AS sales
FROM orders
WHERE status = 'Complete'
GROUP BY region
HAVING SUM(quantity * unit_price) > 200;
```

[[fig:sql-where-having]]

Notice that `HAVING` repeats `SUM(quantity * unit_price)` rather than using the alias `sales`. That follows the same rule as before: `HAVING` comes before `SELECT`, so the alias doesn't exist yet in SQL Server.

A useful habit: **if a filter doesn't need a total, put it in WHERE**. Removing rows before grouping makes the intent of the query clearer.

## Why ORDER BY can use aliases

`ORDER BY` is one of the last steps, after `SELECT`. By then the alias exists, so this works:

```sql
SELECT customer_id, SUM(quantity * unit_price) AS sales
FROM orders
WHERE status = 'Complete'
GROUP BY customer_id
ORDER BY sales DESC
LIMIT 3;
```

This is a common source of confusion. Learners see an alias work in `ORDER BY` and expect it to work in `WHERE`. Once you picture the processing order, the difference makes sense.

## TOP and LIMIT keep the first rows after sorting

The query above returns the **top three customers by sales**. That only works because `LIMIT` is applied after `ORDER BY`. SQL sorts every customer first and then keeps the first three.

`LIMIT` is used by databases such as SQLite. SQL Server uses `TOP` at the start of the query instead, but the logic is the same: it comes last in the processing order.

```sql
SELECT TOP (3) customer_id, SUM(quantity * unit_price) AS sales
FROM orders
WHERE status = 'Complete'
GROUP BY customer_id
ORDER BY sales DESC;
```

If you leave out `ORDER BY`, you get three rows but **no guarantee which three**. Always pair `TOP` or `LIMIT` with an `ORDER BY` when the choice of rows matters.

## Logical order is not the same as physical order

One point is easy to misread. The logical processing order describes **how SQL makes names and results available** to each clause. It is not a promise about the steps the engine physically carries out.

Microsoft's documentation says the query processor decides the actual physical execution, and that this may differ from the list. The engine is free to arrange the work to run faster, so use the logical order to reason about **what your query means**, not how quickly it runs.

## A quick checklist when a query fails

When a query throws an error or returns something unexpected, work through these steps:

1. **Read the query in processing order**, starting from `FROM`, not from `SELECT`.
2. **Check every alias.** Is it used in `WHERE`, `GROUP BY` or `HAVING`? If so, repeat the calculation or move it into a CTE.
3. **Check every filter.** Does it use a total such as `SUM` or `COUNT`? It belongs in `HAVING`. Otherwise it belongs in `WHERE`.
4. **Check TOP or LIMIT.** Is there an `ORDER BY` that decides which rows are kept?

## The bottom line

SQL doesn't read your query from top to bottom. It starts with `FROM`, filters rows with `WHERE`, groups, filters groups with `HAVING`, and only then builds the `SELECT` list, sorts and trims.

Keep that order in mind and you will **fix alias errors in seconds**, choose between `WHERE` and `HAVING` without guessing, and write queries that work in SQL Server and Fabric as well as in more forgiving databases.
