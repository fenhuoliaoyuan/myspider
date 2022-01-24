import json
import os
import random
from urllib.parse import quote
import requests
from concurrent.futures import ThreadPoolExecutor
from configTwitter import *


# class TwitterPhotosDownload(object):
#     
video_updates = []
class TwitterMediaDownload(object):
    data_list = []

    @staticmethod
    def get_user_tweets(user_id, count=2000):
        """获取指定用户的指定数量的推文信息."""
        params = {
            'userId': user_id,
            'count': count,
            'withTweetQuoteCount': True,
            'includePromotedContent': True,
            'withSuperFollowsUserFields': True,
            'withUserResults': True,
            'withBirdwatchPivots': True,
            'withReactionsMetadata': True,
            'withReactionsPerspective': True,
            'withSuperFollowsTweetFields': True,
            'withVoice': True,
        }
        url = f'https://twitter.com/i/api/graphql/Qg0jD2d__FhsMB48vKFKUQ/UserTweets?variables={quote(json.dumps(params, separators=(",", ":")))}'
        return url

    @staticmethod
    def response(url):
        """
        获取网页
        :param url:
        :return:
        """
        headers = HEADERS
        try:
            res = requests.get(url=url, headers=headers)
        except:
            print('response错误')
            return
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
            try:
                entriesList = res['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']
                for entrie in entriesList:
                    try:
                        legacy = entrie['content']['itemContent']['tweet_results']['result']['legacy']
                        try:
                            photoTitle_ = legacy['full_text']
                            photoTitle = photoTitle_.split('https')[0].replace('\n', '')
                            if len(photoTitle) < 1:
                                photoTitle = photoTitle_.split('/')[-1].replace('\n', '')
                            print(photoTitle)
                        except:
                            photoTitle = None
                        try:
                            photoUrls = legacy['entities']['media']
                            # photoUrl = legacy['entities']['media'][0]['media_url_https']
                        except:
                            photoUrls = None
                        if len(photoTitle) > 0 and len(photoUrls) > 0:
                            if len(photoUrls) > 1:
                                for i in photoUrls:
                                    photoUrl = i['media_url_https']
                                    photoTitle = photoTitle + ' ' + photoUrl.split('/')[-1].replace('.jpg', '')
                                    data = {
                                        'photoTitle': photoTitle,
                                        'photoUrl': photoUrl
                                    }
                                    cls.data_list.append(data)
                                    photoTitle = photoTitle.replace(' ' + photoUrl.split('/')[-1].replace('.jpg', ''),
                                                                    '')
                            else:
                                photoUrl = photoUrls[0]['media_url_https']
                                data = {
                                    'photoTitle': photoTitle,
                                    'photoUrl': photoUrl
                                }
                                cls.data_list.append(data)

                    except:
                        pass
                return cls.data_list
            except:
                pass

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
        path_user = data['path_user']
        if 'videoUrl' in data.keys():
            videoTitle = data['videoTitle']
            videoUrl = data['videoUrl']
            path_mp4 = path_user + '\\' + 'Videos' + '\\' + videoTitle.replace(':', '_').replace('/', '_').replace('!',
                                                                                                                   '_').replace(
                '?', '_').replace('|', '_').replace('*', '_') + '.mp4'
            if not os.path.exists(path_mp4):
                mp4Bytes = requests.get(url=videoUrl, headers=headers)
                if mp4Bytes.status_code == 200:
                    with open(path_mp4, 'wb') as wb:
                        wb.write(mp4Bytes.content)
                        video_updates.append(path_mp4)
                        print(videoTitle + '.mp4' + '下载完成')
        elif 'photoTitle' in data.keys():
            photoTitle = data['photoTitle']
            photoUrl = data['photoUrl']
            path_jpg = path_user + '\\' + 'Photos' + '\\' + photoTitle.replace(':', '_').replace('/', '_').replace('!',
                                                                                                                   '_').replace(
                '?', '_').replace('|', '_').replace('*', '_') + '.jpg'
            if not os.path.exists(path_jpg):
                jpgBytes = requests.get(url=photoUrl, headers=headers)
                if jpgBytes.status_code == 200:
                    with open(path_jpg, 'wb') as wb:
                        wb.write(jpgBytes.content)
                        print(photoTitle + '.jpg' + '下载完成')


def downloadInf(user_id, path_user):
    if not os.path.exists(path_user):
        os.mkdir(path_user)
    if not os.path.exists(path_user + '\\' + 'Videos'):
        os.mkdir(path_user + '\\' + 'Videos')
    if not os.path.exists(path_user + '\\' + 'Photos'):
        os.mkdir(path_user + '\\' + 'Photos')
    url_list = []
    res_list = []
    for count in range(1, 2001, 200):
        url = TwitterMediaDownload.get_user_tweets(user_id=user_id, count=count)
        if url is not None:
            url_list.append(url)

    if len(url_list) > 0:
        for url in url_list:
            res = TwitterMediaDownload.response(url=url)
            if res is not None:
                if res.status_code == 200:
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
                # 插入路径
                for i in datasList:
                    i['path_user'] = path_user
                print("抓取的视频/图片列表长度：" + str(len(datasList)))
                print('开始下载视频/图片>>>')
                with ThreadPoolExecutor(10) as tp:
                    for data in datasList:
                        tp.submit(TwitterMediaDownload.saveToFile, data)


def update():
    path_list = [PATH_DIR + '\\' + i for i in os.listdir(PATH_DIR)]
    for row in path_list:
        if '@' in row:
            TwitterMediaDownload.data_list = []
            user_id = row.split('@')[-1]
            path_user = row
            print('更新'+path_user.split('\\')[-1].split('@')[0])
            downloadInf(user_id=user_id, path_user=path_user)


def add_user():
    user_id = input('输入用户id：')
    path_user = PATH_DIR + '\\' + input('输入用户名：') + '@'+user_id
    downloadInf(user_id=user_id,path_user=path_user)
def main():
    while True:
        num = input('选择添加目标用户请输入1\n选择更新已有用户视频请输入2\n选择退出请输入q\n')
        if num == '1':
            add_user()
        elif num == '2':
            update()
        elif num == 'q':
            break
        else:
            print('输入错误，请重新输入\n')



if __name__ == '__main__':
    main()
    print(len(video_updates))
    for i in video_updates:
        print(i)
