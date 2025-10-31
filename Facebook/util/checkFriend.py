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
    time.sleep(3)
    
# def search_friend(driver: WebDriver):
#     xpath = "//span[contains(text(), 'người bạn')]"
#     element = driver.find_element(By.XPATH, xpath)
#     num = int((element.text).split(" ")[0])
#     return num


def check_post(driver: WebDriver):
    xpath = "//span[contains(text(), 'người bạn')]"
    element = driver.find_element(By.XPATH, xpath)
    num = int((element.text).split(" ")[0])
    return num


    
def main():
    account = pd.read_csv("../data/account/account_checked.csv")
    today = date.today()
    cookies = os.listdir("../data/account/cookie")
    account["Message"] = "n"
    account["Post"] = "n"
    account["TotalFriends"] = account["TotalFriends_2025-10-29"]
    account[f"TotalFriends_{today}"] = 0
    account.drop("TotalFriends_2025-10-29", axis=1, inplace=True)
    for cookie in cookies:
        acc_id = cookie.split(".")[0]
        if (account.iloc[:,0] == acc_id).any():
            print(f"[INFO] Đang xử lý tài khoản với ID: {acc_id}")
            driver = loginFacebookWithCookies.runLogin(f"../data/account/cookie/{cookie}")
            if driver:
                login(driver=driver)
                # num = search_friend(driver)
                num = int(input("Nhập số bạn bè: "))
                index = int([i for i in range(len(account)) if account.iloc[i, 0] == acc_id][0])             
                mess = input("Có nhắn tin không: ")
                post_ = input("Có đăng bài không: ")
                account.at[index, f"TotalFriend_{today}"] = num
                account.at[index, "Message"] = mess
                account.at[index, "Post"] = post_
                driver.quit()
            else:
                print(f"[ERROR] Không thể đăng nhập tài khoản với ID: {acc_id}")
    account.to_csv(r"C:\PhiLong\Revoland\Revoland_AI-Automation\Seeding\Facebook\data\account\account_checked.csv")
    
if __name__ == "__main__":
    main()