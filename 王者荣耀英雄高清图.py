import requests
import os
from lxml import etree
import random


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
if not os.path.exists('./王者荣耀英雄高清图/'):  # 创建文件目录
    os.mkdir('./王者荣耀英雄高清图/')
url = 'https://pvp.qq.com/web201605/herolist.shtml'
session = requests.Session()  # 创建Session对象
session.get(url, headers=random.choice(headers_list))  # 捕获且存储cookie
response_page_main = session.get(url,headers=random.choice(headers_list)).text.encode('iso-8859-1').decode('gbk')# print(res.
# text.encode('iso-8859-1').decode('gbk')
# print(response_page_main)
# response_page_main.encode()
tree = etree.HTML(response_page_main)
# print(tree)
# //*[@id="container"]/div[1]/a/img
# //*[@id="container"]/div
lis = tree.xpath('//ul[@class="herolist clearfix"]/li ')#//div[@class="song"]#/html/body/div[3]/div/div/div[2]/div[2]/ul
# /li[1]#/html/body/div[3]/div/div/div[2]/div[2]/ul
# print(lis)
acounts = 0
for li in lis:
    url_detail_page = 'https://pvp.qq.com/web201605/' + li.xpath('./a/@href')[0]
    # print(url_detail_page)
    name_img = li.xpath('./a/img/@alt')[0]#/html/body/div[3]/div/div/div[2]/div[2]/ul/li[1]/a/img
    # print(name_img)
    path_img = './王者荣耀英雄高清图/'+ name_img + '.jpg'
    if os.path.exists(path_img):
        print('文件{}.jpg已存在，跳过'.format(name_img))
        acounts +=1
        continue
    else:
        response_detail_page_txt = session.get(url_detail_page,headers=random.choice(headers_list)).text
        tree = etree.HTML(response_detail_page_txt)
        url_img = 'https:' + tree.xpath('//div[@class="pic-show-box"]/div[@class="cover"]/a/img/@src')[0]#/div[@class="pic-show-box"]/div[@class="cover"]/a/img/@src
        # print(url_img)
        img = session.get(url_img,headers = random.choice(headers_list)).content
        with open(path_img,'wb') as fp:
            fp.write(img)
            acounts+=1
            print('第{}个文件{}.jpg下载成功'.format(acounts,name_img))