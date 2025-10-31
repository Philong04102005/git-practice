import time
import json
import sys
import random
import csv
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

sys.stdout.reconfigure(encoding='utf-8')

# Đảm bảo thư mục cần thiết tồn tại
os.makedirs("data/account", exist_ok=True)
os.makedirs("data/account/cookie", exist_ok=True)


class FacebookAccountManager:
    """Quản lý việc tải tài khoản, khởi tạo driver và logic đăng nhập/cookie."""

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """Tải tài khoản từ file CSV."""
        # ... (Phần load_accounts giữ nguyên như code bạn cung cấp)
        try:
            if not os.path.exists(self.csv_path):
                print(f"[ERROR] File CSV không tồn tại: {self.csv_path}")
                return []
            
            df = pd.read_csv(self.csv_path, header=0)
            df.columns = df.columns.str.strip()

            required_columns = ['acc_id', 'username', 'password', 'name', 'status']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"[ERROR] Thiếu các cột bắt buộc: {missing_columns}")
                return []
            
            accounts = []
            for _, row in df.iterrows():
                account_id = str(row['acc_id']).strip() if pd.notna(row['acc_id']) and str(row['acc_id']).strip() else f"acc_{random.randint(10000, 99999)}"

                account = {
                    'acc_id': account_id,
                    'username': str(row['username']).strip(),
                    'password': str(row['password']).strip(),
                    'name': str(row['name']).strip(),
                    'status': bool(row['status'])
                }
                accounts.append(account)
            
            print(f"[INFO] Đã tải {len(accounts)} tài khoản từ {self.csv_path}")
            return accounts
        except Exception as e:
            print(f"[ERROR] Không thể tải file CSV: {e}")
            return []

    def get_driver(self):
        """Thiết lập và trả về đối tượng Chrome driver."""
        # ... (Phần get_driver giữ nguyên)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--enable-unsafe-swiftshader")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Tắt logging của Chrome
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Tùy chọn để chạy ẩn danh nếu cần
        # chrome_options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def close_popup(self, driver):
        """Đóng các pop-up thường gặp của Facebook."""
        # ... (Phần close_popup giữ nguyên)
        try:
            continue_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[text()='Continue' or text()='Tiếp tục']/ancestor::div[@role='button']"
                ))
            )
            continue_btn.click()
            print("[INFO] Đã click Continue trong màn hình chọn profile")
            time.sleep(3)
        except:
            try:
                save_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//span[text()='Save' or text()='Lưu']/ancestor::div[@role='button']"
                    ))
                )
                save_btn.click()
                print("[INFO] Đã click Save trong popup lưu thông tin đăng nhập")
                time.sleep(2)
            except:
                try:
                    later = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//span[text()='Lúc khác' or text()='Not now']/ancestor::div[@role='button']"
                        ))
                    )
                    later.click()
                    print("[INFO] Đã tắt popup (Lúc khác)")
                except:
                    try:
                        close_btn = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                "//div[@aria-label='Đóng' or @aria-label='Close']"
                            ))
                        )
                        time.sleep(random.uniform(2, 3))
                        close_btn.click()
                        print("[INFO] Đã tắt popup (X)")
                    except:
                        pass
        
        # Xử lý popup thông báo Facebook - chọn Block
        try:
            block_notification_btn = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[text()='Block' or text()='Chặn']"
                ))
            )
            block_notification_btn.click()
            print("[INFO] Đã click Block trong popup thông báo Facebook")
            time.sleep(1)
        except:
            pass 
    
    def login_with_credentials(self, driver, username, password):
        """Đăng nhập bằng username và password."""
        # ... (Phần login_with_credentials giữ nguyên)
        try:
            print(f"[INFO] Đang đăng nhập với tài khoản: {username}")
            driver.get("https://www.facebook.com")
            time.sleep(3)
            
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(random.uniform(1, 2))
            
            password_field = driver.find_element(By.ID, "pass")
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(random.uniform(5, 10))
            
            login_button = driver.find_element(By.NAME, "login")
            login_button.click()
            
            time.sleep(10)
            print(driver.current_url)
            
            if "login" in driver.current_url or "checkpoint" in driver.current_url or "auth_platform" in driver.current_url:
                print(f"[ERROR] Đăng nhập thất bại cho tài khoản: {username}")
                return False
            if "https://www.facebook.com/" == driver.current_url:
                print(f"[INFO] Đăng nhập thành công cho tài khoản: {username}")
                self.close_popup(driver)
                return True
            print(f"[ERROR] Đăng nhập thất bại cho tài khoản: {username}")
            return False
        except Exception as e:
            print(f"[ERROR] Lỗi đăng nhập: {e}")
            return False
    
    def save_cookies(self, driver, account_id):
        """Lưu cookies vào thư mục data/cookie."""
        try:
            cookies = driver.get_cookies()
            # THAY ĐỔI ĐƯỜNG DẪN TỪ data/account -> data/account/cookie
            cookie_file = f"data/account/cookie/{account_id}.json"

            os.makedirs(os.path.dirname(cookie_file), exist_ok=True)
            
            with open(cookie_file, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            print(f"[INFO] Đã lưu cookies cho tài khoản {account_id} tại {cookie_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Không thể lưu cookies: {e}")
            return False
    
    def login_and_getCookie(self, account):
        driver = self.get_driver()
        
        if self.login_with_credentials(driver, account['username'], account['password']):
            self.save_cookies(driver, account['acc_id'])
            print(f"[SUCCESS] Đăng nhập và lưu cookie thành công cho {account['acc_id']} - {account['name']}")
        else:
            driver.quit()
    def update_csv(self):
        """Cập nhật status mới vào file CSV."""
        try:
            df = pd.read_csv(self.csv_path)
            acc_ids = os.listdir(f"data/account/cookie")
            acc_ids = [os.path.splitext(f)[0] for f in acc_ids if f.endswith('.json')]
            
            df['status'] = df['acc_id'].apply(lambda x: True if str(x) in acc_ids else False)
            df.to_csv(self.csv_path, index=False)
            print(f"[INFO] Đã cập nhật file CSV với trạng thái mới.")
        except Exception as e:
            print(f"[ERROR] Không thể cập nhật file CSV: {e}")

def Menu():
    print("=========== Accounts =============")
    print("1. Account đã check")
    print("2. Account chưa check")
    print("3. Lọc Account đã dead")

def main(): 
    Menu()
    choice = int(input("Nhập lựa chọn của bạn: "))
    choice = "_checked.csv" if choice == 1 else "_not_check.csv" if choice == 2 else False
    num_acc = int(input("Nhập số lượng account muốn check: "))
    mainager = FacebookAccountManager(f"data/account/account{choice}") 
    for account in mainager.accounts:
        if num_acc == 0:
            break
        print(f"\n[INFO] Xử lý tài khoản: {account['acc_id']} - {account['name']} ({account['username']})")
        mainager.login_and_getCookie(account)
        time.sleep(5)  # nghỉ giữa các lần đăng nhập tránh bị block
        num_acc -= 1
    
    mainager.update_csv(choice.split('.')[0])

if __name__ == "__main__":
    main()