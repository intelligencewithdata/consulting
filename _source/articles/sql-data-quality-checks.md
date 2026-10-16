---
slug: insights-sql-data-quality-checks
title: Six SQL checks to run before you trust a report
dek: Duplicates, gaps and impossible values quietly distort business reports. These six simple SQL checks catch most of them before the numbers reach a meeting.
category: SQL
author: efua-angela
audience: consulting
date: 2026-10-16
---

A dashboard is only as trustworthy as the data underneath it. When a sales figure looks odd, the cause is rarely the chart. It's usually something in the data: an order loaded twice, a customer record that doesn't exist, or a refund keyed in as a sale.

The frustrating part is that these problems are **easy to find** once you look for them. A handful of short SQL queries, run against your source tables before a report is refreshed, will catch most of the issues that cause awkward questions in a board meeting.

This article walks through six checks we recommend to any organisation that reports from a database. You don't need to be a SQL expert to follow them, and your analyst or IT partner can set them up in an afternoon.

All the examples use two simple tables:

```sql
customers (customer_id, name, city)
orders    (order_id, customer_id, order_date, amount, status)
```

## 1. Reconcile the totals with the source system

Before looking for individual problems, check that the big picture matches. Count the rows, add up the key value and look at the date range.

```sql
SELECT COUNT(*)        AS row_count,
       SUM(amount)     AS total_amount,
       MIN(order_date) AS first_order,
       MAX(order_date) AS last_order
FROM orders;
```

Compare these figures with the system the data came from, such as your finance or order management software. If the source says 4,812 orders last month and your reporting table says 4,830, you know something has gone wrong **before** anyone builds a chart on top of it.

The date range is just as useful. A `last_order` date from three days ago tells you the latest load didn't run, and a date in the future tells you something was keyed incorrectly.

## 2. Find duplicate records

Duplicates are the most common reason totals come out too high. They creep in when a file is imported twice or a data load is re-run after a failure.

Start with the column that should be unique, usually an ID:

```sql
SELECT order_id, COUNT(*) AS copies
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Any row returned is an ID that appears more than once. Sometimes the IDs are different but the records are clearly the same transaction, so it's worth checking the combination of columns that describes a real-world event too:

```sql
SELECT customer_id, order_date, amount, COUNT(*) AS copies
FROM orders
GROUP BY customer_id, order_date, amount
HAVING COUNT(*) > 1;
```

The second query will occasionally flag genuine repeat purchases, so treat its results as **questions to investigate** rather than errors to delete.

## 3. Count missing values

Blank fields make reports quietly wrong. An order with no customer disappears from a "sales by region" chart, and an order with no amount is ignored by a total.

`COUNT(*)` counts every row, while `COUNT(column)` only counts rows where that column has a value. The difference between the two is the number of missing values:

```sql
SELECT COUNT(*)                      AS total_rows,
       COUNT(*) - COUNT(customer_id) AS missing_customer,
       COUNT(*) - COUNT(amount)      AS missing_amount,
       SUM(CASE WHEN status IS NULL OR status = ''
                THEN 1 ELSE 0 END)   AS missing_status
FROM orders;
```

Notice the extra test on `status`. Many systems store an **empty string** rather than a true `NULL` when a text field is left blank, and `COUNT` treats an empty string as a value. Checking for both catches the two kinds of blank.

## 4. Find orphaned records

An orphaned record points to something that doesn't exist, such as an order whose `customer_id` has no matching row in the customers table. When your report joins the two tables, those orders can vanish from the results without any warning.

```sql
SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c
       ON c.customer_id = o.customer_id
WHERE o.customer_id IS NOT NULL
  AND c.customer_id IS NULL;
```

The `LEFT JOIN` keeps every order, and the `WHERE` clause keeps only the ones where no customer was found. We exclude orders with a blank `customer_id` here because check 3 already counts those; this query finds the IDs that are filled in but **wrong**.

Orphans usually mean one system was updated before another, or a customer was deleted without their history being dealt with. Either way, someone needs to decide how those orders should be reported.

## 5. Look at every distinct value in category columns

Status, region, product type and similar columns should only contain a short, known list of values. A quick summary shows you exactly what's in there:

```sql
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;
```

This is where you spot the variations that split one category into several: "Completed" alongside "Complete", or a stray "N/A". In a report, each variation appears as its own slice of a chart, and the main category is understated.

It takes seconds to run, and it's one of the most revealing queries you can show a business owner.

## 6. Flag impossible values

Some values simply shouldn't happen: an order dated next year, a negative quantity or a status nobody recognises. List them directly:

```sql
SELECT order_id, order_date, amount, status
FROM orders
WHERE amount < 0
   OR order_date > CURRENT_DATE
   OR status NOT IN ('Completed', 'Pending', 'Refunded');
```

Two points are worth knowing here.

First, **agree the rules with the business**. A negative amount might be a genuine refund in one system and a keying error in another. The query is only as good as the definition of "impossible" behind it.

Second, `NOT IN` doesn't match rows where `status` is `NULL`, because comparing anything with `NULL` returns unknown rather than true. That's another reason to run the missing-values check in step 3 alongside this one.

If you're using SQL Server, note that `CURRENT_DATE` is supported in SQL Server 2025, Azure SQL Database and Azure SQL Managed Instance. On earlier versions, use `CAST(GETDATE() AS date)` instead.

## Turn the checks into a single health report

Running six queries by hand every week is still a manual process. A better approach is to combine the key checks into one summary that lists each test and how many problems it found:

```sql
SELECT 'Duplicate order IDs' AS check_name, COUNT(*) AS issues
FROM (SELECT order_id
      FROM orders
      GROUP BY order_id
      HAVING COUNT(*) > 1) AS dupes
UNION ALL
SELECT 'Orders with no customer', COUNT(*)
FROM orders
WHERE customer_id IS NULL
UNION ALL
SELECT 'Orphaned orders', COUNT(*)
FROM orders AS o
LEFT JOIN customers AS c
       ON c.customer_id = o.customer_id
WHERE o.customer_id IS NOT NULL
  AND c.customer_id IS NULL
UNION ALL
SELECT 'Negative amounts', COUNT(*)
FROM orders
WHERE amount < 0;
```

`UNION ALL` stacks the results of each check into one table. Saved as a view, it can sit behind a small "data health" page in your reporting tool, so everyone can see at a glance whether this week's numbers are safe to use. A row of zeros is the result you want.

## The bottom line

Most reporting errors aren't caused by complex calculations. They're caused by **ordinary data problems** that nobody checked for: duplicates, blanks, broken links between tables and values that make no sense.

The six checks in this article are short, readable and work on almost any SQL database with minor changes. Run them before every refresh, agree with the business what counts as a problem, and fix issues at the source rather than patching them in the report. Your numbers will be more reliable, and your meetings will spend less time arguing about whose figures are right.
