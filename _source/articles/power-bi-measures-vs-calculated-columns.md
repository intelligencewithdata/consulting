---
slug: insights-power-bi-measures-vs-calculated-columns
title: Measures vs calculated columns in Power BI: when to use each
dek: A plain-English guide to the two kinds of DAX calculation, how each one behaves, and a simple rule for choosing the right one every time.
category: Power BI
author: elijah-parker
audience: training
date: 2026-10-19
---

Sooner or later, everyone learning Power BI writes their first DAX formula and hits the same fork in the road. Should this be a **calculated column** or a **measure**? Both use DAX, both appear in the Data pane, and both can produce a number on a report. Yet they behave very differently, and picking the wrong one is one of the most common reasons a beginner's totals look strange.

This guide explains what each one is, how they differ, and a simple way to decide which to use.

## The short answer

- Use a **calculated column** when you need a new value **for every row** that you want to slice, filter, group or put on an axis.
- Use a **measure** when you need a result that **summarises many rows** and should change as people filter the report.

Microsoft's own tutorial puts it neatly: measures usually go in a visual's **Values** area, while calculated columns are used as new fields in the **rows, axes, legends and group areas** of visuals.

## What a calculated column is

A calculated column is a new column you add to an existing table, with a DAX formula that defines its value. The formula is evaluated **once for each row**, using what DAX calls **row context**: you can think of it as "the current row".

Here is a simple example on a `Sales` table:

```dax
Order Size =
IF ( Sales[Quantity] >= 10, "Bulk", "Standard" )
```

Each row gets the label "Bulk" or "Standard", and you can now use `Order Size` in a slicer or on a chart axis.

The most important thing to understand is **when** the work happens. According to Microsoft's DAX documentation, calculated column values are computed and **stored in the model**. They are only recalculated when the table, or a related table, is refreshed, or when the model is reloaded (for example, when you close and reopen the file). They do **not** react to slicers or filters on the report page.

A calculated column can also look up a value from a related table using `RELATED`, as long as a relationship exists:

```dax
Customer Region =
RELATED ( Customer[Region] )
```

## What a measure is

A measure is a named formula that **aggregates** data. Its result is not stored row by row. Instead, it is worked out **at query time**, whenever someone opens a report or interacts with a visual.

```dax
Total Sales =
SUMX ( Sales, Sales[Quantity] * Sales[Unit Price] )
```

`SUMX` returns the sum of an expression evaluated for each row of a table, so this measure multiplies quantity by unit price row by row and then adds the results up.

Drop `Total Sales` into a table visual next to `Customer Region` and it shows the right figure for each region. Add a year slicer and every number updates. That responsiveness comes from **filter context**: the filters, rows, columns and slicers that apply to each cell of a visual. As Microsoft's documentation puts it, a measure's result cannot be determined without context.

Measures can also reference other measures, which makes them easy to build in layers:

```dax
Average Order Value =
DIVIDE ( [Total Sales], DISTINCTCOUNT ( Sales[Order ID] ) )
```

## Side by side

| | Calculated column | Measure |
|---|---|---|
| Calculated | At refresh, for every row | At query time, for each cell in a visual |
| Stored in the model | Yes, adds to model size | No, only the formula is stored |
| Reacts to slicers and filters | No | Yes |
| Typical use | Slicers, filters, axes, grouping | Totals, ratios, KPIs, comparisons |
| Context it starts with | Row context | Filter context |

## The classic mistake: ratios in a column

Imagine you want a profit margin. A tempting first attempt is a calculated column:

```dax
Margin % =
DIVIDE ( Sales[Profit], Sales[Sales Amount] )
```

That gives a correct margin **for each individual row**. The problem appears in a visual. Put `Margin %` in a table and Power BI will aggregate the column, by default with a sum, so you get percentages added together. Switch it to average and you get the **average of the row margins**, which is not the same as overall margin: a small order with a high margin counts just as much as a large order with a low one.

The correct approach is a measure that divides the totals:

```dax
Margin % =
DIVIDE ( SUM ( Sales[Profit] ), SUM ( Sales[Sales Amount] ) )
```

Now every cell, subtotal and grand total is calculated from the summed figures in its own filter context, so the numbers add up the way the business expects. As a rule, **ratios, percentages and averages almost always belong in measures**.

A note on `DIVIDE`: Microsoft recommends it over the `/` operator when the denominator could be zero or blank. If it is, `DIVIDE` returns BLANK instead of an error, and visuals hide blank results by default. When you are dividing by a constant, the `/` operator is fine.

## Implicit measures and why explicit ones are better

When you drag a numeric column straight into a visual, Power BI summarises it for you, usually with a sum. Microsoft calls this an **implicit measure**. It is handy for quick exploration, but it has drawbacks:

- The logic lives inside one visual, so it cannot be reused or referenced by other measures.
- Different report pages can quietly use different aggregations of the same column.
- Calculation groups, a more advanced modelling feature, only apply to explicit measures, not implicit ones.

Creating an **explicit measure** with **New measure** (on the **Home** tab, or by right-clicking a table) gives the calculation a name, one definition and a single place to fix it. Many teams then hide the raw numeric columns so report builders use the measures instead.

## Should that column be in Power Query instead?

Calculated columns are not wrong, but they are not always the best home for row-level logic. Microsoft's guidance on reducing model size points out that calculated columns typically **compress less efficiently** than columns created in Power Query, and they are built only after all the Power Query tables have loaded, which can **lengthen refresh times**.

The recommendation is to prefer **custom columns in Power Query** where possible, or to calculate the value in the source database itself. A calculated column is still the better choice when the formula needs to evaluate measures or relies on DAX-only functionality.

A practical order of preference for a new row-level value is:

1. **In the source** (for example, a SQL view), if you control it.
2. **In Power Query**, as a custom column.
3. **As a DAX calculated column**, when you need DAX to do it.

## A quick decision checklist

Ask yourself these questions when you write a new formula:

- **Will I put this on a slicer, axis, legend or filter?** Calculated column (or Power Query column).
- **Should the result change when someone filters the report?** Measure.
- **Is it a total, count, average, ratio or percentage?** Measure.
- **Is it a label, category or band for each row?** Calculated column, ideally built in Power Query.
- **Could it be done before the data reaches the model?** Do it upstream.

## The bottom line

Calculated columns describe **each row** and are fixed at refresh time. Measures summarise **many rows** and respond to every filter, slicer and visual. Use columns for things you want to slice by and measures for things you want to see the value of. Get that one distinction right, and most of the "why is my total wrong?" moments in Power BI disappear.
