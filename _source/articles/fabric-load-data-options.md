---
slug: insights-fabric-load-data-options
title: Pipelines, Dataflow Gen2 or notebooks: how to get data into Fabric
dek: A beginner-friendly guide to the main ways of loading data into Microsoft Fabric, what each tool is good at, and a simple way to choose the right one.
category: Microsoft Fabric
author: elijah-parker
audience: training
date: 2026-10-28
---

Once you've created your first lakehouse or warehouse in **Microsoft Fabric**, the next question arrives quickly: how do you actually get data into it? Open the "New item" menu and you'll see pipelines, Dataflow Gen2, notebooks, Copy job, Eventstream, shortcuts and more.

The good news is that each tool has a clear sweet spot. This guide walks through the main options, explains who each one is designed for, and gives you a simple way to choose, so you can spend your time learning one tool properly rather than dabbling in all of them.

## Start with two questions

Before comparing tools, ask yourself two things:

1. **Do I need to copy the data at all?** Sometimes the data already lives somewhere Fabric can reach, and you only need to point at it.
2. **How much do I need to change the data on the way in?** Moving data as it is and reshaping it heavily are different jobs, and Fabric has different tools for each.

Keep those questions in mind as you read the options below.

## Shortcuts: reference data without copying it

A **shortcut** appears as a folder in your lakehouse, but it points to data stored somewhere else: another lakehouse, an Azure Data Lake Storage Gen2 account, Amazon S3 or other supported sources. Microsoft's guidance is to use shortcuts when you want to **reference data without copying it**.

For learners, shortcuts are a useful reminder that "getting data into Fabric" doesn't always mean moving it. If the data is already in a supported store, a shortcut can be the quickest route.

## Uploading files: the simplest starting point

For **small files on your own machine**, such as a CSV export, you can upload them directly through the Lakehouse explorer. No transformation happens; the file simply lands in the lakehouse's **Files** area.

This is ideal when you're practising. Just remember that a file in Files isn't yet a table, so you'll need to load it into a Delta table before the SQL analytics endpoint or a Power BI semantic model can use it.

## Dataflow Gen2: Power Query in the cloud

**Dataflow Gen2** is a low-code tool built on the **Power Query** experience. If you've ever cleaned data in Power BI Desktop or Excel using Power Query, you already know most of what you need.

Microsoft positions it for data ingestion, transformation, wrangling and profiling. You build your steps visually (filtering rows, merging tables, changing types, unpivoting columns) and then choose a **data destination**. Supported destinations include Fabric Lakehouse tables, Fabric Warehouse and Fabric SQL database, among others. On each refresh you can either **replace** the data in the destination or **append** to it.

Microsoft's lakehouse guidance recommends Dataflow Gen2 for **small to medium data with visual transformations**. That makes it a natural first choice for analysts moving from Power BI into Fabric.

## Pipelines and the Copy activity: moving data at scale

A **pipeline** is the orchestration tool in Fabric's Data Factory experience. Inside a pipeline, the **Copy activity** moves data from a source to a destination, with lightweight changes such as type conversion and column mapping along the way.

Microsoft recommends pipelines for **large-scale data movement**. Their real strength, though, is **orchestration**: a pipeline can chain several steps together. Activities include running a Dataflow Gen2, running a Fabric notebook, calling a stored procedure, looping with ForEach, branching with If condition, and even posting a message to Microsoft Teams. You can then schedule the whole pipeline to run whenever you need it.

So a typical pattern is: copy raw data in, run a notebook or dataflow to clean it, then notify the team, all from one scheduled pipeline.

## Copy job: simple, repeatable loads without building a pipeline

**Copy job** is a newer item that sits between "just upload it" and "build a full pipeline". Microsoft describes it as offering bulk copy, **incremental copy** and **change data capture (CDC) replication** without you needing to build a pipeline, while still giving you access to more advanced options.

The key benefit for beginners is incremental loading. With a Copy activity in a pipeline, you're responsible for tracking what was loaded last time. Copy job has **native, watermark-based incremental copy**, so after the first full load it can pick up only new or changed rows on each scheduled run.

## Notebooks and Spark: full control with code

**Notebooks** let you write code, usually PySpark, but also Scala, Spark SQL or R, to load and transform data. Microsoft recommends this route for **complex transformations or unsupported sources**, and it's the most flexible option in the list.

Here's a minimal example that reads a CSV uploaded to the Files area of the notebook's default lakehouse and saves it as a Delta table:

```python
df = spark.read.option("header", "true").csv("Files/sales.csv")

df.write.mode("overwrite").format("delta").saveAsTable("sales")
```

Relative paths like `Files/sales.csv` work for the notebook's **default lakehouse**. For data in a different lakehouse, you'd use the full ABFS path instead. Switch `overwrite` to `append` if you want to add rows to an existing table rather than replace it.

The trade-off is obvious: you need to be comfortable writing code. For learners aiming at data engineering roles, though, notebooks are well worth the investment.

## What about real-time data?

If your data arrives as a continuous stream of events, for example from messaging systems such as Kafka or from databases that support change data capture, none of the batch tools above is the right fit. Fabric's **Eventstream** ingests, transforms and routes real-time events, and can land them in a lakehouse or an eventhouse.

## A quick way to choose

| If you want to… | Start with |
|---|---|
| Use data that already lives in a supported store | Shortcut |
| Load a few small files from your laptop | Upload files |
| Clean and reshape data visually | Dataflow Gen2 |
| Copy tables on a schedule, loading only new rows | Copy job |
| Move large volumes and orchestrate several steps | Pipeline with Copy activity |
| Write custom transformation logic in code | Notebook |
| Ingest real-time events | Eventstream |

These tools aren't rivals. In real Fabric solutions they often work together: a pipeline might run a Copy activity, then a notebook, then a dataflow, in one scheduled run.

## Which should a learner pick first?

That depends on where you're heading:

- **Aspiring data analysts and Power BI developers:** start with **Dataflow Gen2**. Your Power Query skills transfer directly, and you'll quickly see your data in a lakehouse table.
- **Aspiring data engineers:** learn **pipelines** for orchestration and **notebooks** for transformation. Together they cover most engineering scenarios.

## Common beginner mistakes

- **Copying data you could have referenced.** Check whether a shortcut would do the job first.
- **Building a pipeline for a simple scheduled copy.** Copy job may handle it with less effort.
- **Forcing heavy logic into the Copy activity.** It's designed for lightweight changes. Use a dataflow or notebook for real transformation work.
- **Leaving data in Files.** SQL and Power BI work with tables, so load files into Delta tables.

## The bottom line

Fabric gives you several ways to get data in because people work in different ways. **Shortcuts** avoid copying, **Dataflow Gen2** suits Power Query users, **Copy job** handles simple repeatable loads, **pipelines** move data at scale and orchestrate everything else, and **notebooks** give you full control with code. Pick the tool that matches your skills and the job in front of you, learn it well, and add the others as your projects grow.
