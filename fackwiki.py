import os
import requests
from lxml import etree
import re
from Crypto.Cipher import AES
import random
import config
import time
from tqdm import tqdm

headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
ips = config.ips
def get_page_text(url,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        page_text = requests.get(url=url, headers=headers,proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        if acount == 10:
            # print()
            return
        acount += 1
        get_page_text(url,acount)
    else:
        return page_text

def get_page_text_detail(url_detail,acount):
    proxies = random.choice(ips)
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        page_text_detail = requests.get(url=url_detail, headers=headers,proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        if acount == 10:
            return
        acount += 1
        get_page_text_detail(url_detail,acount)
    else:
        return page_text_detail

def get_m3u8_(m3u8_url,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list),
            'referer': 'https://www.mdr18.info/'
        }
        proxies = random.choice(ips)
        m3u8 = requests.get(url=m3u8_url,headers=headers,proxies=proxies)
        if m3u8.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        if acount == 20:
            return
        acount += 1
        get_m3u8_(m3u8_url,acount)
    else:
        return m3u8.text
def get_m3u8(m3u8_url,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        m3u8 = requests.get(url=m3u8_url,headers=headers,proxies=proxies)
        if m3u8.status_code == 200 or m3u8.status_code == 503:
            m3u8 = m3u8.text
        else:
            raise ValueError
    except:

        ips.remove(proxies)
        print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        if acount == 20:
            return
        acount += 1
        get_m3u8(m3u8_url,acount)
    else:
        return m3u8

def get_ts(url_ts_,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        ts = requests.get(url=url_ts_, proxies=proxies,headers=headers)
        if ts.status_code != 200:
            raise ValueError
    except:
        if acount == 10:
            return
        acount += 1
        get_ts(url_ts_,acount)
    else:
        return ts
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
#
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # debuggerAddress调试器地址
# chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"  # 驱动
# bro = webdriver.Chrome(chrome_driver, options=chrome_options)
# url_detail_list = []
# for page in range(1,2):
#     URL = "https://www.mdr18.xyz/index.php/vod/type/id/101/page/{}.html".format(page)
#     bro.get(URL)
#     page_text = bro.page_source
#     bro.switch_to.frame()
def get_href_list(start_page,end_page):
    url_detail_list = []
    for page in range(int(start_page),int(end_page)+1):
        # URL = 'https://www.mdr18.xyz/index.php/vod/type/id/101/page/%d.html'%page
        URL = 'https://mdr18.pw/index.php/vod/search/page/1/wd/%E5%86%AF%E9%9B%AA.html'
        # URL = 'https://www.mdr18.pw/index.php/vod/search/page/{}/wd/%E6%9D%8E%E5%AE%97%E7%91%9E.html'.format(page)
        page_text = get_page_text(url=URL,acount=0)
        if page_text:
            page_text = page_text.text
            tree = etree.HTML(page_text)
            href_list = ['https://www.mdr18.xyz' + href for href in tree.xpath('//a[@class="videoBox"]/@href')]
            url_detail_list.extend(href_list)
    return url_detail_list

def main(url_detail):
    test_conn = config.conn.sadd('url_detail_yunpanpojie',url_detail)
    if test_conn == 1:
        config.conn.srem('url_detail_yunpanpojie',url_detail)
        # url = 'https://www.mdr18.info/index.php/vod/play/id/311680/sid/1/nid/1.html'
        page_detail = get_page_text_detail(url_detail=url_detail,acount=0)
        page_detail_text = page_detail.text
        tree = etree.HTML(page_detail_text)
        title = tree.xpath('/html/head/title/text()')[0]
        title = title.replace('.','#').replace('*','#').replace(':','#').replace('/','#')
        path_mp4 = path_root + '\\' + title + '.mp4'
        m3u8_base64 = re.compile('"url":"(.*?)","url_next"').findall(page_detail_text)
        # url = 'aHR0cHM6Ly93d3cuZm9ybWF4MjMueHl6LzIwMjEwNzE4LzdvZ0c4SEJ0L2luZGV4Lm0zdTgO0O0O'

        url_m3u8_64 = m3u8_base64[0][:64]
        import base64
        # URL = base64.b64decode(url)
        # URL_ = bytes.decode(URL)
        # print(URL_)
        # 麻豆
        url_m3u8 = bytes.decode(base64.b64decode(url_m3u8_64)) + '.m3u8'
        # 李宗瑞
        # url_m3u8 = bytes.decode(base64.b64decode(url_m3u8_64)) + 'dex.m3u8'
        m3u8_text = get_m3u8_(m3u8_url=url_m3u8,acount=0)
        if m3u8_text:
            url_m3u8_ = 'https://www.formax23.xyz' + m3u8_text.split('\n')[-2]
            m3u8 = get_m3u8(m3u8_url=url_m3u8_,acount=0)
            # ts_url_list = [line.replace('jpg','ts') for line in m3u8.split('\n') if 'jpg' in line]
            jpg_url_list = [line for line in m3u8.split('\n') if 'jpg' in line]
            print('---正在更新视频{}.mp4'.format(title))
            tq = tqdm(total=len(jpg_url_list))
            for jpg_url in jpg_url_list:
                test_conn_jpg = config.conn.sadd('jpg_url_yunpanpojie',jpg_url)
                if test_conn_jpg == 0:
                    tq.update(1)
                else:
                    config.conn.srem('jpg_url_yunpanpojie',jpg_url)
                    ts = get_ts(url_ts_=jpg_url,acount=0).content
                    with open(path_mp4,'ab') as mf:
                        mf.write(ts)
                    tq.update(1)
                    config.conn.sadd('jpg_url_yunpanpojie', jpg_url)
            tq.close()
            print('{}.mp4下载成功'.format(title))
            config.conn.sadd('url_detail_yunpanpojie',url_detail)

if __name__ == '__main__':
    path_root = 'F:\国产av'
    # path_root = r'F:\李宗瑞'
    if not os.path.exists(path_root):
        os.mkdir(path_root)
    url_detail_list = get_href_list(1,1)
    # url_detail_list = get_href_list(1, 4)
    print('真正遍历视频个数为{}'.format(len(url_detail_list)))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(30) as tp:
        for url_detail in url_detail_list:
            tp.submit(main,url_detail)
#     url_detail_list += ['https://www.mdr18.xyz' + url_detail_ for url_detail_ in etree.HTML(bro.page_source).xpath('//a[@class="videoBox"]/@href')]
# print('详情页地址抓取完毕共{}个'.format(len(url_detail_list)))
# for url_detail in url_detail_list:
#     bro.get(url_detail)
#     # bro.execute_script("return document.documentElement.outerHTML")
#     text = bro.page_source
#     url_m3u8 = re.compile('var urls = \"(.*?)\";').findall(text)
#     print()

# url_m3u8_ = 'https://3sybf.com/20200716/jCPj9dhx/index.m3u8'
# m3u8_ = requests.get(url=url_m3u8_,headers=headers)
# url_m3u8 = 'https://3sybf.com' + [line for line in m3u8_.text.split('\n') if 'm3u8' in line][-1]
# m3u8 = requests.get(url=url_m3u8,headers=headers)
# m3u8_text = m3u8.text.split('\n')
# url_key = 'https://3sybf.com'+ re.compile('URI=\"(.*?)\"').findall([url_ts_ for url_ts_ in m3u8_text if 'key' in url_ts_][0])[0]
# url_ts_list = ['https://3sybf.com' + url_ts_ for url_ts_ in m3u8_text if 'ts' in url_ts_]
# key_byte = requests.get(url=url_key,headers=headers)
# crt = AES.new(key_byte.content, AES.MODE_CBC)
# for url_ts in url_ts_list:
#     ts = requests.get(url=url_ts, headers=headers)
#     ts_open = crt.decrypt(ts.content)
#     with open('1.mp4', 'ab') as tf:
#         tf.write(ts_open)
#     print()
# print()