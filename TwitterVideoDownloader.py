import os
import sys
import time
import json
import requests
import threading
from contextlib import closing

GUserName = None

class DownloaderTwitterVideo:
    def __init__(self):
        self.threadList = []
        self.videoList = []
        self.postUrl = "http://www.downloadertwittervideo.com/down.html"

class Twitter:
    def __init__(self):
        self.threadList = []
        self.videoList = []
        self.getotal = 0
        self.success = 0
        self.isexist = 0
        self.proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "http://127.0.0.1:1080",
        }

def threadingFinish(self):
    for t in self.threadList:
        if t.isAlive():
            return False
    return True

def appendStart(self):
    for t in self.threadList:
        t.start()
        # 防止超过线程数
        time.sleep(0.01)

def downloaderStart(self):
    self.startTime = time.time()
    # 创建基于twitter用户名的文件夹
    if not (os.path.exists(self.TUserName) and os.path.isdir(self.TUserName)):
        os.mkdir(self.TUserName)
    for t in self.threadList:
        t.start()
        # 防止并发进程数过多
        time.sleep(5)

def appendVideoList(self, UserName, page):
    data = {
        "url": self.TUserLink,
        "page": page
    }
    r = requests.post(self.postUrl, data=data)
    if r.status_code == 200:
        try:
            json_data = json.loads(r.text)
            videoList = json_data['videoList']
            if len(videoList) != 0:
                for Dict in videoList:
                    url = Dict['videoUrl']
                    aStr = Dict['text'].split(" ")[0]
                    sh = len(aStr) < 10 and aStr or aStr[:10]
                    self.videoList.append([url, sh])
        except:
            pass

def getVideoList(UserName):
    startTime = time.time()
    self = DownloaderTwitterVideo()
    self.TUserLink = "https://twitter.com/" + UserName
    print('INFO: 开始获取 ' + self.TUserLink + ' 的视频列表...')
    for page in range(1, 100):
        t = threading.Thread(target=appendVideoList, args=(self, UserName, page))
        self.threadList.append(t)
    appendStart(self)
    while True:
        if threadingFinish(self):
            break
        time.sleep(1)
    if len(self.videoList) != 0:
        print('INFO: 获取完成，用时 ' + '%.0f' %(time.time() - startTime) + ' 秒！共 ' + str(len(self.videoList)) + ' 个视频文件!')
        return self.videoList
    else:
        return None

def downloader(self, url, name):
    videoname = url.split("/")[-1]
    filename = self.TUserName + '/' + videoname
    if os.path.exists(filename) and os.path.isfile(filename):
        filesize = os.path.getsize(filename)
        wgetsize = 0
        try:
            r = requests.head(url, proxies=self.proxies)
            wgetsize = int(r.headers['Content-Length'])
        except:
            pass
        if filesize == wgetsize:
            print('INFO: 文件 [' + name + '] 大小一致，跳过下载...')
            self.isexist = self.isexist + 1
            return
    print('INFO: 开始下载文件 [' + name + '] ...')
    try:
        with closing(requests.get(url, stream=True, proxies=self.proxies)) as r:
            with open(filename, 'wb') as video:
                for data in r.iter_content(1024):
                    video.write(data)
                    video.flush()
        self.success = self.success + 1
    except:
        pass

def getVideoUrl(self):
    global GUserName
    if GUserName == None:
        self.TUserName = input('>>> 请输入twitter用户名：')
    else:
        self.TUserName = GUserName
    self.videoList = getVideoList(self.TUserName)
    if not self.videoList:
        print('INFO: 获取用户 ' + self.TUserName + ' 的视频列表失败!')
        return
    self.getotal = len(self.videoList)
    for List in self.videoList:
        t = threading.Thread(target=downloader, args=(self, List[0], List[-1]))
        self.threadList.append(t)
    downloaderStart(self)
    while True:
        if threadingFinish(self):
            if self.getotal != self.success + self.isexist:
                print('INFO: 文件下载数目不一致，即将再次尝试...')
                GUserName = self.TUserName
                del self
                main()
            else:
                print('INFO: 下载完成！用时 ' + str(time.time() - self.startTime) + ' 秒！')
            print('INFO: 共 ' + str(self.getotal) + ' 个文件！下载 ' + str(self.success) + ' 个，本地存在 ' + str(self.isexist) + ' 个！')
            break
        time.sleep(1)

def main():
    self = Twitter()
    getVideoUrl(self)

if __name__ == '__main__':
    main()
