import requests
import os
import time
import random
import re
from Crypto.Cipher import AES
from UA头 import get_ua_list
from 类库 import get_ts
from concurrent.futures import ThreadPoolExecutor
headers_list = get_ua_list()

def get_cryptor(url_m3u8):
    response = requests.get(url=url_m3u8, headers=random.choice(headers_list))
    m3u8_txt = response.text
    ts_list = []
    url_key = ''
    url_qianzui = ''
    qianZui = url_m3u8.split('/')[-1]
    for line in m3u8_txt.split('\n'):
        if 'URI' in line:
            url_key = url_qianzui + re.compile('URI="(.*)"').findall(line)[0]
        elif 'ts' in line:
            # if qianZui in line:
            #     ts_list.append(url_m3u8+line.replace(qianZui,''))
            # else:
            ts_list.append(url_qianzui + line)
    if len(url_key) == 0:
        return ts_list
    else:
        key_byte = requests.get(url=url_key, headers=random.choice(headers_list)).content
        cryptor = AES.new(key_byte, AES.MODE_CBC)
        return cryptor, ts_list

def download_1(ts_url):
    name_ts = ts_url.split('/')[-1]
    if not os.path.exists('C:\javamost_ts存放区\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content
            ts_open = cryptor.decrypt(ts)
            with open('C:\javamost_ts存放区\\' + name_ts, 'wb') as wt:
                wt.write(ts_open)
                print(name_ts)

def download_2(ts_url):
    name_ts = ts_url.split('/')[-1]
    if not os.path.exists('C:\javamost_ts存放区\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content
            with open('C:\javamost_ts存放区\\' + name_ts, 'wb') as wt:
                wt.write(ts)
                print(name_ts)

if __name__ == '__main__':
    start_time = int(time.time())
    path_and_m3u8_list = []
    while True:
        path_name = r'C:\番号\\' + input('输入影片名(输入完成请直接按回车)：') + '.ts'
        if path_name.split('\\')[-1].replace('.ts','') == '':
            break
        url_m3u8 = input("输入m3u8地址:")
        if url_m3u8 == '':
            break
        path_and_m3u8_list.append(path_name + '##' + url_m3u8)
    for path_and_m3u8 in path_and_m3u8_list:
        path_name = path_and_m3u8.split('##')[0]
        print(path_name)
        url_m3u8 = path_and_m3u8.split('##')[1]
        print(url_m3u8)
        if not os.path.exists(path_name) and not os.path.exists(path_name.replace('.ts','.mp4')) and not os.path.exists(path_name.replace("C",'F')) and not os.path.exists(path_name.replace('.ts','.mp4').replace("C","F")) and not os.path.exists(path_name.replace("C",'G')) and not os.path.exists(path_name.replace('.ts','.mp4').replace("C","G")) :
            list_ts_file = ''
            # url_qianzui = '/'.join(url_m3u8.split('/')[:-1]) + '/'
            # url_qianzui = url_m3u8
            tuple_test = get_cryptor(url_m3u8)
            if len(list(tuple_test)) == 2:
                cryptor, ts_list = get_cryptor(url_m3u8)
                while len(list_ts_file) < len(ts_list):
                    with ThreadPoolExecutor(10) as tp:
                        for ts_url in ts_list:
                            tp.submit(download_1, ts_url)
                        list_ts_file = os.listdir('C:\javamost_ts存放区')
                print('ts下载完成')
            else:
                ts_list = tuple_test
                while len(list_ts_file) < len(ts_list):
                    with ThreadPoolExecutor(10) as tp:
                        for ts_url in ts_list:
                            tp.submit(download_2, ts_url)
                            list_ts_file = os.listdir('C:\javamost_ts存放区')
                print('ts下载完成')
            with open(path_name, 'ab') as ab:
                for i in [j.split('/')[-1] for j in ts_list]:
                    with open('C:\javamost_ts存放区\\' + i, 'rb') as rb:
                        ab.write(rb.read())
                print(path_name + '合并完成')
            for j in ['C:\javamost_ts存放区\\' + i for i in list_ts_file]:
                os.remove(j)
            print('ts删除完成')
            end_time = int(time.time())
            time_all = end_time - start_time
            print('执行时间为：' + str(time_all) + 's')