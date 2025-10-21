from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

def smooth_scroll(driver, delay=0.5):
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(delay)

def view_comment(driver):
    try:
        comment_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Viết bình luận" or @aria-label="Leave a comment"]'))
        )
        comment_box.click()
        smooth_scroll(driver)

        btn = driver.find_element(By.XPATH, '//div[@aria-label="Close" or @aria-label="Đóng"]')
        time.sleep(2)
        btn.click()
        print('[INFO] Đã tắt popup bình luận')
        time.sleep(2)
        return True
        
    except:
        print("[INFO] Cuộn trang để tải thêm bài viết...")
        return False

def run_like_post(driver, max_likes=5):
    driver.get("https://www.facebook.com/")
    time.sleep(5)
    actions = ActionChains(driver)
    actions.scroll_to_element(driver.find_element(By.XPATH, '//div[@aria-posinset]')).perform()
    while max_likes:
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Thích" or @aria-label="Like"]')))
            actions.click_and_hold(btn).perform()
            rd = random.choice([1,2])
            if rd == 1:
                actions.click(btn).perform()
            else:
                actions.click(driver.find_element(By.XPATH, '//div[@aria-label="Yêu thích" or @aria-label="Love"]')).perform()
                view_comment(driver)
            
            max_likes -= 1
            print(f"[SUCCESS] Đã like {5 - max_likes}/5 bài viết")
            time.sleep(random.uniform(2, 5))
            smooth_scroll(driver)
            time.sleep(random.uniform(2, 5))
        except:
            print("[WARNING] Không tìm thấy bài viết để like.")
            smooth_scroll(driver)
            time.sleep(2)
