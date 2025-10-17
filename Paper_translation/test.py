from requests_html import HTMLSession
import pandas as pd

def crawl_world_bank(url, url_list):
    
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=30)  # render() = chạy JS để tải nội dung

    # Tìm danh sách bài viết
    articles = r.html.find('div.search-listing li')
    title_list = []
    href_list = []
    for li in articles:
        a_tag = li.find('a', first=True)
        if a_tag:
            title_list.append(a_tag.text)
            href_list.append(a_tag.attrs.get('href'))

        # chuyển thành dataFrame
    file = pd.DataFrame({
        "Thể loại": url_list.iloc[0, 0],
        "Tiêu đề": title_list,
        "Link bài báo": href_list
    })
    return file

url = 'https://www.worldbank.org/en/news/immersive-story/2025/10/14/building-jobs-and-futures-ida-in-africa'

session = HTMLSession()
r = session.get(url)
r.html.render(timeout=40)  # cho JS chạy để load nội dung

# Lấy tiêu đề
title = r.html.find('h1', first=True)
print("Title:", title.text if title else "Không tìm thấy tiêu đề")

# Lấy nội dung chính (thường nằm trong <p> hoặc div có class 'text', 'body', 'story-body', ...)
paragraphs = [p.text for p in r.html.find('p')]
print(paragraphs[10])
content = "\n".join(paragraphs)
# print(content)
