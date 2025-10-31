import pandas as pd
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
 
def add_friend(driver: WebDriver, friend_link: str):
    try:
        driver.get(friend_link + "/friends")
        time.sleep(random.uniform(2, 3))

        add_friend_button = driver.find_element(
            By.XPATH,
            "//span[contains(text(), 'Thêm bạn bè') or contains(text(), 'Add Friend')]/ancestor::div[@role='button']"
        )
        if add_friend_button:
            add_friend_button.click()
        else: 
            print(f"[INFO] Không tìm thấy nút 'Thêm bạn bè' trên trang: {friend_link}")
            return False
        
        time.sleep(random.uniform(2, 4))

        print(f"[SUCCESS] Đã gửi lời mời kết bạn tới: {friend_link}")
        return True 

    except Exception as e:
        print(f"[ERROR] Lỗi khi gửi lời mời kết bạn tới bạn bè của {friend_link}: {e}")
        return False
