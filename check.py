import asyncio
from playwright.async_api import async_playwright, Playwright
import time

url = 'https://www.amazon.com/s?k=gaming+headsets&_encoding=UTF8&content-id=amzn1.sym.12129333-2117-4490-9c17-6d31baf0582a&pd_rd_r=3978412d-3c67-4c01-83f0-f244be38ab2b&pd_rd_w=RlFz5&pd_rd_wg=m0OhB&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=4XFYV3PJFVZZHK4JWM4Q&ref=pd_hp_d_atf_unk'
async def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(url)
    time.sleep(5)

    # other actions...
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
