import pandas as pd

account_not_check = pd.read_csv("data/account/account.csv")
emails = [
    "O909816580",
    "anhtuchatgptplus@gmail.com",
    "chupp794@gmail.com",
    "sonyeuchaunhieulam@gmail.com",
    "thienlamgreyrat80@gmail.com",
    "TuanNHuy260705@gmail.com",
    "pnam7801241@gmail.com",  # acc_0012
    "pnaam7801234@gmail.com",  # acc_0013
    "anhyeutnhieulam@gmail.com",  # acc_0015
    "tvan07062@gmail.com",
    "thienlamgreyrat35@gmail.com",
    "907564907",
    "sonnamtrungthangthuc123@gmail.com",
    "907564907",
    "907564907",
    "Thienlamgreyrat101@gmail.com",
    "thienlamgreyrat46@gmail.com",
    "907564907",
    "taibell2509@gmail.com",
    "mercury542270@gmail.com",
    "chinbacgia@gmail.com",
    "bangho.chau8@gmail.com",
    "907564907",
    "hungdung209387@gmail.com",
    "thienlamgreyrat47@gmail.com",
    "phamxuandepgai789@gmail.com",
    "kaisermarine01@gmail.com",
    "nhntjun02",
    "tranlinhdepgai3@gmail.com",
    "nhntjun03",
    "thienlamgreyrat12@gmail.com",
    "kidturick@gmail.com",
    "Thienlamgreyrat42@gmail.com",
    "laclan7846gjr7eglfw@gmail.com",
    "thienlamgreyrat46@gmail.com"
]

account_current = pd.DataFrame(columns=account_not_check.columns)
for username in emails:
    for i in range(len(account_not_check)):
        if account_not_check.iloc[i,1] == username:
            account_current = pd.concat([account_current, account_not_check.iloc[[i]]])
            account_not_check.drop(i, inplace=True)
            account_not_check.reset_index(drop=True, inplace=True)
            break

# account_current.drop("status", axis= 1, inplace=True)
# account_not_check.drop("status", axis= 1, inplace=True)

account_current.to_csv("data/account/account_checked.csv", index=False)
account_not_check.to_csv("data/account/account_not_check.csv", index=False)
