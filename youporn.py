import requests
import os
import re
import random
from lxml import etree
from multiprocessing.dummy import Pool
from config import user_agent_list


def get_url(url):
    # url = 'https://cn.pornhub.com/model/hongkongdoll/videos'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'user-agent': random.choice(user_agent_list),
    }
    # page_text_mian = requests.get(url=url, headers=headers).text.split('charset=UTF-8')
    page_text_mian = requests.get(url=url, headers=headers).text.split('Videos uploaded')
    page_text_mian = page_text_mian[1]
    tree = etree.HTML(page_text_mian)
    href_list = tree.xpath("//a[@class='video-box-image']/@href")
    # start_href_list = tree.xpath('//li[@class="pcVideoListItem js-pop videoblock videoBox alpha"]/div/div/a/@href')
    # href_list = tree.xpath('//li[@class="pcVideoListItem js-pop videoblock videoBox"]/div/div/a/@href')
    # end_href_list = tree.xpath('//li[@class="pcVideoListItem js-pop videoblock videoBox"]/div/div/a/@href')

    for href in href_list:
        print(href)
        # href = href_[0]
        # 加上youtube-dl命令
        # url_video_cmd = 'youtube-dl ' + 'https://cn.pornhub.com' + href
        url_video_cmd = 'yt-dlp -f \"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best\" ' + 'https://www.youporn.com' + href
        # print(url_video,acounts)
        url_list_cmd.append(url_video_cmd)
    return url_list_cmd


if __name__ == '__main__':
    # URL  = input('例如https://cn.pornhub.com/model/hongkongdoll/videos\n输入你要下载的用户视频列表地址  ：')
    # URL = 'https://cn.pornhub.com/model/hongkongdoll/videos'
    URL = 'https://www.youporn.com/uservids/17818230/hentai-tv/'
    # dir_name = input("输入你要存储视频的目录路径 ：")https://cn.pornhub.com/model/uuuujapan/videos
    dir_name = r'D:\hhh\youporn'
    # page_all = input("输入要下载的视频列表的总页数：")
    page_all = '2'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    dir_name = dir_name + '\\' + URL.split('/')[-2]
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    url_list_cmd = []
    for page in range(1, int(page_all) + 1):
        url = URL + '?page={}'.format(page)
        url_list_cmd = get_url(url)
    # print(url_list_cmd)
    # pool = Pool(1)  # 实例化开启多条线程
    # pool.map(os.system, url_list_cmd)
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(8) as tp:
        for url in url_list_cmd:
            tp.submit(os.system, url)
