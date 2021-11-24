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
            'Accept-Language': 'zh-CN',
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)

        page_text_jiajin = session.get(url=url_jiajin_, headers=headers)
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
            'Accept-Language': 'zh-CN',
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin_ = session.get(url=url_jiajin_detail, headers=headers)
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
        page_text = session.get(url=url, headers=headers)
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
        page_text_detail = session.get(url=url_detail, headers=headers)
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
        m3u8 = session.get(url=m3u8_url, headers=headers)
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
        session.get(url='https://www.91porn.com/index.php', headers=headers, timeout=10)
    except:
        print('重试中')
        i += 1
    else:
        i = 10

path_list = os.listdir(r'G:\ghs\91porn')


def get_user(a, b):
    # n = 0
    m = 0
    for page in range(a, b + 1):
        print('第{}页解析'.format(page))
        url_jiajin_ = 'https://www.91porn.com/v.php?category=rf&viewtype=basic&page={}'.format(page)
        # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
        page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
        if page_text_jiajin is not None:
            tree = etree.HTML(page_text_jiajin)
            div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
            for div in div_list:
                url_jiajin_detail = div.xpath('./a/@href')[0]
                user = div.xpath('./text()')[5]
                user = user.strip()
                path_ = r'G:\ghs\91porn' + '\\' + user
                if not os.path.exists(path_):
                    os.mkdir(path_)
                    print(user)
                # page_text_jiajin_ = requests.get(url=url_jiajin_detail,headers=headers).text
                page_text_jiajin_ = get_page_text_jiajin_(url_jiajin_detail, acount=0)
                if page_text_jiajin_ is not None:
                    tree__ = etree.HTML(page_text_jiajin_)
                    try:
                        title = tree__.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0]
                        if title != 'guolifeng_513':
                            # // *[ @ id = "wrapper"] / div[1] / div[3] / div / div / div[1] / div / text()[2]
                            # user_name = conn.sadd('user_name',title)
                            # user_name = conn.zadd('user_name_', title, n)
                            user_name = conn.sadd('UN', title)
                            # n += 1
                            if user_name == 1:
                                URL__ = 'https://www.91porn.com/' + \
                                        tree__.xpath('//*[@id="videodetails-content"]/span[@class="title"]/a[1]/@href')[
                                            0]
                                # URL_list.append(URL__)
                                print('第{}页用户视频列表获取成功----{}---更新用户{}'.format(page, URL__, title))
                                # conn.zadd('91users_videos_list_url_guonei_', URL__, m)
                                conn.sadd("91jingxuan", URL__)
                                m += 1
                        else:
                            print(title)
                    except:
                        print('没拿到用户名')


def get_jiajin(page_jiajin):
    print('第{}页解析'.format(page_jiajin))
    url_jiajin_ = 'https://www.91porn.com/v.php?next=watch&page={}'.format(page_jiajin)
    # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
    page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
    if page_text_jiajin is not None:
        tree = etree.HTML(page_text_jiajin)
        div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
        for div in div_list:
            url_jiajin_detail = div.xpath('./a/@href')[0]
            viewkey = re.compile('viewkey=(.*?)&page').findall(url_jiajin_detail)[0]
            user_name_ = div.xpath('./text()')[5]
            user_name_ = user_name_.strip()
            if user_name_ in path_list:
                url_detail_test = conn.sadd('url_video', viewkey)
                if url_detail_test == 0:
                    continue
                else:
                    print('{}用户存在，开始下载该视频\n视频地址：{}'.format(user_name_, url_jiajin_detail))
                    # 删除键值
                    conn.srem('url_video', viewkey)
                    page_text_detail = get_page_text_detail(url_jiajin_detail, acount=0).text
                    tree_ = etree.HTML(page_text_detail)
                    video_name = tree_.xpath('/html/head/title/text()')[0]
                    video_name = video_name.replace('?', '').replace('Chinese homemade video', '').strip()
                    video_name = video_name.replace(':', '')
                    video_name = video_name.replace('!', '')
                    video_name = video_name.replace('|', '')
                    video_name = video_name.replace('*', '')
                    user_name = tree_.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0]
                    path_mp4 = r'G:\ghs\91porn' + '\\' + user_name + '\\' + user_name + video_name + '.mp4'
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
                                ts_id = url_ts_.replace('.ts', '').split('/')[-1]
                                # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                                ts_url = conn.sadd('ts_url', ts_id)
                                # 返回1即插入成功，返回零即该url已存在
                                if ts_url == 0:
                                    # print('该ts数据已经下载')
                                    pbar.update(1)
                                    continue
                                else:
                                    # 删除刚刚插入的值
                                    conn.srem('ts_url', ts_id)
                                    ts = get_ts(url_ts_, acount=0)
                                    # ts = requests.get(url=url_ts_, headers=headers).content
                                    if ts.status_code == 200:
                                        with open(path_mp4, 'ab') as fp:
                                            fp.write(ts.content)
                                            # 写入成功再添加值
                                            conn.sadd('ts_url', ts_id)
                                            pbar.update(1)
                            pbar.close()
                            # 该视频下载完成后添加键值
                            print(
                                '————————————————————————————————————————视频{}---{}下载成功'.format(user_name_, video_name))
                            conn.sadd('url_video', viewkey)



if __name__ == '__main__':
    # get_user(1,2)
    with ThreadPoolExecutor(10) as tp:
        for page_jiajin in range(1, 1000):
            tp.submit(get_jiajin, page_jiajin)
