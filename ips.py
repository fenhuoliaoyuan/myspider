import requests
from lxml import etree
import time
import random
from 爬虫小项目 import config

user_agent_list = config.get_ua()
headers = {
            'user-agent': random.choice(user_agent_list)
        }
url = ['https://www.baidu.com','https://www.sogou.com','https://www.so.com',]
ip_list = config.conn_ip.smembers('ip_proxies')
ip_list__ = []
for ip_ in ip_list:
    ip = {'http' : bytes.decode(ip_)}
    # print(ip)
    ip_list__.append(ip)
for ip__ in ip_list__:
    try:
        status = requests.get(url=random.choice(url),headers=headers,proxies=ip__,timeout=1)
    except:
        # config.conn_ip.srem('ip_proxies',ip__['http'])
        print('无用ip--{}'.format(ip__['http']))
    else:
        print('优质ip--{}'.format(ip__['http']))
        config.conn_ip.sadd('ip_proxies_good', ip__['http'])
