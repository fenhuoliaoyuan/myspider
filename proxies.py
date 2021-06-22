import requests
from lxml import etree
import time
import random
from 爬虫小项目 import config

def Proxy():
    # def check_ip(proxies_list):
    #     time.sleep(1)
    #     can_use = []
    #
    #     for ip in proxies_list:
    #         try:
    #             response = requests.get(url='https://www.baidu.com', proxies=ip, timeout=0.1)
    #             if response.status_code == 200:
    #                 can_use.append(ip)
    #         except:
    #             print('当前的代理:', ip, '请求超时，检测不合格')
    #         else:
    #             print('当前的代理:', ip, '检测合格')
    #
    #     return can_use

    proxies_list = []

    for page in range(1,5):
        time.sleep(1)
        print(f'===============正在爬取第{page}页数据================')
        url = f'https://www.kuaidaili.com/free/inha/{page}/'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding

        page_text = response.text

        tree = etree.HTML(page_text)
        trs = tree.xpath('//*[@id="list"]/table/tbody/tr')

        for tr in trs:
            ip_num = tr.xpath('./td[1]/text()')[0]
            ip_port = tr.xpath('./td[2]/text()')[0]

            ip_proxy = ip_num + ':' + ip_port
            # print(ip_proxy)
            if tr.xpath('./td[4]/text()')[0] == 'HTTP':
                proxy_dict = {
                    'http': 'http://' + ip_proxy,
                }
            if tr.xpath('./td[4]/text()')[0] == 'HTTPS':
                proxy_dict = {
                    'https': 'https://' + ip_proxy,
                }

            proxies_list.append(proxy_dict)
            print('保存成功:', proxy_dict)
    time.sleep(1)
    can_use = []
    print('\n===========================正在检测===================================')
    for ip in proxies_list:
        try:
            response = requests.get(url='https://www.baidu.com', proxies=ip, timeout=1)
            # response = requests.get(url='https://www.bilibili.com/', proxies=ip, timeout=0.5)
            # if response.status_code == 200:
        except:
            print('当前的代理:', ip, '请求超时，检测不合格')
        else:
            can_use.append(ip)
            print('当前的代理:', ip, '检测合格')

    return can_use

if __name__ == '__main__':
    Ips = Proxy()
    for ip in Ips:
        ip_input = config.conn_ip.sadd('ip_proxies',ip)
        if ip_input == 0:
            pass
        else:
            print('更新一个ip : ',ip)

