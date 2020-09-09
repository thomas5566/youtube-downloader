import googleapiclient.discovery
import json, time, re
import requests as req

from urllib.parse import parse_qs, urlparse
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class YoutubePlaylist():

    def __init__(self, url):
        self.url = url
        # self.playlist_id = playlist_id

    def get_link(self):
        try:
            # extract playlist id from url
            # url = 'https://www.youtube.com/watch?v=t-GxDNi6UAM&list=PLJOPIkGndY6IPvwi33qvN9DIM8yoSzquz'
            query = parse_qs(urlparse(self.url).query, keep_blank_values=True)
            playlist_id = query["list"][0]

            print(f'get all playlist items links from {playlist_id}')
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyDCbYBINqbrqBXOjdSa8Z2mfKKr-am5v4w")

            request = youtube.playlistItems().list(
                # snippet property contains numerous fields, including the title,
                # description, position, and resourceId properties.
                # As such, if you set part=snippet, the API response will contain all of those properties.
                part = "snippet, contentDetails",
                playlistId = playlist_id,
                maxResults = 50,
                prettyPrint = True
            )
            response = request.execute()

            # print(response)

            playlist_items = []

            while request is not None:
                response = request.execute()
                playlist_items += response["items"]
                request = youtube.playlistItems().list_next(request, response)

            # print([
            #     f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&index={position}'
            #     for t in playlist_items
            # ])
            urls = []
            titles = []
            for t in playlist_items:
                url = f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&index={t["snippet"]["position"]}'
                urls.append(url)

                titles = f't["snippet"]["title"]'
                titles.append(titles)
            # print(urls)

            return urls

        except:
            urls = [] # Playlist URL
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

            if '&list=' not in self.url:
                return urls
                # if URL not incolude "&list" that is singl video

            response = req.get(self.url) # send GET request
            if response.status_code != 200:
                print('Request false!!')
                return

            # Version1 use regular expression
            page_text = response.text
            # regular expression
            parser = re.compile(r"watch\?v=\S+?list\=[A-Za-z0-9]+\S+?index\=[0-9]")
            # set() 不會包含重複的資料
            playlist = set(re.findall(parser, page_text))
            # map()是 Python 內建的高階函式，它接收一個函式 f 和一個 list，
            # 並通過把函式 f 依次作用在 list 的每個元素上，得到一個新的 list 並返回。
            playlist = map(
                (lambda x: "https://www.youtube.com/" + x.replace("\\u0026", "&")), playlist
            )

            for self.url in playlist:
                if ('&index=' in self.url) and (self.url not in urls):
                    urls.append(self.url)
            # 過濾不符合撥放清單URL的位址
            urls = [x for x in urls if "儲存播放清單" not in x]

            return urls

            # Version2 use selenium + BeautifulSoup
            # options = Options()
            # options.add_argument("--disable-notifications")

            # driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
            # driver.get(self.url)
            # time.sleep(5)

            # soup = BeautifulSoup(driver.page_source, 'html.parser')
            # a_list = soup.find_all('a')
            # base = 'https://www.youtube.com'

            # for i in a_list:
            #     href = i.get('href')
            #     self.url = base + str(href)  # 主網址結合 href 才是正確的影片網址
            #     if ('&index=' in self.url) and (self.url not in urls):
            #         urls.append(self.url)
            # return urls




# url = 'https://www.youtube.com/watch?v=t-GxDNi6UAM&list=PLJOPIkGndY6IPvwi33qvN9DIM8yoSzquz'
# a = YoutubePlaylist(url)
# a.get_link()

