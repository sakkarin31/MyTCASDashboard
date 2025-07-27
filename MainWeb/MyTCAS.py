import asyncio
import csv
from playwright.async_api import async_playwright

async def get_all_universities(page):
    # เปิดหน้าเว็บรวมมหาวิทยาลัย
    await page.goto("https://course.mytcas.com/universities")
    await page.wait_for_selector("a.brand")

    universities = []
    links = await page.query_selector_all("a.brand")

    for link in links:
        href = await link.get_attribute("href")
        text = (await link.inner_text()).strip()

        if href and href.startswith("/universities/"):
            universities.append({
                "name": text,
                "url": "https://course.mytcas.com" + href
            })

    return universities

async def scrape_and_save():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=True ไม่แสดงหน้าจอ
        page = await browser.new_page()

        universities = await get_all_universities(page)

        # ปิด browser
        await browser.close()

    # ✅ บันทึกลง CSV
    with open("universities_list.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url"])
        writer.writeheader()
        writer.writerows(universities)

    print(f"✅ บันทึกข้อมูล {len(universities)} มหาวิทยาลัยลง universities_list.csv เรียบร้อย!")

asyncio.run(scrape_and_save())
