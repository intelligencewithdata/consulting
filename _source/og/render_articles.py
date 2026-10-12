"""Render a 1200x630 link-preview PNG for every Insights article that doesn't have one yet.
Usage: python3 _source/og/render_articles.py [--all]"""
import asyncio, html, pathlib, sys
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import insights


def variant(a):
    t, c = html.escape(a["title"]), html.escape(a["category"].upper())
    return (f'<span class="chip"><i></i>Insights &middot; {c}</span>'
            f'<h1 style="font-size:{62 if len(a["title"]) < 70 else 54}px;max-width:1040px">{t}</h1>'
            f'<p>By {a["au"]["name"]} &middot; {a["au"]["role"]}</p>'
            '<div class="foot"><span class="btn">Read the article &rarr;</span><span class="url">intelligencewithdata.com/insights</span></div>')


async def main(force):
    todo = [a for a in insights.load() if force or not (HERE / f'og-{a["slug"]}.png').exists()]
    if not todo:
        print("no new preview images needed"); return
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for a in todo:
            await pg.goto((HERE / "og.html").as_uri())
            await pg.evaluate("h => document.getElementById('content').outerHTML = h", variant(a))
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=str(HERE / f'og-{a["slug"]}.png'))
            print("rendered", a["slug"])
        await b.close()

asyncio.run(main("--all" in sys.argv))
