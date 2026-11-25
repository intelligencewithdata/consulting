---
slug: insights-fabric-onelake-shortcuts
title: OneLake shortcuts: use your data in Fabric without copying it
dek: What OneLake shortcuts are, which sources they can point to, and when a shortcut beats copying data into Microsoft Fabric for your business.
category: Microsoft Fabric
author: elijah-parker
audience: consulting
date: 2026-11-25
---

Most businesses already have data spread across several places: files in cloud storage, tables in another team's lakehouse, documents in SharePoint. The traditional answer is to **copy** all of it into one central store before anyone can report on it. That works, but every copy needs a pipeline, a schedule, storage and someone to notice when it fails.

Microsoft Fabric offers another option: **OneLake shortcuts**. A shortcut lets data appear inside your Fabric lakehouse while it stays where it already lives. This guide explains what shortcuts are, where they can point, and how to decide between a shortcut and a copy.

## In short

- A **shortcut** is a pointer in OneLake to data stored somewhere else. Microsoft says shortcuts behave like symbolic links.
- Shortcuts can point to other **Fabric items** (internal) or to **external storage** such as Azure Data Lake Storage Gen2, Amazon S3 and Google Cloud Storage.
- Shortcuts in a lakehouse's **Tables** folder can be read by the SQL analytics endpoint and by Power BI semantic models.
- Use a shortcut when the data is already in good shape; **copy and transform** it when it needs cleaning first.

## What a OneLake shortcut is

Microsoft's documentation describes shortcuts as **objects in OneLake that point to other storage locations**. The location the shortcut points at is called the **target**. The shortcut itself appears as a folder in your lakehouse, and tools such as Spark, SQL and Power BI read through it as if the data were stored there.

The key point for a business is that **no data is moved**. Microsoft's lakehouse guide says shortcuts let you reference data without copying it. There is no extra pipeline to build and no second copy that can drift out of date. When the source changes, people reading through the shortcut see the change.

[[fig:onelake-shortcut]]

## Where shortcuts can point

Microsoft groups shortcuts into two kinds.

**Internal shortcuts** point to other Fabric items. Microsoft's current list of supported targets includes lakehouses, warehouses, KQL databases, SQL databases, mirrored databases, mirrored Azure Databricks catalogs and semantic models. A common use is letting the finance team read a curated table from the sales team's lakehouse without either team duplicating it.

**External shortcuts** point to storage outside Fabric. Microsoft lists:

- Azure Data Lake Storage Gen2 and Azure Blob Storage
- Amazon S3 and Amazon S3 compatible storage
- Google Cloud Storage
- Dataverse
- Iceberg tables
- OneDrive and SharePoint

Microsoft also documents reaching on-premises or network-restricted storage through the **on-premises data gateway**. Shortcuts can be created in **lakehouses** and **KQL databases**. Support changes over time, so check [Microsoft's shortcuts overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts) for the current list and any preview labels before you plan around a particular source.

## Tables folder or Files folder?

A lakehouse has two top-level areas, and where you create a shortcut changes what you can do with it.

1. **Tables folder.** Shortcuts here can only be created at the top level, not in subfolders. If the target holds a supported table format such as **Delta**, the lakehouse recognises the folder as a table automatically. Microsoft's guide says you can read these shortcuts through the **SQL analytics endpoint** and build **semantic models**, including Direct Lake models, on top of them.
2. **Files folder.** Shortcuts can be created at any level, and they're ideal for raw files such as CSV or JSON. Tables aren't discovered here, so the data won't appear as a SQL table until you process it.

Two practical rules from Microsoft's documentation are worth knowing. A shortcut whose name contains a **space** isn't recognised as a Delta table. And schema-level shortcuts, which bring in a whole folder of tables at once, need a **schema-enabled lakehouse**.

## Shortcut or copy: how to decide

Shortcuts are not a replacement for every pipeline. The question is whether the data is already fit for use.

[[fig:shortcut-or-copy]]

A shortcut is usually the better choice when:

- the data is **already clean** and in a table format such as Delta, for example a curated table owned by another team
- you want **one source of truth** rather than a second copy to keep in sync
- the data sits in another cloud and moving it would mean building and maintaining a new pipeline

Copying with a pipeline, Dataflow Gen2 or notebook is usually better when:

- the data needs **cleaning, reshaping or combining** before anyone reports on it
- you need a **point-in-time snapshot** that won't change when the source changes
- the source owner may move or rename files, which Microsoft warns **can break a shortcut**

In a medallion setup, the two work together. Microsoft's medallion guidance suggests creating shortcuts in the bronze layer when source data already sits in supported storage, then transforming it into silver and gold.

## Security: who sees what

Shortcuts don't bypass security, but the rules differ by type.

**Internal shortcuts** normally use the **identity of the person reading the data**. That user needs read access to the target as well as to your lakehouse. Microsoft's security guide notes some exceptions, including Power BI semantic models using Direct Lake over SQL, where the item owner's identity is used instead. Review that page before you rely on shortcut security for sensitive data.

**External shortcuts** use **delegated authentication**. The credentials in the cloud connection set up when the shortcut is created are used for every read. Microsoft's lakehouse guide is explicit: any user with access to the lakehouse can read data through the shortcut using those stored credentials. In practice, **access to the lakehouse becomes access to that external data**, so treat lakehouse permissions with the same care as the source.

Creating a shortcut needs **write** access where the shortcut will live and **read** access to the target.

## Things to check before you rely on shortcuts

1. **Deleting the shortcut is safe.** Microsoft says removing a shortcut only removes the pointer; the target data is unchanged.
2. **Deleting files through a shortcut is not.** If you delete a file or folder inside a shortcut and have permission at the source, it's **deleted in the target** too.
3. **Cross-cloud reads.** For Google Cloud Storage, Amazon S3, S3 compatible and gateway shortcuts, Fabric offers **shortcut caching** in workspace settings. Microsoft says it can reduce egress costs; cached files are kept for 1 to 28 days and files over 1 GB aren't cached.
4. **Limits.** Microsoft documents limits such as up to 100,000 shortcuts per item and up to 10 shortcuts in a single OneLake path. Most small and mid-sized businesses won't get near them, but they're worth knowing.

## The bottom line

OneLake shortcuts let you **use data where it already lives**, which means fewer pipelines, fewer copies and fewer versions of the truth. They work best for data that is already clean and well owned.

Our usual advice is to **start with a shortcut, and copy only when you need to transform or freeze the data**. Get the permissions right from day one, especially for external shortcuts, and shortcuts can remove a surprising amount of plumbing from a Fabric project.
