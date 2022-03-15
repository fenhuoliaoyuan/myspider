import config
import random
import requests
from lxml import etree
from config import conn
import re
from tqdm import tqdm
import os
session = requests.Session()
user_agent_list = config.get_ua()
def get_ips():
    ips_ = config.conn_ip
    IPs = ips_.smembers('ip_proxies_good')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        ips__.append({'http': ip})
    return ips__
ips = get_ips()
def get_page_text_jiajin(url_jiajin_,acount):
    proxies = random.choice(ips)
    print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'Accept-Language': 'zh-CN'
        }
        if acount == 10:
            session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin = session.get(url=url_jiajin_,headers=headers ,proxies=proxies,timeout=3)
        page_text_jiajin.encoding = page_text_jiajin.apparent_encoding
        page_text_jiajin = page_text_jiajin.text
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 100:
            # print()
            return
        acount += 1
        print('重试中...')
        page_text_jiajin= get_page_text_jiajin(url_jiajin_,acount)
    return page_text_jiajin
def get_page_text_jiajin_(url_jiajin_detail,acount):
    proxies = random.choice(ips)
    print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'Accept-Language': 'zh-CN'
        }
        if acount == 10:
            session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin_ = session.get(url=url_jiajin_detail,proxies=proxies,timeout=3).text
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 100:
            # print()
            return
        acount += 1
        print('重试中...')
        page_text_jiajin_ = get_page_text_jiajin_(url_jiajin_detail,acount)
    return page_text_jiajin_
def get_page_text_detail(url_detail,acount):
    proxies = random.choice(ips)
    print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'Accept-Language': 'zh-CN'
        }
        if acount == 3:
            session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_detail = session.get(url=url_detail, headers=headers,proxies=proxies,timeout=3)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 100:
            # print()
            return
        acount += 1
        print('重试中...')
        page_text_detail = get_page_text_detail(url_detail,acount)
    return page_text_detail
def get_m3u8(m3u8_url,acount):
    proxies = random.choice(ips)
    print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            # 'Accept-Language': 'zh-CN'
        }
        if acount == 10:
            session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        m3u8 = session.get(url=m3u8_url, proxies=proxies,timeout=5)
        if m3u8.status_code != 200:
            raise ValueError
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 100:
            # print()
            return
        acount += 1
        print('重试中...')
        m3u8 = get_m3u8(m3u8_url,acount)
    return m3u8

def get_ts(url_ts_,acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        if acount == 10:
            session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        ts = session.get(url=url_ts_, proxies=proxies,timeout=10)
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        print('删除连接超时Ip---{}-get_ts'.format(proxies))
        print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 100:
            # print()
            return
        if acount == 10:
            session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        acount += 1
        print('重试中...')
        ts = get_ts(url_ts_,acount)
    return ts

for page_jiajin in range(1,1000):
    print('第{}页解析'.format(page_jiajin))
    url_jiajin_ = 'https://g0527.91p47.com/v.php?next=watch&page={}'.format(page_jiajin)
    # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
    page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_,acount=0)
    if page_text_jiajin is not None:
        tree = etree.HTML(page_text_jiajin)
        div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
        for div in div_list:
            url_jiajin_detail = div.xpath('./a/@href')[0]
            try:
                name_video = div.xpath('./a/span[@class="video-title title-truncate m-t-5"]/text()')[0]
            except:
                print('没抓到')
            else:
                if '骑乘' in name_video:
                    set_houru = conn.sadd('url_video_qicheng',url_jiajin_detail)
                    set_houru = conn.sadd('name_video_qicheng', name_video)
                    print('插入一个视频详情页地址成功{}--{}'.format(name_video,url_jiajin_detail))
print(len(conn.smembers('url_video_qicheng')))