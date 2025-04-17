from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# 基本網站URL
base_url = "https://csie.asia.edu.tw"

# 初始化 Chrome Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://csie.asia.edu.tw/zh_tw/TeacherIntroduction")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # 確認頁面有教師資料
    all_links = driver.find_elements(By.TAG_NAME, "a")
    if not all_links:
        print(f"無法找到{faculty_type}教授資料")
        continue

    professor_links = []
    for link in all_links:
        name = link.text.strip()
        href = link.get_attribute("href")
        # 只選取包含"Professor" 且有 href 屬性的教師個人頁面
        if name and href and "/TeacherIntroduction/" in href and "Professor" in href:
            # 構建完整的 URL
            full_url = base_url + href if href.startswith("/") else href
            professor_links.append((name, full_url))

    print(f"發現 {len(professor_links)} 位 {faculty_type} 教授")

    # 確認抓取到的教授個人頁面
    if len(professor_links) == 0:
        print(f"未發現任何{faculty_type}教授，請檢查頁面結構或載入時間。")
    else:
        for name, href in professor_links:
            print(f"🔍 進入 {name} 的頁面...")
            driver.get(href)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "field")))

            # 抓取研究領域
            try:
                expertise = "[無資料]"
                fields = driver.find_elements(By.CSS_SELECTOR, ".field")
                print(f"抓取 {name} 的研究領域...")
                for field in fields:
                    label_elements = field.find_elements(By.CLASS_NAME, "field-label")
                    if label_elements and "研究領域" in label_elements[0].text:
                        value_element = field.find_element(By.CLASS_NAME, "field-item")
                        expertise = value_element.text.strip()
                        break
                if expertise == "[無資料]":
                    print(f"{name} 研究領域資料抓取失敗或無資料。")
            except Exception as e:
                expertise = "[擷取失敗]"
                print(f"錯誤: {e}")

            writer.writerow([faculty_type, name, expertise])
            print(f"{faculty_type} - {name}: {expertise}")
            time.sleep(1)

driver.quit()
csv_file.close()
print("\n所有資料擷取完成，已寫入 professors_expertise.csv")
