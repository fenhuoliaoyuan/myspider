import os
import random

import requests
from concurrent.futures import ThreadPoolExecutor
from configTwitter import *

if not os.path.exists(PATH_DIR):
    os.mkdir(PATH_DIR)


class TwitterVideoDownload(object):
    data_list = []

    @staticmethod
    def response(url):
        """
        获取网页
        :param url:
        :return:
        """
        headers = HEADERS
        res = requests.get(url=url, headers=headers)
        return res

    @classmethod
    def parseResponse(cls, response):
        """
        解析response
        :param response:
        :return:
        """
        if response is not None:
            res = response.json()
            try:
                entriesList = res['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']
                for entrie in entriesList:
                    try:
                        legacy = entrie['content']['itemContent']['tweet_results']['result']['legacy']
                        try:
                            videoTitle = legacy['full_text']
                            videoTitle = videoTitle.split('https')[0].replace('\n','')
                            print(videoTitle)
                        except:
                            videoTitle = None
                        try:
                            videoUrl = ''
                            videoUrls = legacy['extended_entities']['media'][0]['video_info']['variants']#[1]['url']
                            videoUrls = [i for i in videoUrls if i['content_type'] == 'video/mp4']
                            videoUrl = videoUrls[0]['url']
                            print(videoUrl)
                            # for row i
                            # n videoUrls:
                            #     if row['content_type'] == 'video/mp4':
                            #         videoUrl = row['url']

                        except:
                            videoUrl = None
                        if videoUrl is not None:
                            data = {
                                'videoTitle': videoTitle,
                                'videoUrl': videoUrl
                            }
                            cls.data_list.append(data)
                    except:
                        pass
            except:
                pass

            return cls.data_list

    @staticmethod
    def saveToFile(data):
        """
        持久化存储
        :param data:
        :return:
        """
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        videoTitle = data['videoTitle']
        videoUrl = data['videoUrl']
        path_mp4 = PATH_DIR + '\\' + videoTitle.replace(':', '_').replace('/', '_').replace('!', '_').replace('?',
                                                                                                              '_').replace(
            '|', '_').replace('*', '_') + '.mp4'
        if not os.path.exists(path_mp4):
            mp4Bytes = requests.get(url=videoUrl, headers=headers)
            if mp4Bytes.status_code == 200:
                with open(path_mp4, 'wb') as wb:
                    wb.write(mp4Bytes.content)
                    print(videoTitle + '下载完成')


def main():
    url_list = []
    while True:
        url = input('输入接口地址（搜索UserMedia）：')
        if len(url) < 1:
            break
        url_list.append(url)
    if len(url_list) > 0:
        res_list = []
        for url in url_list:
            res = TwitterVideoDownload.response(url=url)
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            datasList = []
            for res in res_list:
                datas = TwitterVideoDownload.parseResponse(response=res)
                if datas is not None:
                    datasList.extend(datas)
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                with ThreadPoolExecutor(10) as tp:
                    for data in datasList:
                        tp.submit(TwitterVideoDownload.saveToFile, data)


if __name__ == '__main__':
    main()
