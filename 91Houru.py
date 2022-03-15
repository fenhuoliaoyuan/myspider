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
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'Accept-Language': 'zh-CN'
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin = session.get(url=url_jiajin_,headers=headers ,proxies=proxies)
        page_text_jiajin.encoding = page_text_jiajin.apparent_encoding
        if page_text_jiajin.status_code != 200:
            raise ValueError
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 20:
            # print()
            return
        acount += 1
        print('重试中...')
        get_page_text_jiajin(url_jiajin_,acount)
    else:
        return page_text_jiajin
def get_page_text_jiajin_(url_jiajin_detail,acount):
    proxies = random.choice(ips)
    print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'Accept-Language': 'zh-CN'
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin_ = session.get(url=url_jiajin_detail,proxies=proxies,headers=headers)
        if page_text_jiajin_.status_code != 200:
            raise ValueError
    except:
        if acount == 20:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_jiajin_(url_jiajin_detail,acount)
    else:
        return page_text_jiajin_
def get_page_text_detail(url_detail,acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'Accept-Language': 'zh-CN'
        }
        # if acount == 3:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_detail = session.get(url=url_detail, headers=headers,proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 20:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_detail(url_detail,acount)
    else:
        return page_text_detail
def get_m3u8(m3u8_url,acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            # 'Accept-Language': 'zh-CN'
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        m3u8 = session.get(url=m3u8_url,headers=headers, proxies=proxies)
        if m3u8.status_code != 200:
            raise ValueError
    except:
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 20:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_m3u8(m3u8_url,acount)
    else:
        return m3u8

def get_ts(url_ts_,acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        ts = session.get(url=url_ts_, headers=headers,proxies=proxies)
        if ts.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        if acount == 20:
            # print()
            return
        acount += 1
        get_ts(url_ts_,acount)
    else:
        return ts

def save():
    with ThreadPoolExecutor(100) as ape:
        for page_jiajin in range(1000,1500):
            ape.submit(save_0,page_jiajin)

def save_0(page_jiajin):
    print('第{}页解析'.format(page_jiajin))
    url_jiajin_ = 'https://0316.workarea2.live/v.php?next=watch&page={}'.format(page_jiajin)
    # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
    page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
    if page_text_jiajin is not None:
        tree = etree.HTML(page_text_jiajin.text)
        div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
        for div in div_list:
            url_jiajin_detail = div.xpath('./a/@href')[0]
            try:
                name_video = div.xpath('./a/span[@class="video-title title-truncate m-t-5"]/text()')[0]
            except:
                print('没抓到')
            else:
                if '后入' in name_video or '臀' in name_video:
                    conn.sadd('url_video_houru', url_jiajin_detail)
                    conn.sadd('name_video_houru', name_video)
                    print('插入{}--{}'.format(name_video, url_jiajin_detail))


def main(url_video_houru):
    url_video_houru_test = conn.sadd('url_video_houru_', url_video_houru)
    if url_video_houru_test == 1:
        conn.srem('url_video_houru_', url_video_houru)
        # url_video_houru = 'https://0316.workarea2.live/' + url_video_houru.split('/')[-1]
        page_text_detail = get_page_text_detail(url_video_houru, acount=0)
        if page_text_detail is not None:
            tree_ = etree.HTML(page_text_detail.text)
            # UID = tree_.xpath('//div[@id=VID]/text()')[0]
            # 获取m3u8

            name_video = tree_.xpath('//*[@id="videodetails"]/h4/text()')[0].strip()
            name_video = name_video.replace('?', '')
            name_video = name_video.replace(':', '')
            name_video = name_video.replace('!', '')
            name_video = name_video.replace('|', '')
            path_mp4 = path_root_ + '\\' + name_video + '.mp4'
            VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail.text)[0]
            m3u8_url = 'https://cdn.91p07.com//m3u8/{}/{}.m3u8'.format(VID, VID)
            # print(m3u8_url)
            m3u8 = get_m3u8(m3u8_url, acount=0)
            # m3u8 = requests.get(url=m3u8_url, headers=headers).text
            # 提取ts地址
            if m3u8 is not None:
                if m3u8.status_code == 200:
                    m3u8 = m3u8.text
                    ts_list = []
                    for ts_ in m3u8.split('\n'):
                        if 'ts' in ts_:
                            url_ts = 'https://cdn.91p07.com//m3u8/{}/'.format(VID) + ts_
                            ts_list.append(url_ts)
                    # print('ts数量为{}'.format(len(ts_list)))
                    if len(ts_list)<20:
                        print('-------------------------------开始下载{}.mp4'.format(name_video))
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
                                if ts is not None:
                                    with open(path_mp4, 'ab') as fp:
                                        fp.write(ts.content)
                                        # 写入成功再添加值
                                        conn.sadd('ts_url', url_ts_)
                                        pbar.update(1)

                        pbar.close()
                    # 该视频下载完成后添加键值
                        conn.sadd('url_video_houru_', url_video_houru)
                    else:
                        print('文件太大')
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
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
    save()
    url_video_houru_list = conn.smembers('url_video_houru')
    path_root = r'G:\ghs\91'
    path_root_ = path_root + '\\' + '后入'
    if not os.path.exists(path_root_):
        os.mkdir(path_root_)

    with ThreadPoolExecutor(100) as tp:
        for url_video_houru in list(url_video_houru_list)[::-1]:
            tp.submit(main,bytes.decode(url_video_houru))