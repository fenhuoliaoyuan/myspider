# pip install youtube-dl
import os
import re
import requests

# https://space.bilibili.com/8366990/video?tid=0&page=4&keyword=&order=pubdate
URL_0 = input('例如https://space.bilibili.com/8366990/video?tid=0&page=4&keyword=&order=pubdate\n输入你要爬取的用户视频列表地址 :   ')
if 'page' not in URL_0:
    URL_0_0 = URL_0.split('?')
    URL_0 = URL_0_0[0] + '?' + 'page=1&' + URL_0_0[1]
URL_1 = list(re.compile('(.*)page=\d(&.*)').findall(URL_0)[0])
start_page = input('输入你要爬取的开始页数： ')
end_page = input('输入你要爬取的截至页数： ')
# 切换目录 r'E:\B站视频下载\'
# os.chdir(input("输入你要存储视频的目录路径 ："))
dir_name = input("输入你要存储视频的目录路径 ：")
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}
acounts = 0
for page in range(int(start_page),int(end_page)+1):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++第{}页下载开始'.format(page))
    URL = URL_1[0] + 'page=%d'%page + URL_1[1]
    mid = re.compile('com/(\d+)/?').findall(URL)[0]
    # print(mid)
    params = {
        'mid': mid,
        'ps': 30,
        'tid': 0,
        'pn': page,
        'keyword': '',
        'order': 'pubdate',
        'jsonp': 'jsonp'
    }
    url_api = 'https://api.bilibili.com/x/space/arc/search?'
    # print(url_api)
    json_response = requests.get(url=url_api,headers=headers,params=params).json()
    list_video = json_response["data"]["list"]["vlist"]
    for v in list_video:
        url_video = 'https://www.bilibili.com/video/' + v["bvid"]
        # print(url_video)
        acounts += 1
        print('第{}个文件下载开始'.format(acounts))
        os.system('youtube-dl ' + url_video)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++第{}页下载结束'.format(page))