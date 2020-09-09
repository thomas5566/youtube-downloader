from pytube import YouTube
from bs4 import BeautifulSoup

import requests as req
import os, subprocess, re

fileobj = {} # 儲存下載檔的路徑和檔名
download_count = 1 # 紀錄下載次數

def check_media(filename):
    r = subprocess.Popen([".\\ffmpeg\\bin\\ffprobe.exe", filename],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = r.communicate()

    if (out.decode('utf-8').find('Audio') == -1):
        return -1
    else:
        return 1

def merge_media():
    temp_video = os.path.join(fileobj['dir'], 'temp_video.mp4')
    temp_audio = os.path.join(fileobj['dir'], 'temp_audio.mp4')
    temp_output = os.path.join(fileobj['dir'], ' output.mp4')

    cmd = f'".\\ffmpeg\\bin\\ffmpeg.exe" -i "{temp_video}" -i "{temp_audio}" \
        -map 0:v -map 1:a -c copy -y "{temp_output}"'

    try:
        subprocess.call(cmd, shell=True)
        # Rename
        os.rename(temp_output, os.path.join(fileobj['dir'], fileobj['name']))
        os.remove(temp_audio)
        os.remove(temp_video)
        print('Audio and Video merge complite!')
    except:
        print('Audio and Video merge false!')

def onProgess(stream, chunk, remains):
    total = stream.filesize
    percent = (total - remains) / total * 100
    print('Downloading... {:05.2f}%'.format(percent), end='\r')

def download_sound():
    try:
        yt.streams.filter(type="audio").first().download()
    except:
        print('Download Error, Please check URL')
        return

# File download callback Function
def onComplete(stream, file_path):
    global download_count, fileobj
    fileobj['name'] = os.path.basename(file_path) # Save file name
    fileobj['dir'] = os.path.dirname(file_path) # Save dir path
    print('\r')

    if download_count == 1:
        if check_media(file_path) == -1:
            print('This Video has no sound')
            download_count += 1
            try:
                # Rename Video
                os.rename(file_path, os.path.join(
                    fileobj['dir'], 'temp_video.mp4'))
            except:
                print('Video rename false...')
                return

            print('Prepare Download audio')
            download_sound() # Download sound
    else:
        try:
            # Rename audio
            os.rename(file_path, os.path.join(
                fileobj['dir'], 'temp_audio.mp4'))
        except:
            print('Rename audio false...')

        merge_media() # merge media

def playlist_urls(url):  # 取得播放清單所有影片網址的自訂函式
    urls = []   # 播放清單網址
    if '&list=' not in url : return urls    # 單一影片
    response = req.get(url)    # 發送 GET 請求
    if response.status_code != 200:
        print('請求失敗')
        return
    #-----↓ 請求成功, 解析網頁 ↓------#
    soup = BeautifulSoup(response.text, 'lxml')
    a_list = soup.find_all('a')
    base = 'https://www.youtube.com/'    # Youtube 網址
    for a in a_list:
        href = a.get('href')
        url = base + href  # 主網址結合 href 才是完整的影片網址
        if ('&index=' in url) and (url not in urls):
            urls.append(url)
    return urls

playlist_link = 'https://www.youtube.com/watch?v=4QG4mdHGxyY&list=PLPh89N96p4453fm9THjT8uFI4xWFeXXy_' #影片播放清單連結

urls = playlist_urls(playlist_link)   #執行 playlist_urls 函式
#對所有影片網址做排序
urls.sort(key = lambda s:int(re.search("index=\d+",s).group()[6:]))

for url in urls:
    download_count = 1 #改回 1
    print(url) #印出影片網址
    yt = YouTube(url, on_progress_callback=onProgress,on_complete_callback=onComplete)
    try:
        print(yt.streams.filter(subtype='mp4',resolution="1080p")[0].download())
    except:
        print(yt.streams.filter(subtype='mp4',resolution="1080p")[1].download())
    print(fileobj)