import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from operator import itemgetter
import json

class YoutubePlaylist():

    def __init__(self, url):
        self.url = url
        # self.playlist_id = playlist_id

    def get_link(self):
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
        position_items = {}

        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        # for item in playlist_items:
        #     for k, v in item.items():
        #         x = [v['position'] for d in v if 'position' in d]
        #         if x is not None:
        #             position_items.append(x)

        # list2 = [x for x in position_items if x]
        # str1 = ''.join(str(e) for e in list2)

        # print(list2)
        # print([
        #     f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&index={position}'
        #     for t in playlist_items
        # ])
        urls = []
        for t in playlist_items:
            url = f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&index={t["snippet"]["position"]}'
            urls.append(url)
        # print(urls)

        return urls

# url = 'https://www.youtube.com/watch?v=t-GxDNi6UAM&list=PLJOPIkGndY6IPvwi33qvN9DIM8yoSzquz'
# a = YoutubePlaylist(url)
# a.get_link()

