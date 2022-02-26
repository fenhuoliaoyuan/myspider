import json
import os
import random
from concurrent.futures import ThreadPoolExecutor
import requests
import time
from urllib.parse import unquote
from configDouyin import *
import re
from lxml import etree

PATH_DIR = r'G:\ghs\douyin'


def scroll_to_bottom(driver):
    js = 'return action=document.body.scrollHeight'
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = driver.execute_script(js)
    while height < new_height:
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 1000):
            # window.scrollTo(0, document.body.scrollHeight)
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
            height = new_height
            time.sleep(1)
            new_height = driver.execute_script(js)


# 滑动滚动条至底部
from selenium.webdriver.support.ui import WebDriverWait


def scroll_until_loaded(driver):
    WAIT = WebDriverWait(driver, 10)
    check_height = driver.execute_script("return document.body.scrollHeight;")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WAIT.until(lambda h: driver.execute_script("return document.body.scrollHeight;") > check_height)
            check_height = driver.execute_script("return document.body.scrollHeight;")
        except:
            break


def get_url_detail(URL):
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # debuggerAddress调试器地址
    chrome_driver = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"  # 驱动
    bro = webdriver.Chrome(chrome_driver, options=chrome_options)
    # 使用webkit无界面浏览器
    # 如果路径为 exe 启动程序的路径，那么该路径需要加一个 r
    # bro = webdriver.PhantomJS(executable_path=r'E:\pachon\study_documents\python_pachonjiaoben\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    bro.get(url=URL)
    scroll_until_loaded(bro)
    tree = etree.HTML(bro.page_source)
    url_detail_list = tree.xpath('//li[@class="ECMy_Zdt"]/a/@href')
    user_name = tree.xpath('//html/head/title/text()')[0].replace('的主页 - 抖音', '').strip()
    data_detail = {
        'url_detail_list': url_detail_list,
        'user_name': user_name
    }
    return data_detail




def get_ips():
    with open('ips.txt', 'r', encoding='utf-8') as rd:
        ips = []
        for line in [i.replace('\n', '') for i in rd.readlines()]:
            ip = {
                'http': 'http://' + line,
                # 'https': 'http://' + line
            }
            ips.append(ip)
        # pprint(ips)
        return ips


ips = get_ips()


def createDir(PATH_DIR):
    pathList = PATH_DIR.split('\\')
    path_dir = ''
    for i in range(0, len(pathList)):
        if i == 0:
            path_dir = pathList[0]
        else:
            path_dir = path_dir + '\\' + pathList[i]
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)


def downloadMp4(data, acount=0):
    try:
        url = data['url']
        path_dir = data['path_dir']
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        req = requests.get(url=url, headers=headers, proxies=proxies)
        if req.status_code == 200:
            SCRETS_STR = \
                re.compile('<script id="RENDER_DATA" type="application/json">(.*?)</script>').findall(req.text)[0]
            STR = unquote(SCRETS_STR)
            jsonVideo = json.loads(STR)
            # .33.aweme.detail.desc
            DESC = jsonVideo['33']['aweme']['detail']['desc']
            # .33.aweme.detail.video.playAddr[0].src
            VIDEO_URL = jsonVideo['33']['aweme']['detail']['video']['playAddr'][0]['src']
            data = {
                'DESC': DESC,
                'VIDEO_URL': VIDEO_URL
            }
            dst = path_dir + '\\' + data['DESC'].replace(':', ' ').replace('/', ' ').replace('!', ' ').replace('?',' ').replace('|', ' ').replace('*', ' ').replace('\n', '').replace('.', ' ') + '.mp4'

            if not os.path.exists(dst):
                ts = requests.get(url='https:'+ VIDEO_URL, headers=headers, proxies=proxies)
                with open(dst, 'wb') as wb:
                    wb.write(ts.content)
                    print(data['DESC'] + '.mp4' + '下载完成')
    except:
        if acount == 10:
            pass
        else:
            acount += 1
            downloadMp4(data=data,acount=acount)

def downloadDouYin():
    URL = input('输入链接：')
    data_detail = get_url_detail(URL)
    url_detail_list = data_detail['url_detail_list']
    user_name = data_detail['user_name']
    path_dir = PATH_DIR + '\\' + user_name
    createDir(path_dir)

    # # dict的去重
    # DouYin.datas = [dict(t) for t in set([tuple(d.items()) for d in DouYin.datas])]
    print('用户名：' + user_name)
    print("抓取的视频长度：" + str(len(url_detail_list)))
    print('开始下载视频>>>')
    with ThreadPoolExecutor(5) as tp:
        for url in url_detail_list:
            data = {
                'url': 'https:' + url,
                'path_dir': path_dir
            }
            tp.submit(downloadMp4, data)


if __name__ == '__main__':
    downloadDouYin()
