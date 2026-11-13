---
slug: insights-fabric-workspace-roles
title: Fabric workspace roles explained: who should get which access
dek: A practical guide to the four Microsoft Fabric workspace roles, what each one can really do, and a simple access plan that keeps your data safe as your team grows.
category: Microsoft Fabric
author: elijah-parker
audience: consulting
date: 2026-11-13
---

When a business starts using **Microsoft Fabric**, access tends to grow organically. Someone creates a workspace, adds a few colleagues as Admins "to save time", and six months later nobody is quite sure who can delete what, or why the sales manager can see every table in the lakehouse.

Workspace roles are the first and broadest layer of security in Fabric, so getting them right early saves a lot of tidying up later. This guide explains the four roles in plain English, highlights the details that most often catch teams out, and suggests a simple access plan for a small or mid-sized organisation.

## What a workspace role controls

A **workspace** is a container for Fabric items: lakehouses, warehouses, pipelines, notebooks, semantic models, reports and more. A workspace role applies to **every item in that workspace**.

Microsoft is clear that roles are confined to the workspace they're granted in. They don't apply to other workspaces, to the capacity the workspace runs on, or to the tenant as a whole. That's useful: you can give someone broad rights in a development workspace without touching anything in production.

There are four roles, from most to least powerful: **Admin, Member, Contributor and Viewer**.

## The four roles at a glance

| Role | In short | Typical person |
|---|---|---|
| Admin | Full control, including deleting the workspace and managing all access | One or two people who own the workspace |
| Member | Builds content and can add people (but not Admins) | Team leads who manage their own colleagues |
| Contributor | Creates, edits and runs content, but can't manage access | Data engineers and report developers |
| Viewer | Reads content, can't change it | Business users and reviewers |

## Admin: owns the workspace

Admins can do everything. According to Microsoft's role documentation, only Admins can **update and delete the workspace**, **add or remove people including other Admins**, connect the workspace to a **Git repository** and create a **workspace identity**.

Whoever creates a workspace becomes an Admin automatically. Because the role includes the power to delete the whole workspace, it's worth keeping the list short, ideally two people so you're never locked out if one is away.

## Member: builds content and manages the team

Members can do almost everything an Admin can when it comes to content. They can also **add people to the Member, Contributor or Viewer roles** and allow others to reshare items. What they can't do is add Admins or delete the workspace.

This makes Member a good fit for a team lead who needs to onboard colleagues without involving IT every time.

## Contributor: does the hands-on work

Contributors can **create, edit and delete items** such as lakehouses, warehouses, pipelines, notebooks and dataflows. They can run and cancel pipelines and notebooks, read lakehouse data through Spark and the Lakehouse explorer, and schedule refreshes through an on-premises gateway (with separate gateway permissions as well).

They **can't manage workspace access**. For most data engineers and report builders, Contributor is all they need.

## Viewer: reads, doesn't change

Viewers can open content and view pipeline and notebook outputs, but they can't create or modify anything. One detail surprises many teams: Viewers can **connect to the SQL analytics endpoint** of a lakehouse or warehouse and **read the data with T-SQL**. What they can't do is read data through Spark, the OneLake APIs or the Lakehouse explorer.

So "read-only" in Fabric still means **read access to the data**, not just the reports. Keep that in mind before adding a large group as Viewers on a workspace full of raw data.

## Three details that catch teams out

**1. Row-level security only applies to Viewers.** If you've built row-level security (RLS) into a Power BI semantic model, it filters data for people with the Viewer role. Microsoft notes that RLS isn't enforced for users with Write permission, which includes Admins, Members and Contributors. Give a regional manager Contributor "just in case" and they'll see every region.

**2. Removing someone from a report isn't always enough.** Microsoft's permission model explains that if a person has a workspace role, removing their item-level permission from a report doesn't stop them seeing it, because the workspace role still lets them in. To truly restrict access, you need to change or remove their workspace role.

**3. Changes aren't instant.** Adding or removing access takes effect the **next time the user signs in** to Fabric. If someone has just been removed and is still active, bear that in mind.

## Use groups, not individuals

Roles can be assigned to individual users, but also to **security groups, mail-enabled security groups, distribution lists and Microsoft 365 groups**. If a person belongs to several groups, they get the **highest** permission across them.

Assigning roles to groups has two big benefits:

- **Joiners and leavers are handled once**, in Microsoft Entra ID, rather than workspace by workspace.
- **Access is easy to audit**: a workspace with four groups is far easier to review than one with forty named people.

A workspace can hold up to **1,000 users or groups** in its roles, but a group counts as one entry however many people are in it, which is another reason to work with groups.

## Most business users don't need a workspace role at all

It's tempting to make everyone a Viewer so they can find their reports. Microsoft's own guidance recommends a different approach for report consumers: **distribute content with a Power BI app**.

An app gives consumers a polished, read-only view of the reports you choose, without exposing semantic models, pipelines or lakehouses. You can also organise app content into **audiences**, so different groups see different subsets of reports. And because app users only get Read permission, row-level security is enforced for them, as long as they don't also hold a Contributor (or higher) workspace role or Write permission on the semantic model.

For very small audiences who need one or two items, **sharing the item directly** also works. Microsoft notes that sharing an item grants Read permission by default, which lets people view it but **doesn't give them access to the underlying data** in SQL or OneLake.

## A simple access plan for a small or mid-sized business

Here's a pattern we often recommend as a starting point:

1. **Separate workspaces by purpose**, for example a data engineering workspace (lakehouses, pipelines, notebooks) and a reporting workspace (semantic models and reports). Add development and production versions if you have the people to manage them.
2. **Two named Admins per workspace**, usually from IT or the data team.
3. **A "data team" security group as Contributor** on the workspaces they build in.
4. **Team leads as Members** only where they genuinely need to manage access themselves.
5. **Business users through a Power BI app**, with audiences for different departments, rather than workspace roles.
6. **Review access every quarter**, removing anyone who has changed role or left.

This keeps the number of people with write access small, makes row-level security work as designed, and stops raw data being visible to people who only need the finished reports.

## The bottom line

Fabric workspace roles are simple once you know what each one really allows. Keep **Admin** for owners, give builders **Contributor**, use **Member** sparingly for team leads, and remember that **Viewer** can still query data through SQL. For most business users, a Power BI app is a safer and tidier way in than any workspace role. Put the plan in place early, use groups rather than individuals, and your Fabric estate will stay secure as it grows.
