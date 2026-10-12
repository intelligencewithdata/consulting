---
slug: insights-power-bi-date-table
title: How to build a date table in Power BI (and why you need one)
dek: A step-by-step guide to creating a proper date table with DAX, marking it correctly and using it for year-to-date and UK financial-year reporting.
category: Power BI
author: thomas-forrester
audience: training
date: 2026-10-12
---

Almost every Power BI report answers a question about time. How did sales do this month? Are we ahead of last year? What is the year-to-date figure for the financial year? Getting those answers right depends on one unglamorous table: the **date table**.

This guide explains what a date table is, why the built-in option only goes so far, and how to build, mark and use your own with a few lines of DAX.

## What a date table is

A date table is simply a table with **one row for every day** across the period your data covers, plus useful columns describing each day: year, quarter, month name, weekday and so on. Your fact tables (sales, orders, invoices) then relate to it through their date columns.

Microsoft's guidance sets out clear requirements. The date column must:

- be of data type **Date** (or Date/Time)
- contain **unique values** with **no blanks**
- have **no missing dates**, so the range is contiguous
- span **full years** (which need not be calendar years)

Get that right and every visual slices by year, quarter or month from one consistent source.

## Why not just use auto date/time?

Power BI Desktop has an option called **Auto date/time**, switched on by default in a new installation. For each eligible date column in an Import table, it quietly creates a hidden date table with a Year, Quarter, Month and Day hierarchy.

It is convenient for quick exploration, but it has real limitations:

- **Calendar years only.** Years always run from 1 January to 31 December, so a UK financial year starting in April is not supported.
- **No shared filter.** Each date column gets its own hidden table, so filtering one does not filter the others.
- **Bigger models.** Every hidden table adds to model size and refresh time.
- **Limited reach.** The hidden tables aren't available in Analyze in Excel or to non-Power BI report designers.

Microsoft recommends keeping auto date/time only for simple, calendar-based models or ad hoc exploration. To switch it off for new files, go to **File > Options and settings > Options** and use the **Time intelligence** section of the **Global** page.

## Step 1: Create the table with DAX

In Power BI Desktop, go to **Modeling > New table** and enter the following. It assumes a `Sales` table with an `OrderDate` column, so swap in your own names.

```dax
Date =
ADDCOLUMNS (
    CALENDAR (
        DATE ( YEAR ( MIN ( Sales[OrderDate] ) ), 1, 1 ),
        DATE ( YEAR ( MAX ( Sales[OrderDate] ) ), 12, 31 )
    ),
    "Year", YEAR ( [Date] ),
    "Quarter", "Q" & QUARTER ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month Name", FORMAT ( [Date], "mmm" ),
    "Year Month", FORMAT ( [Date], "mmm yyyy" ),
    "Year Month Sort", YEAR ( [Date] ) * 100 + MONTH ( [Date] ),
    "Weekday Number", WEEKDAY ( [Date], 2 ),
    "Weekday Name", FORMAT ( [Date], "ddd" )
)
```

Here is what each part does:

- **`CALENDAR`** returns a single column called `Date` containing every day between a start and end date, inclusive.
- Wrapping the earliest and latest order dates in `DATE ( YEAR ( … ), 1, 1 )` and `DATE ( YEAR ( … ), 12, 31 )` **rounds the range out to full years**, which keeps you within the requirements above.
- **`WEEKDAY`** with a second argument of `2` numbers the week from Monday (1) to Sunday (7), which suits UK reporting better than the default Sunday start.

If you would rather the table cover every date found anywhere in the model, **`CALENDARAUTO()`** is an alternative to `CALENDAR`. It also returns full years, but a stray placeholder date such as 1900 elsewhere in the model will stretch the range.

One thing to watch: `FORMAT` produces text using the model's locale, so month and day names follow your report's language settings.

## Step 2: Sort the month names properly

Text columns sort alphabetically, so "Apr" will appear before "Jan" in your visuals. Fix this with **Sort by column**:

1. Select the `Month Name` column in the Data pane.
2. On the **Column tools** tab, choose **Sort by column** and pick `Month Number`.
3. Repeat for `Year Month` (sort by `Year Month Sort`) and `Weekday Name` (sort by `Weekday Number`).

## Step 3: Mark it as a date table

Next, tell Power BI this is your date table. Right-click the `Date` table in the Data pane and choose **Mark as date table**, then select the `Date` column.

Power BI checks that the column has unique values, no blanks and a contiguous range of dates. Marking it is required if you use the standard (classic) DAX time intelligence functions, such as the ones in step 5.

Two side effects are worth knowing:

- Power BI **removes the hidden auto date/time tables** for that table, so any visual that relied on them will need repointing at your new columns.
- It also stops building the automatic date hierarchy for you. If you want a drill-down path, create your own hierarchy of Year, Quarter, Month Name and Date.

## Step 4: Create the relationship

In **Model view**, drag `Date[Date]` onto `Sales[OrderDate]` to create a **one-to-many** relationship from the date table to the sales table. From now on, use the columns from the **date table** in your slicers and visuals, not the date column in the sales table.

If you have several fact tables, such as sales and budgets, relate each one to the same date table. That single, shared calendar is the main reason to build one.

## Step 5: Add UK financial-year columns and measures

Many UK organisations report on a financial year from 1 April to 31 March. Add these as calculated columns on the `Date` table:

```dax
Fiscal Year =
VAR FYStart =
    IF (
        MONTH ( 'Date'[Date] ) >= 4,
        YEAR ( 'Date'[Date] ),
        YEAR ( 'Date'[Date] ) - 1
    )
RETURN
    "FY " & FYStart & "/" & RIGHT ( FORMAT ( FYStart + 1, "0" ), 2 )
```

```dax
Fiscal Month Number = MOD ( MONTH ( 'Date'[Date] ) - 4, 12 ) + 1
```

`Fiscal Year` labels 15 May 2026 as "FY 2026/27", and `Fiscal Month Number` makes April month 1 and March month 12. DAX's `MOD` returns a result with the same sign as the divisor, so January (month 1) correctly becomes fiscal month 10. If you rely on fiscal years, consider starting your table on 1 April and ending it on 31 March so the range covers whole financial years.

Now the time intelligence measures. Assuming a base measure such as `Total Sales = SUM ( Sales[Amount] )`:

```dax
Sales YTD = TOTALYTD ( [Total Sales], 'Date'[Date] )

Sales FYTD = TOTALYTD ( [Total Sales], 'Date'[Date], "3/31" )

Sales Last Year =
CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
```

The last argument of `TOTALYTD` sets the **year-end date**, so `"3/31"` gives a financial year-to-date ending on 31 March. Microsoft recommends the month/day form for this string, and notes it must resolve in the locale of the report, so test it with your own settings.

## A note on the newer calendar approach

Microsoft has introduced **calendar-based time intelligence**, which defines calendars (including week-based ones) as metadata on a table. At the time of writing it is a **preview** feature, enabled through the Enhanced DAX Time Intelligence preview option. It still builds on a date table like this one, so nothing here is wasted.

## The bottom line

A good date table takes ten minutes to build and saves hours of confusion later. Create it with `CALENDAR` and `ADDCOLUMNS`, round it out to full years, sort your month names, **mark it as a date table** and relate it to every fact table. Then build your year-to-date and last-year measures on top of it.

Better still, save it in a Power BI template so every new project starts with the same trusted calendar.
