---
slug: insights-power-bi-shared-semantic-model
title: One semantic model, many reports: stop copying data in Power BI
dek: Why every new Power BI report shouldn't bring its own copy of the data, and how a shared semantic model gives your business one version of the numbers.
category: Power BI
author: efua-angela
audience: consulting
date: 2026-11-23
---

Ask three managers for last month's revenue and you might get three different answers, each backed by a Power BI report. Nobody is being careless. The usual cause is that **each report was built with its own copy of the data and its own version of the measures**, so small differences crept in over time.

Power BI has a built-in answer to this: build the data model once, publish it as a **shared semantic model**, and connect every report to it. This guide explains what that means, why it matters for a growing business, and how to set it up.

## In short

- A **semantic model** holds your data, relationships and measures. A report is just the pages and visuals on top.
- Most businesses end up with one model per report. That means repeated refreshes and definitions that drift apart.
- Instead, publish **one shared model** and connect new reports to it with a **live connection**.
- Control who can build reports with **Build permission**, and flag the trusted model with **endorsement**.

## What a semantic model is (and why copies cause trouble)

When you build a report in Power BI Desktop, you are really building two things in one file. The first is the **semantic model**: the imported tables, the relationships between them and the DAX measures such as Total Sales or Gross Margin. The second is the **report**: the pages, charts and slicers people look at.

Publish that file and both parts go to the Power BI service together. That is fine for the first report. The trouble starts with the second and third, when someone opens a new file, imports the same sales data again and rewrites the measures.

Now you have several semantic models covering the same data. Each one:

- **refreshes separately**, putting extra load on your source systems and gateways;
- **holds its own measure definitions**, so a change to how revenue is calculated has to be made in several places, and is easy to miss in one;
- **needs its own security**, so a row-level security rule added to one model doesn't protect the others.

[[fig:pbi-shared-model]]

## The shared model approach

Microsoft's guidance on managed self-service BI is direct about this. It says the key to making the approach work is **"to minimize the number of semantic models"**, and it recommends decoupling the semantic model from the reports.

In practice that means two kinds of Power BI Desktop file:

1. **The model file.** It contains the data, relationships and measures. It may have no report pages, or just a simple test page. It is published once and refreshed on a schedule.
2. **Thin report files.** They contain no data of their own. Each one connects to the published model and holds only pages and visuals.

Microsoft's scenario goes a step further and suggests keeping the shared model in **its own workspace**, separate from the workspace that holds the reports. That makes it clear who is responsible for which content.

The trade-off is worth stating plainly. Because every report depends on the shared model, **any change to the model affects every report connected to it**. Renaming or removing a measure can break visuals elsewhere, so changes to the model need a little more care.

## How to connect a report to a shared model

Once the model is published, report authors connect to it from Power BI Desktop rather than importing the data again.

1. Open Power BI Desktop and start a new, blank report.
2. On the **Home** tab, select **Get data**, then **Power BI semantic models**.
3. In the OneLake catalog that opens, choose the shared model and select **Connect**.
4. Build your pages and visuals using the tables and measures from the model.
5. Publish the report to the reports workspace.

Microsoft calls this a **Power BI service live connection**. The report points at the existing model, so **no new semantic model is created** when you publish it. Microsoft's guide to [connecting to semantic models in Power BI](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-report-lifecycle-datasets) shows these screens step by step.

On a live connection the model itself is read-only from the report. Report authors **can't add new tables or change the model's relationships**, but they can still add report-level measures for one-off calculations. If a measure proves useful to more than one report, it belongs in the shared model instead.

## Who can do what: Build permission

Not everyone who reads reports should be creating them. Power BI handles this with **Build permission** on the semantic model. According to Microsoft's documentation on semantic model permissions, Build lets a user create new content from the model, and only users with Build can connect to it with a live connection.

There are several ways a person gets Build:

- **Workspace roles.** Admin, Member and Contributor roles on the model's workspace include Build automatically. The Viewer role does not.
- **Direct permission.** A workspace Admin or Member can grant Build to individual people or groups from the model's manage permissions page.
- **Through an app.** An app owner can allow app users to build content from the semantic models the app uses.

Licensing matters here too. Microsoft notes that users need a **Pro or Premium Per User licence** to store reports in another workspace or share them. Check your own licences before rolling this out.

[[fig:pbi-shared-model-roles]]

Security carries through as well. If the shared model uses row-level security, readers of the connected reports still only see the rows they are allowed to see, so you define the rules once in the model rather than in every report.

## Point people at the right model: endorsement

Once you have a trusted shared model, you want people to find it rather than build yet another copy. Power BI's **endorsement** feature helps with this. There are two levels:

- **Promoted.** The content owner, or a workspace member with write permissions, can promote a semantic model to say it is ready for others to use.
- **Certified.** Only reviewers authorised by your Power BI administrator can certify content, and the administrator must enable and configure certification first. It signals that the model meets the organisation's quality standards.

Endorsed models are labelled when people browse for data, which nudges report authors towards the approved model and away from importing their own.

## When a separate model still makes sense

A shared model is not a rule for every situation. A one-off analysis using data nobody else needs doesn't have to join it. If a team needs to add its own data to the shared model, Power BI also supports **composite models**, which combine a published model with other sources; that is a bigger topic and worth planning carefully.

As a simple test, ask: **will more than one report need these numbers?** If the answer is yes, the data and measures belong in a shared model.

## The bottom line

Multiple copies of the same data are the quiet cause of most "which number is right?" conversations. Building **one shared semantic model** and connecting thin reports to it means measures are defined once, refreshed once and secured once.

Start with your most-used data, such as sales or finance. Publish it as a shared model, grant Build permission to the people who create reports, and promote or certify it so everyone can find it. New reports then become quicker to build, and the numbers agree from one report to the next.
