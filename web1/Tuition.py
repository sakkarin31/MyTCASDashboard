
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # เปิด browser แบบไม่ซ่อน
        page = await browser.new_page()
        await page.goto("https://www.mytcas.com/", timeout=60000)

        print("หน้าเว็บจะเปิดค้างไว้ 10 วินาที...")
        await asyncio.sleep(10)  # ค้างไว้ 10 วินาที

        await browser.close()

asyncio.run(main())