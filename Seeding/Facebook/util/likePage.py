from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

def scroll(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)

def like_page(driver, max_likes=5):
    actions = ActionChains(driver)
    driver.get("https://www.facebook.com/Revolandofficial")
    time.sleep(5)
    actions.scroll_to_element(driver.find_element(By.XPATH, '//div[@aria-posinset]')).perform()
    while max_likes:
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Thích" or @aria-label="Like"]'))
            )
            actions.click_and_hold(btn).perform()
            time.sleep(2)
            rd = random.randint(1, 2)
            if rd == 1:
                like_btn = driver.find_element(By.XPATH, '//div[@aria-label="Thích" or @aria-label="Like"]')
                actions.click(like_btn).perform() 
                
            else:
                like_btn = driver.find_element(By.XPATH, '//div[@aria-label="Love" or @aria-label="Yêu thích"]')
                actions.click(like_btn).perform()

            print(f"[INFO] Đã thích {5 - max_likes + 1} bài viết")
            max_likes -= 1
            time.sleep(2)
            scroll(driver)
            time.sleep(3)
        except Exception as e:
            scroll(driver)

    print("[INFO] Hoàn thành thích bài viết trên trang Revoland")