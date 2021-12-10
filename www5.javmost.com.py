import requests
import os
import random
from lxml import etree
import re
from Crypto.Cipher import AES
from base64 import b64decode
import 类库
from UA头 import get_ua_list
from 类库 import get_ts, get_page_text
from concurrent.futures import ThreadPoolExecutor

from 转码 import fanhao_zhangma

# headers_list = [
#     {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'},
#     {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"},
#     {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"},
#     {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"},
#     {
#         'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"},
#     {
#         'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"},
#     {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
#     {'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
#     {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
# ]
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

            # name_ts = name_ts.split('.')[0]
            ts_open = cryptor.decrypt(ts)
            # dict_ts[name_ts]= ts_open
            with open('C:\javamost_ts存放区\\' + name_ts, 'wb') as wt:
                wt.write(ts_open)
                print(name_ts)
            # with open('./jable_第一个mp4.mp4', 'ab') as fp:
            #     fp.write(ts_open)
            #     print('{}下载成功'.format(name_ts))


def download_2(ts_url):
    name_ts = ts_url.split('/')[-1]
    if not os.path.exists('C:\javamost_ts存放区\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content
            # name_ts = name_ts.split('.')[0]
            # ts_open = cryptor.decrypt(ts)
            # dict_ts[name_ts]= ts_open
            with open('C:\javamost_ts存放区\\' + name_ts, 'wb') as wt:
                wt.write(ts)
                print(name_ts)


if __name__ == '__main__':
    import time

    start_time = int(time.time())
    path_and_m3u8_list = []
    while True:
        path_name = r'G:\番号\\' + input('输入影片名(输入完成请直接按回车)：') + '.ts'
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
    # path_name = r'E:\番号\FSDSS-003 肩負著片商希望的FALENO專屬新人美乃雀AV出道.ts'
    # path_name = r'G:\番号\SW-806黑色连裤袜女员工丰满内衣诱惑 按摩双脚时，敏感的厚桃和臀部的全貌反应出刺痛的感觉。我在等待我的连裤袜被撕破和热的 Ichimotsu 被扔进我的办公室.ts'
        if not os.path.exists(path_name) and not os.path.exists(path_name.replace('F', 'C')) and not os.path.exists \
                    (path_name.replace('E', 'C')) and not os.path.exists(path_name.replace('C', 'F')) and not os.path.exists \
                    (path_name.replace('E', 'F')) and not os.path.exists(path_name.replace('C', 'E')) and not os.path.exists \
                    (path_name.replace('F', 'E')):
            list_ts_file = ''
            # url_m3u8 = 'https://www316.sbcdnvideo.com/hls/tysxes4ab666j6cdacwbbxcso6gkxukxqey264e3inrbhkysqlxefjbsgm7q/index-v1-a1.m3u8'
            # 'https://2xingav.com/video/m3u8/20a770ddca8b5b14dc545e5a2277feb9dddb720a.m3u8?video_server=lacdn'
            # 'https://c.s1c.xyz/videos/20a770ddca8b5b14dc545e5a2277feb9dddb720a/p00015.ts'
            url_qianzui = '/'.join(url_m3u8.split('/')[:-1]) + '/'
            if len(list(get_cryptor(url_m3u8))) == 2:
                cryptor, ts_list = get_cryptor(url_m3u8)
                while len(list_ts_file) < len(ts_list):
                    with ThreadPoolExecutor(10) as tp:
                        for ts_url in ts_list:
                            tp.submit(download_1, ts_url)
                        list_ts_file = os.listdir('C:\javamost_ts存放区')
                print('ts下载完成')
            else:
                ts_list = get_cryptor(url_m3u8)
                while len(list_ts_file) < len(ts_list):
                    with ThreadPoolExecutor(10) as tp:
                        for ts_url in ts_list:
                            tp.submit(download_2, ts_url)
                            list_ts_file = os.listdir('C:\javamost_ts存放区')
                print('ts下载完成')
            # dict_ts = sorted(dict_ts)
            # with open('第一个MP4.mp4','ab') as rb:
            #     for i in dict_ts:
            #         rb.write(dict_ts[i])
            #         print(i+'写入成功')
            # list_ts_file = os.listdir('./测试')
            with open(path_name, 'ab') as ab:
                for i in [j.replace(url_qianzui, '') for j in ts_list]:
                    with open('C:\javamost_ts存放区\\' + i, 'rb') as rb:
                        ab.write(rb.read())
                print(path_name + '合并完成')
            # with open(path_name, 'ab') as ab:
            #     for i in sorted([int(i.split('.')[0]) for i in list_ts_file]):
            #         with open('C:\javamost_ts存放区\\' + str(i) + '.ts', 'rb') as rb:
            #             ab.write(rb.read())
            #     print(path_name+'合并完成')
            for j in ['C:\javamost_ts存放区\\' + i for i in list_ts_file]:
                # print(j)
                os.remove(j)
            print('ts删除完成')
            # fanhao_zhangma("E:\番号")
            # fanhao_zhangma("C:\番号")
            # fanhao_zhangma("F:\番号")
            # fanhao_zhangma("G:\番号")
            end_time = int(time.time())
            time_all = end_time - start_time
            print('执行时间为：' + str(time_all) + 's')
            from smtplib邮件通知 import my_send_email
            my_send_email("标题：91porn用户视频更新",
                          "<h1>更新视频：<br>{}".join(path_name.split('\\')[-1].replace(".ts",'')),
                          "2319423737@qq.com",
                          "2319423737@qq.com", )
            print('更新完成,邮件发送完成，等待八个小时继续更新...')