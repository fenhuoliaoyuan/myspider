import requests
import os
import re
from lxml import etree
import config
from multiprocessing.dummy import Pool
from tqdm import tqdm
from time import sleep
import random



headers = {
            'user-agent':config.get_ua()['user-agent'],
            'cookie':'_hjid=53bb752b-0bf6-408a-970b-210de97bbcb3; a=MWItcVOFBlcwQZHWkg1enA80hcqOSxB4; _gid=GA1.2.672286493.1623826199; _hjShownFeedbackMessage=true; _popfired_expires=Invalid%20Date; fpestid=smIppwTtc50m7sc--RCFTm1Z3aFGf9jeRnY15xOg1D1jT5egcXzF8J4vxw2pq7S4zxcpKw; _popfired=25; lastOpenAt_=1623853440963; _hjAbsoluteSessionInProgress=0; _popprepop=1; _ga=GA1.2.1097375884.1623826197; _gat_gtag_UA_178112556_1=1; _ga_JHERDQ67YJ=GS1.1.1623864917.5.1.1623866864.0'
        }

def get_detail_urls(startpage,endpage,URL):
    # URL = 'https://asiantolick.com/ajax/buscar_posts.php?post=&cat=&tag=&search=cosplay%20sex&index=1&ver=12'
    cat = re.compile('cat=(\d+)?&').findall(URL)[0]
    search = re.compile('search=(.*?)&').findall(URL)
    if len(search) == 0:
        search = ''
    else:
        search = search[0]
    ver = re.compile('ver=(\d+)?').findall(URL)[0]
    # search_ = search.split('%20')
    for page in range(int(startpage),int(endpage)+1):
        # params = {
        #     'post': '',
        #     'cat': cat,
        #     'tag': '',
        #     'search': search_[0]+search_[1],
        #     'index': page-1,
        #     'ver': int(ver),
        # }

        url = 'https://asiantolick.com/ajax/buscar_posts.php?post=&cat={}&tag=&search={}&index={}&ver={}'.format(cat,search,page-1,ver)

        # page_text = requests.get(url=url,headers=config.get_ua(),params=params).text
        page_text = requests.get(url=url, headers=headers).text
        sleep(random.randint(1,2))
        tree = etree.HTML(page_text)
        url_list = tree.xpath('//a/@href')
        url_list_ap = []
        for url_ in url_list:
            url_list_ap.append(url_)
            # print(url_)
    return search,url_list_ap

def get_img_url(url_detail):
    dir_img_name = os.path.split(url_detail)[1]
    page_text = requests.get(url=url_detail,headers=headers).text
    sleep(random.randint(1,2))
    tree = etree.HTML(page_text)
    img_url_true_list = tree.xpath('//div[@class="spotlight-group"]/div/@data-src')
    img_url_true_ap = []
    for img_url_true_ in img_url_true_list:
        img_url_true_ap.append(img_url_true_)
    return dir_img_name,img_url_true_ap

def write_file(search,path_img_,dir_img_name,img_url_true):
    if not os.path.exists(path_img_ + '//' + search):
        os.mkdir(path_img_ + '//' + search)
    if not os.path.exists(path_img_ + '//' + search + '//' + dir_img_name):
        os.mkdir(path_img_ + '//' + search + '//' + dir_img_name)
    name_img = os.path.split(img_url_true)[1]
    path_img = path_img_ + '//' + search + '//' + dir_img_name + '//' + name_img
    if os.path.exists(path_img):
        print('文件已存在')
    else:
        img = requests.get(url=img_url_true,headers=headers).content
        with open(path_img,'wb') as fp:
            fp.write(img)
            # print('图片{}下载成功'.format(name_img))
if __name__ == '__main__':
    URL = input('例如：https://asiantolick.com/ajax/buscar_posts.php?post=&cat=&tag=&search=cosplay%20sex&index=1&ver=12\n输入找到的网址： ')
    start_page = input('输入开始的页码： ')
    end_page = input('输入结束的页码： ')
    search,url_list_ap = get_detail_urls(start_page,end_page,URL)
    search_ = input('例如：无圣光sexy cosplay\n如果你想更换相册目录,请输入你的搜索词或自己要的命名（防止有些相册目录无效）\n若不想更换直接点回车 ：')
    if len(search_) != 0:
        search = search_
    # pool = Pool(3)  # 实例化开启多条线程
    # pool.map(get_img_url, url_list_ap)
    path_img_ = input("例如:'C:\番号\\asiantolick_com'\n输入存储图片路径目录： ")
    for url_list_ in url_list_ap:
        dir_img_name, img_url_true_ap = get_img_url(url_list_)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++{}下载开始'.format(dir_img_name))
        pbar = tqdm(total=len(img_url_true_ap))
        for img_url in img_url_true_ap:
            write_file(search, path_img_, dir_img_name, img_url)
            pbar.update(1)
        pbar.close()