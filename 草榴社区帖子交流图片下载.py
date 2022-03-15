import requests
import os
from lxml import etree
import re
import random
import config
from proxies import proxies_test


if not os.path.exists('./草榴社区图片/'):
    os.mkdir('./草榴社区图片/')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}
# proxy = config.set_socks4_proxy()
session = requests.Session()#实例化
start_pages = input('输入开始页码： ')
end_pages = input('输入结束页码： ')
for page in range(int(start_pages),int(end_pages)+1):
    URL = 'https://t66y.com/thread0806.php?fid=7&search=&page=%d' % page
    print(URL)
    session.get(url=URL, headers=headers)  # 获取cookie
    response_0 = session.get(url=URL, headers=headers,verify=False) # 获取目标页面text
    response_0.encoding = response_0.apparent_encoding
    page_text = response_0.text
    tree = etree.HTML(page_text)
    acounts = 0 # 帖子数（含图片的）
    ex_url = 'href="(htm_data/.*?.html)"'
    # ex_text = r'href=("htm_data/2106.*?.html")'
    url_detail_list = re.findall(ex_url,page_text,re.S)
    # name_page_list = re.findall(ex_text,page_text,re.S)
    # td_list = tree.xpath('//tbody[@style="table-layout:fixed;"]//td[@class="tal"]')
    for u in url_detail_list:
        print('//a[@href="{}"]/@href'.format(u))
        # url_detail = tree.xpath('//a[@href="{}"]/@href'.format(u))[0]
        # name_page = tree.xpath('//a[@href="{u}"]/text()')[0]
        if len(tree.xpath('//a[@href="{}"]/text()'.format(u))) != 0:
            if 'P]' in tree.xpath('//a[@href="{}"]/text()'.format(u))[0]:
                acounts_1 = 0 #每张帖子的图片数量
                url_detail = 'https://t66y.com/' + tree.xpath('//a[@href="{}"]/@href'.format(u))[0]
                name_page = tree.xpath('//a[@href="{}"]/text()'.format(u))[0]
                # url_detail = 'https://t66y.com/' + u
                # name_page = n
                name_page = name_page.replace('/', '_')
                name_page = name_page.replace('.', '_')
                name_page = name_page.replace(':','_')
                print(name_page)
                path_dir = './草榴社区图片/' + name_page + '/'
                if not os.path.exists(path_dir):
                    os.mkdir(path_dir)
                # 详情页解析
                response_1 = session.get(url=url_detail, headers=headers, verify=False)
                response_1.encoding = response_1.apparent_encoding
                page_detail_text = response_1.text
                tree_0 = etree.HTML(page_detail_text)
                ex_img_url = "<img.*?ess-data='(.*?)'>"
                url_img_list = re.findall(ex_img_url,page_detail_text,re.S)
                for url_img_0 in url_img_list:
                # // *[ @ id = "main"] / div[3] / table / tbody / tr[1] / th[2] / table / tbody / tr / td / div[4] / div[2]
                # div_list = tree_0.xpath('//div[@class="tpc_content do_not_catch"]/img')
                # for div in url_img_list:
                    url_img = url_img_0
                    # print(url_img)
                    name_img = url_img.split('/')[-1]
                    # name_img = dl.xpath('/@alt')[0]
                    # 下载图片
                    path_img = path_dir + name_img
                    if os.path.exists(path_img):
                        acounts_1 += 1
                        print(f'第{acounts+1}文件{name_img}已存在，跳过==========第{page}页{name_page}')
                        continue
                    else:
                        try:
                            response_2 = session.get(url=url_img, headers=headers).content
                        except:
                            print('拿到的地址错误')
                        else:
                            try:
                                with open(path_img, 'wb') as fp:
                                    fp.write(response_2)
                                    acounts_1 += 1
                                    print(f'第{acounts_1}个文件{name_img}下载完成==========第{page}页{name_page}')
                            except:
                                print('DSError')
            acounts += 1
            try:
                print(f'========================第{page}页第{acounts}张帖子{name_page}共{acounts_1}张图片下载完成===========================')
            except:
                print("NameError")
    print('====================第{}页共{}个帖子已下载完成===================='.format(page,str(acounts)))
