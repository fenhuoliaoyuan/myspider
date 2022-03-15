import requests
import os
import re
from lxml import etree
import random
import config
from time import sleep
from tqdm import tqdm
from config import conn

# headers = config.get_ua()
# session = requests.Session()
# session.get(url='https://www.91porn.com',headers=headers)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'cookie': '__utmz=50351329.1620127544.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 91username=c129F%2BTyLiYr%2BNpWec169n%2B9pZvVlb5r%2FzSHeYAzwf8LBBP8hMuodTIqEg; __utmc=50351329; watch_times=0; CLIPSHARE=uebu5cijc5frjlbv9v3ibfeuoa; level=7; cf_clearance=86efd21db8ea13371e93fa1f2e125ff7d776c1d1-1624286837-0-150; __utma=50351329.1431892130.1620127544.1624278463.1624286839.33; __utmb=50351329.0.10.1624286839; __cf_bm=9184724fc8f7c776731d5301e2d2e7286517c136-1624286838-1800-AWfx+kCgiKw1QGhh8jN2DFvKZjNEA1S3Zz8x1bTUYf1s8eedq4s1Vcal3axLvYpwQ9k+VbfMzASDrLIZyB9BEBaDE6IekPtLh7REM6L4NhNYkBMWMxCNEgFUoLEL2KlEoQ=='
}
# proxies =[{'http': 'http://' + '3.211.65.185:80',},
#           {'http': 'http://' + '173.192.128.238:9999'}]
URL_list = []
while True:
    URL = input('例如：https://www.91porn.com/uvideos.php?UID=2ee6XCROiUEaLyheXVbVFIS837SG5erMPqdjHgwim8GV5qhp&type=public \n输入你要添加的下载用户视频列表视频地址(若没有点击回车) :')
    if URL != '':
        URL_list.append(URL)
    else:
        # URL = 'https://www.91porn.com/uvideos.php?UID=2ee6XCROiUEaLyheXVbVFIS837SG5erMPqdjHgwim8GV5qhp&type=public'
        break
for URL_ in URL_list:
    conn.sadd('91users_videos_list_url',URL_)
users_videos_list_url = conn.smembers('91users_videos_list_url')
print('===================================================开始遍历{}用户的视频列表'.format(len(users_videos_list_url)))
for users_videos_list_ in users_videos_list_url:
    # print(users_videos_list_)
    URL = bytes.decode(users_videos_list_)
    print('===================================================开始遍历\n{}'.format(URL))
    # start_page = input('输入你要下载的起始页码 ：')
    # end_page = input('输入你要下载的结束页码 ：')
    start_page = 1
    end_page = 10
    # path_root = input('例如：C:\番号\91porn \n输入你要存储视频的根目录 ：')
    path_root = r'C:\番号\91porn'
    if not os.path.exists(path_root):
        os.mkdir(path_root)
    for page in range(int(start_page),int(end_page)+1):
        # print('===================================================第{}页下载开始'.format(page))
        url = f'{URL}&page={page}'
        # headers = config.get_ua()
        page_text = requests.get(url=url,headers=headers)
        page_text.encoding = page_text.apparent_encoding
        page_text = page_text.text
        # user_name = re.compile('>?(.*?)公开视频').findall(page_text)
        tree = etree.HTML(page_text)
        user_name_ = tree.xpath('//*[@id="wrapper"]/div[1]/div[1]/h4/text()')[0]
        user_name = re.compile('(.*?)Public Videos').findall(user_name_)[0].strip()
        path_root_ = path_root + '\\' + user_name + '\\'
        if not os.path.exists(path_root_):
            os.mkdir(path_root_)
        div_list = tree.xpath('//div[@class="well well-sm"]')

        # div_len = tqdm(total=len(div_list))
        # 解析视频列表
        for div in div_list:
            url_detail = div.xpath('./a/@href')[0]
            title = div.xpath('./a/span/text()')[0]
            path_mp4 = path_root_ + title + '.mp4'
            # mp4_title = conn.sadd('mp4_title',title)
            # if mp4_title == 0:
            #     print('{}.mp4已存在'.format(title))
            # else:
            # print('有新数据更新...')
            url_detail_test = conn.sadd('url_video', url_detail)
            if url_detail_test == 0:
                continue
            else:
                print('有新数据更新...')
                # 删除键值
                conn.srem('url_video', url_detail)
                print('==================================================={}.mp4下载开始---{}'.format(title,user_name))
                page_text_detail = requests.get(url=url_detail, headers=headers)
                page_text_detail.encoding = page_text_detail.apparent_encoding
                page_text_detail = page_text_detail.text
                tree_ = etree.HTML(page_text_detail)
                # UID = tree_.xpath('//div[@id=VID]/text()')[0]
                # 获取m3u8
                VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]
                m3u8_url = 'https://cdn.91p07.com//m3u8/{}/{}.m3u8'.format(VID, VID)

                m3u8 = requests.get(url=m3u8_url, headers=headers).text
                # 提取ts地址
                ts_list = []
                for ts_ in m3u8.split('\n'):
                    if 'ts' in ts_:
                        url_ts = 'https://cdn.91p07.com//m3u8/{}/'.format(VID) + ts_
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
                        conn.srem('ts_url',url_ts_)
                        ts = requests.get(url=url_ts_, headers=headers).content
                        with open(path_mp4, 'ab') as fp:
                            fp.write(ts)
                            # 写入成功再添加值
                            conn.sadd('ts_url',url_ts_)
                            pbar.update(1)
                pbar.close()
                # 该视频下载完成后添加键值
                conn.sadd('url_video',url_detail)
                conn.sadd('url_video_m3u8',m3u8_url)