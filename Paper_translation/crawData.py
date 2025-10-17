import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests_html import HTMLSession
def get_article_content(url):


    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm div chứa nội dung chính
    content_div = soup.find("div", class_="entry-content")

    if not content_div:
        return "No content found"

    # Lấy tất cả các đoạn văn <p>, loại bỏ quảng cáo, CTA, các block khác
    paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p")]

    # Ghép lại thành 1 chuỗi
    article_text = "\n".join(paragraphs)
    return article_text

def find_link_paper(url, url_list): 
    headers = {"User-Agent": "Mozilla/5.0"}  # Tránh bị chặn

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("a", class_="loop-card__title-link")
    time_tag = soup.find_all("time", class_="loop-card__meta-item")
    title_list = []
    href_list = []
    type_list = []
    for i in range(min(len(time_tag), len(articles))):
        if time_tag[i].get_text(strip=True) == "1 day ago":
            break   
        href_list.append(articles[i].get("href"))
        title_list.append(f"{articles[i].get_text(strip=True)}.")
        type_list.append(url_list.iloc[0, 0])
    # chuyển thành dataFrame
    file = pd.DataFrame({
        "Thể loại": type_list,
        "Tiêu đề": title_list,
        "Link bài báo": href_list
    })
    return file

def crawl_venturebeat_links(url, url_list):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Error fetching home page:", e)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    href_list = []
    title_list = []

    for h2 in soup.find_all("h2"):
        a = h2.find("a", href=True)
        if a:
            title_list.append(f"{a.get_text(strip=True)}.")
            href = a["href"]
            href_list.append(urljoin(url, href))
        
    # chuyển thành dataFrame
    file = pd.DataFrame({
        "Thể loại": url_list.iloc[0, 0],
        "Tiêu đề": title_list,
        "Link bài báo": href_list
    })
    return file

def get_venturebeat_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm đúng div chứa nội dung bài viết
    content_div = soup.find("div", class_="article-body whitespace-pre-wrap")

    if not content_div:
        return "No content found"

    # Lấy toàn bộ đoạn văn 
    paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p")]

    return "\n".join(paragraphs)

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

def main():
    url_list = pd.read_csv("data/tech_sources.csv")
    techrun = find_link_paper("https://techcrunch.com/category/startups/", url_list)
    venturbeat = crawl_venturebeat_links("https://venturebeat.com/", url_list)
    file = pd.concat([techrun, venturbeat], ignore_index=True)
    # print(crawl_venturebeat_links("https://venturebeat.com/"))
    list_content = []
    # print(len((techrun.iloc[:,0])))
    for i in range(len(file.iloc[:,0])):
        if i < len(techrun.iloc[:,0]): 
            list_content.append(get_article_content(file.iloc[i, 2]))
        else:
            list_content.append(get_venturebeat_content(file.iloc[i, 2]))
    file["content"] = list_content
    
    file.to_csv("data/contentSum.csv", index= False)

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



