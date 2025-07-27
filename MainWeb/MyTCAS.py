import asyncio
import csv
from playwright.async_api import async_playwright

async def get_all_universities(page):
    # ดึงรายชื่อมหาวิทยาลัยทั้งหมด
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

async def scrape_universities_with_engineering():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        universities = await get_all_universities(page)
        results = []

        for uni in universities:
            await page.goto(uni["url"])
            await page.wait_for_timeout(5000)  

            faculty_links = await page.query_selector_all("a[href*='/faculties/']")

            if not faculty_links:
                print(f"ไม่มีข้อมูลคณะสำหรับ {uni['name']}")
                continue  # ข้ามมหาวิทยาลัยนี้

            for fl in faculty_links:
                text = (await fl.inner_text()).strip()

                if "วิศวกรรมศาสตร์" in text:
                    results.append({
                        "name": uni["name"],
                        "faculty": text
                    })

        await browser.close()

    # บันทึกลง CSV
    with open("universities_with_engineering4.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "faculty"])
        writer.writeheader()
        writer.writerows(results)

    print(f"เจอมหาวิทยาลัยที่มีคณะวิศวกรรมศาสตร์ {len(results)} แห่ง")

asyncio.run(scrape_universities_with_engineering())
