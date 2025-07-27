import asyncio
import csv
import re
from playwright.async_api import async_playwright

async def get_faculty_url(page, university_url, faculty_code):
    await page.goto(university_url)
    await page.wait_for_timeout(10000)  # รอโหลด

    faculty_links = await page.query_selector_all("a[href*='/faculties/']")
    for fl in faculty_links:
        text = (await fl.inner_text()).strip()
        match = re.match(r"(\d+)\.\s*(.+)", text)
        if match:
            code = match.group(1)
            if code == faculty_code:
                href = await fl.get_attribute("href")
                return "https://course.mytcas.com" + href
    return None

async def scrape_fields(page, faculty_url):
    await page.goto(faculty_url)
    await page.wait_for_selector("ul.u-list a[href*='/fields/']", timeout=20000)

    field_links = await page.query_selector_all("ul.u-list a[href*='/fields/']")
    fields = []
    for link in field_links:
        href = await link.get_attribute("href")
        name = (await link.inner_text()).strip()
        fields.append({
            "field_name": name,
            "field_url": "https://course.mytcas.com" + href
        })
    return fields

async def main():
    input_file = "universities_with_engineering4.csv"
    output_file = "universities_faculty_filtered_fields2.csv"

    rows = []
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        results = []
        for row in rows:
            university_name = row["name"].strip()
            faculty_full = row["faculty"].strip()
            faculty_code = faculty_full.split(".")[0]

            await page.goto("https://course.mytcas.com/universities")
            await page.wait_for_selector("a.brand")
            unv_links = await page.query_selector_all("a.brand")
            university_url = None
            for ul in unv_links:
                text = (await ul.inner_text()).strip()
                if text == university_name:
                    href = await ul.get_attribute("href")
                    university_url = "https://course.mytcas.com" + href
                    break
            if not university_url:
                print(f"ไม่พบ URL มหาวิทยาลัย: {university_name}")
                continue

            faculty_url = await get_faculty_url(page, university_url, faculty_code)
            if not faculty_url:
                print(f"ไม่พบ URL คณะ {faculty_full} ใน {university_name}")
                continue

            try:
                fields = await scrape_fields(page, faculty_url)
                if not fields:
                    print(f"ไม่พบสาขาใน {faculty_full} ของ {university_name}")
                    continue
                for f in fields:
                    if "คอมพิวเตอร์" in f["field_name"] or "ปัญญาประดิษฐ์" in f["field_name"]:
                        results.append({
                            "university": university_name,
                            "faculty": faculty_full,
                            "field_name": f["field_name"],
                            "field_url": f["field_url"]
                        })
                print(f"ดึงข้อมูลสาขาที่กรองใน {faculty_full} ของ {university_name} จำนวน {len(results)} รายการ")
            except Exception as e:
                print(f"Error ดึงสาขา {faculty_full} ใน {university_name}: {e}")

        await browser.close()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["university", "faculty", "field_name", "field_url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"จบการทำงาน บันทึกไฟล์ {output_file}")

asyncio.run(main())
