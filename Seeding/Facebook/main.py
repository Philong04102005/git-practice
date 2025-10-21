from enum import Enum
import pandas as pd
import random
from util import(
    loginFacebookWithCookies,
    addNewFriend,
    acceptFriend,
    messageFriend,
    likePost,
    sendInviteRevoland,
    likePage,
    sharePostWeb
)
from playasHuman import HumanBehavior


class HandleFunctions(Enum):
    ADD_FRIEND_FROM_GROUP = 1
    ACCEPT_FRIEND = 2
    MESSAGE_FRIEND = 3
    SURFING_WEB = 4
    SEND_INVITE_REVOLAND = 5
    LIKE_REVOLAND_PAGE = 6
    SHARE_POST_WEB = 7
    PLAY_AS_HUMAN = 100
    QUIT = 0

class Menu:
    def __init__(self, accounts:pd.DataFrame, groups:pd.DataFrame, posts:pd.DataFrame):
        self.accounts = accounts
        self.groups = groups
        self.posts = posts
        self.functions = HandleFunctions
        self.driver = None
        self.choice = None
        self.account = None
        self.choice_sub = None

    def show_accounts_menu(self):
        print("----------Accounts Menu----------")
        for idx, acc in self.accounts.iterrows():
            print(f"{idx + 1}. {acc['acc_id']} - {acc['name']}")
        print("0. Quit")
        print("---------------------------------")
        self.choice = int(input("Choose an account: "))
        self._handle_account_choice()

    def _handle_account_choice(self):
        if self.choice == 0:
            print("Quiting...")
            return
        
        try:
            self.choice -= 1
            self.account = self.accounts.iloc[self.choice]
        except (ValueError, IndexError):
            print("[ERROR] Lựa chọn không hợp lệ.")

        self._handle_account()
        
    def _handle_account(self):
        print(f"\n[INFO] Đang đăng nhập: {[self.account['acc_id'], self.account['name']]}")
        self.driver = loginFacebookWithCookies.runLogin(f"data/account/cookie/{self.account['acc_id']}.json")

        if not self.driver:
            print(f"[ERROR] Đăng nhập thất bại cho {self.account['name']}")
            return

        print(f"[SUCCESS] Đăng nhập thành công cho {self.account['name']}")

        self.show_functions_menu()

    def show_functions_menu(self):
        print("----------Functions Menu----------")
        for func in self.functions:
            print(f"{func.value}. {func.name}")
        print("---------------------------------")
        self.choice_sub = int(input("Choose a function: "))
        self._handle_functions_menu()

    def _handle_functions_menu(self):
        if self.choice_sub == 0:
            print('Back to choose account...')
            self.driver.quit()
            self.driver = None

            print("\n" * 2)
            self.show_accounts_menu()
        else:
            match self.choice_sub:
                case 1:
                        print("[INFO] Start send friend request in group.")
#                         1. acc_0012 - Mai Ngân
#                         2. acc_0013 - Uyển Nhu
#                         3. acc_0015 - Kiều Diễm
                        addNewFriend.runAddFriend(
                            groups= pd.read_csv(f"data/group/group{self.choice + 1}.csv"),
                            driver= self.driver,
                            max_scroll=2,
                            max_requests=4
                        )

                case 2:
                        print("[INFO] Accept friend request.")
                        stats = acceptFriend.runAcceptFriend(self.driver, max_accept=100)
                        print(f"[RESULT] Chấp nhận thành công {stats['successful_accepts']}/{stats['total_found']}")
                    
                case 3:
                    print("[INFO] Chat with friend.")
                    messageFriend.run_manual_range(
                        driver=self.driver,
                        friends=pd.read_csv(f"./data/account/friends/friends_{self.account['acc_id']}.csv"),
                        messages=pd.read_csv("./data/content/message.csv")
                    ) 

                case 4:
                    print("[INFO] Surfing web (Like, View Comment, Reels,...)")
                    likePost.run_like_post(self.driver, max_likes=5) 

                case 5:
                    print("[INFO] Send invite like page REVOLAND.")
                    sendInviteRevoland.run_send_invite(self.driver)

                case 6:
                    print("[INFO] Like post on REVOLAND page.")
                    likePage.like_page(self.driver)

                case 7:
                    print("[INFO] Share post to group.")
                    sharePostWeb.share_post_from_web(
                        driver=self.driver, 
                        link_group= random.choice(self.groups["Link"].to_list()), 
                        link_share= random.choice(self.posts["loc"].to_list())) 

                case 100:
                    print("[INFO] Run bot.")
                    num_cycles = int(input("Nhập số chu kỳ (cycles) muốn chạy (mỗi chu kỳ ~ 10-15 phút): "))
                    bot = HumanBehavior(driver=self.driver, acc=self.account["acc_id"], num_cycles=num_cycles)
                    bot.run_bot() 

                case _:
                    print("[INFO] Invalid selection.")
                    self.show_functions_menu()
            
            print('\n'*2)
            self.show_functions_menu()        

def main():
    df = pd.read_csv("data/account/account.csv")
    accounts = df[df['status'] == True]
    groups = pd.read_csv("data/group/group.csv")
    posts = pd.read_csv("data/content/linkpost.csv")
    accounts = accounts.reset_index(drop=True)
    menu = Menu(accounts=accounts, groups=groups, posts=posts)
    menu.show_accounts_menu()

if __name__ == "__main__":
    ascii_art = r"""
        ██████╗ ███████╗██╗   ██╗ ██████╗ ██╗      █████╗ ███╗   ██╗██████╗ 
        ██╔══██╗██╔════╝██║   ██║██╔═══██╗██║     ██╔══██╗████╗  ██║██╔══██╗
        ██████╔╝█████╗  ██║   ██║██║   ██║██║     ███████║██╔██╗ ██║██║  ██║
        ██╔══██╗██╔══╝  ██║   ██║██║   ██║██║     ██╔══██║██║╚██╗██║██║  ██║
        ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗██║  ██║██║ ╚████║██████╔╝
        ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ 
        """
    print(ascii_art)
    main()