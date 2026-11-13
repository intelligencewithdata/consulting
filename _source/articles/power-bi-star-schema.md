---
slug: insights-power-bi-star-schema
title: Star schema in Power BI: how to shape your data model
dek: What fact and dimension tables are, why Power BI works best with a star schema, and how to turn a flat spreadsheet export into one.
category: Power BI
author: efua-angela
audience: training
date: 2026-11-13
---

Most people learning Power BI start the same way: load one big spreadsheet, drag fields onto a canvas and build visuals. It works, until the totals stop making sense, the measures get complicated and the file grows sluggish. The fix is rarely a cleverer formula. It is usually the **shape of the data model**.

Microsoft's own modelling guidance points Power BI developers towards the **star schema**. This guide explains what that means in plain terms, why it matters, and how to reshape a typical flat export into one.

## What a star schema is

A star schema organises your data into two kinds of table.

**Fact tables** store observations or events: sales orders, invoices, stock balances, website visits. Each row records something that happened, with numeric columns you want to add up (quantity, value, cost) and key columns that say *who*, *what*, *where* and *when*. Fact tables tend to have a lot of rows and keep growing.

**Dimension tables** describe the business entities you analyse by: customers, products, stores, dates. Each has a unique key column plus descriptive columns used for filtering and grouping, such as product category or customer region. Dimension tables are usually much smaller.

Draw it on paper with the fact table in the middle and the dimensions around it, and you get the star shape that gives the design its name.

| Table | Type | Example columns |
|---|---|---|
| Sales | Fact | OrderNumber, OrderDate, ShipDate, ProductKey, CustomerKey, Quantity, SalesAmount |
| Product | Dimension | ProductKey, Product, Subcategory, Category |
| Customer | Dimension | CustomerKey, Customer, City, Region |
| Date | Dimension | Date, Month, Quarter, Financial Year |

One detail surprises people: there is no setting in Power BI that marks a table as a fact or a dimension. As Microsoft's documentation notes, the role is **determined by the relationships** you create.

## Why Power BI prefers this shape

Relationships in a Power BI model are filter paths. When you pick "North" in a Region slicer, that filter travels from the Customer table along the relationship to the Sales table, and every measure recalculates for northern customers only.

In a star schema, the most common relationship is **one-to-many**: the "one" side is the dimension (each product appears once) and the "many" side is the fact table (each product appears on many sales rows). Filters flow cleanly from dimensions into facts, which brings several benefits:

- **Simpler DAX.** Measures such as total sales or average order value can be written once and respond correctly to any slicer.
- **Consistent numbers.** Everyone filters by the same Product and Customer tables, so "sales by region" means the same thing on every page.
- **A tidier field list.** Report authors find attributes in obvious places instead of hunting through one wide table.
- **Better performance and usability.** Microsoft's guidance presents star schema design as the way to build Power BI semantic models that are optimised for both.

A single flat table can hold the same information, but it repeats every product and customer detail on every row, and it makes some calculations awkward, particularly when you add a second fact table such as budgets or targets.

## Turning a flat export into a star schema

Suppose your finance system gives you one CSV with a row per order line: order number, order date, product name, category, customer name, city, quantity and value. Microsoft's advice for this situation is to **use Power Query to shape the export into separate fact and dimension tables**. A practical approach:

1. **Load the export once** as a staging query and untick *Enable load* so it doesn't appear in the model.
2. **Create each dimension by referencing it.** Right-click the staging query, choose *Reference*, keep only the product columns, then use *Remove Duplicates*. Repeat for customers.
3. **Make sure each dimension has a unique key.** If the source has a reliable product code, use it. If not, add an *Index Column* to create one. This is called a **surrogate key**, because it doesn't exist in the source data.
4. **Build the fact table.** Reference the staging query again, merge in the new keys, and keep only the keys, dates and numeric columns.
5. **Add a proper date table** and relate it to the order date. Our guide on [building a date table in Power BI](insights-power-bi-date-table.html) covers that step.
6. **Create the relationships** in Model view, one-to-many from each dimension to the fact table.

Once the shape is right, measures become short and reusable:

```dax
Total Sales = SUM ( Sales[SalesAmount] )

Average Order Value =
DIVIDE ( [Total Sales], DISTINCTCOUNT ( Sales[OrderNumber] ) )
```

The order number stays in the fact table. Microsoft calls an attribute like this a **degenerate dimension**: an attribute of the fact table that's needed for filtering, where a separate table holding just that one column would only add storage and clutter.

## Snowflakes and when to flatten

Data from a database often arrives **normalised**, with products in one table, subcategories in another and categories in a third. This is a **snowflake** dimension.

Power BI can model it as-is, but Microsoft's guidance lists the drawbacks: more tables to load, longer filter paths and more tables cluttering the Data pane (the field list). You also **can't build a hierarchy from columns in more than one table**, so a Category › Subcategory › Product drill-down needs everything in one place. The general recommendation is to merge the snowflake into a **single Product table** in Power Query. The small amount of repeated text is usually a good trade for a simpler model.

## Common mistakes to avoid

**Turning on bi-directional filtering everywhere.** It can feel like a quick fix when a slicer doesn't behave, but Microsoft recommends you **minimise bi-directional relationships** because they can hurt query performance and confuse report users. Keep relationships single-direction by default. Where you need the other direction for one calculation, the `CROSSFILTER` function can change it inside a single measure instead of across the whole model.

**One date table, several date columns.** If your sales table has an order date and a ship date, you can relate both to one date table, but only **one relationship can be active** between two tables. The other must be inactive and is only usable through `USERELATIONSHIP` in a measure:

```dax
Sales by Ship Date =
CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] ) )
```

If report users need to slice by both dates freely, Microsoft suggests creating a separate date table for each role, such as Order Date and Ship Date, with clearly named columns.

**Mixing grains in a fact table.** Fact tables should load data at a **consistent grain**. Daily sales and monthly targets belong in separate fact tables, both related to the same dimensions.

**Relying on implicit sums.** Dragging a numeric column onto a visual lets Power BI sum it automatically. That is fine for quantities but wrong for something like unit price, which should never be added up. Writing **explicit measures** and hiding raw numeric columns keeps the model honest.

## The bottom line

A star schema is not an advanced technique reserved for large organisations. It is the shape Power BI is built around. Split your data into **facts** (what happened) and **dimensions** (what you analyse it by), connect them with **one-to-many, single-direction** relationships, and flatten snowflakes into single tables where you can.

Get the model right first and the DAX, the visuals and the performance tend to follow. If you are learning Power BI, practise reshaping a flat export into a star schema; it is one of the most valuable habits you can build.
