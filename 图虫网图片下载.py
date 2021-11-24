import requests
import parsel
import random
import os
import time
from lxml import etree
from proxies import proxies_test
import config
from tqdm import tqdm
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
# ip_list = config.conn_ip.smembers('ip_proxies')
def get_ips():
    ips = config.conn_ip
    IPs = ips.smembers('ip_proxies')
    ips = []
    for IP in IPs:
        ip = bytes.decode(IP)
        ips.append({'http': ip })
    return ips
ips = get_ips()
def get_img(src,acount):
    # proxies = bytes.decode(random.choice(list(ip_list)))
    proxies = random.choice(ips)
    try:
        img = session.get(url=src, headers=header,proxies=proxies,timeout = 2).content
    except:
        ips.remove(proxies)
        print("删除连超时的ip--{}".format(proxies))
        print('重连......')
        if acount == 10:
            return
        acount += 1
        img = get_img(src,acount)
    return img
# ips = proxies_test.Proxy()
path_root = 'E:\图虫网\美女'
url_mainpage = 'https://tuchong.com/tags/%E7%BE%8E%E5%A5%B3?type=new'
# print(int(time.time()))
#动态获取cookie
header = random.choice(headers_list)#随机挑选头部，进行UA伪装
session = requests.Session()#创建Session对象
session.get(url_mainpage,headers=header)#捕获且存储cookie
#发现网页用js渲染，查找json文件找到详情页地址

for pages in range(1,100):
    #快速查找到真实地址
    # page: 4
    # count: 20
    # order: new
    # before_timestamp: 1624344502
    url_true = 'https://tuchong.com/rest/tags/%E7%BE%8E%E5%A5%B3/posts?page={}&count=20&order=new&before_timestamp={}'.format(pages,int(time.time()))
    response_mianpage = session.get(url = url_true,headers = header).json()#得到JSON数据
    # print(response_mianpage)
    response_mianpage_1 = response_mianpage['postList']#取出里面的数组
    # print(response_mianpage_1)
    for i in response_mianpage_1:#遍历数组里面的字典
        url_detail = i['url']#得到每个相册的真实地址
        # print(url_detail)
        # response_detail = requests.get(url = url_detail,headers = header).text#相册详情页获取
        page_detail_text = session.get(url=url_detail,headers=header).text
        # page_detail_text = get_page_detail_text(url_detail,acount=0)
        if page_detail_text is not None:
            tree = etree.HTML(page_detail_text)
            src_list = tree.xpath('//*[@class="post-content"]/img/@src')
            tqdm_ = tqdm(total=len(src_list))
            for src in src_list:
                name_img = src.split('/')[-1]
                if 'jpg' in name_img:
                    path_img = path_root + '/' + name_img
                    test = config.conn_1.sadd('img_url',src)
                    if test == 0:
                        tqdm_.update(1)
                        continue
                    else:
                        print('有图片更新......')
                        config.conn_1.srem('img_url',src)
                        # img = session.get(url=src,headers=header).content
                        img = get_img(src,acount=0)
                        if img is not None:
                            with open(path_img,'wb') as fp:
                                fp.write(img)
                                tqdm_.update(1)
                                config.conn_1.sadd('img_url',src)
            tqdm_.close()
                    # print()


        # data_img = parsel.Selector(response_detail)#构建选择器
        # url_img_list = data_img.xpath('/html/body/main/div[1]/article/img/@src').getall()# /html/body/main/div[1]/article#将选择器数据化
        # #获取文件名，有特殊字符进行替换
        # name_img_text = data_img.xpath('/html/body/main/div[1]/article/text()').getall()[0]
        # name_img_text_0 = name_img_text.replace(' ','')
        # name_img_1 = name_img_text_0.replace('\n','')
        # name_img_2 = name_img_1.replace('/','')
        # name_img_3 = name_img_2.replace(':', '')
        # name_img = name_img_3.replace('|','')
        # print(name_img,url_img_list)
        # for url_img in url_img_list:#遍历每个图片地址
        #     name_img_detail = url_img.split('/')[-1]#从图片地址中获取图片名称
        #     if len(name_img)>100:#防止文件名过长出现报错
        #         name_img = name_img[0:50]
        #     else:
        #         path_img = './图虫网图片/' + name_img + '/'+ name_img_detail
        #         if not os.path.exists('./图虫网图片/' + name_img):#创建文件目录
        #             os.mkdir('./图虫网图片/' + name_img)
        #         if os.path.exists(path_img):#跳过已存在的文件
        #             print('文件{}已存在,跳过'.format(path_img))
        #             continue
        #         else:
        #             response_img = session.get(url = url_img,headers = header).content#获得图片二进制数据
        #             with open(path_img,'wb') as fp:#将图片二进制数据写入文件中
        #                 fp.write(response_img)
        #                 print(name_img_detail,'下载成功')



