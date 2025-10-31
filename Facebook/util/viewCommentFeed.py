from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random

def scroll(driver):
    actions = ActionChains(driver)
    for _ in range(random.randint(3, 6)):
        actions.send_keys(Keys.SPACE).perform()
    time.sleep(2)

def comment(driver, content):
    try:
        comment_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Viết bình luận" or @aria-label="Leave a comment"]'))
        )
        comment_box.click()
        scroll(driver)

        btn = driver.find_element(By.XPATH, '//div[@aria-label="Close" or @aria-label="Đóng"]')
        time.sleep(2)
        btn.click()
        print('[INFO] Đã tắt popup bình luận')
        time.sleep(2)
        return True
        
    except:
        print("[INFO] Cuộn trang để tải thêm bài viết...")
        return False
        

def comment_in_feed(driver, content, max_comments=2):
    driver.get("https://m.facebook.com/")
    print("[INFO] Bắt đầu bình luận trong feed...")
    time.sleep(2)

    while max_comments:
        try:
            scroll(driver)
            time.sleep(5)
            res = comment(driver, content)
            if res: 
                max_comments -= 1
        except Exception as e:
            print(f"[ERROR] Vòng lặp chính lỗi: {e}")
            break
