from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# 初始化 Chrome Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://csie.asia.edu.tw/zh_tw/TeacherIntroduction")
time.sleep(2)
print("載入教師介紹主頁成功")

# 定義教師分類頁面
faculty_pages = {
    "Full-time": "https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Full_time_faculty",
    "Part-time": "https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Part_time_faculty"
}

# 準備 CSV 檔案寫入
csv_file = open("professors_expertise.csv", "w", newline="", encoding="utf-8-sig")
writer = csv.writer(csv_file)
writer.writerow(["教師類型", "姓名", "研究領域"])

for faculty_type, url in faculty_pages.items():
    print(f"\n處理：{faculty_type} 教授頁面")
    driver.get(url)
    time.sleep(3)

    # 抓出所有 <a> 標籤，篩選出教師個人頁面
    all_links = driver.find_elements(By.TAG_NAME, "a")
    professor_links = []
    for link in all_links:
        name = link.text.strip()
        href = link.get_attribute("href")
        if name and href and "/TeacherIntroduction/" in href and href.endswith(".html") is False:
            professor_links.append((name, href))

    print(f"發現 {len(professor_links)} 位 {faculty_type} 教授")
    if not professor_links:
        print(f"⚠ 未發現任何{faculty_type}教授，請檢查頁面結構或載入時間。")

    for name, href in professor_links:
        print(f"🔍 進入 {name} 的頁面...")
        driver.get(href)
        time.sleep(2)

        # 擷取研究領域
        try:
            expertise_element = driver.find_element(By.CLASS_NAME, "member-data-value-7")
            expertise = expertise_element.text.strip()
        except:
            expertise = "[擷取失敗]"

        writer.writerow([faculty_type, name, expertise])
        print(f"{faculty_type} - {name}: {expertise}")
        time.sleep(1)

driver.quit()
csv_file.close()
print("\n 所有資料擷取完成，已寫入 professors_expertise.csv")
