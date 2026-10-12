import asyncio, pathlib
from playwright.async_api import async_playwright
here = pathlib.Path(__file__).parent
VARIANTS = {
 "og-free-training.png": '''<span class="chip"><i></i>Free &middot; Live every Friday</span>
<h1>Power BI &amp; SQL Fridays. <em>Learn live, for free.</em></h1>
<p>Every Friday &middot; 6:00 PM UK &middot; Live on Google Meet</p>
<div class="foot"><span class="btn">Reserve your free seat &rarr;</span><span class="url">intelligencewithdata.com/free-training</span></div>
<div class="cal"><span>Every</span><b>FRI</b><em>6:00 PM UK</em></div>''',
 "og-default.png": '''<span class="chip"><i></i>Power BI &middot; Microsoft Fabric &middot; AI</span>
<h1 style="max-width:1000px">Stop rebuilding the same reports. <em>Let them run themselves.</em></h1>
<p>Data consultancy &amp; training for UK businesses and career-switchers</p>
<div class="foot"><span class="btn">Book a discovery call &rarr;</span><span class="url">intelligencewithdata.com</span></div>''',
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1200,"height":630})
        for name, html in VARIANTS.items():
            await pg.goto((here/"og.html").as_uri())
            await pg.evaluate("h => document.getElementById('content').outerHTML = h", html)
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=str(here/name))
        await b.close()
asyncio.run(main())
