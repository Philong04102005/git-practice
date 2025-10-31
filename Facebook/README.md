# QuinTech_SEEDING
```
Seeding
|- data
|    |- account
|    |    |- friends      # Chứa danh sách bạn bè của từng account
|    |    |- cookie       # Chứa cookie để đăng nhập của từng account
|    |- content
|    |- group
|- util
|- app.py
|- getAllFriend.py
|- getCookieFile.py
|- main.py
|- playasHuman.py
|- ...
```


# Hướng dẫn sử dụng:
### Chạy 2 dòng lệnh bên dưới để cài đặt thư viện.
```bash
cd Seeding
pip install -r requirements.txt
```

Sau khi đã cài đặt xong thì các bạn chọn chạy file **getCookieFile.py** để lưu toàn bộ cookie về máy.

Cuối cùng:
- Với **playasHuman.py** sẽ cho chọn account và tự động chạy các task khác.
- Với **main.py** sẽ cho chọn account và task sẽ thực hiện trong từng phiên.