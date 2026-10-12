---
slug: insights-10-sql-queries
title: The 10 SQL queries every new data analyst should know
dek: You don't need to memorise the whole language. Master these ten patterns and you can answer most of the questions a business will ask you.
category: SQL
author: jayne-carter
audience: training
date: 2026-10-12
---

SQL can look intimidating when you start. There are hundreds of functions, several dialects and endless edge cases. The good news is that day-to-day analyst work relies on a **small set of patterns**, used again and again.

All the examples below use two simple tables: `customers` and `orders`.

```sql
customers (customer_id, name, city, signup_date)
orders    (order_id, customer_id, order_date, amount, status)
```

## 1. Select only the columns you need

The most basic query, and the habit that matters most: ask for specific columns, not `SELECT *`.

```sql
SELECT order_id, order_date, amount
FROM orders;
```

Naming columns makes your query faster, easier to read and less likely to break when the table changes.

## 2. Filter rows with WHERE

`WHERE` narrows your results to the rows you care about. Combine conditions with `AND`, `OR` and `IN`.

```sql
SELECT order_id, customer_id, amount
FROM orders
WHERE status = 'Completed'
  AND amount >= 100
  AND order_date BETWEEN '2026-01-01' AND '2026-03-31';
```

## 3. Sort and limit results

"What were our five biggest orders?" is a sort plus a limit.

```sql
SELECT order_id, customer_id, amount
FROM orders
ORDER BY amount DESC
LIMIT 5;
```

In SQL Server, write `SELECT TOP 5 ...` instead of `LIMIT 5`.

## 4. Summarise with GROUP BY

Aggregations turn thousands of rows into an answer: totals, averages and counts per group.

```sql
SELECT status,
       COUNT(*)    AS order_count,
       SUM(amount) AS total_value,
       AVG(amount) AS average_value
FROM orders
GROUP BY status;
```

Every column in the `SELECT` must either be in the `GROUP BY` or wrapped in an aggregate function.

## 5. Filter groups with HAVING

`WHERE` filters rows *before* grouping. `HAVING` filters groups *after* aggregation.

```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

This finds your customers who have spent more than £1,000 in total.

## 6. Combine tables with INNER JOIN

Real questions need data from more than one table. An `INNER JOIN` returns only the rows that match in both.

```sql
SELECT c.name, c.city, o.order_id, o.amount
FROM orders AS o
INNER JOIN customers AS c
        ON c.customer_id = o.customer_id;
```

Short table aliases like `o` and `c` keep joins readable.

## 7. Find what's missing with LEFT JOIN

A `LEFT JOIN` keeps every row from the left table, even without a match. That makes it perfect for finding gaps, such as customers who have never ordered.

```sql
SELECT c.customer_id, c.name
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```

[[fig:sql-joins]]

## 8. Categorise with CASE

`CASE` is SQL's if-then-else. Use it to create bands, flags and labels.

```sql
SELECT order_id,
       amount,
       CASE
           WHEN amount >= 500 THEN 'Large'
           WHEN amount >= 100 THEN 'Medium'
           ELSE 'Small'
       END AS order_size
FROM orders;
```

## 9. Break problems into steps with a CTE

A Common Table Expression (`WITH ...`) lets you build a query in readable stages, like named steps in a recipe.

```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders
    WHERE status = 'Completed'
    GROUP BY customer_id
)
SELECT c.name, ct.total_spent
FROM customer_totals AS ct
INNER JOIN customers AS c
        ON c.customer_id = ct.customer_id
ORDER BY ct.total_spent DESC;
```

## 10. Rank and compare with window functions

Window functions calculate across related rows without collapsing them. A classic use is finding each customer's most recent order.

```sql
WITH ranked_orders AS (
    SELECT customer_id,
           order_id,
           order_date,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY order_date DESC
           ) AS order_rank
    FROM orders
)
SELECT customer_id, order_id, order_date
FROM ranked_orders
WHERE order_rank = 1;
```

[[fig:sql-window]]

Swap `ROW_NUMBER()` for `SUM(amount) OVER (...)` and you have running totals. This is one of the most powerful patterns in SQL.

## Putting it into practice

Reading SQL is easy; writing it under pressure is a skill. The fastest way to build it is to **practise on real questions**: take a dataset and ask what sold best, who stopped buying, or how this month compares with last.

That's exactly what we do, live and hands-on, in our free Power BI and SQL class every Friday.
