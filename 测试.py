import requests
import os
import random
from lxml import etree
import re
from Crypto.Cipher import AES
from base64 import b64decode
import 类库
from 类库 import get_ts
from concurrent.futures import ThreadPoolExecutor
from 爬虫小项目 import config
def get_ips():
    ips_ = config.conn_ip
    IPs = ips_.smembers('ip_proxies_good')
    # IPs = ips_.smembers('ip_proxies_1')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        # ips__.append({'http': ip,'https':'https://'+ip.split('/')[-1]})
        # ips__.append({'https': 'https://' + ip.split('/')[-1]})
        ips__.append({'http': ip})
    return ips__
ips = get_ips()
def get_ips():
    ips_ = config.conn_ip
    IPs = ips_.smembers('ip_proxies_good')
    # IPs = ips_.smembers('ip_proxies_1')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        # ips__.append({'http': ip,'https':'https://'+ip.split('/')[-1]})
        # ips__.append({'https': 'https://' + ip.split('/')[-1]})
        ips__.append({'http': ip})
    return ips__


ips = get_ips()
user_agent_list = config.user_agent_list
def get_page_text(url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            # 'cookie': 'PHPSESSID=0cv23m2b1aao4j0ejd8lu3q97o; _ga=GA1.1.303687662.1623823577; kt_tcookie=1; asgsc262182=2; kt_ips=103.152.113.48%2C103.152.113.169%2C103.152.113.219%2C103.152.113.96%2C103.152.113.90%2C103.152.113.52; __cf_bm=vpYodyet98dDmvrhfTosLXH2LF.EK8I8tLTR9GJtPeU-1634919841-0-AWuwZRDhbUlrAUA9lIyVJED9PKThrKu3v/OVmLs6LAAYKlSeq7/aa5jQer4ColKFfJiw/CPvAw9B8jkwgWLi2ko=; _ga_1DTX7D4FHE=GS1.1.1634918629.35.1.1634919926.0',
            # 'user-agent': random.choice(user_agent_list),
            # 'referer': 'https://jable.tv/search/%E6%9C%AC%E5%BA%84/'
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'PHPSESSID=0cv23m2b1aao4j0ejd8lu3q97o; _ga=GA1.1.303687662.1623823577; kt_tcookie=1; asgsc262182=2; kt_ips=103.152.113.48%2C103.152.113.169%2C103.152.113.219%2C103.152.113.96%2C103.152.113.90%2C103.152.113.52; __cf_bm=vpYodyet98dDmvrhfTosLXH2LF.EK8I8tLTR9GJtPeU-1634919841-0-AWuwZRDhbUlrAUA9lIyVJED9PKThrKu3v/OVmLs6LAAYKlSeq7/aa5jQer4ColKFfJiw/CPvAw9B8jkwgWLi2ko=; _ga_1DTX7D4FHE=GS1.1.1634918629.35.1.1634919926.0',
            'pragma': 'no-cache',
            'referer': 'https://jable.tv/search/%E6%9C%AC%E5%BA%84/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text = requests.get(url=url, headers=headers, proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 20:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text(url, acount)
    else:
        return page_text
# url = 'https://jable.tv/videos/stars-330/'
# page_text = get_page_text(url, acount=0)
# if page_text is not None:
#     page_text = page_text.text
#     url_m3u8 = re.compile("hlsUrl = '(.*?)'").findall(page_text)
# print()
if __name__ == '__main__':
    import base64
    a = bytes.decode(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAwAAAADCAYAAACnI+4yAAAAEklEQVR42mP4//8/AymYgeYaABssa5WUTzsyAAAAAElFTkSuQmCC'[:64]),encoding='unicode_escape')
    print()