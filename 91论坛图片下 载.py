import requests
import os
from lxml import etree
import random
import config
from proxies import proxies_test



headers = config.request_headers()
# proxy = config.set_socks4_proxy()
session = requests.Session()#实例化
start_pages = input('输入开始页码： ')
end_pages = input('输入结束页码： ')
for page in range(int(start_pages),int(end_pages)+1):
    # URL = 'https://f0416.wonderfulday30.live/forumdisplay.php?fid=4&page=%d'%page
    URL = 'https://f0416.wonderfulday30.live/forumdisplay.php?fid=4&filter=digest&page=%d' % page
    print(URL)
    # proxies = proxy.Proxy()
    # URL = 'https://f0416.wonderfulday30.live/forumdisplay.php?fid=4&page=1'
    # URL = 'https://baidu.com'
    session.get(url=URL, headers=headers)  # 获取cookie
    response_0 = session.get(url=URL, headers=headers,verify=False) # 获取目标页面text
    # print(response_0.encoding)
    # print(response_0.apparent_encoding)
    response_0.encoding = response_0.apparent_encoding
    # print(response_0.text)
    page_text = response_0.text
    # html = response_0.text.encode('iso-8859-1').decode('gbk')
    # print(html)
    # response_0.encoding = 'UTF-8'
    acounts = 0
    # print(response_0.text)
    tree = etree.HTML(page_text)
    if len(tree.xpath('//th[@class="subject new"]')):
        div_list = tree.xpath('//th[@class="subject new"]')
        for div in div_list:
            url_detail = 'https://f0416.wonderfulday30.live/' + div.xpath('./span/a/@href')[0]
            name_page = div.xpath('./span/a/text()')[0]
            name_page = name_page.replace('/', '_')
            name_page = name_page.replace('.', '_')
            path_dir = './91论坛图片/' + name_page + '/'
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)
            # 详情页解析
            response_1 = session.get(url=url_detail, headers=headers, verify=False)
            response_1.encoding = response_1.apparent_encoding
            page_detail_text = response_1.text
            tree_0 = etree.HTML(page_detail_text)
            dl_list = tree_0.xpath('//td[@class="t_msgfont"]/img')
            if len(dl_list) == 0:
                dl_list = tree_0.xpath('//dl[@class="t_attachlist attachimg"]/dd/div/img')
            if len(dl_list) == 0:
                dl_list = tree_0.xpath('//dl[@class="t_attachlist attachimg"]/dd/div[2]/img')
            if len(dl_list) == 0:
                dl_list = tree_0.xpath('//img[@onload="thumbImg(this)"]')
            for dl in dl_list:
                acounts_1 = 0
                # //*[@id="pid5971211"]/tbody/tr[1]/td[2]/div[3]/div[4]/div[2]/div/dl[2]/dd/div[2]
                if len(dl.xpath('./@file')) == 0:
                    url_img = dl.xpath('./@src')[0]
                else:
                    url_img = dl.xpath('./@file')[0]
                name_img = url_img.split('/')[-1]
                # name_img = dl.xpath('/@alt')[0]
                # 下载图片
                path_img = path_dir + name_img
                if os.path.exists(path_img):
                    acounts += 1
                    acounts_1 += 1
                    print(f'第{acounts}文件{name_img}已存在，跳过==========第{page}页{name_page}')
                    continue
                else:
                    try:
                        response_2 = session.get(url=url_img, headers=headers).content
                    except:
                        print('拿到的地址错误')
                    else:
                        with open(path_img, 'wb') as fp:
                            fp.write(response_2)
                            acounts += 1
                            acounts_1 += 1
                            print(f'第{acounts}个文件{name_img}下载完成==========第{page}页{name_page}')
    elif len(tree.xpath('//th[@class="subject common"]')):
        div_list = tree.xpath('//th[@class="subject common"]')
        for div in div_list:
            url_detail = 'https://f0416.wonderfulday30.live/' + div.xpath('./span/a/@href')[0]
            name_page = div.xpath('./span/a/text()')[0]
            name_page = name_page.replace('/','_')
            name_page = name_page.replace('.','_')
            path_dir = './91论坛图片/' + name_page + '/'
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)
            # 详情页解析
            response_1 = session.get(url=url_detail,headers=headers,verify=False)
            response_1.encoding = response_1.apparent_encoding
            page_detail_text = response_1.text
            tree_0 = etree.HTML(page_detail_text)
            dl_list = tree_0.xpath('//td[@class="t_msgfont"]/img')
            if len(dl_list) == 0:
                dl_list = tree_0.xpath('//dl[@class="t_attachlist attachimg"]/dd/div/img')
            if len(dl_list) == 0:
                dl_list = tree_0.xpath('//dl[@class="t_attachlist attachimg"]/dd/div[2]/img')
            if len(dl_list) == 0:
                dl_list = tree_0.xpath('//img[@onload="thumbImg(this)"]')
            for dl in dl_list:
                acounts_1 = 0
                # //*[@id="pid5971211"]/tbody/tr[1]/td[2]/div[3]/div[4]/div[2]/div/dl[2]/dd/div[2]
                if len(dl.xpath('./@file')) == 0:
                    url_img = dl.xpath('./@src')[0]
                else:
                    url_img = dl.xpath('./@file')[0]
                name_img = url_img.split('/')[-1]
                # name_img = dl.xpath('/@alt')[0]

                # 下载图片
                path_img = path_dir + name_img
                if os.path.exists(path_img):
                    acounts += 1
                    acounts_1 += 1
                    print(f'第{acounts}文件{name_img}已存在，跳过==========第{page}页{name_page}')
                    continue
                else:
                    try:
                        response_2 = session.get(url=url_img,headers=headers).content
                    except:
                        print('拿到的地址错误')
                    else:
                        with open(path_img,'wb') as fp:
                            fp.write(response_2)
                            acounts += 1
                            acounts_1 += 1
                            print(f'第{acounts}个文件{name_img}下载完成==========第{page}页{name_page}')
            print(f'========================第{page}页{name_page}下载完成===========================')
    print('====================第{}页{}共{}张图片已下载完成===================='.format(page,name_page,str(acounts_1)))





