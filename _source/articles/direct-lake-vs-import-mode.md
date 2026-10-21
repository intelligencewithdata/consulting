---
slug: insights-direct-lake-vs-import-mode
title: Direct Lake vs Import mode: which suits your Power BI reports?
dek: A plain-English comparison of Direct Lake and Import mode in Microsoft Fabric, what each costs you in refresh time and flexibility, and how to choose.
category: Microsoft Fabric
author: thomas-forrester
audience: consulting
date: 2026-10-21
---

If your business is moving its reporting onto **Microsoft Fabric**, someone will eventually ask a question that sounds technical but has real consequences for cost, speed and how fresh your numbers are: "Should our Power BI semantic model use **Direct Lake** or **Import mode**?"

This guide explains what each option does and the practical questions we ask before recommending one.

## What a storage mode actually decides

Every Power BI report sits on a **semantic model**: the tables, relationships and measures behind the numbers. Each table has a **storage mode**, which decides where the data lives and how it reaches the report.

There are three you'll hear about:

- **Import:** Power BI copies the data into the model. Microsoft describes the result as a **point-in-time copy**, so the model must be refreshed to pick up changes.
- **DirectQuery:** nothing is copied. Each time a visual needs data, Power BI sends a query to the source system and waits for the answer.
- **Direct Lake:** a Fabric-only option that reads **Delta tables stored in OneLake** (Fabric's single data lake) and loads them into memory on demand, without making a separate copy of the data.

The interesting choice for most Fabric customers is between Import and Direct Lake, because both use the same in-memory engine (VertiPaq) to answer queries. Microsoft's documentation notes that Direct Lake and Import queries **normally outperform DirectQuery** when people interact with report visuals.

## How Import mode works

Import mode is what most Power BI users already know: connect to a source, shape the data with **Power Query**, publish, and let a scheduled refresh re-copy the data.

The strengths are real:

- It works with **almost any data source**, not just Fabric.
- It runs on **any Fabric or Power BI licence**, including the free tier, according to Microsoft's comparison.
- It supports the widest range of modelling features, such as calculated columns, calculated tables, hybrid tables and custom partitions.

The trade-off is the refresh. Every refresh rebuilds a copy of the data, which Microsoft warns **can take considerable time and consume significant source and capacity resources**. There are also limits on how often you can schedule it: semantic models on shared capacity get eight scheduled refreshes a day, while models on Premium, Premium Per User or Fabric capacity can schedule up to 48. Between refreshes, the report shows yesterday's (or this morning's) numbers.

## How Direct Lake works

Direct Lake takes a different approach. Your data is prepared upstream in Fabric, using pipelines, dataflows, notebooks or T-SQL, and lands as Delta tables in a **lakehouse**, **warehouse** or another supported Fabric item. The semantic model then points at those tables.

Two ideas make it work:

- **Framing.** A Direct Lake "refresh" doesn't copy data. It only updates the model's references to the latest version of each Delta table, which Microsoft says **usually takes a few seconds**.
- **On-demand loading.** Columns are loaded into memory only when a query first asks for them. Once loaded, they stay in memory for later queries until they're evicted, for example after the underlying table changes, after a period of not being used, or when the capacity is under memory pressure.

By default, a setting called **"Keep your Direct Lake data up to date"** is switched on, so the model reframes automatically whenever it detects changes in the underlying Delta tables.

## The catches with Direct Lake

Direct Lake is not a free upgrade, and it's worth being clear-eyed about its limits:

- **It needs a Fabric capacity.** Microsoft states that Direct Lake semantic models require a Fabric capacity licence (F SKUs). It isn't available on the free tier or on shared capacity.
- **Your data must already be in OneLake as Delta tables.** Direct Lake has no Power Query step inside the model, so any cleaning and shaping has to happen upstream in Fabric. If your team can't change the source tables, Import is often the more practical choice.
- **Capacity guardrails apply.** Each Fabric capacity size has limits on things such as the number of Parquet files, row groups and rows per table, plus how much memory a model can use. Smaller capacities have tighter limits. Microsoft's advice when a table exceeds them is to run `OPTIMIZE` and `VACUUM` on the Delta table and, if that isn't enough, move to a larger capacity.
- **Some modelling features are restricted.** Calculated columns and calculated tables are limited or in preview depending on the Direct Lake variant, and features like hybrid tables and custom partitions aren't available.
- **There are two flavours.** **Direct Lake on SQL endpoints** can fall back to slower DirectQuery when it can't read a Delta table directly, such as when it hits a SQL view. **Direct Lake on OneLake** doesn't fall back; if guardrails are exceeded, the refresh fails until the tables are brought back within limits.

## Side by side

| | Import | Direct Lake |
|---|---|---|
| Where data is prepared | Power Query, inside the model | Upstream in Fabric (pipelines, notebooks, T-SQL, dataflows) |
| What a refresh does | Copies all the data again | Updates metadata only (framing), usually seconds |
| Data freshness | As fresh as the last scheduled refresh | Can update automatically when Delta tables change |
| Data sources | Almost anything | Delta tables in supported Fabric items |
| Licensing | Any Fabric or Power BI licence | Fabric capacity only |
| Modelling flexibility | Widest | More restricted |

## How we help clients choose

Microsoft frames the decision in terms of who owns the data. Its guidance describes Direct Lake as typically suited to **IT-driven, lake-centric projects**, and an ideal fit for the curated "gold" layer of a medallion lakehouse. Import mode, by contrast, **often suits self-service analysts** who need to move quickly without depending on IT to add new data.

In practice, we ask four questions:

1. **Are you already on (or committing to) a Fabric capacity?** If not, Import is your only option of the two, and that's fine for many small businesses.
2. **Is your data already landing in a lakehouse or warehouse?** If yes, Direct Lake removes a second copy and a second refresh schedule. If your data still lives in spreadsheets and a handful of cloud apps, Import is usually simpler.
3. **How fresh do the numbers need to be?** If an overnight refresh is fine, Import's main drawback barely matters. If managers want figures soon after each data load, Direct Lake's automatic updates are a strong argument.
4. **Who maintains the reports?** If analysts need to add data themselves in Power Query, Import keeps them productive. If a data team owns a governed set of tables, Direct Lake fits naturally.

It doesn't have to be all or nothing. Microsoft's comparison lists **composite models** as supported for Direct Lake on OneLake, so a model can mix Direct Lake tables with Import tables where that makes sense. Microsoft also recommends building a **proof of concept** before committing, and we agree: test with your own data and your own capacity size before rebuilding every report.

## The bottom line

**Import mode** is flexible, works everywhere and remains the right answer for many businesses, particularly those without a Fabric capacity or a lakehouse yet. **Direct Lake** shines when your data is already curated as Delta tables in Fabric: a refresh updates metadata rather than copying data, there's no second copy to maintain, and reports can pick up new data automatically.

The right choice depends less on the technology and more on where your data lives, who looks after it and how fresh your decisions need it to be. Answer those first, prove it on a small model, and the choice usually becomes clear.
