# Insights publishing playbook — Intelligence With Data

This repository is the live website for **https://www.intelligencewithdata.com** (GitHub Pages, branch `main`, root folder).
The site is generated from `_source/`. Never hand-edit the HTML in the repo root — edit `_source/` and run the publisher.

## Schedule (Europe/London)

| Day | Topic (category value) |
|---|---|
| Monday | `Power BI` |
| Wednesday | `Microsoft Fabric` |
| Friday | `SQL` |

Publish **one** article per run, in the category for that weekday. If run on another day, pick the category with the oldest most-recent article.

## 1. Set up

```bash
pip install --break-system-packages -q markdown   # if not installed
cd <repo root>
git pull origin main
```

## 2. Choose the topic

- List existing articles: `grep -h "^title:" _source/articles/*.md`. **Never repeat or closely overlap** an existing title or angle.
- Audiences: UK small/mid-sized businesses (consulting leads) and career-switchers learning data skills (training leads). Alternate between them.
- Prefer practical, searchable questions (e.g. "How to build a date table in Power BI", "DirectLake vs Import mode explained", "SQL GROUP BY mistakes beginners make").
- `audience:` must be `consulting` (business-owner topics → CTA "Book a discovery call") or `training` (learner topics → CTA "Free Fridays").

## 3. Assign the author

Read `_source/insights_state.json`. Use `author_rotation[next_author_index]`, then increment `next_author_index` (wrap to 0) and save the file.
Valid author keys are defined in `AUTHORS` in `_source/insights.py`. **Never use David Chen. Never use hakeem-falade** (reserved for his personal career stories).

## 4. Write the article

Create `_source/articles/<short-kebab-name>.md`:

```markdown
---
slug: insights-<short-kebab-name>
title: <Title in sentence case, under ~70 characters>
dek: <One or two sentences, under ~200 characters, saying what the reader gets>
category: Power BI | Microsoft Fabric | SQL
author: <author key from step 3>
audience: consulting | training
date: <today, YYYY-MM-DD>
---

<intro paragraphs — the first paragraph is shown larger>

## <Section heading>   (h2 headings build the "On this page" contents)
...
## The bottom line
```

Writing rules:
- **800–1,300 words**, UK English spelling (organisation, modelling, analyse), plain and practical, short paragraphs, `**bold**` for key ideas.
- Voice: "we" for the company; no first-person personal anecdotes (the authors' backgrounds are not documented — never invent experience, clients, numbers, quotes or results).
- **Accuracy is mandatory.** Verify every product fact (features, licensing, limits, names, release status) against official Microsoft documentation (learn.microsoft.com) using web search/fetch before stating it. Don't quote prices. If unsure, leave it out.
- SQL: use ` ```sql ` fenced blocks, ANSI-style syntax, and **test every query** in Python `sqlite3` with a small sample table (note SQL Server differences such as `TOP` vs `LIMIT` in the text when relevant).
- DAX / M code: use ` ```dax ` or ` ```m ` fences; only use functions that exist and that you have checked.
- End with a short `## The bottom line` (or similar) section. Do not add your own CTA — the template adds one automatically.
- **Visuals are required (owner request, for neurodivergent and visual readers).** Every article must include **at least one, ideally two, diagrams** that show the idea rather than describe it — e.g. a workspace with its items and roles, a before/after data shape, a step-by-step flow, a which-option-when comparison. Build them as new entries in `FIGURES` in `_source/figures.py` reusing the existing building blocks (`flow`, `step`, `table`, `.arch`, `.journey`) and place `[[fig:<name>]]` on its own line in the markdown, near the text it explains. Every figure needs a plain-English `<figcaption>` saying what it shows. Check each figure renders at 1440px and 390px.
- **Do not copy Microsoft screenshots, product images or icons** into the site, and don't hotlink external images. Their reuse terms are not confirmed for a commercial site (the Fabric icon terms only allow diagrams, training materials or documentation, and the docs licence doesn't clearly cover images). Instead, where a real Microsoft screen helps, link to the relevant learn.microsoft.com page in the text (e.g. "Microsoft's guide shows this screen").
- **Readability for neurodivergent readers:** one idea per paragraph (2–4 sentences), numbered steps for any procedure, descriptive headings, a short `## In short` bullet list (3–4 bullets) right after the intro, and consistent terms (don't switch between synonyms for the same thing).

## 5. Publish

```bash
python3 _source/publish.py        # renders the link-preview image + rebuilds the site into the repo root
```

Check before committing:
- The new page exists: `ls insights-*.html` and the article appears first on `insights.html` and in `sitemap.xml`.
- Take Playwright screenshots of the new article at 1440px and 390px wide (Chromium is preinstalled) and look at them: no horizontal overflow, code blocks and any figure render correctly.
- `git status` shows only the expected changes (new article page + updated listing/home/sitemap/other pages' shared chrome, new `og-*.png`, `_source` changes).

Commit and push:

```bash
git add -A
git commit -m "Insights: <title>"
git push origin main
```

GitHub Pages updates the live site within a couple of minutes. Finish by reporting the article title, author, category and live URL:
`https://www.intelligencewithdata.com/<slug>`

## Never

- Never delete or rewrite existing articles, pages, `CNAME`, `.nojekyll`, or the contact/careers Formspree endpoints.
- Never change DNS, GitHub Pages settings, or anything outside this repository.
- Never publish anything that fails the accuracy checks above — skip the run and report why instead.
