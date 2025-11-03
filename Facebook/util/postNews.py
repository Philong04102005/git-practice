# Chưa
import re
import os
import sys
import json
import time
import random
import shutil
import tempfile
import math
from selenium.common.exceptions import TimeoutException
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
import pandas as pd

def post_to_facebook_group(driver: WebDriver, group_url: str, content = None, img = None):
    driver.get(group_url)
    time.sleep(random.uniform(4, 7))

    post_box = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div[1]/span",
    )

    if not post_box:
        print(f"[SKIP] Không tìm thấy nút 'Đăng bài'.")

    time.sleep(0.2)
    post_box.click()
    time.sleep(random.uniform(3, 5))

    # Nhập content
    if content != None:
        active_box = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]",
        )
        active_box.send_keys(content)
        time.sleep(random.uniform(3, 5))

    # Tải hình ảnh lên
    if img != "Không cần ảnh":
        file_input = driver.find_element(
            By.XPATH,
            "//input[@type='file' and @accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']",
        )
        file_input.send_keys(img)
        time.sleep(random.uniform(3, 5))

    # Nút đăng bài
    post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
    post_button.click()
    time.sleep(5)

def postFb(driver: WebDriver, content = None, img = None):
    post_box = driver.find_element(
        By.XPATH,
        "//span[contains(text(), 'Bạn đang nghĩ gì?')]/../..",
    )
    if not post_box:
        return "[SKIP] Không tìm thấy nút 'Đăng bài'."

    time.sleep(0.2)
    post_box.click()
    time.sleep(random.uniform(3, 5))

    # Nhập content
    if content != None:
        active_box = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]",
        )
        active_box.send_keys(content)
        time.sleep(random.uniform(3, 5))

    # Tải hình ảnh lên
    if img != "Không cần ảnh":
        file_input = driver.find_element(
            By.XPATH,
            "//input[@type='file' and @accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']",
        )
        file_input.send_keys(img)
        time.sleep(random.uniform(3, 5))

    # Nút đăng bài
    post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
    post_button.click()
    time.sleep(5)



def read_content(path):
    contents = pd.read_csv(path)
    contents["status"] = contents["status"].astype(int)
    return contents


def runPostNews(driver: WebDriver, groups: pd.DataFrame, path, check_date = False):   
    contents = read_content(path)
    print(f"[INFO] Bắt đầu quy trình đăng bài trên group.")    
    print("Các bài viết chưa đăng: ")
    start, end = 0
    for i in contents.iloc[:,5]:
        if contents.iloc[:,5][i] == 0:
            print(f"{end}. Content: {contents.iloc[:,3][i]}")
            end += 1
            if end == 1:
                start = i
    choice = int(input("Chọn content muốn đăng: "))
    
    _, _, type, content, img, _ = contents.iloc[[choice + start]]
    if type == "both":
        for fanpage, link in groups.values:
            print(f"[INFO] Tiến hành đăng bài trên group: {fanpage}")
            post_to_facebook_group(
                driver, group_url=link, content=content, img=img
            )
            print(
                f"[SUCCESS] Đăng thành công bài viết với content: [{content}] tại group: {fanpage}"
            )
        print("Đăng trên page chưa có")
    elif type == "group":
        for fanpage, link in groups.values:
            print(f"[INFO] Tiến hành đăng bài trên group: {fanpage}")
            post_to_facebook_group(
                driver, group_url=link, content=content, img=img
            )
            print(
                f"[SUCCESS] Đăng thành công bài viết với content: [{content}] tại group: {fanpage}"
            )
        print("Đăng trên page chưa có")
    elif type == "page":
        print("Chưa có")
    else:
        print("Pass vì ko có cột type")
    # Cập nhật Status thành đã đăng
    contents.at[choice + start, "status"] = 1
    contents.to_csv(path, index=False)    
    
    
def filterPost(dataframe):
    for i in range(len(dataframe.iloc[:,1])):
        if dataframe.iloc[:,1][i] != "post":
            dataframe = dataframe.drop(index= i)
            
def check_datetime(date):  
    today = datetime.now().strftime("%d/%m/%Y")
    return date == None or date == today

def crawlContent(num_sheet = 0, spreadsheet_id = "1pDS-IWI--FWVgOYuMBqsbbANGTvGkmHIBWdFgFvR-hU"):
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={num_sheet}"
    try:
        df = pd.read_csv(url, on_bad_lines='skip', quotechar='"')
    except Exception as e:
        print("Error:", e)

    df = df.drop(columns="instruction")
    df["status"] = 0
    try:
        df_old = pd.read_csv("../data/content/contentFull.csv")
        new_row = df.iloc[len(df_old):]
        df_final = pd.concat([df_old, new_row], ignore_index=True)
    except Exception as e:
        print("File cũ không tồn tại")
        df_final = df
    filterPost(df_final)
    df_final.to_csv("../data/content/contentFull.csv", index=False)
    
def Menu():
    print("========== Chức năng =============")
    print("1. Crawl dữ liệu content từ gg sheet")
    print("2. Đăng toàn bộ post lên")
    print("3. Đăng bài post của ngày hôm nay")
    print("0. Thoát chương trình")

def subMenu():
    print("========Chọn cái cần chỉnh sửa========")
    print("1. Chỉnh spreadsheet_id")
    print("2. Chỉnh sheet_id")
    print("3. Chỉnh spreadsheet_id và sheet_id")
    print("4. Không upgrade")
    print("0. Thoát chức năng")

def post_main(driver, groups, contents_path):
    while True:
        Menu()
        choice = int(input("Nhập chức năng: "))
        match choice:
            case 1:
                subMenu()
                sub_choice = int(input("Nhập lựa chọn: "))
                match sub_choice:
                    case 1:
                        spreadsheet_id = input("Nhập spreadsheet_id: ")
                        crawlContent(spreadsheet_id=spreadsheet_id)
                    case 2:
                        sheet_id = input("Nhập sheet_id: ")
                        crawlContent(num_sheet=sheet_id)
                    case 3:
                        spreadsheet_id = input("Nhập spreadsheet_id: ")
                        sheet_id = input("Nhập sheet_id: ")
                        crawlContent(spreadsheet_id=spreadsheet_id, num_sheet=sheet_id)
                    case 4:
                        crawlContent()
                    case 0:
                        break
                    case _:
                        print("[INFO] Invalid selection.")
            case 2:
                runPostNews(driver, groups, contents_path)
                print("Chạy đang bài xong")
            case 3:
                break
            case 0:
                break
            case _:
                print("[INFO] Invalid selection.")

