# Đã Check
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import pandas as pd

def scroll_and_get_post_authors(driver, max_scroll=5):
    authors = set()

    for _ in range(max_scroll):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(random.uniform(1, 3))

        try:
            # Lấy tất cả thẻ <a> có chứa "/user/" trong href
            a_tags = driver.find_elements(By.TAG_NAME, "a")
            for a in a_tags:
                try:
                    href = a.get_attribute("href")
                    if href and "/user/" in href:
                        # Loại bỏ query params nếu có
                        clean_href = href.split("?")[0]
                        full_url = (
                            f"https://m.facebook.com{clean_href}"
                            if clean_href.startswith("/")
                            else clean_href
                        )
                        authors.add(full_url)
                except:
                    continue 
        except Exception as e:
            print(f"[WARNING] Lỗi khi xử lý thẻ <a>: {e}")

    print(f"[INFO] Tìm thấy {len(authors)} người đăng bài.")
    return list(authors)


def send_friend_request(driver, profile_url):
    print(f"[INFO] Truy cập profile: {profile_url}")
    driver.get(profile_url)
    time.sleep(random.uniform(2, 4))

    try:
        # Tìm nút thêm bạn bè
        add_buttons = driver.find_elements(
            By.XPATH,
            "//div[(@role='button') and (contains(@aria-label, 'Kết bạn với') or contains(@aria-label, 'Add Friend'))]",
        )

        if not add_buttons:
            print(f"[SKIP] Không tìm thấy nút 'Thêm bạn bè'.")
            return
        else:            
            add_buttons[0].click()
            print(f"[SUCCESS] Đã gửi lời mời kết bạn đến: {profile_url}")
            time.sleep(random.uniform(2, 4))

    except Exception as e:
        print(f"[ERROR] Không gửi được lời mời ({profile_url}): {e}")

def runAddFriend(driver: WebDriver, groups: pd.DataFrame, max_scroll=2, max_requests=3):
    group_list = groups['Link'].tolist()
    while group_list:
        group = random.choice(group_list)
        driver.get(group)
        print(f"[INFO] Truy cập nhóm: {group}")
        time.sleep(random.uniform(1, 3))
        
        authors = scroll_and_get_post_authors(driver, max_scroll=max_scroll)
        for i, author in enumerate(authors):
            if i >= max_requests:
                break
            send_friend_request(driver, author)
            time.sleep(random.uniform(2, 3))  
        time.sleep(10)
        group_list.remove(group)