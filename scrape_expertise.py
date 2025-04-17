from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 啟動瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)

# 目標網址（教師介紹主頁）
main_url = "https://csie.asia.edu.tw/zh_tw/TeacherIntroduction"
driver.get(main_url)

# 儲存結果的檔案
output_file = "professors_expertise.txt"
f = open(output_file, "w", encoding="utf-8")

# 定義要爬的頁面（全職與兼任）
faculty_pages = {
    "Full-time": "https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Full_time_faculty",
    "Part-time": "https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Part_time_faculty"
}

for faculty_type, url in faculty_pages.items():
    print(f"抓取 {faculty_type} 教授資料中...")
    driver.get(url)
    time.sleep(2)

    # 抓取所有教授連結
    links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".views-field-title a")
    ))
    
    for link in links:
        name = link.text.strip()
        href = link.get_attribute("href")
        driver.get(href)
        time.sleep(1)

        # 抓取專長欄位
        try:
            expertise_elems = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".field-name-field-discipline-expertise .field-item")
            ))
            for exp in expertise_elems:
                f.write(f"{faculty_type} - {name}: {exp.text.strip()}\n")
        except:
            f.write(f"{faculty_type} - {name}: [無專長資訊]\n")
        
        driver.back()
        time.sleep(1)

f.close()
driver.quit()
print("完成，資料已儲存到 professors_expertise.txt")
