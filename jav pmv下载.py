import requests
import os
import re
from lxml import etree
import random
import config
from time import sleep
from tqdm import tqdm
from config import conn,conn_2
from proxies import proxies
import random
import execjs
# ips = config.ips

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # debuggerAddress调试器地址
chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"  # 驱动
bro = webdriver.Chrome(chrome_driver, options=chrome_options)
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile

def get_url_detail_list(page):
    # page = 1
    # url = 'https://spankbang.com/s/jav+pmv/%d/?o=new'%page
    url = 'https://spankbang.com/s/hmv/%d/?o=top'%page
    bro.get(url)
    tree = etree.HTML(bro.page_source)
    href_list = tree.xpath('//div[@class="video-list video-rotate video-list-with-ads"]/div/a[1]/@href')
    # url_detail_list = ['https://spankbang.com'+i for i in href_list]
    # return url_detail_list
    for i in href_list:
        url_detail = 'https://spankbang.com' + i
        # conn_2.sadd('url_detail_javpmv',url_detail)
        conn_2.sadd('url_detail_hmv', url_detail)
        print('插入{}'.format(url_detail))

# get_url_detail_list(1)
def get_url_mp4(url_detail):
    # url_detail = 'https://spankbang.com/5pavi/video/hexjav+pmv'
    bro.get(url_detail)
    mp4_url_list = re.compile("'\d+p': \[(.*?)\]").findall(bro.page_source)
    for url_mp4 in mp4_url_list[::-1]:
        if url_mp4 != '':
            # conn_2.sadd('javpmv_mp4_url',url_mp4)
            conn_2.sadd('hmv_mp4_url', url_mp4)
            print('{}插入成功'.format(url_mp4))
            return url_mp4

# get_url_mp4(url_detail='')
def get_mp4(url_mp4):
    name_mp4 = url_mp4.split('=')[-1]
    path_mp4 = r'G:\hhh\jav_pmv' + '\\' + name_mp4 + '.mp4'
    if not os.path.exists(path_mp4):
        print('下载中-{}'.format(name_mp4+'.mp4'))
        while True:
            try:
                # proxies = random.choice(ips)
                headers = {
                    'user-agent': random.choice(config.user_agent_list)
                }
                mp4 = requests.get(url=url_mp4, headers=headers)
                if mp4.status_code != 200:
                    raise ValueError
            except:
                pass
                # ips.remove(proxies)
                # get_mp4(url_mp4)
            else:
                if mp4 is not None:
                    with open(path_mp4, 'wb') as fp:
                        fp.write(mp4.content)
                        print('{}下载成功'.format(name_mp4+'.mp4'))
                break

# url_mp4 = 'https://vdownload-4.sb-cd.com/9/5/9578574-480p.mp4?secure=_eFawb3203yLf3BO1WKybA,1627081039&m=4&d=5&_tid=9578574'
# mp4 = get_mp4(url_mp4,acount=0)
if __name__ == '__main__':
    for page in range(11,20):
        get_url_detail_list(page)
    for url_detail in list(conn_2.smembers('url_detail_hmv'))[::-1]:
        url_detail = bytes.decode(url_detail)
        get_url_mp4(url_detail=url_detail)
    for url_mp4_ in list(conn_2.smembers('hmv_mp4_url')):
        url_mp4 = bytes.decode(url_mp4_)[1:][:-1]
        print(url_mp4)
        # get_mp4(url_mp4)
        with open('url_hmv.txt','a') as wf:
            wf.write(url_mp4+'\n')
