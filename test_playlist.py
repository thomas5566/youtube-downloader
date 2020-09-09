import requests as req
import re, json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

def playlist_urls(url):
    urls = []
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    options = Options()
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a_list = soup.find_all('a')
    base = 'https://www.youtube.com'

    for i in a_list:
        href = i.get('href')
        url = base + str(href)  # 主網址結合 href 才是正確的影片網址
        if ('&index=' in url) and (url not in urls):
            urls.append(url)
    return urls


playlist_link = 'https://www.youtube.com/watch?v=EGOuDuvnzaA&list=RDCMUCec6QE03CMLgtf0f1-uDdbw'

urls = playlist_urls(playlist_link)

urls.sort(key = lambda s:int(re.search('index=\d+', s).group()[6:]))

for url in urls:
    print(url)

