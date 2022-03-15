import requests
import os
import random
from lxml import etree
import re
from Crypto.Cipher import AES
from base64 import b64decode
import 类库
from 类库 import get_ts, get_page_text
from concurrent.futures import ThreadPoolExecutor

url_href_list = []
def get_txt(page):
    # for page in range(1, 658):
    url = 'https://2xingav.com/app/topic/list?start={}&limit=30&type=released&from_cache=true&online_videos=true&s' \
          'ettotop=false&fid=cn'.format((page - 1) * 30)
    page_text = get_page_text(url, acount=0)
    if page_text is not None:
        page_text = page_text.json()
        data_list = page_text['data']['datas']
        for data in data_list:
            title = data['title']
            view_key = data['id']
            url_href = 'https://2xingav.com/video/' + view_key
            if '许晴' in title:
                url_href_list.append(url_href + '  ' + title)
                print(url_href + ' ' + title)

if __name__ == '__main__':
    with ThreadPoolExecutor(40) as tp:
        for page in range(1, 658):
            tp.submit(get_txt,page)
    for i in url_href_list:
        with open('传媒.txt','a',encoding='utf-8') as txt:
            txt.write(i+'\n')
            print(i)
    print('抓取完成')