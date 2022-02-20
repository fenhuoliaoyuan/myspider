import requests
import re
from lxml import etree
import os
# from fontTools.ttLib import TTFont
import config
import random
import io

headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
def get_page_text(url,acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        page_text = requests.get(url=url, headers=headers, proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        if acount == 10:
            return
        acount += 1
        get_page_text(url, acount)
    else:
        return page_text
def get_page_text_detail(url_detail,acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        page_text_detail = requests.get(url=url_detail, headers=headers,proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        if acount == 10:
            return
        acount += 1
        get_page_text_detail(url_detail,acount)
    else:
        return page_text_detail
def get_img(url_img,acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        img = requests.get(url=url_img, proxies=proxies,headers=headers)
        if img.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        if acount == 10:
            return
        acount += 1
        get_img(url_img,acount)
    else:
        return img
def main(page):
    url = 'https://bbs6.u79m.xyz/2048/thread.php?fid-29-type-9-page-{}.html'.format(page)
    # page_text = requests.get(url=url,headers=headers)
    page_text = get_page_text(url=url,acount=0)
    page_text.encoding = page_text.apparent_encoding
    page_text = page_text.text
    a_list = etree.HTML(page_text).xpath('//a[@class="subject"]')
    for a in a_list:
        url_detail = 'https://bbs6.unr1.xyz/2048/' + a.xpath('./@href')[0]
        name_page_text = a.xpath('./text()')[0]
        test_url_detail = config.conn_ip.sadd('url_detail_page_gif', url_detail)
        if test_url_detail == 1:
            print('\033[1;32;40m更新{}-{}'.format(name_page_text,page))
            config.conn_ip.srem('url_detail_page_gif', url_detail)
        # page_text_detail = requests.get(url=url_detail,headers=headers).text
            page_text_detail = get_page_text_detail(url_detail=url_detail,acount=0).text
            url_img_list = etree.HTML(page_text_detail).xpath('//div[@class="f14"]//img/@src')
            # url_img_list = etree.HTML(page_text_detail).xpath('//ignore_js_op[@class="att_img"]/img/@src')
            for url_img in url_img_list:
                name_img = '_'.join(url_img.split('/')[-4:])
                path_img = path_root + '\\' + name_img
                if not os.path.exists(path_img):
                    if 'gif' in name_img:
                        # img_content = requests.get(url=url_img,headers=headers)
                        img_content = get_img(url_img=url_img, acount=0)
                        with open(path_img, 'wb') as fp:
                            fp.write(img_content.content)
                            print('\033[1;34;40m{}下载成功-{}'.format(name_img, page))
            config.conn_ip.sadd('url_detail_page_gif', url_detail)
            print('\033[1;31;40m{}更新完成-{}'.format(name_page_text,page))
    print('\033[1;33;40m第{}页下载完成'.format(page))
if __name__ == '__main__':
    ips = config.ips
    path_root = r'G:\ghs\动图'
    if not os.path.exists(path_root):
        os.mkdir(path_root)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(5) as tp:
        for page in range(11, 20):
            tp.submit(main, page)
    # main(2)