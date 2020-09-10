# -*- coding: utf-8 -*-

import tkinter as tk
import os, subprocess, threading, time, string, re
import lxml, json
import urllib.request
import requests as req

from lxml import etree
from lxml import html
from lxml.html import fromstring
from PIL import Image, ImageTk
from pytube import YouTube

from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askdirectory

from youtubeplaylist import YoutubePlaylist
from quality import Quality
from mediaStuff import Media

fileobj = {} # 儲存下載檔的路徑和檔名
download_count = 1 # 紀錄下載次數
yt = None  # global variable must exist in global namespace first

# 檢查影片檔是否包含聲音
def check_media(filename):
    # media = Media(filename)
    # return media.check_media()
    r = subprocess.Popen(["ffprobe.exe", filename],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                            # send data to stdin
                            # stdout and stderr read data
                            # .PIPE Special value that can be used as the stdin,
                            # stdout or stderr argument to Popen and indicates
                            # that a pipe to the standard stream should be opened.
                            # Most useful with Popen.communicate().
                            # .STDOUT Special value that can be used as the stderr argument to
                            # Popen and indicates that standard error should go
                            # into the same handle as standard output.
    out, err = r.communicate()
    # Popen.communicate()方法用於和子進程交互：發送數據到stdin，
    # 並從stdout和stderr讀數據，直到收到EOF。等待子進程結束。
    if (out.decode('utf-8').find('Audio') == -1):
        return -1 # 沒有聲音
    else:
        return 1

# 合併影片檔
def merge_media():
    temp_video = os.path.join(fileobj['dir'], 'temp_video.mp4')
    temp_audio = os.path.join(fileobj['dir'], 'temp_audio.mp4')
    temp_output = os.path.join(fileobj['dir'], 'output.mp4')

    # ffmpeg merge command
    # cmd = f'"ffmpeg.exe" -i "{temp_video}" -i "{temp_audio}" -map 0:v -map 1:a -c copy -y "{temp_output}"'
    cmd = f'"ffmpeg.exe" -i "{temp_video}" -i "{temp_audio}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "{temp_output}"'

    try:
        subprocess.call(cmd, shell=True)
        # subprocess的call方法可以用於執行一個外部命令，
        # 但該方法不能返回執行的結果，只能返回執行的狀態碼： 成功（0） 或 錯誤（非0）
        # Rename
        os.rename(temp_output, os.path.join(fileobj['dir'], fileobj['name']))
        os.remove(temp_audio)
        os.remove(temp_video)
        print('Audio and Video merge complite!')
    except:
        print('Audio and Video merge false!')

# Progess Bar
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
            print('This Video has no sound! Download completed')
    else:
        try:
            # Rename audio
            os.rename(file_path, os.path.join(
                fileobj['dir'], 'temp_audio.mp4'))
        except:
            print('Rename audio false...')

        merge_media() # merge media

def links_get(url): # GTE playlist video All URLS
    playlist = YoutubePlaylist(url)
    return playlist.get_link()

# 當你有兩個function，第二個function需要等第一個function執行完畢才能使用時，
# 就需要使用LOCK把她鎖住不讓他執行。
lock = threading.Lock()

def video_download(url, listbox, name, video_path, itag):
    download_count = 1 #改回1
    print(url)
    global yt
    yt = YouTube(url, on_progress_callback=onProgess, on_complete_callback=onComplete)
    # name = yt.title
    time.sleep(0.01)
    # lock.acquire當function呼叫acquire時，表示他獲得了執行權限，
    # 若同時有另外一個function去呼叫acquire時，需要等這個function執行完畢才能執行
    lock.acquire() # 進行鎖定
    no = listbox.size() # 以目前列表框筆數為下載編號
    listbox.insert(tk.END, f'{no:02d}:{name}.....Downloading')
    # print('Insert:', no, name)

    # lock.release當function執行完畢時，讀取到release時，
    # 他會去讓下一個申請執行的function去執行。
    lock.release() # 釋放鎖定
    try:
        if itag == '' or itag == 'default':
            os.system('you-get '+' -o '+ "\"" +video_path+ "\""+" "+"\""+ url + "\"")
        if itag != '':
            os.system('you-get '+'--itag='+itag+' -o '+ "\"" +video_path+ "\""+" "+"\""+ url + "\"")
    except:
        try:
            print(yt.streams.filter(subtype='mp4', resolution="1080p")[0].download())
        except:
            print(yt.streams.filter(subtype='mp4', resolution="1080p")[1].download())
    lock.acquire() # 進行鎖定
    print('Update:', no, name)

    listbox.delete(no)
    listbox.insert(no, f'{no:02d}:👍{name}.....Download complete')

    lock.release() # 釋放鎖定
    return

def yget_quality(url, video_quality):
    quality = Quality(url, video_quality)
    return quality.yget_quality()

def btn_click(): # 按鈕的函式
    listbox.delete(0, tk.END)

    url = inptu_url.get() # 取得文字輸入框的網址
    try:  #  測試 pytube 是否支援此網址或者網址是否正確
        YouTube(url)
    except:
        messagebox.showerror('ERROR', 'pytube 不支援此影片或者網址錯誤')
        return

    # select quality
    video_itag = yget_quality(url, cbb.get())
    if video_itag == '':
        messagebox.showwarning('Quality', 'video quality not support download default quality')

    # select download path
    if var_path_text.get() == '':
        messagebox.showwarning('Download path', 'please choose a Download path')
        return

    # if pytube support this URL continue web scraping
    urls = links_get(url)
    ytname = []

    #輸入網址中有影片清單
    if urls and messagebox.askyesno('確認方塊', 'Download all playlists?') :
        # Starting Download all list video
        print('開始下載清單')
        listbox.insert(tk.END, '.....開始下載清單.....')
        urls.sort(key = lambda s: int(re.search("index=\d+", s).group()[6:]))

        for url in urls:
            youtube = etree.HTML(urllib.request.urlopen(url).read().decode('utf-8'))
            video_title = youtube.xpath("//meta[@name='title']/@content")
            ytname.append(''.join(video_title))
        # print (ytname)

        # ytname = [x.unicode(x) for x in ytname]

        # for i in range(len(urls)):
        #     yt_title = YouTube(urls[i]).title
        #     re_yt_title = yt_title.translate(str.maketrans('', '', string.punctuation))
        #     new_title = re.sub(r"\s+", "", re_yt_title)
        #     # rgx = re.compile(r'(【】《》「」『』)★！｜')
        #     # yt_title = re.sub('(【】《》「」『』)★！｜', '', yt_title)
        #     time.sleep(0.2)
        #     print('title', new_title)
        #     ytname.append(new_title)


        # full_punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' + '→↓△▿⋄•！？?〞＃＄％＆』（）＊＋，－╱︰；＜＝＞＠〔╲〕 ＿ˋ｛∣｝∼、〃》「」『』【】﹝﹞【】〝〞–—『』「」…﹏【】|'
        # ytname = list(map(lambda it: it.strip(), ytname))
        # ytname_2 = []
        # ytname_2 =[ele for ele in ytname if not ele in full_punctuation]
        #

        # create therad
        for i in range(len(urls)):
            time.sleep(0.5)
            threading.Thread(target=video_download,
                            args=(urls[i], listbox, ytname[i], var_path_text.get(), video_itag)).start()

    else:
        yt = YouTube(url)
        if messagebox.askyesno('確認方塊', f'是否下載{yt.title}影片？') :
            threading.Thread(target=video_download,
                            args=(url, listbox, yt.title, var_path_text.get(), video_itag)).start()
        else:
            print('取消下載')

# 解析度下拉選單
def callbackFunc(event):
    print("Selected" + cbb.get())

# Select download PATH
def select_path():
    path_ = askdirectory()
    var_path_text.set(path_)

# 建立主視窗物件
win = tk.Tk()
win.geometry('640x640') # 設定主視窗預設尺寸為640x600
win.resizable(False, False) # 設定主視窗的寬跟高皆不可縮放
win.title('Youtube Video Downloader')
win.iconbitmap('./YT.ico')

# Label：顯示圖片
img = Image.open('youtube.png')
img = ImageTk.PhotoImage(img)
imLabel = tk.Label(win, image=img)
imLabel.pack()

# Set input URL area
input_frm = tk.Frame(win, width=640, height=50)
input_frm.pack()

# Set Prompt text
lb = tk.Label(input_frm, text='Type a URL like a video or a playlist', fg='black')
lb.place(rely=0.2, relx=0.5, anchor='center')

inptu_url = tk.StringVar() # Get USER input URL
input_et = tk.Entry(input_frm, textvariable=inptu_url, width=60)
input_et.place(rely=0.75, relx=0.5, anchor='center')

btn = tk.Button(input_frm, text='Download', command=btn_click, bg='orange', fg='Black')
btn.place(rely=0.75, relx=0.9, anchor='center')

# select list
choice_frm = tk.Frame(win, width=640, height=50)
choice_frm.pack()
lb = tk.Label(choice_frm, text='choose video quality :', fg='black')
lb.place(rely=0.2, relx=0.1)

cbb = ttk.Combobox(choice_frm,
                    values=[
                        "default quality",
                        "1080p",
                        "720p",
                        "480p",
                        "360p"], state="readonly", width=12)
cbb.place(rely=0.2, relx=0.3)
cbb.current(0)
cbb.bind("<<ComboboxSelected>>", callbackFunc)

label_path = tk.Label(choice_frm, text='Download path :', cursor='xterm')
label_path.place(rely=0.2, relx=0.5)
var_path_text = tk.StringVar()
entry_path = tk.Entry(choice_frm, fg='gray', bd=2, width=20, textvariable=var_path_text, cursor='xterm')
entry_path.place(rely=0.2, relx=0.66)
button_choice = tk.Button(choice_frm, text='change', bd=1, width=6, command=select_path, cursor='hand2')
button_choice.place(rely=0.15, relx=0.9)

#下載清單區域
dl_frm = tk.Frame(win, width=640, height=460)
dl_frm.pack()
#設定提示文字
lb = tk.Label(dl_frm, text='Download list', fg='black')
lb.place(rely=0.01, relx=0.5, anchor='center')
#設定顯示清單
listbox = tk.Listbox(dl_frm, width=65, height=26)
listbox.place(rely=0.5, relx=0.5, anchor='center')
#設定捲軸
sbar = tk.Scrollbar(dl_frm)
sbar.place(rely=0.5, relx=0.87, anchor='center', relheight=0.93)
#連結清單和捲軸
listbox.config(yscrollcommand=sbar.set)
sbar.config(command=listbox.yview)

win.mainloop()