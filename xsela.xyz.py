import requests
import os
import random
from lxml import etree
import re
from Crypto.Cipher import AES
from base64 import b64decode

from tqdm import tqdm

import 类库
from UA头 import get_ua_list
from 类库 import get_ts, get_page_text
from concurrent.futures import ThreadPoolExecutor
from 转码 import fanhao_zhangma
headers_list = get_ua_list()

def get_cryptor(url_m3u8):
    # url_m3u8 = 'https://kingdom-b.alonestreaming.com/hls/LABUvA1N2MSC7uTh8Fi1Pg/1634916782/16000/16665/16665.m3u8'
    response = requests.get(url=url_m3u8, headers=random.choice(headers_list))
    m3u8_txt = response.text
    # print()
    ts_list = []
    url_key = ''
    for line in m3u8_txt.split('\n'):
        # print(line)
        if 'URI' in line:
            url_key = url_qianzui + re.compile('URI="(.*)"').findall(line)[0]
            # iv = b64decode(re.compile('IV=(.*)').findall(line)[0])
            # print(url_key)
        elif 'ts' in line:
            ts_list.append(url_qianzui + line)
        elif '.ttf' in line:
            ts_list.append(url_qianzui + line)
    if len(url_key) == 0:
        return ts_list
    else:
        key_byte = requests.get(url=url_key, headers=random.choice(headers_list)).content
        cryptor = AES.new(key_byte, AES.MODE_CBC)
        return cryptor, ts_list


def download_1(ts_url):
    name_ts = ts_url.split('/')[-1].replace('.ttf','.ts')
    if not os.path.exists(pathTsRoot+'\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content

            # name_ts = name_ts.split('.')[0]
            ts_open = cryptor.decrypt(ts)
            # dict_ts[name_ts]= ts_open
            with open(pathTsRoot+'\\' + name_ts, 'wb') as wt:
                wt.write(ts_open)
                # print(name_ts)
            tq.update(1)
            # with open('./jable_第一个mp4.mp4', 'ab') as fp:
            #     fp.write(ts_open)
            #     print('{}下载成功'.format(name_ts))
    else:
        tq.update(1)

def download_2(ts_url):
    name_ts = ts_url.split('/')[-1].replace('.ttf','.ts')
    if not os.path.exists(pathTsRoot+'\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content
            # name_ts = name_ts.split('.')[0]
            # ts_open = cryptor.decrypt(ts)
            # dict_ts[name_ts]= ts_open
            with open(pathTsRoot+'\\'+ name_ts, 'wb') as wt:
                wt.write(ts)
                # print(name_ts)
                tq.update(1)
    else:
        tq.update(1)
from 类库 import ips,user_agent_list
def get_page_text_m3u8(url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            'referer': '{}'.format(yuMing)+'/'
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
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_m3u8(url, acount)
    else:
        return page_text

if __name__ == '__main__':
    import time

    start_time = int(time.time())
    yuMing = 'https://xsela.xyz'
    pathTsRoot = 'C:\\ts\\xsela_xyz'
    path_root = 'D:\hhh\\国产\\Alleys'
    # path_name = r'E:\番号\FSDSS-003 肩負著片商希望的FALENO專屬新人美乃雀AV出道.ts'
    for page in range(1,4):
        url_search = 'https://xsela.xyz/search/videos/Alleys?page={}'.format(page)
        page_text_ = get_page_text(url_search,acount=0)
        if page_text_ is not None:
            page_text_ = page_text_.text
            tree = etree.HTML(page_text_)
            article_list = tree.xpath('//div[@class="content-info"]')
            for row in article_list:
                url = yuMing+row.xpath('./a/@href')[0]
                title = row.xpath('./a/span/text()')[0]

                if not os.path.exists(path_root):
                    os.mkdir(path_root)
                path_name = path_root+'\\'+ title.replace('!','').replace('/','_').replace('?','').replace('.','').replace(':','') +'.ts'
                if not os.path.exists(path_name) and not os.path.exists(path_name.replace('.ts','.mp4')):
                    list_ts_file = ''
                    print(title+'开始下载')
                    # url = 'https://madou.club/mmz038-%e7%88%b1%e4%b8%8a%e9%99%aa%e7%8e%a9%e5%b0%8f%e5%a7%90%e5%a7%90-%e9%9a%be%e4%bb%a5%e5%8e%8b%e6%8a%91%e7%9a%84%e6%80%a7%e6%ac%b2%e6%82%b8%e5%8a%a8.html'
                    page_text = get_page_text(url=url,acount=0)
                    if page_text is not None:
                        page_text = page_text.text
                        iframe_url = yuMing + re.compile('src=\"(/importer/video_player\.php.*?)\"').findall(page_text)[0]
                        page_text_iframe = get_page_text(iframe_url,acount=0)
                        if page_text_iframe is not None:
                            page_text_iframe = page_text_iframe.text
                        # token = re.compile('var token = \"(.*?)\";').findall(page_text)[0]
                            url_m3u8= re.compile('https?.*?.m3u8').findall(page_text_iframe)[-1]
                            # url_m3u8 = yuMing + m3u8_ + '?' + 'token={}'.format(token)
                            print(url_m3u8)
                            # url_m3u8 = 'https://dash.madou.club/videos/61ad9038ac9edb19a57a752a/index.m3u8?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJ2aWV3IiwiaWF0IjoxNjM5MjczMTg2LCJleHAiOjE2MzkyNzMyODZ9.P0kmIlG6Fqkb782huuXNF0T1SnbqRaQ3r1BYFbA3r4c'
                            # 'https://2xingav.com/video/m3u8/20a770ddca8b5b14dc545e5a2277feb9dddb720a.m3u8?video_server=lacdn'
                            # 'https://c.s1c.xyz/videos/20a770ddca8b5b14dc545e5a2277feb9dddb720a/p00015.ts'
                            # url_qianzui = '/'.join(url_m3u8.split('/')[:-1]) + '/'
                            url_qianzui = ''
                            tuple_test = get_cryptor(url_m3u8)
                            if len(list(tuple_test)) == 2:
                                cryptor, ts_list = tuple_test
                                # tq = tqdm(total=len(ts_list))
                                ts_list = [yuMing + '/'.join(url_m3u8.split('/')[:-1]) + '/' + i for i in
                                           ts_list]
                                tq = tqdm(total=len(ts_list))
                                while len(list_ts_file) < len(ts_list):
                                    with ThreadPoolExecutor(10) as tp:
                                        for ts_url in ts_list:
                                            tp.submit(download_1, ts_url)
                                        list_ts_file = os.listdir(pathTsRoot)
                                tq.close()
                                print('ts下载完成')
                            else:
                                ts_list = tuple_test
                                ts_list = ['/'.join(url_m3u8.split('/')[:-1]) + '/' + i.split('/')[-1] for i in
                                           ts_list]
                                tq = tqdm(total=len(ts_list))
                                while len(list_ts_file) < len(ts_list):
                                    with ThreadPoolExecutor(10) as tp:
                                        for ts_url in ts_list:
                                            tp.submit(download_2, ts_url)
                                            list_ts_file = os.listdir(pathTsRoot)
                                tq.close()
                                print('ts下载完成')
                            # dict_ts = sorted(dict_ts)
                            # with open('第一个MP4.mp4','ab') as rb:
                            #     for i in dict_ts:
                            #         rb.write(dict_ts[i])
                            #         print(i+'写入成功')
                            # list_ts_file = os.listdir('./测试')
                            with open(path_name, 'ab') as ab:
                                for i in [j.split('/')[-1].replace('.ttf','.ts') for j in ts_list]:
                                    with open(pathTsRoot+'\\' + i, 'rb') as rb:
                                        ab.write(rb.read())
                                print(path_name + '合并完成')
                            for j in [pathTsRoot+'\\' + i for i in list_ts_file]:
                                # print(j)
                                os.remove(j)
                            print('ts删除完成')

                            end_time = int(time.time())
                            time_all = end_time - start_time
                            print('执行时间为：' + str(time_all) + 's')
    fanhao_zhangma(path_root)
    end_time = int(time.time())
    time_all = end_time - start_time
    print('执行时间为：' + str(time_all) + 's')