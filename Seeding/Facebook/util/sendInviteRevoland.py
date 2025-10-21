# Đã Check
import json
import time
import random
import sys
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
import pandas as pd
import csv


def run_send_invite(driver: WebDriver):
    print("[INFO] Bắt đầu gửi lời mời thích trang Revoland...")
    try:
        driver.get("https://www.facebook.com/Revolandofficial")

        time.sleep(random.uniform(3, 5))
        
        btn = driver.find_element(
                        By.XPATH, "//div[@role='button' and (@aria-label='Xem thêm tùy chọn trong phần cài đặt trang cá nhân' or @aria-label='Profile settings see more options')]"
                    )
        
        btn.click() 
        time.sleep(random.uniform(2, 4))
        
        btn_invite = driver.find_element(
                        By.XPATH, "//span[contains(text(), 'Mời bạn bè') or contains(text(), 'Invite friends')]"
                    )
        btn_invite.click()
        time.sleep(random.uniform(2, 4))    
        
        select_all = driver.find_element(
            By.XPATH,
            "//div[contains(@aria-label, 'Chọn tất cả') or contains(@aria-label, 'Select All')]"
        )
        
        select_all.click() 
        time.sleep(random.uniform(2, 4))
        
        send_invite = driver.find_element(
            By.XPATH,
            "//span[contains(text(), 'Gửi lời mời') or contains(text(), 'Send Invitations')]"  
        )
        send_invite.click()      
        
        print("[SUCCESS] Đã gửi lời mời thích trang Revoland.") 
    except Exception as e:
        print(f"[ERROR] Lỗi khi gửi lời mời thích trang Revoland: {e}")
        return 
    