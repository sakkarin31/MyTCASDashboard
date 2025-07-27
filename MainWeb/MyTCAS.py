import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_programs(page, field_url):
    """
    เข้าไปที่หน้า field_url แล้วดึงชื่อหลักสูตรและ URL ของหลักสูตรทั้งหมดในหน้านั้น
    """
    await page.goto(field_url)
    await page.wait_for_selector("a[href*='/programs/']", timeout=10000)

    program_links = await page.query_selector_all("a[href*='/programs/']")
    programs = []
    for a in program_links:
        href = await a.get_attribute("href")
        # ดึงชื่อหลักสูตรจาก
        program_span = await a.query_selector("span.program")
        if program_span:
            name = (await program_span.inner_text()).strip()
        else:
            name = (await a.inner_text()).strip()

        if href and name:
            full_url = href if href.startswith("http") else "https://course.mytcas.com" + href
            programs.append({
                "program_name": name,
                "program_url": full_url
            })
    return programs

async def main():
    input_file = "universities_faculty_filtered_fields2.csv"  
    output_file = "programs_engineering.csv"

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
            university = row["university"]
            faculty = row["faculty"]
            field_name = row["field_name"]
            field_url = row["field_url"]

            print(f"Processing {university} | {faculty} | {field_name}")

            try:
                programs = await scrape_programs(page, field_url)
                if not programs:
                    print(f"ไม่พบหลักสูตรใน {field_name} ของ {university}")
                    continue
                for prog in programs:
                    results.append({
                        "university": university,
                        "faculty": faculty,
                        "field_name": field_name,
                        "program_name": prog["program_name"],
                        "program_url": prog["program_url"]
                    })
                print(f"เจอหลักสูตร {len(programs)} รายการ ใน {field_name} ของ {university}")
            except Exception as e:
                print(f"Error ดึงหลักสูตรจาก {field_url}: {e}")

        await browser.close()

    # บันทึกไฟล์ CSV ผลลัพธ์
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["university", "faculty", "field_name", "program_name", "program_url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"จบงาน บันทึกไฟล์ {output_file}")

asyncio.run(main())
