import requests
import os
import random
from lxml import etree



headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"},
    { 'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
    {'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
    { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
]
if not os.path.exists('./番号预览/'):  # 创建文件目录
    os.mkdir('./番号预览/')
for page in range(1,51):
    print('==========================================第{}页下载开始=========================================='.format(page))
    URL = 'https://javdb6.com/makers/7R?page={}'.format(page)
    # header = random.choice(headers_list)
    session = requests.Session()  # 创建Session对象
    session.get(URL, headers=random.choice(headers_list), verify=False)  # 捕获且存储cookie
    if session:
        print('cookie获取成功')
        response_page_1 = session.get(URL,headers=random.choice(headers_list),verify=False).text
        print('该主页面请求成功')
        tree = etree.HTML(response_page_1)
        # //*[@id="videos"]/div/div[1]
        div_list = tree.xpath('//*[@id="videos"]/div/div')
        for div in div_list:
            name_video = div.xpath('./a/div[2]/text()')[0]
            # print(name_video)
            url_detail_page = 'https://javdb6.com' + div.xpath('./a/@href')[0]
            # print(url_detail_page)
            path_video = './番号预览/' + name_video + '.mp4'
            if os.path.exists(path_video):
                print('{}.mp4已存在，跳过'.format(name_video))
                continue
            else:
                response_detail_page = session.get(url_detail_page,headers = random.choice(headers_list),verify = False).text
                # print('{}详情页请求成功'.format(name_video))
                tree = etree.HTML(response_detail_page)
                url_keneng_video_str = tree.xpath('//*[@id="preview-video"]/source/@src')[0]
                try:
                    url_video = 'https:' + tree.xpath('//*[@id="preview-video"]/source/@src')[0]
                    # print(url_video)
                    video = session.get(url_video, headers=random.choice(headers_list), verify=False,timeout = 1000).content
                except:
                    print('没有预览视频或请求失败')
                else:
                    with open(path_video, 'wb') as fp:
                        fp.write(video)
                        print('{}.mp4下载成功'.format(name_video))
    else:
        print('没有cookie')
        response_page_1 = requests.get(URL, headers=random.choice(headers_list), verify=False).text
        print('该主页面请求成功')
        tree = etree.HTML(response_page_1)
        # //*[@id="videos"]/div/div[1]
        div_list = tree.xpath('//*[@id="videos"]/div/div')
        for div in div_list:
            name_video = div.xpath('./a/div[2]/text()')[0]
            # print(name_video)
            url_detail_page = 'https://javdb6.com' + div.xpath('./a/@href')[0]
            # print(url_detail_page)
            path_video = './番号预览/' + name_video + '.mp4'
            if os.path.exists(path_video):
                print('{}.mp4已存在，跳过'.format(name_video))
                continue
            else:
                response_detail_page = requests.get(url_detail_page, headers=random.choice(headers_list),
                                                   verify=False).text
                # print('{}详情页请求成功'.format(name_video))
                tree = etree.HTML(response_detail_page)
                url_keneng_video_str = tree.xpath('//*[@id="preview-video"]/source/@src')[0]
                try:
                    url_video = 'https:' + tree.xpath('//*[@id="preview-video"]/source/@src')[0]
                    # print(url_video)
                    video = requests.get(url_video, headers=random.choice(headers_list), verify=False,timeout=1000).content
                except:
                    print('没有预览视频或请求失败')
                else:
                    with open(path_video, 'wb') as fp:
                        fp.write(video)
                        print('{}.mp4下载成功'.format(name_video))

    print('================================第{}页下载成功================================'.format(page))