import random
from pprint import pprint
import os
from configXvideo import *
import requests
import re

def get_ips():
    with open('ips.txt', 'r', encoding='utf-8') as rd:
        ips = []
        for line in [i.replace('\n', '') for i in rd.readlines()]:
            ip = {
                'http': 'http://' + line,
                # 'https': 'http://' + line
            }
            ips.append(ip)
        # pprint(ips)
        return ips


ips = get_ips()


def get_ts(url_ts_, acount):
    try:
        proxies = random.choice(ips)
        if 'delivery' in url_ts_:
            Host = re.compile('(delivery.*?)/hls').findall(url_ts_)[0]
            headers = {
                'Accept': '*/*',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': Host,
                'Origin': 'https://mm9844.cc',
                'Pragma': 'no-cache',
                'Referer': 'https://mm9844.cc/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            }
        else:
            headers = {
                'user-agent': random.choice(user_agent_list)
            }
        ts = requests.get(url=url_ts_, headers=headers, proxies=proxies)
        if ts.status_code != 200:
            raise ValueError
    except:
        if acount == 10:
            return
        acount += 1
        get_ts(url_ts_, acount)
    else:
        return ts


path_ffmpeg = r'C:\软件安装\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\bin'


def fanhao_zhangma(path_dir):
    os.chdir(path_ffmpeg)
    list_file = os.listdir(path_dir)
    list_ts = [path_dir + "\\" + i for i in list_file if ".ts" in i]
    for path_ts in list_ts:
        # print(path_ts)
        if os.path.exists(path_ts) and os.path.exists(path_ts.replace(".ts", ".mp4")):
            os.remove(path_ts)
            print("{}已存在，删除ts".format(path_ts.replace(".ts", ".mp4")))
        elif os.path.exists(path_ts) and not os.path.exists(path_ts.replace(".ts", ".mp4")):
            os.system("ffmpeg -i \"{}\" -acodec copy -vcodec copy -f mp4 \"{}\"".
                      format(path_ts, path_ts.replace(".ts", '.mp4')))
            if os.path.exists(path_ts.replace(".ts", '.mp4')) and os.path.exists(path_ts):
                os.remove(path_ts)
                print("文件{}转换成mp4完成，删除ts完成".format(path_ts))
