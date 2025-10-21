import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd


def share_post_from_web(driver: WebDriver, link_group: str, link_share: str): 
    try: 
        print(f"[INFO] Truy cập để share bài trên group: {link_group}.")
        driver.get(link_group)
        time.sleep(random.uniform(2, 3))

        write_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Write something...') or contains(text(), 'Bạn viết gì đi...')]"))
        )

        write_btn.click() 
        time.sleep(random.uniform(3, 5)) 
        
        # Dán đường link vô 
        # Tìm ô nhập bình luận
        input_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@role='textbox' and @contenteditable='true' and (@aria-placeholder='Create a public post…' or @aria-placeholder='Tạo bài viết công khai...')]")
            )
        )
        
        input_box.click()
        time.sleep(random.uniform(1, 2))
        
        # Nhập nội dung 
        for ch in link_share:
            input_box.send_keys(ch)
            time.sleep(random.uniform(0.05, 0.15))  # Giả lập gõ phím

        time.sleep(random.uniform(2, 3))

        # Xoá đường link 
        # 1. Gửi tổ hợp phím Ctrl + A (Select All)
        input_box.send_keys(Keys.CONTROL, 'a')
        
        time.sleep(random.uniform(1, 2))
        
        # 2. Gửi phím Delete
        input_box.send_keys(Keys.DELETE)
        
        time.sleep(random.uniform(2, 3))
        
        # Bấm đăng bài
        close_post = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[(@aria-label='Post' or @aria-label='Đăng') and @role='button']")
            )
        )
        close_post.click()
        time.sleep(random.uniform(6, 8))
        

        print("[SUCCESS] Đăng bài thành công.")
        driver.get("https://www.facebook.com/")
        time.sleep(random.uniform(1, 2))
        
        
    except Exception as e: 
        print(f"[ERORR] Đăng bài không thành công, lỗi {e}")
        