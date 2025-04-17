from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 设置 WebDriver，使用 webdriver-manager 自动管理驱动
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 打开主页面
url = "https://csie.asia.edu.tw/zh_tw/TeacherIntroduction"
driver.get(url)

# 等待主页面加载并点击进入兼职教授页面
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Part-time Faculty"))
)
part_time_link = driver.find_element(By.LINK_TEXT, "Part-time Faculty")
part_time_link.click()

# 等待兼职教授页面加载
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.views-row .views-field-title a'))
)

# 获取兼职教授个人页面的链接
part_time_professor_links = driver.find_elements(By.CSS_SELECTOR, '.views-row .views-field-title a')

# 保存兼职教授专长信息
with open('professors_expertise.txt', 'w', encoding='utf-8') as f:
    # 遍历每个教授的个人页面链接
    for link in part_time_professor_links:
        professor_url = link.get_attribute('href')
        driver.get(professor_url)
        
        # 等待教授页面加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.field-name-field-discipline-expertise .field-item'))
        )
        
        # 获取教授的专长信息
        professor_expertise = driver.find_elements(By.CSS_SELECTOR, '.field-name-field-discipline-expertise .field-item')
        
        # 将教授的专长信息写入文件
        for expertise in professor_expertise:
            f.write(f"Part-time - {link.text}: {expertise.text}\n")
        
        # 返回兼职教授列表页
        driver.back()

# 返回主页面并点击进入全职教授页面
driver.back()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Full-time Faculty"))
)
full_time_link = driver.find_element(By.LINK_TEXT, "Full-time Faculty")
full_time_link.click()

# 等待全职教授页面加载
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.views-row .views-field-title a'))
)

# 获取全职教授个人页面的链接
full_time_professor_links = driver.find_elements(By.CSS_SELECTOR, '.views-row .views-field-title a')

# 保存全职教授专长信息
with open('professors_expertise.txt', 'a', encoding='utf-8') as f:
    # 遍历每个教授的个人页面链接
    for link in full_time_professor_links:
        professor_url = link.get_attribute('href')
        driver.get(professor_url)
        
        # 等待教授页面加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.field-name-field-discipline-expertise .field-item'))
        )
        
        # 获取教授的专长信息
        professor_expertise = driver.find_elements(By.CSS_SELECTOR, '.field-name-field-discipline-expertise .field-item')
        
        # 将教授的专长信息写入文件
        for expertise in professor_expertise:
            f.write(f"Full-time - {link.text}: {expertise.text}\n")
        
        # 返回全职教授列表页
        driver.back()

# 关闭浏览器
driver.quit()
