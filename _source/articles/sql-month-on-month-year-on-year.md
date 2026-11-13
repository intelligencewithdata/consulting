---
slug: insights-sql-month-on-month-year-on-year
title: Month-on-month and year-on-year growth in SQL, done properly
dek: "Are we up on last month?" is the question every report should answer. Here's how to calculate growth in SQL without missing months, divide-by-zero errors or misleading figures.
category: SQL
author: jayne-carter
audience: consulting
date: 2026-11-13
---

Almost every management report comes down to one question: **are we doing better or worse than before?** A revenue figure on its own means little. The same figure next to last month, or the same month last year, tells you whether to celebrate or start asking questions.

Many organisations still work these comparisons out by hand, copying monthly totals into a spreadsheet and adding formulas each time. That's slow and easy to get wrong. Done in SQL, the comparison is calculated the same way every time, straight from the source data, and can feed a Power BI report or a scheduled email without anyone touching it.

This article shows the patterns we use, plus the three mistakes that most often make growth figures quietly wrong. The examples use one simple table:

```sql
orders (order_id, order_date, amount)
```

The queries use SQL Server's `YEAR()` and `MONTH()` functions. In PostgreSQL you'd write `EXTRACT(YEAR FROM order_date)`, and in SQLite `strftime('%Y', order_date)`; the logic is otherwise the same.

## Step 1: Get one row per month

Growth is calculated between periods, so the first job is to summarise the orders into **one row per month**.

```sql
SELECT YEAR(order_date)  AS yr,
       MONTH(order_date) AS mth,
       SUM(amount)       AS revenue
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY yr, mth;
```

Keep this as the foundation. Every comparison below starts from it, wrapped in a common table expression (CTE) called `monthly` so the rest of the query stays readable.

## Month-on-month change with LAG

`LAG` is a window function that reads a value from an earlier row without collapsing the result. With no offset it looks back one row, so ordering by year and month gives you **the previous month's revenue** alongside the current one.

```sql
WITH monthly AS (
    SELECT YEAR(order_date)  AS yr,
           MONTH(order_date) AS mth,
           SUM(amount)       AS revenue
    FROM orders
    GROUP BY YEAR(order_date), MONTH(order_date)
),
with_previous AS (
    SELECT yr, mth, revenue,
           LAG(revenue) OVER (ORDER BY yr, mth) AS previous_month
    FROM monthly
)
SELECT yr, mth, revenue, previous_month,
       revenue - previous_month AS change,
       ROUND(100.0 * (revenue - previous_month)
             / NULLIF(previous_month, 0), 1) AS pct_change
FROM with_previous
ORDER BY yr, mth;
```

Two details here matter more than they look:

- **`NULLIF(previous_month, 0)`** turns a zero into NULL. A month with no revenue would otherwise cause a divide-by-zero error; with `NULLIF`, the percentage simply comes back empty, which is the honest answer.
- **`100.0 *`** forces decimal arithmetic. In SQL Server, dividing one integer by another gives an integer with the fractional part dropped, so if your amounts are stored as whole numbers a 7.9% fall can come back rounded down, or even as zero.

The very first month has no previous row, so `LAG` returns NULL. That's correct: there's nothing to compare it with.

## Year-on-year: compare like with like

Month-on-month figures are useful, but many businesses are seasonal. A dip from December to January may be completely normal. **Year-on-year comparison** removes that noise by comparing each month with the same month last year.

You could use `LAG(revenue, 12)`, which looks back twelve rows, but that only works if every month is present. The safer approach is to join the monthly summary to itself on "same month, previous year":

```sql
WITH monthly AS (
    SELECT YEAR(order_date)  AS yr,
           MONTH(order_date) AS mth,
           SUM(amount)       AS revenue
    FROM orders
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT cur.yr, cur.mth, cur.revenue,
       prev.revenue AS same_month_last_year,
       ROUND(100.0 * (cur.revenue - prev.revenue)
             / NULLIF(prev.revenue, 0), 1) AS pct_change
FROM monthly AS cur
LEFT JOIN monthly AS prev
       ON prev.yr  = cur.yr - 1
      AND prev.mth = cur.mth
ORDER BY cur.yr, cur.mth;
```

The `LEFT JOIN` keeps every current month, even when there's no matching month last year. Those rows show an empty comparison rather than disappearing from the report.

## Running totals and financial year to date

Boards and lenders often want **year-to-date** figures rather than single months. A running total is the same window function idea, using `SUM` instead of `LAG`.

Many UK organisations report on a financial year that doesn't match the calendar year, so this example labels each month with a financial year starting in April, then restarts the running total each time a new financial year begins:

```sql
WITH monthly AS (
    SELECT YEAR(order_date)  AS yr,
           MONTH(order_date) AS mth,
           SUM(amount)       AS revenue
    FROM orders
    GROUP BY YEAR(order_date), MONTH(order_date)
),
labelled AS (
    SELECT yr, mth, revenue,
           CASE WHEN mth >= 4 THEN yr ELSE yr - 1 END AS fin_year
    FROM monthly
)
SELECT fin_year, yr, mth, revenue,
       SUM(revenue) OVER (
           PARTITION BY fin_year
           ORDER BY yr, mth
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS fytd_revenue
FROM labelled
ORDER BY yr, mth;
```

Here `fin_year` 2025 means the year from April 2025 to March 2026. Change the `4` if your year starts in a different month.

We spell out `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` deliberately. If you add `ORDER BY` without a frame, SQL Server uses `RANGE` as the default, which treats rows with the same ordering value as a single group. With one row per month the result is identical, but stating the frame makes the intention clear and avoids surprises if the query is later changed.

## Three mistakes that make growth figures wrong

### 1. Missing months

`LAG` compares with the previous **row**, not the previous **month**. If a month has no orders at all, it doesn't appear in the summary, and the next month gets compared with the wrong period. September is compared with July, and nobody notices.

The fix is a small table holding every year and month you report on (or the month columns of a date table, if you already have one). Join your summary to it so every month exists, with zero where nothing was sold:

```sql
WITH monthly AS (
    SELECT YEAR(order_date)  AS yr,
           MONTH(order_date) AS mth,
           SUM(amount)       AS revenue
    FROM orders
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT m.yr, m.mth,
       COALESCE(s.revenue, 0) AS revenue
FROM months AS m
LEFT JOIN monthly AS s
       ON s.yr  = m.yr
      AND s.mth = m.mth
ORDER BY m.yr, m.mth;
```

Use this as your `monthly` step and the `LAG` comparisons line up correctly again. Limit the `months` table to the periods you actually report on, so future months don't show as zero.

### 2. Comparing a part-month with a full month

On the 10th of the month, the current month holds ten days of sales and last month holds thirty. The comparison will almost always show a sharp fall. For headline growth figures, **exclude the current, incomplete month**:

```sql
SELECT YEAR(order_date)  AS yr,
       MONTH(order_date) AS mth,
       SUM(amount)       AS revenue
FROM orders
WHERE order_date < DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY yr, mth;
```

`DATEFROMPARTS` builds the first day of the current month, so only complete months are included. If people do want to see the month so far, show it separately and label it clearly.

### 3. Growth from a tiny base

A month that goes from £200 to £1,000 shows **400% growth**. Mathematically correct, practically meaningless. Always show the actual figures and the change in pounds next to the percentage, so readers can judge whether a big percentage is a big deal.

## The bottom line

Month-on-month and year-on-year figures are some of the most-read numbers in any business, which is exactly why they should be calculated by a repeatable query rather than rebuilt by hand each month.

Start with one row per month, use `LAG` for the previous month and a self-join for the same month last year, and protect every percentage with `NULLIF`. Fill in missing months, leave out the incomplete current month and always show the underlying numbers. Do that, and the growth figures in your reports will mean what everyone assumes they mean.
