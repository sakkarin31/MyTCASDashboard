import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_fee(page, program_url):
    """
    เข้าไปหน้า program_url แล้วดึงค่าใช้จ่ายของหลักสูตร
    """
    await page.goto(program_url)
    await page.wait_for_selector("dl", timeout=10000)

    # หา element <dt> ที่มีข้อความ "ค่าใช้จ่าย"
    dt_elements = await page.query_selector_all("dl dt")
    for dt in dt_elements:
        dt_text = (await dt.inner_text()).strip()
        if "ค่าใช้จ่าย" in dt_text:
            dd = await dt.evaluate_handle("el => el.nextElementSibling")
            if dd:
                fee_text = (await dd.inner_text()).strip()
                return fee_text
    return "ไม่พบข้อมูล"

async def main():
    input_file = "programs_engineering.csv"  
    output_file = "programs_with_fee.csv"

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
            program_name = row["program_name"]
            program_url = row["program_url"]

            print(f"ดึงค่าใช้จ่าย: {university} | {program_name}")

            try:
                fee = await scrape_fee(page, program_url)
            except Exception as e:
                print(f"Error: {e}")
                fee = "ไม่สามารถดึงข้อมูลได้"

            results.append({
                "university": university,
                "faculty": faculty,
                "field_name": field_name,
                "program_name": program_name,
                "fee": fee
            })

        await browser.close()

    # เขียนไฟล์ CSV ใหม่ โดยแทน program_url ด้วยค่าใช้จ่าย
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["university", "faculty", "field_name", "program_name", "fee"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"เสร็จสิ้น บันทึกไฟล์ {output_file}")

asyncio.run(main())
