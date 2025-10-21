import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from util import (
    loginFacebookWithCookies
)


def main():
    driver = loginFacebookWithCookies.runLogin(
        f"data/account/cookie/acc_0001.json")
    print('[INFO] Đăng nhập thành công.')
    time.sleep(5)
    actions = ActionChains(driver=driver)

    groups = ["https://www.facebook.com/groups/muanhadathcm",
            "https://www.facebook.com/groups/nhabanhcm",
            "https://www.facebook.com/groups/804187998316826",
            "https://www.facebook.com/groups/785225373106811",
            ]
    
    links = list()
    names = list()
    for idx, gr in enumerate(groups):
        driver.get(gr + '/members')
        print(f"[INFO] Truy cập link {idx + 1}")
        time.sleep(5)
        for _ in range(100):
            hrefs = driver.find_elements(By.XPATH, "//a[@href]")
            links.extend([link.get_attribute("href") for link in hrefs])
            names.extend([name.get_attribute("aria-label") for name in hrefs])
            time.sleep(5)

            actions.send_keys(Keys.END).perform()
            time.sleep(5)

    
    
    df = pd.DataFrame(data={'names':names,
                            "links": links})
    
    remove_list = ["Facebook", "Trang chủ", "Video", "Marketplace", "Nhóm", "Xem tất cả", "Ảnh bìa", "Xem trang cá nhân của mọi người", "Trò chơi"]
    df = df[~df["names"].isin(remove_list)]
    df.drop_duplicates(keep="first")
    
    df.to_csv("test.csv", index=False)


if __name__ == "__main__":
    main()
