# Đã Check
import pandas as pd
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

def send_message(driver, link, message):
    try:
        driver.get(link)
        time.sleep(random.uniform(2, 4))
        close_buttons = driver.find_elements(
            By.XPATH, "//div[@role='button' and (@aria-label='Đóng đoạn chat' or @aria-label='Close chat')]"
        )

        # Duyệt qua từng nút và nhấn
        for i, btn in enumerate(close_buttons, start=1):
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.3)
                btn.click()
                print(f"[INFO] Đã đóng chat {i}/{len(close_buttons)}")
            except (ElementClickInterceptedException, StaleElementReferenceException):
                print(f"[WARNING] Không thể đóng chat {i}, bỏ qua.")
            except Exception as e:
                print(f"[ERROR] Lỗi khi đóng chat {i}: {e}")

        # Nhấn nút "Nhắn tin"
        btn = driver.find_element(
            By.XPATH, "//span[text()='Nhắn tin' or text()='Message']/ancestor::div[@role='button']"
        )
        btn.click()
        time.sleep(random.uniform(3, 5))

        # Gõ và gửi tin
        input_box = driver.find_element(
            By.XPATH, "//div[@role='textbox' and (@aria-label='Message' or @aria-placeholder='Aa')]"
        )

        lines = message.split("\n")

        for idx, line in enumerate(lines):
            input_box.send_keys(line)  # gõ nguyên dòng
            if idx != len(lines) - 1:  # xuống dòng nếu không phải dòng cuối
                input_box.send_keys(Keys.SHIFT, Keys.ENTER)
            # Thêm delay tự nhiên giữa các dòng
            time.sleep(random.uniform(0.2, 0.5))
        
        time.sleep(random.uniform(0.8, 1.5))
        input_box.send_keys(Keys.ENTER)
        
        time.sleep(random.uniform(1, 2))

        close_btn = driver.find_element(
            By.XPATH, "//div[@role='button' and (@aria-label='Đóng đoạn chat' or @aria-label='Close chat')]"
        )
        close_btn.click()
        time.sleep(random.uniform(1, 2)) 
        print(f"[SUCCESS] Đã gửi tin nhắn cho: {link}")
        time.sleep(random.uniform(2, 3))

    except Exception as e:
        print(f"[ERROR] Lỗi khi gửi tin cho {link}: {e}")
            
def run_manual_range(driver, friends, messages):
    """Cho phép nhập khoảng index và gửi tin nhắn cho những bạn đó."""
    friends = friends.to_dict('records')
    messages = messages.to_dict('records')
    if not friends:
        print("[ERROR] Không có bạn bè nào để gửi.")
        return

    total = len(friends)
    print(f"\n Tổng số bạn bè: {total}")
    start = int(input(f"Nhập index bắt đầu (0 → {total - 1}): "))
    end = int(input(f"Nhập index kết thúc (<= {total - 1}): "))

    if start < 0 or end >= total or start > end:
        print("[ERROR] Khoảng index không hợp lệ.")
        return

    selected = friends[start:end + 1]
    print(f"\n[START] Bắt đầu gửi cho {len(selected)} bạn (từ {start} → {end})...\n")

    for idx, friend in enumerate(selected, start=start):
        name = friend.get("name", "Unknown")
        link = friend.get("link")
        message = random.choice(messages).get("CONTENT", "Hello!")
        print(f"👤 [{idx}/{end}] → Gửi tin cho: {name}")
        send_message(driver, link, message)

        print("\n[END] Hoàn tất gửi tin cho nhóm bạn đã chọn!")
