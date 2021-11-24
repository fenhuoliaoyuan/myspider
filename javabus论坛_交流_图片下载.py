import requests
import os
from lxml import etree
import numpy as np
from time import sleep
from config import conn_ip,user_agent_list
import random
def get_response_0(url,acount):
    proxies = random.choice(ips)
    try:
        response_0 = requests.get(url=url, headers=headers, proxies=proxies, timeout=10)  # 获取目标页面text
        if response_0.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print("删除连超时的ip--{}".format(proxies))
        print('重连......')
        if acount == 30:
            return
        acount += 1
        get_response_0(url, acount)
    else:
        return response_0
def get_response_1(url,acount):
    proxies = random.choice(ips)
    try:
        response_1 = requests.get(url=url, headers=headers, proxies=proxies, timeout=10)
        if response_1.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print("删除连超时的ip--{}".format(proxies))
        print('重连......')
        if acount == 30:
            return
        acount += 1
        get_response_1(url, acount)
    else:
        return response_1


def get_img(url,acount):
    # proxies = bytes.decode(random.choice(list(ip_list)))
    proxies = random.choice(ips)
    try:
        response_2 = requests.get(url=url, headers=headers,proxies=proxies,timeout=10)
        if response_2.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print("删除连超时的ip--{}".format(proxies))
        print('重连......')
        if acount == 30:
            return
        acount += 1
        get_img(url,acount)
    else:
        return response_2.content
def get_ips():
    ips_ = conn_ip
    IPs = ips_.smembers('ip_proxies_good')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        # ips__.append({'http': ip,'https':'https://'+ip.split('/')[-1]})
        # ips__.append({'https': 'https://' + ip.split('/')[-1]})
        ips__.append({'http': ip})
    return ips__
ips = get_ips()

if not os.path.exists(r'C:\javDB图片'):
    os.mkdir(r'C:\javDB图片')
# cookies = {
#     'cookie': 'theme=auto; locale=zh; _ym_uid=1625286066655939122; _ym_d=1625286066; _ym_isad=2; over18=1; __cf_bm=390546fbb1382eb14702537333a9e6b22e4a604f-1625287058-1800-AZbNmLSY6WCtWuiboKzoKz+hqQQcBGIsT/rRVJKYUkAcxFn538T4kUz4JvjOoFabn1EmbSJ5yk9KD03uEYfpZ3gOs7UaFMmGK60E6R/vaOI8MNiF9tP7QCnp8HjN4aGgQg==; _jdb_session=IN1K3LLkxoXB4J4f0FeB5KW9vrU8CSPF3IlwwaETbTRGtCXN2f2b1ECNYgUBoRfr6Mtz8FlENJ3dNr4Td%2BlltQt7g8kWNXyW8xsUHNahi2t69RbMhKai21ssuWP41Xpn%2BVtpArkbSrIePWMa2r7gdyH7KKcDGtMdP24DtFPN0JW03Co7Bu8mWgTjoNQQOYjl6T6NMHxg4ry0WPY4rGrJ6m6iYteM7iG22g%2FU6zimAaWNTsgaDVnMluwqggbIR3bxNyvTdIhxr%2BmXyNu%2BGtCJzMZyAYjrI6RySFv9UkVfkKeufRe9O0WQycH3--TJlORBIBd1NH8SqX--JVMUitlzvSCNUibDQXRx6g%3D%3D'
# }
headers = {
    'user-agent': random.choice(user_agent_list)
}

def main(page):
# for page in range(int(start_pages),int(end_pages)+1):
    # URL = 'https://www.javbus.com/forum/forum.php?mod=forumdisplay&fid=2&typeid=7&typeid=7&filter=typeid&page=%d'%page
    URL = 'https://javdb30.com/makers/zKW?f=preview&page=%d'%page
    # print(URL)
    # session.get(url=URL, headers=headers)  # 获取cookie
    print('=======================第{}页爬取开始======================='.format(page))
    sleep(np.random.rand()*10)
    response_0 = get_response_0(url=URL,acount=0)
    # response_0 = requests.get(url=URL, headers=headers,cookies=cookies) # 获取目标页面text
    # print(response_0.url)
    response_0.encoding = response_0.apparent_encoding
    page_text = response_0.text
    tree = etree.HTML(page_text)
    a_list = tree.xpath('//a[@class="box"]')
    # // *[ @ id = "videos"] / div / div[1] / a
    # // *[ @ id = "videos"] / div / div
    for div in a_list:
        # url_detail = 'https://www.javbus.com/forum/' + div.xpath('./@href')[0]
        url_detail = 'https://javdb30.com' + div.xpath('./@href')[0]
        img_name_fanhao = div.xpath('./div[@class="uid"]/text()')[0]
        # 详情页解析
        # sleep(np.random.rand() * 10)
        response_1 = get_response_1(url_detail,acount=0)
        # response_1 = requests.get(url=url_detail, headers=headers, cookies=cookies)
        response_1.encoding = response_1.apparent_encoding
        page_detail_text = response_1.text
        tree_0 = etree.HTML(page_detail_text)
        # ex_img_url = '<img.*?src="(/i.imgur.com/.*?)".*?>'
        # url_img_list = re.findall(ex_img_url, page_detail_text, re.S)
        img_list = tree_0.xpath('//a[@data-fancybox="gallery"]')
        for img in img_list:
            url_img = img.xpath('./@href')[0]
            name_img = url_img.split('/')[-1]
            name_img = name_img.replace('?','_')
            name_img = name_img.replace('/','_')
            name_img = name_img.replace(':','_')
            # name_img = dl.xpath('/@alt')[0]
            # 下载图片
            if 'jpg' in name_img:
                path_img = r'C:\javDB图片' + '\\' + img_name_fanhao + '_' + name_img
                if os.path.exists(path_img):
                    print('{}_图片{}已存在--{}'.format(img_name_fanhao, name_img,page))
                    continue
                else:
                    # sleep(np.random.rand() * 10)
                    response_2 = get_img(url_img, acount=0)
                    # response_2 = requests.get(url=url_img, headers=headers,cookies=cookies).content
                    with open(path_img, 'wb') as fp:
                        fp.write(response_2)
                        print('{}_{}下载完成---{}'.format(img_name_fanhao, name_img,page))

    print('========================第{}页爬取结束============================'.format(page))
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    acounts = 0
    # proxy = config.set_socks4_proxy()
    # session = requests.Session()#实例化
    start_pages = input('输入开始页码： ')
    end_pages = input('输入结束页码： ')
    with ThreadPoolExecutor(50) as tp:
        for page in range(int(start_pages),int(end_pages)+1):
            tp.submit(main,page)