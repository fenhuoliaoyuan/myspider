import json
import os
import pprint
import random
from urllib.parse import quote
import requests
from concurrent.futures import ThreadPoolExecutor
from configTwitter import *

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
            'withVoice': True
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
                entriesList = res['data']['user']['result']['timeline']['timeline']['instructions'][1]['entries']
                for entrie in entriesList:
                    try:
                        legacy = entrie['content']['itemContent']['tweet_results']['result']['legacy']
                        try:
                            videoTitle = legacy['full_text']
                            videoTitle = videoTitle.split('https')[0].replace('\n', '')
                            # print(videoTitle)
                        except:
                            videoTitle = None
                        try:
                            videoUrl = ''
                            videoUrls = legacy['extended_entities']['media'][0]['video_info']['variants']  # [1]['url']
                            videoUrls = [i for i in videoUrls if i['content_type'] == 'video/mp4']
                            videoUrls = sorted(videoUrls, key=lambda e: e['bitrate'], reverse=True)
                            videoUrl = videoUrls[0]['url']
                            # print(videoUrl)
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
                entriesList = res['data']['user']['result']['timeline']['timeline']['instructions'][1]['entries']
                for entrie in entriesList:
                    try:
                        legacy = entrie['content']['itemContent']['tweet_results']['result']['legacy']
                        try:
                            photoTitle_ = legacy['full_text']
                            photoTitle = photoTitle_.split('https')[0].replace('\n', '')
                            if len(photoTitle) < 1:
                                photoTitle = photoTitle_.split('/')[-1].replace('\n', '')
                            # print(photoTitle)
                        except:
                            photoTitle = None
                        try:
                            # photoUrls = legacy['entities']['media']
                            # 使用extended_entities更好些
                            photoUrls = legacy['extended_entities']['media']
                            # photoUrl = legacy['entities']['media'][0]['media_url_https']
                        except:
                            photoUrls = None
                        if len(photoTitle) > 0 and len(photoUrls) > 0:
                            if len(photoUrls) > 1:
                                for i in photoUrls:
                                    # 排除抓取到视频封面的情况
                                    keys = list(i.keys())
                                    if 'video_info' not in keys:
                                        photoUrl = i['media_url_https']
                                        photoTitle = photoTitle + ' ' + photoUrl.split('/')[-1].replace('.jpg', '')
                                        data = {
                                            'photoTitle': photoTitle,
                                            'photoUrl': photoUrl
                                        }
                                        cls.data_list.append(data)
                                        photoTitle = photoTitle.replace(
                                            ' ' + photoUrl.split('/')[-1].replace('.jpg', ''),
                                            '')
                            else:
                                if 'video_info' not in list(photoUrls[0].keys()):
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
            path_mp4 = path_user + '\\' + 'Videos' + '\\' + format_str(videoTitle) + '.mp4'
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
            # if photoUrl.split('.')[-1] == 'jpg':
            path_jpg = path_user + '\\' + 'Photos' + '\\' + format_str(photoTitle) + '.jpg'
            # gif动图地址传递过来时是MP4
            # elif photoUrl.split('.')[-1] == 'gif':
            #     path_jpg = path_user + '\\' + 'Photos' + '\\' + format_str(photoTitle) + '.gif'
            if not os.path.exists(path_jpg):
                jpgBytes = requests.get(url=photoUrl, headers=headers)
                if jpgBytes.status_code == 200:
                    with open(path_jpg, 'wb') as wb:
                        wb.write(jpgBytes.content)
                        print(photoTitle + '.' + photoUrl.split('.')[-1] + '下载完成')


def format_str(str_mabge):
    return str_mabge.replace('.', ' ').replace('?', ' ').replace('\n', ' ').replace('|', ' ').replace(':', ' ').replace(
        '!', ' ').replace('/', ' ').replace('\\', ' ').replace('*', ' ').replace('<', ' ').replace('>', ' ').strip()


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
            print('更新' + path_user.split('\\')[-1].split('@')[0])
            downloadInf(user_id=user_id, path_user=path_user)


def updateOneOf():
    userlist = []
    while True:
        user_name = format_str(input('例如：REDZ-PMV,不输入请回车\n输入用户名：'))
        if len(user_name) > 0:
            userlist.append(user_name)
        else:
            break
    for user_name in userlist:
        file = [i for i in os.listdir(PATH_DIR) if user_name in i]
        if len(file) > 0:
            file = file[0]
            if '@' in file:
                user_id = file.split('@')[-1]
                path_user = PATH_DIR + '\\' + file
                TwitterMediaDownload.data_list = []
                downloadInf(user_id=user_id, path_user=path_user)


def add_user():
    userData = []
    while True:
        user_id = input('例如：1093330681764212737,不输入请回车\n输入用户id：')
        user_name = format_str(input('例如：REDZ-PMV,不输入请回车\n输入用户名：'))
        if len(user_name) > 0 and len(user_id) > 0:
            data = {
                'user_id': user_id,
                'user_name': user_name
            }
            userData.append(data)
        else:
            break
    if len(userData) > 0:
        for data in userData:
            user_id = data['user_id']
            user_name = data['user_name']
            path_user = PATH_DIR + '\\' + user_name + '@' + user_id
            TwitterMediaDownload.data_list = []
            downloadInf(user_id=user_id, path_user=path_user)

def parse_legacy(legacy):
    datasList = []
    try:
        videoTitle = legacy['full_text']
        videoTitle = videoTitle.split('https')[0].replace('\n', '')
        # print(videoTitle)
    except:
        videoTitle = None
    try:
        videoUrl = ''
        videoUrls = legacy['extended_entities']['media'][0]['video_info']['variants']  # [1]['url']
        videoUrls = [i for i in videoUrls if i['content_type'] == 'video/mp4']
        videoUrls = sorted(videoUrls, key=lambda e: e['bitrate'], reverse=True)
        videoUrl = videoUrls[0]['url']
        # print(videoUrl)
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
        datasList.append(data)

    ##########################################################
    try:
        photoTitle_ = legacy['full_text']
        photoTitle = photoTitle_.split('https')[0].replace('\n', '')
        if len(photoTitle) < 1:
            photoTitle = photoTitle_.split('/')[-1].replace('\n', '')
        # print(photoTitle)
    except:
        photoTitle = None
    try:
        # photoUrls = legacy['entities']['media']
        # 使用extended_entities更好些
        photoUrls = legacy['extended_entities']['media']
        # photoUrl = legacy['entities']['media'][0]['media_url_https']
    except:
        photoUrls = None
    if len(photoTitle) > 0 and len(photoUrls) > 0:
        if len(photoUrls) > 1:
            for i in photoUrls:
                # 排除抓取到视频封面的情况
                keys = list(i.keys())
                if 'video_info' not in keys:
                    photoUrl = i['media_url_https']
                    photoTitle = photoTitle + ' ' + photoUrl.split('/')[-1].replace('.jpg', '')
                    data = {
                        'photoTitle': photoTitle,
                        'photoUrl': photoUrl
                    }
                    datasList.append(data)
                    photoTitle = photoTitle.replace(
                        ' ' + photoUrl.split('/')[-1].replace('.jpg', ''),
                        '')
        else:
            if 'video_info' not in list(photoUrls[0].keys()):
                photoUrl = photoUrls[0]['media_url_https']
                data = {
                    'photoTitle': photoTitle,
                    'photoUrl': photoUrl
                }
                datasList.append(data)
    return datasList
def download_one():
    url = input('输入你要下载的视频或图片所在网页地址：')
    path_user = input('输入你的存储目录：')
    focalTweetId = url.split('/')[-1]
    params_detail = {"focalTweetId": focalTweetId,
                     "with_rux_injections": False,
                     "includePromotedContent": True,
                     "withCommunity": True,
                     "withQuickPromoteEligibilityTweetFields": True,
                     "withBirdwatchNotes": False,
                     "withSuperFollowsUserFields": True,
                     "withDownvotePerspective": False,
                     "withReactionsMetadata": False,
                     "withReactionsPerspective": False,
                     "withSuperFollowsTweetFields": True,
                     "withVoice": True,
                     "withV2Timeline": True,
                     "__fs_dont_mention_me_view_api_enabled": True,
                     "__fs_interactive_text_enabled": True,
                     "__fs_responsive_web_uc_gql_enabled": False}

    url_detail_inf = f'https://twitter.com/i/api/graphql/x67pmns2hNpQZHBOHuGBBQ/TweetDetail?variables={quote(json.dumps(params_detail, separators=(",", ":")))}'
    headers = {
        'accept': '*/*',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'cookie': 'kdt=SNua313K5dXV5Tpj0hmADRf5AK1AgaM7vBItF02t; remember_checked_on=1; guest_id_marketing=v1%3A162211230601704388; guest_id_ads=v1%3A162211230601704388; lang=zh-cn; dnt=1; personalization_id="v1_vgqD3xek7JXRMdh0TemIlw=="; guest_id=v1%3A164653051595729144; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLju3Vx%252FAToMY3NyZl9p%250AZCIlYTYzZjExM2U2MjdkMGY5NzMxYWIwYTA5ODE5NmUwMTk6B2lkIiVmZWQ0%250ANjkxNmU3YTI2Y2RmNzQxNmY5N2IzMmY4ZWQ1MQ%253D%253D--1a6e87c3cf286b07b59e5889659b7a8534fa6a84; g_state={"i_l":1,"i_p":1646537827556}; auth_token=e05d22cfc8f27f151480a9c88ce11e3ac0a4a274; ct0=02d7ba522df0f1d306d146c80c4785f506ae62e5580b436b1a1aa292673ee67fba2203fef79a35af8b121cfe09bfcdb92d5b037e3d6cf0632eafd724223e771fe91227946b8091ce1247e08acc7051a0; twid=u%3D1254983364622180352; at_check=true; mbox=session#0d30c14b97c049f287eee5b061d455ca#1647425340|PC#0d30c14b97c049f287eee5b061d455ca.38_0#1710668280; _ga_BYKEBDM7DS=GS1.1.1647423485.1.0.1647423485.0; _ga=GA1.2.1554362123.1636996095; _gid=GA1.2.242504478.1649393409',
        'referer': url,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'x-csrf-token': '02d7ba522df0f1d306d146c80c4785f506ae62e5580b436b1a1aa292673ee67fba2203fef79a35af8b121cfe09bfcdb92d5b037e3d6cf0632eafd724223e771fe91227946b8091ce1247e08acc7051a0',
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'zh-cn',
    }
    res = requests.get(url=url_detail_inf,headers=headers)
    datasList = []
    if res.status_code == 200:
        res = res.json()
        try:
            legacy = res['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']

        except:
            pass
            # legacy = data.threaded_conversation_with_injections_v2.instructions[0].entries[0].content.itemContent.tweet_results.result.legacy
        datasList = parse_legacy(legacy=legacy)
        if len(datasList) > 0:
            # dict的去重
            datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
            # 插入路径
            for i in datasList:
                i['path_user'] = path_user
            print("抓取的视频/图片列表长度：" + str(len(datasList)))
            print('开始下载视频/图片>>>')
            with ThreadPoolExecutor(1) as tp:
                for data in datasList:
                    tp.submit(TwitterMediaDownload.saveToFile, data)

def main():
    while True:
        num = input('选择添加目标用户请输入1\n选择更新已有个别用户视频请输入2\n选择更新已有所有用户视频请输入3\n选择下载单个视频或图片请输入4\n选择退出请输入q\n')
        if num == '1':
            add_user()
        elif num == '2':
            updateOneOf()
        elif num == '3':
            update()
        elif num == '4':
            download_one()
        elif num == 'q':
            break
        else:
            print('输入错误，请重新输入\n')


if __name__ == '__main__':
    main()
    print(len(video_updates))
    for i in video_updates:
        print(i)
