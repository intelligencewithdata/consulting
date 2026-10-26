---
slug: insights-power-bi-row-level-security
title: Row-level security in Power BI: one report, the right data for everyone
dek: How row-level security lets each manager, region or client see only their own figures in a single Power BI report, and the mistakes that quietly undo it.
category: Power BI
author: efua-angela
audience: consulting
date: 2026-10-26
---

Many growing businesses reach the same point with Power BI. The sales report works well, the leadership team loves it, and now the regional managers want it too. The catch is that each manager should only see **their own region**, and nobody wants to maintain five copies of the same report.

That is exactly what **row-level security (RLS)** is for. It lets you publish one report on one semantic model, and Power BI filters the data according to who is looking at it. This guide explains how it works, how to set it up, and the gaps that catch organisations out.

## What row-level security does

RLS restricts which **rows** of data a user can see. You define **roles** in Power BI Desktop, and each role has a DAX filter on one or more tables. Microsoft's documentation describes the filter simply: the expression returns true or false, and **only rows that return TRUE are visible**. Everything else is removed from that user's view of the model.

Because the filter sits in the model rather than on a report page, it applies to every visual, every total and every page built on that model. A manager in the North region does not see a filtered-out "South" bar; as far as their reports are concerned, the South data does not exist.

Two things RLS does **not** do are worth knowing from the start:

- **It does not hide columns.** If someone can see a row, they can see every column in it. Hiding a salary column, for example, needs object-level security instead.
- **It is not a replacement for sensible access management.** RLS filters data for the people it applies to, but, as we explain below, not everyone it might seem to apply to.

## Static roles: the simple starting point

The simplest form is a **static** role, where the filter value is fixed. For a regional sales model you might create a role called "North" with this filter on the `Region` table:

```dax
[Region] = "North"
```

Then another for "South", and so on. In Power BI Desktop you do this from the **Modeling** tab with **Manage roles**, where you can use the default editor or switch to the DAX editor.

Static roles are quick to set up and easy to understand. Their weakness is maintenance: every new region, branch or client means a new role, and every person has to be placed in the right one.

## Dynamic roles: one rule for everyone

For most businesses, **dynamic RLS** scales far better. Instead of one role per region, you create a single role whose filter compares a column in your data with the identity of the person signed in.

You add a small **mapping table** to the model that lists each user's sign-in name alongside what they are allowed to see, such as their region or account manager code. The role's filter then looks like this:

```dax
[UserEmail] = USERPRINCIPALNAME()
```

In the Power BI service, `USERPRINCIPALNAME()` returns the user's **User Principal Name (UPN)**. Microsoft points out that this is the user's **sign-in identifier, not necessarily their email address**, so build the mapping table from the UPN value rather than assuming the two match.

With a relationship from the mapping table to your Region dimension, the filter flows through to the sales data. When someone joins or changes territory, you update one row in the mapping table rather than editing roles.

## Assigning people to roles

You cannot assign users to roles in Power BI Desktop. Once you publish the model, you assign members in the **Power BI service**: open the semantic model's **More options** menu in the workspace and choose **Security**.

Microsoft recommends mapping **security groups** to roles wherever possible, rather than individual people, so that joiners and leavers are handled by your normal IT processes. Distribution groups and mail-enabled groups are also supported, but **Microsoft 365 groups are not** and cannot be added to RLS roles.

If a user is assigned to more than one role, the roles are **additive**: they see the combined rows of all their roles. Unlike some database permission models, there is no "deny" that overrides an allow.

## The mistake that undoes RLS: workspace roles

This is the point we would most like business owners to take away. According to Microsoft's documentation, **RLS only restricts data for users with the Viewer role** in a workspace. It **does not apply to Admin, Member or Contributor** roles, because those roles have edit permission on the semantic model.

In practice, that means if you add regional managers to the workspace as Members "so they can find things easily", every one of them can see every region. The report looks identical in the meeting, so nobody notices.

The safe pattern is:

- Keep **Admin, Member and Contributor** roles for the small group who build and maintain content.
- Give report consumers **Viewer** access, or share content with them through an app.
- Make sure consumers have only **Read** permission on the underlying semantic model when RLS must be enforced, which is the point Microsoft's RLS guidance stresses.

## Test before anyone else sees it

Never assume a role works because the formula looks right. Power BI gives you two places to check:

- In Power BI Desktop, use **View as** on the **Modeling** ribbon to see the report through a role.
- In the Power BI service, open the semantic model's Security page, choose **More options** next to a role and select **Test as role**. For dynamic rules, you can also test as a specific person.

Microsoft's guidance is to test for **expected and unexpected values**, and to design rules so that accidental or unexpected values return **no rows** rather than everything. A useful trick is a simple measure that shows who Power BI thinks you are:

```dax
Who Am I =
USERPRINCIPALNAME ()
```

Put it in a card visual while testing and you can see immediately whether a mismatch in the mapping table is the cause of a blank report. Note that the Test as role feature has limits: it cannot validate everything, including Q&A visuals and Copilot, and it does not work for paginated reports.

## Design tips that keep it fast and reliable

A few habits make RLS models easier to live with:

- **Filter dimension tables, not fact tables.** Microsoft notes that it is often more efficient to apply RLS filters to dimension tables and let relationships carry the filter to the facts.
- **Rely on relationships.** RLS filters only propagate through **active** relationships, so a well-designed star schema matters even more once security is involved.
- **Be careful with bidirectional security filtering.** The "Apply security filter in both directions" option exists for some dynamic patterns, but Microsoft warns it can hurt query performance, so test it thoroughly.
- **Consider whether you need RLS at all.** If you only have two or three audiences with simple, fixed rules, Microsoft suggests separate semantic models and workspaces can be a reasonable alternative, with the trade-off of duplicated content.

## The bottom line

Row-level security lets one Power BI report serve your whole organisation, with each person seeing only the figures they should. Start with a clear idea of who should see what, prefer **dynamic roles with a mapping table** and **security groups**, and keep report consumers on the **Viewer** role, because RLS does not apply to anyone who can edit the model. Then test every role, including what happens when something unexpected turns up. Done well, it removes the need for duplicate reports and gives everyone confidence that sensitive numbers stay where they belong.
