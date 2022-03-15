import requests
import os
from lxml import etree
import random

target_url = 'https://amazfitwatchfaces.com/gtr/top'
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
# if not os.path.exists('./amazfitwatchfaces_com/'):
#     os.mkdir('./amazfitwatchfaces_com/')
acounts = 0#用于计数
session = requests.Session()#实例化
session.get(url=target_url,headers=random.choice(headers_list))#获取cookie
response_0 = session.get(url=target_url,headers=random.choice(headers_list)).text#获取目标页面text
tree = etree.HTML(response_0)
# 获取各项div列表,注意标签过滤广告div
# div_list = tree.xpath('//div[@class="col-md-3 col-sm-6 col-xs-12"]')
# 获取各项a标签列表
a_list = tree.xpath('//a[@class="wf-act"]')
for a in a_list:
    # / html / body / div[2] / div[1] / div[1] / div[2] / div[5] / div[1] / div / div[2] / a
    # // *[ @ id = "wf-row"] / div[1] / div / div[2] / a
    # 获取详情页地址
    url_detail = 'https://amazfitwatchfaces.com' + a.xpath('./@href')[0]

    # name_target = ''
    # 获取详情页text
    response_1 = session.get(url=url_detail,headers=random.choice(headers_list)).text
    tree = etree.HTML(response_1)
    # 获取下载列表
    url_download_list = tree.xpath('//*[@id="dwModal"]/div/div/div[2]/a')
    # 获取名称作为目录
    dir_0 = tree.xpath('//*[@id="main-wrapper"]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/h4/text()')[0]
    # 替换里面的'/'以免出现路径异常
    dir_0 = dir_0.replace('/','_')
    # gif 下载地址获取
    url_gif = 'https:' + tree.xpath('//*[@id="watchface-preview"]/@src')[0]
    name_gif = tree.xpath('//*[@id="watchface-preview"]/@alt')[0] + tree.xpath('//*[@id="watchface-preview"]/@src')[0].split('/')[-1]
    name_gif = name_gif.replace('/','_')
    # 双层目录组成
    path_dir = './amazfitwatchfaces_com/' + dir_0 + '/'
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    # 组成gif路径
    path_gif = path_dir + name_gif
    # if not os.path.exists(path_dir):
    #     os.mkdir(path_dir)
    # 下载gif
    if os.path.exists(path_gif):
        acounts += 1
        print('第{}个动图{}已存在，跳过下载'.format(acounts,name_gif))
        continue
    else:
        response_gif = session.get(url=url_gif,headers=random.choice(headers_list)).content
        with open(path_gif,'wb') as gif:
            gif.write(response_gif)
            acounts += 1
            print('第{}个动图{}下载成功'.format(acounts,name_gif))
    # 下载bin文件
    for url_download in url_download_list:
        url_download_finally = 'https://amazfitwatchfaces.com' + url_download.xpath('./@href')[0]
        name_download = url_download.xpath('./text()')[0]
        path_download = path_dir + name_download + '.bin'
        if os.path.exists(path_download):
            print('文件{}.bin已存在，跳过下载'.format(name_download))
            continue
        else:
            response_download = session.get(url=url_download_finally,headers=random.choice(headers_list)).content
            with open(path_download,mode='wb') as fp:
                fp.write(response_download)
                print('文件{}.bin下载成功'.format(name_download))
