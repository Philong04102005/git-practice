import sys
import os
import pandas as pd
import time
import random
from util import (
    addNewFriend,
    acceptFriend,
    messageFriend,
    sendInviteRevoland,
    sharePostWeb,
    addFriendofFriend,
    viewCommentFeed
)
sys.stdout.reconfigure(encoding="utf-8")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from pyfiglet import Figlet
from termcolor import colored

from util import * 

import random


class HumanBehavior: 
    def __init__(self, driver, acc, num_cycles=5):
        self.driver = driver
        self.acc = acc 
        self.num_cycles = num_cycles
        self.friends = pd.read_csv(f"./data/account/friends/friends_{acc}.csv") 
        self.messages = pd.read_csv(f"./data/content/message.csv")
        self.comments = pd.read_csv(f"./data/content/comment.csv")
        self.groups = pd.read_csv(f"./data/group/group.csv")
        self.linkpost = pd.read_csv(f"./data/content/linkpost.csv")
        self.cnt_message = 0
        self.cnt_add_friend = 0 
        self.cnt_accept = 0 
        self.cnt_comment = 0 
        self.cnt_share = 0
        
        
    # LƯỚT NEW FEED, LIKE BÀI VIẾT : CHƯA ỔN
    def newfeed(self):
        self.driver.get("https://www.facebook.com")
        time.sleep(random.uniform(3, 5))
        try: 
            scroll_times = random.randint(3, 6)
            
            for _ in range(scroll_times):
                scroll_height = random.randint(300, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_height});")
                time.sleep(random.uniform(2, 4))

                # Random like bài viết 
                if random.random() < 0.2: 
                    try:
                        like_buttons = self.driver.find_elements(
                            By.XPATH, "//div[@aria-label='Thích' or @aria-label='Like']"
                        )
                        if len(like_buttons) > 0:
                            like_buttons[-1].click()
                            print("[SUCCESS] Đã like bài viết.")
                            time.sleep(random.uniform(2, 4))
                    except Exception as e:
                        print(f"[ERROR] Lỗi khi like bài viết: {e}")
                        return False

                # Random comment bài viết 
                if random.random() < 0.1:  
                    try:
                        comment_buttons = self.driver.find_elements(
                            By.XPATH, "//div[@aria-label='Bình luận' or @aria-label='Comment']"
                        )
                        if comment_buttons:
                            comment_button = comment_buttons[-1]
                            comment_button.click()
                            time.sleep(random.uniform(2, 4))

                            comment_box = self.driver.switch_to.active_element
                            message = random.choice(self.messages).get("CONTENT", "Nice post!")
                            comment_box.send_keys(message)
                            comment_box.send_keys(Keys.ENTER)
                            print("[SUCCESS] Đã bình luận một bài viết.")
                            time.sleep(random.uniform(2, 4))
                    except Exception as e:
                        print(f"[ERROR] Lỗi khi bình luận bài viết: {e}")
                        return False
            print("[SUCCESS] Hoàn thành lướt new feed.")
            return True
        except Exception as e:
            print(f"[ERROR] Lỗi khi lướt new feed: {e}")
            return False

    # GỬI TIN NHẮN : OK
    def send_inbox(self):
        try:
            if self.friends["Message_Status"].all():
                print("[INFO] Đã gửi tin nhắn cho tất cả bạn bè. Tổng số tin nhắn đã gửi:", self.cnt_message)
                return True 

            friends_to_message = self.friends[self.friends["Message_Status"] == False] 
            num_to_message = random.randint(1, 3)
            selected_friends = friends_to_message.sample(n=min(num_to_message, len(friends_to_message)))
            
            for _, friend in selected_friends.iterrows():
                messageFriend.send_message(self.driver, friend["link"], random.choice(self.messages["CONTENT"]))
                
                self.friends.loc[self.friends['link'] == friend['link'], 'Message_Status'] = True
                self.cnt_message += 1
                
            print(f"[SUCCESS] Đã gửi tin nhắn cho {len(selected_friends)} bạn bè.")
            return True
        except Exception as e:
            print(f"[ERROR] Lỗi khi gửi tin nhắn: {e}")
            return False
    
    # GỬI LỜI MỜI KẾT BẠN TỪ DANH SÁCH BẠN BÈ CỦA BẠN BÈ: TEST    
    def add_friend_from_friend_list(self):
        try:
            # Lấy random 1 friend 
            friend = random.choice(self.friends["link"].tolist()) 
            
            # Vào trang bạn bè của bạn bè và gửi lời mời kết bạn 
            num_add = random.randint(1, 2)
            for i in range(num_add):
                a = addFriendofFriend.add_friend(self.driver, friend) 
                if a: 
                    self.cnt_add_friend += 1       
            print(f"[SUCCESS] Đã gửi lời mời kết bạn từ bạn bè của {friend}.")
            return True   
        except Exception as e:
            print(f"[ERROR] Lỗi khi gửi lời mời kết bạn: {e}")  
            return False

    # CHẤP NHẬN LỜI MỜI KẾT BẠN : TEST
    def accept_friend(self):
        try:  
            result = acceptFriend.runAcceptFriend(self.driver, max_accept=2)
            self.cnt_accept += result["successful_accepts"] 
            print(f"[SUCCESS] Đã chấp nhận {result['successful_accepts']} lời mời kết bạn.")
            return True
        except Exception as e:
            print(f"[ERROR] Lỗi khi chấp nhận lời mời kết bạn: {e}")
            return False
        
    # GỬI LỜI MỜI KẾT BẠN VỚI CÁC SALES ĐĂNG BÀI TRONG CÁC GROUP: CHƯA FIX
    def add_friend_from_group(self):
        try: 
            group = random.choice(self.groups['Link'].tolist()) 
            self.driver.get(group)
            time.sleep(random.uniform(2, 4))
            authors = addNewFriend.scroll_and_get_post_authors(self.driver, max_scroll=3)
            for author in authors:
                addNewFriend.send_friend_request(self.driver, author)
                self.cnt_add_friend += 1
            return True
            
        except Exception as e:
            print(f"[ERROR] Lỗi khi gửi lời mời kết bạn từ nhóm: {e}")
            return False
        
    # COMMENT BÀI VIẾT TRONG CÁC GROUP: TEST 
    def comment_in_group(self):
        try: 
            group = random.choice(self.groups['Link'].tolist()) 
            self.driver.get(group)
            time.sleep(random.uniform(1, 3))
            
            comment = random.choice(self.comments["CONTENT"].tolist())
            viewCommentFeed.first_comment(self.driver, content=comment)
            return True
        except Exception as e:
            print(f"[ERROR] Lỗi khi bình luận trong nhóm: {e}")
            return False    
    
    def share_post(self): 
        group = random.choice(self.groups["Link"].to_list())
        post = random.choice(self.linkpost['loc'].to_list())
        
        try: 
            sharePostWeb.share_post_from_web(self.driver, group, post) 
            print("[SUCCESS] Share thành công")
            self.cnt_share += 1
            return True 
        except Exception as e: 
            print("[ERROR] Share thất bại. Lỗi {e}")
            return False
    
    def play_as_human(self):
        """
        Thiết lập hành động như một con người. 
        
        Driver đã đăng nhập vào tài khoản: 
        - Vào trang Revoland, gửi lời mời thích trang (làm 1 lần duy nhất)
        - Lướt new feed 
        - Like, comment bài viết trong new feed 
        - Gửi tin nhắn cho bạn bè trong danh sách bạn bè (1 lần 2 3 người, tin nhắn random) 
        - Vào trang chấp nhận lời mời kết bạn (chấp nhận 1 - 2 người đầu).
        - Vào nhóm, like, comment, share tin đăng từ revoland. 
        """
        
        # Ngẫu nhiên hành động 
        # HẠN CHẾ SPAM BÌNH LUẬN (DỄ BỊ BAN)
        actions = [
                self.newfeed,                 
                self.send_inbox,              
                self.add_friend_from_group,   
                self.accept_friend,          
                self.comment_in_group,
                self.share_post         
        ]
        weights = [10, 20, 30, 5, 5, 30]

        # 2. Chọn ngẫu nhiên MỘT hành động dựa trên trọng số
        for i in range(40):
            selected_action = random.choices(actions, weights=weights, k=1)[0]
            
            # 3. Thực hiện hành động
            print(f"[INFO] Thực hiện hành động: {selected_action.__name__}")
            
            status = selected_action()
            
            time.sleep(random.uniform(2, 4))
            
            if not status:
                print("[WARNING] Hành động bị lỗi, dừng chương trình.")
                return False
            
        return True

    
    def run_bot(self):
        # Gửi lời mời thích trang Revoland (làm 1 lần duy nhất)
        print(colored(Figlet(font="smblock").renderText('Facebook Automation'), 'blue'))
        runInvite = False # Cái này sửa sau
        if runInvite: 
            sendInviteRevoland.run_send_invite(self.driver)
            time.sleep(random.uniform(2, 4)) 
            self.driver.get("https://www.facebook.com") 
            time.sleep(random.uniform(1, 2)) 
        else: 
            print("[INFO] Đã gửi lời mời thích trang Revoland trong ngày, bỏ qua bước này.")
            
        for cycle in range(self.num_cycles):
            print("\n[INFO] ===============================")
            print(f"[INFO] Bắt đầu chu kỳ {cycle + 1}/{self.num_cycles}")
            print("[INFO] ===============================\n")
            
            # Chạy hành vi như người thật
            status = self.play_as_human()
            if not status:
                print("[WARNING] Bot bị lỗi trong chu kỳ này, dừng bot.")
                break
            if cycle == self.num_cycles - 1:
                break
            wait_time = random.randint(60, 120)  # Chờ từ 1 đến 2 phút
            print(f"[INFO] Chờ {wait_time // 60} phút trước khi bắt đầu chu kỳ tiếp theo...")
            time.sleep(wait_time)
        
        # Lưu trạng thái gửi tin nhắn của bạn bè
        self.friends.to_csv(f"./data/account/friends/friends_{self.acc}.csv", index=False)
        print(f"""[INFO] Kết thúc bot. 
        Tổng số tin nhắn đã gửi: {self.cnt_message}, 
        Tổng số lời mời kết bạn đã gửi: {self.cnt_add_friend}, 
        Tổng số lời mời kết bạn đã chấp nhận: {self.cnt_accept}, 
        Tổng số bình luận đã thực hiện: {self.cnt_comment}, 
        Tổng số lần chia sẻ: {self.cnt_share}
        """)
        