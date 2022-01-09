import os
import random

import requests
from concurrent.futures import ThreadPoolExecutor
from configTwitter import *

if not os.path.exists(PATH_DIR):
    os.mkdir(PATH_DIR)
if not os.path.exists(PATH_DIR + '\\' + 'Videos'):
    os.mkdir(PATH_DIR + '\\' + 'Videos')
if not os.path.exists(PATH_DIR + '\\' + 'Photos'):
    os.mkdir(PATH_DIR + '\\' + 'Photos')


# class TwitterPhotosDownload(object):
#     

class TwitterMediaDownload(object):
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
    def parseOfVideo(cls, response):
        """
        解析视频
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
                            videoTitle = videoTitle.split('https')[0].replace('\n', '')
                            print(videoTitle)
                        except:
                            videoTitle = None
                        try:
                            videoUrl = ''
                            videoUrls = legacy['extended_entities']['media'][0]['video_info']['variants']  # [1]['url']
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

    @classmethod
    def parseOfPhotos(cls, response):
        """
        解析图片
        :param response:
        :return:
        """
        if response is not None:
            res = response.json()
            entriesList = res['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']
            for entrie in entriesList:
                try:
                    legacy = entrie['content']['itemContent']['tweet_results']['result']['legacy']
                    try:
                        photoTitle_ = legacy['full_text']
                        photoTitle = photoTitle_.split('https')[0].replace('\n', '')
                        print(photoTitle)
                        if len(photoTitle) < 1:
                            photoTitle = photoTitle_.split('/')[-1].replace('\n', '')
                    except:
                        photoTitle = None
                    try:
                        photoUrl = legacy['entities']['media'][0]['media_url_https']
                    except:
                        photoUrl = None
                    if len(photoTitle) > 0 and len(photoUrl) > 0:
                        data = {
                            'photoTitle': photoTitle,
                            'photoUrl': photoUrl
                        }
                        cls.data_list.append(data)

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
        if 'videoTitle' in data.keys():
            videoTitle = data['videoTitle']
            videoUrl = data['videoUrl']
            path_mp4 = PATH_DIR + '\\' + 'Videos' + '\\' + + videoTitle.replace(':', '_').replace('/', '_').replace('!',
                                                                                                                    '_').replace(
                '?', '|', '_').replace('*', '_') + '.mp4'
            if not os.path.exists(path_mp4):
                mp4Bytes = requests.get(url=videoUrl, headers=headers)
                if mp4Bytes.status_code == 200:
                    with open(path_mp4, 'wb') as wb:
                        wb.write(mp4Bytes.content)
                        print(videoTitle + '.mp4' + '下载完成')
        elif 'photoTitle' in data.keys():
            photoTitle = data['photoTitle']
            photoUrl = data['photoUrl']
            path_jpg = PATH_DIR + '\\' + 'Photos' + '\\' + photoTitle.replace(':', '_').replace('/', '_').replace('!',
                                                                                                                  '_').replace(
                '?', '_').replace('|', '_').replace('*', '_') + '.jpg'
            if not os.path.exists(path_jpg):
                jpgBytes = requests.get(url=photoUrl, headers=headers)
                if jpgBytes.status_code == 200:
                    with open(path_jpg, 'wb') as wb:
                        wb.write(jpgBytes.content)
                        print(photoTitle + '.jpg' + '下载完成')


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
            res = TwitterMediaDownload.response(url=url)
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            datasList = []
            for res in res_list:
                datasVideo = TwitterMediaDownload.parseOfVideo(response=res)
                if datasVideo is not None:
                    datasList.extend(datasVideo)
                datasPhoto = TwitterMediaDownload.parseOfPhotos(response=res)
                if datasPhoto is not None:
                    datasList.extend(datasPhoto)
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                print("抓取的视频/图片列表长度：" + str(len(datasList)))
                print('开始下载视频/图片>>>')
                with ThreadPoolExecutor(10) as tp:
                    for data in datasList:
                        tp.submit(TwitterMediaDownload.saveToFile, data)


if __name__ == '__main__':
    main()
