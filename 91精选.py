import requests
import os
import re
from lxml import etree
import random
import config
from time import sleep
from tqdm import tqdm
from config import conn
from proxies import proxies
import random
import execjs
from concurrent.futures import ThreadPoolExecutor


def get_page_text_jiajin(url_jiajin_, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {

            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)

        page_text_jiajin = session.get(url=url_jiajin_, headers=headers, proxies=proxies)
        if page_text_jiajin.status_code != 200:
            raise ValueError
        page_text_jiajin = page_text_jiajin.text
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_jiajin(url_jiajin_, acount)
    else:
        return page_text_jiajin


def get_page_text_jiajin_(url_jiajin_detail, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin_ = session.get(url=url_jiajin_detail, headers=headers, proxies=proxies)
        if page_text_jiajin_.status_code != 200:
            raise ValueError
        page_text_jiajin_ = page_text_jiajin_.text
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_jiajin_(url_jiajin_detail, acount)
    else:
        return page_text_jiajin_


def get_page_text(url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text = session.get(url=url, headers=headers, proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text(url, acount)
    else:
        return page_text


def get_page_text_detail(url_detail, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'Accept-Language': 'zh-CN',
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 3:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_detail = session.get(url=url_detail, headers=headers, proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_detail(url_detail, acount)
    else:
        return page_text_detail


def get_m3u8(m3u8_url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 2:
        #     session.get(url='https://g0527.91p47.com', headers=headers, proxies=proxies)
        m3u8 = session.get(url=m3u8_url, headers=headers, proxies=proxies)
        if m3u8.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 5:
            # print('该视频地址应该为mp4,跳过')
            return
        acount += 1
        # print('重试中...')
        get_m3u8(m3u8_url, acount)
    else:
        return m3u8


def get_ts(url_ts_, acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        ts = session.get(url=url_ts_, proxies=proxies, headers=headers)
        if ts.status_code != 200:
            raise ValueError
    except:
        # ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_ts'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        # if acount == 2:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        acount += 1
        # print('重试中...')
        get_ts(url_ts_, acount)
    else:
        return ts


def get_mp4(url_video_mp4, acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        # print(proxies)
        mp4 = session.get(url=url_video_mp4, headers=headers, proxies=proxies)
        if mp4.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies',proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_mp4'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            return
        acount += 1
        # print('重试中...')
        get_mp4(url_video_mp4, acount)
    else:
        return mp4


user_agent_list = config.get_ua()

# proxies =[{'http': 'http://' + '3.211.65.185:80',},
#           {'http': 'http://' + '173.192.128.238:9999'}]

URL_list = []


# ips = proxies.Proxy()
def get_ips():
    ips_ = config.conn_ip
    IPs = ips_.smembers('ip_proxies_good')
    # IPs = ips_.smembers('ip_proxies_1')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        # ips__.append({'http': ip,'https':'https://'+ip.split('/')[-1]})
        # ips__.append({'https': 'https://' + ip.split('/')[-1]})
        ips__.append({'http': ip})
    return ips__


ips = get_ips()
# 加精页面获取，获取用户视频列表地址

session = requests.Session()

i = 0
while i < 10:
    headers = {
        'user-agent': random.choice(user_agent_list),
    }
    proxies = random.choice(ips)
    try:
        session.get(url='https://0316.workarea2.live/index.php', headers=headers, proxies=proxies, timeout=10)
    except:
        print('重试中')
        i += 1
    else:
        i = 10


def get_jiajin(page_jiajin):
    print('第{}页解析'.format(page_jiajin))
    url_jiajin_ = 'https://0316.workarea2.live/v.php?category=rf&viewtype=basic&page={}'.format(page_jiajin)
    # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
    page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
    if page_text_jiajin is not None:
        tree = etree.HTML(page_text_jiajin)
        div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
        for div in div_list:
            url_jiajin_detail = div.xpath('./a/@href')[0]
            url_detail_test = conn.sadd('url_video', url_jiajin_detail)
            if url_detail_test == 0:
                continue
            else:
                print('有新数据更新...')
                # 删除键值
                conn.srem('url_video', url_jiajin_detail)
                page_text_detail = get_page_text_detail(url_jiajin_detail, acount=0).text
                tree_ = etree.HTML(page_text_detail)
                video_name = tree_.xpath('/html/head/title/text()')[0]
                video_name = video_name.replace('?', '').replace('Chinese homemade video', '').strip()
                video_name = video_name.replace(':', '')
                video_name = video_name.replace('!', '')
                video_name = video_name.replace('|', '')
                video_name = video_name.replace('*', '')
                user_name = tree_.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0]
                path_mp4 = r'G:\ghs\91\91最近加精' + '\\' + user_name + '_' + video_name + '.mp4'

                # UID = tree_.xpath('//div[@id=VID]/text()')[0]
                # 获取m3u8
                VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]

                m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
                print(m3u8_url)
                m3u8 = get_m3u8(m3u8_url, acount=0)
                # m3u8 = requests.get(url=m3u8_url, headers=headers).text
                # 提取ts地址
                if m3u8 is not None:
                    if m3u8.status_code == 200:
                        m3u8 = m3u8.text
                        ts_list = []
                        for ts_ in m3u8.split('\n'):
                            if 'ts' in ts_:
                                url_ts = 'https://ccn.killcovid2021.com//m3u8/{}/'.format(VID) + ts_
                                ts_list.append(url_ts)
                        # print('ts数量为{}'.format(len(ts_list)))
                        pbar = tqdm(total=len(ts_list))
                        for url_ts_ in ts_list:
                            # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                            ts_url = conn.sadd('ts_url', url_ts_)
                            # 返回1即插入成功，返回零即该url已存在
                            if ts_url == 0:
                                # print('该ts数据已经下载')
                                pbar.update(1)
                                continue
                            else:
                                # 删除刚刚插入的值
                                conn.srem('ts_url', url_ts_)
                                ts = get_ts(url_ts_, acount=0)
                                # ts = requests.get(url=url_ts_, headers=headers).content
                                if ts.status_code == 200:
                                    with open(path_mp4, 'ab') as fp:
                                        fp.write(ts.content)
                                        # 写入成功再添加值
                                        conn.sadd('ts_url', url_ts_)
                                        pbar.update(1)
                        pbar.close()
                        # 该视频下载完成后添加键值
                        print('————————————————————————————————————————视频{}下载成功'.format(video_name))
                        conn.sadd('url_video', url_jiajin_detail)
                        conn.sadd('url_video_m3u8', m3u8_url)


if __name__ == '__main__':
    with ThreadPoolExecutor(20) as tp:
        for page_jiajin in range(21, 41):
            tp.submit(get_jiajin,page_jiajin)
