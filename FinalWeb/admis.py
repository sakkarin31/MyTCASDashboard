import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_rounds(page, url):
    await page.goto(url)
    await page.wait_for_selector("ul.body.t-program")

    rounds = {"r1": "-", "r2": "-", "r3": "-", "r4": "-"}

    for r in rounds.keys():
        li = await page.query_selector(f"li#{r}")
        if not li:
            continue

        # ถ้าไม่เปิดรับสมัคร
        not_open = await li.query_selector(".not-open")
        if not_open:
            rounds[r] = "-"
            continue

        # หา <small class="receive-quota"> <b>60</b> </small>
        quota_b = await li.query_selector("small.receive-quota b")
        if quota_b:
            rounds[r] = (await quota_b.text_content()).strip()
        else:
            rounds[r] = "-"

    return rounds

async def main():
    input_file = "programs_engineering.csv"   # ไฟล์ input ที่มี program_url
    output_file = "programs_with_rounds.csv"  # ไฟล์ output

    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        results = []
        for row in rows:
            print(f"กำลังดึงข้อมูล: {row['program_name']}")
            rounds = await scrape_rounds(page, row["program_url"])
            print(f"ผลลัพธ์: {rounds}")  # Debug ดูค่าที่ดึงได้

            results.append({
                "university": row["university"],
                "faculty": row["faculty"],
                "field_name": row["field_name"],
                "program_name": row["program_name"],
                "r1": rounds["r1"],
                "r2": rounds["r2"],
                "r3": rounds["r3"],
                "r4": rounds["r4"],
            })

        await browser.close()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["university", "faculty", "field_name", "program_name", "r1", "r2", "r3", "r4"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"บันทึกไฟล์เสร็จ: {output_file}")

asyncio.run(main())
