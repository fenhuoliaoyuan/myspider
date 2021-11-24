import requests
from urllib import request
from urllib.request import build_opener, ProxyHandler
import urllib.request
import os
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import signal
import sys
import threading
import random
import socket


socket.setdefaulttimeout(5)
# User_Agent列表
user_agent_list = [
    "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
    "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
    "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
    "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
]
cookie = "__cfduid=d1c26deefff55a971fa351b1a039867551602474174; PHPSESSID=ktjdfcisc79ii25hddrl5s05p2; 227c9_ck_info=%2F%09; 227c9_winduser=CwUGBwIDPwQKB1UEW1NVVFMAWAJUAgFRB1UAXAJTUlEBAFIGWwdTPg%3D%3D; 227c9_groupid=8; 227c9_lastvisit=0%091603803655%09%2Findex.php%3F"
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36",
# 'Connection': 'keep-alive',
# 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
# 'Cookie': ''}
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36"}
# {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36",'Cache-Control': 'no-cache'}


# 产生一个随机User-Agent
# header ={
#     # 从上面列表中随机取出一个
#     # random.choice:从一个不为空的课表里面随机取出一个
#     'User-Agent':random.choice(user_agent_list)
# }

requestURL = 'https://www.98zudisw.xyz/'


# 'https://cl.fr67.cf/'
# 'https://cl.de33.xyz/'

def get_info(site, titles, links):
    # ip地址列表：
    proxy = {
        'http': 'http://121.31.102.26:8123',
        'https': 'https://121.31.102.26:8123'
    }
    # re = requests.get('http://icanhazip.com/', headers=header,proxies=proxy)
    # seesion = requests.session()
    # re = seesion.get(site, headers=header)
    re = s.get(site, headers=header)
    re.encoding = 'utf-8'
    td = BeautifulSoup(re.text, "html.parser").find_all('a', class_='s xst')
    for i in td:
        titles.append(i.text)
        links.append(requestURL + i['href'])


# Registration Name: Vladimir Putin #2
# Registration Code: XLEVD-PNASB-6A3BD-Z72GJ-SPAH7

def download_img(title, link):
    nomakechar = [":", "/", "\\", "?", "*", "“", "<", ">", "|", "”"]
    for item in nomakechar:
        if title.find(item) > -1:
            title = title.replace(item, '')
    if os.path.exists('./98图片下载/' + title):
        return
    os.makedirs('./98图片下载/' + title)

    re = s.get(link, headers=header)
    re.encoding = 'gbk'
    img = BeautifulSoup(re.text, "html.parser").find_all(
        'img', class_='zoom')
    pbar = tqdm(total=len(img))
    for i in img:

        file_name = './98图片下载/' + title + '/' + str(img.index(i)) + '.jpg'
        if not os.path.exists(file_name):
            download_link = ''
            # if i.get('src') == None:
            #     download_link = i.get('file')
            # else:
            #     download_link = i.get('src')
            download_link = i.get('file')
            index = 1
            while index <= 1:
                try:
                    re = s.get(download_link, headers=header, timeout=5)
                    with open(file_name, 'wb') as f:
                        f.write(re.content)
                except:
                    index += 1
                    continue
                else:
                    break
        pbar.update(1)
    pbar.close()


def quit(signum, frame):
    print("Bye!")
    sys.exit(0)


requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接


def work():
    re = s.get(
        requestURL + 'forum-125-1.html', headers=header)
    re.encoding = 'utf-8'
    tabA = BeautifulSoup(re.text, "html.parser").find('a', class_='last')
    pages = tabA.contents[0].replace("... ", "")
    print(pages)
    inputPage = input("请输入开始下载的页数：")
    page = int(inputPage)
    inputtitle = input("请输入从当前页的第几个帖子开始下载：")
    while int(page) <= int(pages):
        # while int(page) < 1:
        site = requestURL + 'forum-125-' + str(page) + ".html"
        titles = []
        links = []
        get_info(site, titles, links)
        arr = []
        if page == 1:
            arr = range(8 + int(inputtitle), len(titles))
        else:
            arr = range(-1 + int(inputtitle), len(titles))
        for i in arr:
            print('#' * 100)
            if page == 1:
                print(
                    '第' + str(page) + '页数据,共' + str(len(titles)) + '条帖子 =>>>> 正在下载第' + str(i - 7) + '个帖子……' + titles[i])
            else:
                print(
                    '第' + str(page) + '页数据,共' + str(len(titles)) + '条帖子 =>>>> 正在下载第' + str(i + 1) + '个帖子……' + titles[i])
            download_img(titles[i], links[i])
            print('#' * 100 + '\n\n')
            time.sleep(3)
        page += 1
        # page -= 1
        inputtitle = 1


def main():
    work_thread = threading.Thread(target=work)#传入任务对象作为参数实例化一个线程
    work_thread.daemon = True
    '''daemon指示此线程是否为守护线程的布尔值。这必须在调用 start() 之前设置，否则会引发 RuntimeError。它的初始值是从创建线程
    继承的；主线程不是守护线程，因此在主线程中创建的所有线程默认为 daemon = False。当没有存活的非守护线程时，整个 Python 
    程序就会退出。'''
    work_thread.start()
    signal.signal(signal.SIGINT, quit)
    print("Start Working")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()