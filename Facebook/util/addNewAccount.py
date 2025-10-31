import pandas as pd

account_checked = pd.read_csv("../data/account/account_checked.csv")
account_not_checked = pd.read_csv("../data/account/account_not_check.csv")

list_user_new = [
    "phamxuandepgai789@gmail.com",
    "Thienlamgreyrat42@gmail.com",
    "chupp794@gmail.com",
    "sonyeuchaunhieulam@gmail.com",
    "TuanNHuy260705@gmail.com",
    "kidturick@gmail.com",
    "pnam7801241@gmail.com (acc_0012)",
    "pnaam7801234@gmail.com (acc_0013)",
    "anhyeutnhieulam@gmail.com (acc_0015)",
    "kaisermarine01@gmail.com",
    "tvan07062@gmail.com",
    "907564907",
    "sonnamtrungthangthuc123@gmail.com",
    "907564907",
    "907564907",
    "tranlinhdepgai3@gmail.com",
    "907564907",
    "taibell2509@gmail.com",
    "mercury542270@gmail.com",
    "chinbacgia@gmail.com",
    "bangho.chau8@gmail.com",
    "907564907",
    "hungdung209387@gmail.com"
]
reset_account_list = pd.DataFrame(columns=account_checked)
for user in list_user_new:
    
        # if username == user :
        #     reset_account_list = pd.concat([reset_account_list, pd.DataFrame([row])], ignore_index=True)


# for user in list_user_new:
#     reset_account_list = pd.concat([reset_account_list, account_checked.apply(lambda x: x["username"] == user, axis=1)])
# print(len(list_user_new) == len(reset_account_list))
print(reset_account_list)
