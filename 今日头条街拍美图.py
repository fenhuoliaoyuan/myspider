import requests
import os
import random
import json
from time import sleep

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
if not os.path.exists('./今日头条街拍美图/'):  # 创建文件目录
    os.mkdir('./今日头条街拍美图/')
URL = 'https://so.toutiao.com'
# header = random.choice(headers_list)
session = requests.Session()#创建Session对象
session.get(URL,headers=random.choice(headers_list))#捕获且存储cookie
for i in range(23,50):
    url_mainpage = 'https://so.toutiao.com/search?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3&pd=atlas&source=search_subtab' \
                   '_switch&dvpf=pc&aid=4916&page_num={}&rawJSON=1&search_id=202105222209210101510440282924F8D1'.format(i)
    # data = {
    #     'keyword': '街拍美女',
    #     'pd': 'atlas',
    #     'source': 'search_subtab_switch',
    #     'dvpf': 'pc',
    #     'aid': '4916',
    #     'page_num': '1',
    #     'rawJSON': '1',
    #     'search_id': '202105222157220102121921344017BC5B'
    # }
    # # response_1 = requests.post(url=url_mainpage,headers = random.choice(headers_list),data=data).json()
    # try:  #响应异常处理
    response_1 = session.get(url=url_mainpage, headers=random.choice(headers_list)).json()
    sleep(random.random())
    # print(response_1)
    response_2 = response_1['rawData']
    try:
        items = response_2['data']
        for item in items:
            name_img = item['text']
            name_img_0 = name_img.replace(' ', '')
            name_img_1 = name_img_0.replace('\n', '')
            name_img_2 = name_img_1.replace('/', '')
            name_img_3 = name_img_2.replace(':', '')
            name_img_4 = name_img_3.replace('|', '')
            name_img_5 = name_img_4.replace('"','_')
            name_img = name_img_5.replace('?','')
            url_img = item['img_url']
            path_img = './今日头条街拍美图/' + name_img + '.jpg'
            if os.path.exists(path_img):  # 跳过已存在的文件
                print('文件{}已存在,跳过'.format(name_img + '.jpg'))
                continue
            else:
                try:
                    img_file = session.get(url_img, headers=random.choice(headers_list)).content
                except:
                    print("图片获取异常")
                else:
                    with open(path_img, 'wb') as fp:
                        fp.write(img_file)
                        print(name_img + '.jpg', '下载成功')
        # print(items)
    except:
        print("没拿到items",i)
    else:
        pass
    # except:
    #     print('请求异常')
    # else:
    #     print('请求成功')


