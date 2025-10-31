import pandas as pd
import os 

def update_csv(csv_path):
        """Cập nhật status mới vào file CSV."""
        try:
            df = pd.read_csv(csv_path)
            acc_ids = os.listdir(f"data/account/cookie")
            acc_ids = [os.path.splitext(f)[0] for f in acc_ids if f.endswith('.json')]
            
            df['status'] = df['acc_id'].apply(lambda x: True if str(x) in acc_ids else False)
            df.to_csv(csv_path, index=False)
            print(f"[INFO] Đã cập nhật file CSV với trạng thái mới.")
        except Exception as e:
            print(f"[ERROR] Không thể cập nhật file CSV: {e}")

update_csv("data/account/account_checked.csv")