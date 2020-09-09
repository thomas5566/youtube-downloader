import subprocess

class Quality():

    def __init__(self, url, video_quality):
        self.url = url
        self.video_quality = video_quality

    def yget_quality(self):

        if self.video_quality == 'default quality':
            return 'default'
        process = subprocess.Popen('you-get -i' + self.url,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        r = process.communicate()
        s = str(r[0], 'utf-8')
        print(s)

        if s.find('title:') < 0: # 搜不到 title: 則視為失敗
            print('影片資訊讀取失敗')

        # strip： 用來去除頭尾字符、空白符
        # lstrip：用來去除開頭字符、空白符
        # rstrip：用來去除結尾字符、空白符
        #限定Full HD 1080p
        fhdq_s = s[s.find('1920x1080')-80:s.rfind('1920x1080')+115].rstrip()
        #限定Full HD 1080p mp4 格式
        fhdq_mp4 = fhdq_s[fhdq_s.find('mp4')-50:fhdq_s.find('mp4')+135]
        fhdq_itag = fhdq_mp4[fhdq_mp4.find('itag:')+6: fhdq_mp4.find('container')].strip()

        if len(fhdq_itag) > 8: #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
            fhdq_itag = fhdq_itag[4:-4] #去除、前後4個 ESC 字元
        if self.video_quality == '1080p':
            return fhdq_itag

        #限定HD 720p
        hdq_s = s[s.find('1280x720')-80:s.rfind('1280x720')+115].rstrip()
        #限定HD 720p mp4 格式
        hdq_mp4 = hdq_s[hdq_s.find('mp4')-50:hdq_s.find('mp4')+135]
        hdq_itag = hdq_mp4[hdq_mp4.find('itag:')+6: hdq_mp4.find('container')].strip()

        if len(hdq_itag) > 8: #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
            hdq_itag = hdq_itag[4:-4]
        if self.video_quality == '720p':
            return hdq_itag

        # middle quality 480p
        mq_s = s[s.find('854x480')-80:s.rfind('854x480')+115].rstrip()
        mq_mp4 = mq_s[mq_s.find('mp4')-50:mq_s.find('mp4')+135]
        mq_itag = mq_mp4[mq_mp4.find('itag:')+6: mq_mp4.find('container')]

        if len(mq_itag) > 8:
            mq_itag = mq_itag[4:-4]
        if self.video_quality == '480p':
            return mq_itag

        # low quality 360p
        lq_s = s[s.find('640x360')-80:s.find('640x360')+115].rstrip()
        # low quality 360p mp4 格式
        lq_mp4 = lq_s[lq_s.find('mp4')-50:lq_s.find('mp4')+135]
        lq_itag = lq_mp4[lq_mp4.find('itag')+6: lq_mp4.find('container')]

        if len(lq_itag) > 8:
            lq_itag = lq_itag[4:-4]
        if self.video_quality == '360p':
            return lq_itag