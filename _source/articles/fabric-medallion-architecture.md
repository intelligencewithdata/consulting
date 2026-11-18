---
slug: insights-fabric-medallion-architecture
title: Medallion architecture in Microsoft Fabric: bronze, silver and gold explained
dek: What the bronze, silver and gold layers are, what belongs in each, and how to set them up in Microsoft Fabric without overcomplicating your first project.
category: Microsoft Fabric
author: thomas-forrester
audience: training
date: 2026-11-18
---

If you're learning **Microsoft Fabric**, you'll soon meet the words bronze, silver and gold. They appear in Microsoft's documentation, in job adverts and in almost every Fabric tutorial. They describe the **medallion architecture**, a simple way of organising data in layers so it gets cleaner and more useful as it moves towards your reports.

Microsoft describes medallion architecture as a **design pattern** and the recommended design approach for Fabric. It isn't a feature you switch on. It's a habit of keeping raw, cleaned and report-ready data apart. This guide explains each layer in plain English, shows the same data at every stage, and walks through a sensible first setup.

## In short

- **Bronze** keeps data exactly as it arrived from the source.
- **Silver** holds the cleaned version: errors fixed, formats standardised, duplicates removed.
- **Gold** holds data shaped for reports and dashboards.
- Microsoft recommends keeping each layer in **its own lakehouse** (or warehouse), and ideally its own workspace.

## Why use layers at all?

Without layers, cleaning and reporting logic tends to pile up in one place. A report reads straight from a messy export, someone fixes a problem inside the report, and the original data is lost or overwritten.

Layers solve three problems at once:

1. **You can always go back.** The raw data is preserved, so if a cleaning rule turns out to be wrong you can fix it and rebuild, rather than re-requesting data from the source.
2. **Each step has one job.** Cleaning happens in one place and report shaping in another, which makes problems easier to find.
3. **Quality is visible.** Microsoft's guide puts it simply: each layer indicates the quality of the data stored in it, with higher layers representing higher quality.

[[fig:medallion-flow]]

## Bronze: store it exactly as it arrives

The **bronze layer** is your landing zone. Microsoft's guidance is to store everything exactly as it arrives, in the same format as the source. No fixes, no filters, no "quick tidy-ups".

That might feel wasteful when you can already see problems in the data. The point is that bronze is your **source of truth**. If a supplier sends a file with a mistake, bronze shows what they actually sent.

Microsoft recommends storing bronze data in its original format, or as Parquet or Delta Lake. Where the source data already sits in OneLake, Azure Data Lake Storage Gen2, Amazon S3 or Google Cloud Storage, the guide suggests creating a **shortcut** in the bronze layer instead of copying the data across.

## Silver: clean it once, properly

The **silver layer** is where you fix things. Microsoft's own example lists typical silver work:

- standardising date formats across all sources
- converting values to a single currency
- removing test transactions
- matching customer records across systems

The key idea is that you clean **once, centrally**, rather than repeating the same fixes in every report. When five reports all read from one cleaned silver table, they all get the same answer.

For silver and gold, Microsoft recommends **Delta tables**, which are the default table format in a Fabric lakehouse. When Fabric engines write Delta tables they can apply **V-Order**, an optimisation that speeds up reads by Power BI, SQL and Spark.

## Gold: shape it for the people using it

The **gold layer** is organised for reporting. Instead of every order line, you might hold a daily sales table, a customer lifetime value table or a stock forecasting table: Microsoft's example uses exactly these three.

Gold is what business users and Power BI reports should read from. It's usually smaller, simpler and named in business language, so someone opening it can understand it without a data dictionary.

Here's how the same handful of orders looks at each layer.

[[fig:medallion-data]]

The query behind a gold daily sales table can be very simple, because silver has already done the hard work:

```sql
SELECT
    order_date,
    COUNT(*)    AS orders,
    SUM(amount) AS sales
FROM silver_orders
GROUP BY order_date
ORDER BY order_date;
```

Notice there's no de-duplication or date fixing here. If you find yourself cleaning data in a gold query, that's a sign the cleaning belongs in silver.

## How to set it up in Fabric

Microsoft's guide describes two common patterns:

| Pattern | Bronze | Silver | Gold | Business users query through |
|---|---|---|---|---|
| 1 | Lakehouse | Lakehouse | Lakehouse | The SQL analytics endpoint |
| 2 | Lakehouse | Lakehouse | Warehouse | The warehouse endpoint |

The guide says the choice should be based on your preference and your team's skills. If your team is more comfortable with Spark and notebooks, pattern 1 keeps everything in lakehouses. If your team thinks in T-SQL, a warehouse for gold may feel more natural.

A practical first setup looks like this:

1. **Create one lakehouse per layer**, for example `bronze_sales`, `silver_sales` and `gold_sales`.
2. **Decide on workspaces.** You can keep all three in one workspace while learning. For real projects, Microsoft recommends a separate workspace for each layer, which gives you more control and better governance at layer level.
3. **Load raw data into bronze** with the ingestion tool that suits the source, such as a pipeline, a Dataflow Gen2 or a notebook.
4. **Write cleaned Delta tables into silver**, keeping your cleaning rules in one place.
5. **Build gold tables** for each reporting need, then point your Power BI semantic model at gold.

Microsoft's medallion guide also describes **materialized lake views**, which let you define the transformations between layers in SQL and have Fabric manage dependencies and refreshes. It's worth reading Microsoft's tutorial on them and checking their current status before relying on them in production.

## Common mistakes to avoid

- **Cleaning in bronze.** Once you change raw data, you lose the ability to check it against the source.
- **Reports reading from bronze or silver.** This spreads business logic across reports and brings back the inconsistency the layers were meant to remove.
- **Too many layers too soon.** Bronze, silver and gold are a guide, not a rule. A small project with one tidy source may not need every layer to be separate on day one.
- **Unclear names.** Use consistent prefixes or workspace names so everyone knows which layer they're looking at.

## The bottom line

Medallion architecture is less about technology and more about discipline: **keep the raw data, clean it once, and shape it for the people who use it**. In Fabric that usually means three lakehouses (or two lakehouses and a warehouse) and a clear rule that reports only read from gold.

If you're learning Fabric, building a small bronze-silver-gold project with a sample dataset is one of the best ways to practise. It touches ingestion, cleaning, Delta tables and Power BI, and it's exactly the kind of structure employers expect you to recognise.
