import os
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm import tqdm
from configkuaishou import *
PATH_DIR = r'G:\ghs\快手'
"""
快手用户视频批量下载爬虫
"""

class KuaiShou(object):
    datas = []
    pcursor = ''
    author = ''

    @classmethod
    def get_datas(cls, userId):
        try:
            headers = {
                'Host': 'www.kuaishou.com',
                'Connection': 'keep-alive',
                'Content-Length': '1307',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                'accept': '*/*',
                'content-type': 'application/json',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
                'Origin': 'https://www.kuaishou.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.kuaishou.com/profile/3xvkvcwvfa99g7k',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                'Cookie': 'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_a18c0e8ee3c39bed0d44da966df2afa4',
            }
            json_dict = {
                "operationName": "visionProfilePhotoList",
                "variables": {
                    "userId": userId,
                    "pcursor": cls.pcursor,
                    "page": "profile"
                },
                "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        profileUserTopPhoto\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"
            }
            url = 'https://www.kuaishou.com/graphql'
            res = requests.post(url=url, headers=headers, json=json_dict)

            if res.status_code == 200:
                json_data = res.json()
                # data.visionProfilePhotoList.feeds
                feeds = json_data['data']['visionProfilePhotoList']['feeds']
                # data.visionProfilePhotoList.feeds[0].photo.photoUrls[0]
                for feed in feeds:
                    photoUrl = feed['photo']['photoUrls']
                    # data.visionProfilePhotoList.feeds[0].photo.caption
                    caption = feed['photo']['caption']
                    if len(photoUrl) > 0 and len(caption) > 0:
                        data = {
                            'photoUrl': photoUrl[0]['url'],
                            'caption': caption
                        }
                        cls.datas.append(data)
                # data.visionProfilePhotoList.pcursor
                cls.pcursor = json_data['data']['visionProfilePhotoList']['pcursor']
                # data.visionProfilePhotoList.feeds[0].author
                try:
                    cls.author = json_data['data']['visionProfilePhotoList']['feeds'][0]['author']['name']
                except:
                    pass
                if cls.pcursor != 'no_more':
                    cls.get_datas(userId=userId)
        except:
            pass

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


def createDir(PATH_DIR):
    pathList = PATH_DIR.split('\\')
    path_dir = ''
    for i in range(0, len(pathList)):
        if i == 0:
            path_dir = pathList[0]
        else:
            path_dir = path_dir + '\\' + pathList[i]
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)


def downloadKuaishou():
    URL = input('输入链接：')
    userId = URL.split('/')[-1]
    KuaiShou.get_datas(userId=userId)
    path_dir = PATH_DIR + '\\' + KuaiShou.author + '@' + userId
    createDir(path_dir)

    def downloadMp4(data, acount=0):
        url = data['photoUrl']
        dst = path_dir + '\\' + data['caption'].replace(':', ' ').replace('/', ' ').replace('!', ' ').replace('?',' ').replace('|', ' ').replace('*', ' ').replace('\n', '').replace('.', ' ') + '.mp4'
        if not os.path.exists(dst):
            try:
                proxies = random.choice(ips)
                headers = {
                    'user-agent': random.choice(user_agent_list)
                }
                ts = requests.get(url=url, headers=headers, proxies=proxies)
                if ts.status_code != 200:
                    raise ValueError
            except:
                if acount == 10:
                    return
                acount += 1
                downloadMp4(data, acount)
            else:
                with open(dst, 'wb') as wb:
                    wb.write(ts.content)
                    print(data['caption'] + '.mp4' + '下载完成')

    # def saveToFile(data):
    #     """mp4下载"""
    #     # proxies = random.choice(ips)
    #     url = data['photoUrl']
    #     dst = path_dir + '\\' + data['caption'].replace(':', ' ').replace('/', ' ').replace('!', ' ').replace('?',
    #                                                                                                           ' ').replace(
    #         '|', ' ').replace('*', ' ').replace('\n', '').replace('.', ' ') + '.mp4'
    #     # 设置stream=True参数读取大文件
    #     response = requests.get(url, stream=True)
    #     # 通过header的content-length属性可以获取文件的总容量
    #     file_size = int(response.headers['content-length'])
    #     if os.path.exists(dst):
    #         # 获取本地已经下载的部分文件的容量，方便继续下载，如果不存在就从头开始下载。
    #         first_byte = os.path.getsize(dst)
    #     else:
    #         first_byte = 0
    #     # 如果大于或者等于则表示已经下载完成，否则继续
    #     if first_byte >= file_size:
    #         return file_size
    #     header = {"Range": f"bytes={first_byte}-{file_size}"}
    #
    #     pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
    #     req = requests.get(url, headers=header, stream=True)
    #     with open(dst, 'ab') as f:
    #         # 每次读取一个1024个字节
    #         for chunk in req.iter_content(chunk_size=1024):
    #             if chunk:
    #                 f.write(chunk)
    #                 pbar.update(1024)
    #     pbar.close()
    #     return file_size

    # print(KuaiShou.datas)
    # dict的去重
    KuaiShou.datas = [dict(t) for t in set([tuple(d.items()) for d in KuaiShou.datas])]
    print('用户名：' + KuaiShou.author)
    print("抓取的视频长度：" + str(len(KuaiShou.datas)))
    print('开始下载视频>>>')
    with ThreadPoolExecutor(5) as tp:
        for data in KuaiShou.datas:
            tp.submit(downloadMp4, data)


if __name__ == '__main__':
    # URL = input('输入链接：')
    # userId = URL.split('/')[-1]
    # KuaiShou.get_datas(userId=userId)
    # print(KuaiShou.datas)
    downloadKuaishou()
