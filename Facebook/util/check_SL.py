import time
import random
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import StaleElementReferenceException 
from typing import List, Dict, Set
import loginFacebookWithCookies
from datetime import date

def login(driver):
    driver.get("https://www.facebook.com/me") 
    driver.execute_script("window.scrollBy(0, 1300);")

def type():
    type = input("Loại: ")
    return type

def main():
    account = pd.read_csv("../data/account/status_false.csv")
    # today = date.today()
    cookies = os.listdir("../data/account/cookie")
    # account["TotalFriends"] = account["TotalFriends_2025-10-29"]
    # account.drop("TotalFriends_2025-10-29", axis=1, inplace=True)
    account["Type"] = ""
    for cookie in cookies:
        acc_id = cookie.split(".")[0]
        if (account.iloc[:,0] == acc_id).any():
            print(f"[INFO] Đang xử lý tài khoản với ID: {acc_id}")
            driver = loginFacebookWithCookies.runLogin(f"../data/account/cookie/{cookie}")
            if driver:
                login(driver=driver)
                num = type()
                index = int([i for i in range(len(account)) if account.iloc[i, 0] == acc_id][0])             
                account.at[index, "Type"] = num
                account.to_csv("../data/account/status_false.csv", index=False)
                driver.quit()
            else:
                print(f"[ERROR] Không thể đăng nhập tài khoản với ID: {acc_id}")
    
    
if __name__ == "__main__":
    main()