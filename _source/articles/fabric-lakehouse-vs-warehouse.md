---
slug: insights-fabric-lakehouse-vs-warehouse
title: Lakehouse vs Warehouse in Microsoft Fabric: which should you use?
dek: A plain-English guide to the two main places to store data in Fabric, what each can and can't do, and a simple way to decide between them.
category: Microsoft Fabric
author: jayne-carter
audience: training
date: 2026-10-14
---

One of the first questions people ask when they start learning **Microsoft Fabric** is: "Should I create a Lakehouse or a Warehouse?" Both store data, both can be queried with SQL, and both can feed Power BI reports. So what's the difference, and does the choice really matter?

It does matter, but probably less than you think. This guide explains what each item is, where they overlap, where they differ, and how to choose without overthinking it.

## What they have in common

Before looking at the differences, it helps to know how much the two share. According to Microsoft's own decision guide:

- **Both store data in OneLake** in the open **Delta Lake** format. Neither locks your data away in a proprietary file type.
- **Both use the same SQL engine** for T-SQL queries.
- **Both can feed Power BI.** Direct Lake semantic models are supported on lakehouses and warehouses, so either can sit behind your reports.

In other words, this isn't a choice between two completely different products. It's a choice about **how you want to work with the data**: mainly with Apache Spark, or mainly with T-SQL.

## What a Lakehouse is

A **Lakehouse** combines the flexibility of a data lake with warehouse-style querying. It's organised into two top-level folders:

- **Tables:** managed Delta tables, ready to query.
- **Files:** anything else, such as CSV files, JSON, images or other unstructured or non-Delta data.

You mainly build and change a lakehouse with **notebooks and Apache Spark**, writing Python, Scala, Spark SQL or R. You can also load data with pipelines and dataflows, and use **shortcuts** to reference data held elsewhere without copying it.

Every lakehouse automatically gets a **SQL analytics endpoint**. This lets analysts query the Delta tables with T-SQL, but it's important to understand its limits: the endpoint is **read-only**. You can write `SELECT` queries and create **views** and **table-valued functions**, but you can't `INSERT`, `UPDATE` or `DELETE` rows through it. To change the data, you go back to Spark (or a pipeline or dataflow).

Two more details catch beginners out. Only Delta tables in the **Tables** area appear in the SQL analytics endpoint, so a CSV sitting in **Files** won't show up until you load it into a table. And since September 2025, new lakehouses no longer create a default semantic model automatically, so you build your own Power BI semantic model when you're ready to report.

## What a Warehouse is

A **Warehouse** is a full relational data warehouse that you develop mainly with **T-SQL**. If you've worked with SQL Server or Azure SQL, it will feel familiar. It gives you:

- **Full read and write T-SQL:** `CREATE TABLE`, `INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE AS SELECT` and `COPY INTO`.
- **Multi-table transactions:** several changes across several tables either all succeed or all roll back together.
- **Views, functions and stored procedures** to package up business logic.
- **No infrastructure tuning:** Microsoft describes its workload management as autonomous, with no compute or storage settings for you to configure.

The data still lands in OneLake in Delta format, so other Fabric tools can read it.

## The key differences side by side

| | Lakehouse (via SQL analytics endpoint) | Warehouse |
|---|---|---|
| Main way to build | Apache Spark notebooks | T-SQL |
| Changing data with SQL | No: read-only | Yes: full DML and DDL |
| Multi-table transactions | No | Yes |
| Unstructured files | Yes, in the Files area | No: structured tables only |
| Typical users | Data engineers and SQL developers | SQL developers and citizen developers |
| Storage | Delta format in OneLake | Delta format in OneLake |

## A simple way to decide

Microsoft's decision guide boils the choice down to three questions. We find them a reliable starting point:

1. **How will you build it?** If your team writes Python or Spark, choose a **Lakehouse**. If your team writes T-SQL, choose a **Warehouse**.
2. **Do you need multi-table transactions?** If yes, choose a **Warehouse**.
3. **What kind of data do you have?** If you have unstructured or mixed data, or you're not sure yet, choose a **Lakehouse**. If it's structured, tabular data only, a **Warehouse** works well.

For someone learning Fabric with a SQL background, that often points to the Warehouse. For someone learning Python and data engineering, the Lakehouse will feel more natural.

## What the SQL looks like in each

Here's a small example. Imagine an `orders` table with columns `order_id`, `customer`, `order_date` and `amount`.

On a **lakehouse SQL analytics endpoint**, you can read the data and save reusable logic as a view:

```sql
CREATE VIEW monthly_sales AS
SELECT
    SUBSTRING(order_date, 1, 7) AS order_month,
    COUNT(*)                    AS orders,
    SUM(amount)                 AS revenue
FROM orders
GROUP BY SUBSTRING(order_date, 1, 7);
```

That works, because creating a view is allowed. But the next statement would fail on the endpoint, because it changes data:

```sql
UPDATE orders
SET amount = 0
WHERE order_id = 3;
```

In a **Warehouse**, both statements are fine. You can also build a new, cleaned-up table from a query in one step with `CREATE TABLE AS SELECT` (often shortened to CTAS):

```sql
CREATE TABLE large_orders AS
SELECT order_id, customer, amount
FROM orders
WHERE amount >= 500;
```

These examples use a text date for simplicity. In practice you'd store `order_date` as a proper `date` type and use T-SQL date functions such as `YEAR()` and `MONTH()` to group by month. Also note that in T-SQL you limit rows with `TOP`, as in `SELECT TOP 10 ...`, rather than the `LIMIT` keyword used in some other databases.

## You don't have to pick only one

Many real Fabric solutions use **both**. A common pattern is the **medallion architecture**: raw data lands in a lakehouse (bronze), gets cleaned with Spark (silver), and the final, business-ready tables (gold) are served either from a lakehouse or a warehouse.

Because both items share the same SQL engine, a Warehouse can query lakehouse tables in the same workspace using **three-part names**, such as `SalesLakehouse.dbo.orders`. You can join lakehouse and warehouse tables in one query, or insert data from a lakehouse table into a warehouse table, without building a separate copy process. Microsoft describes these as cross-database queries with no data duplication.

So the decision isn't permanent. Starting with one and adding the other later is perfectly normal.

## Common beginner mistakes

- **Trying to update data through the SQL analytics endpoint.** It's read-only. Use Spark, a pipeline or a dataflow, or use a Warehouse instead.
- **Leaving data in Files and wondering why SQL can't see it.** Load it into a Delta table in the Tables area first.
- **Expecting an automatic semantic model.** New lakehouses don't create one any more. Create a semantic model yourself for reporting.
- **Choosing based on which sounds more "serious".** Both are production-grade. Choose based on your team's skills and your data.

## The bottom line

The Lakehouse and the Warehouse in Microsoft Fabric store data in the same place and in the same open format. The real difference is **how you work with it**: a Lakehouse is built mainly with Spark and handles any type of data, with a read-only SQL endpoint for querying; a Warehouse gives you full read-and-write T-SQL with transactions. **Pick the one that matches your skills and your data**, and remember that you can combine them as your solution grows.
