from M3u8RouVideo import *
from lxml import etree
import time

PATHTSDIR = r'E:\tsAvolTv'
PATH_DIR = r'G:\ghs\国产'


class RouVideo(object):
    data_list = []

    @staticmethod
    def getDetailUrl(url, pages):
        """
        获取详情页地址和标题
        :param url:
        :param pages:
        :return:
        """
        detaiLUrlList = []
        for page in range(1, int(pages) + 1):
            # URL = url + 'page/' + str(page) + '/'
            URL = url
            params = {
                'order': 'createdAt',
                'page': page,
            }
            if 'search' == url.split('/')[-1].split('?')[0]:
                params = {
                    'page': page
                }
            res = requests.get(URL, headers=HEADERS, params=params)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath('//div[@class="relative"]')
                for article in articleList:
                    detailUrl = article.xpath('./a/@href')
                    title = article.xpath('./a/img/@alt')
                    if len(detailUrl) > 0 and len(title) > 0:
                        dataDetailUrl = {
                            'detailUrl': 'https://rou.video' + detailUrl[0],
                            'title': title[0]
                        }
                        detaiLUrlList.append(dataDetailUrl)
        return detaiLUrlList

    @staticmethod
    def response(url):
        """
        获取网页
        :param url:
        :return:
        """
        # proxies = random.choice(ips)
        res = requests.get(url=url, headers=HEADERS)
        return res

    @classmethod
    def parseResponse(cls, response):
        """
        解析response
        :param response:
        :return:
        """
        if response is not None:
            pageText = response.text
            tree = etree.HTML(pageText)
            # videoTitle = tree.xpath('//div[@class="headline"]/h1/text()')
            videoTitle = tree.xpath('/html/head/title/text()')
            videoUrl = re.compile('"videoUrl":\"(.*?)\"}').findall(pageText)
            if len(videoTitle) > 0 and len(videoUrl) > 0:
                data = {
                    'videoName': videoTitle[0].replace('- 肉視頻,您的私人AV影院', '').strip(),
                    'url_m3u8': videoUrl[-1].replace('\\u0026', '&'),
                    'PATH_DIR': PATH_DIR,
                    'PATHTSDIR': PATHTSDIR
                }

                cls.data_list.append(data)
                return cls.data_list


def rouVideoDownload():
    # 'https://rou.video/t/%E6%9D%8F%E5%90%A7'
    url = input('例如：https://rou.video/t/%E6%9D%8F%E5%90%A7 \n输入链接地址：')
    pages = input('输入下载的总页数：')
    detaiLUrlList = RouVideo.getDetailUrl(url=url, pages=pages)
    if len(detaiLUrlList) > 0:
        res_list = []
        for row in detaiLUrlList:
            res = RouVideo.response(url=row['detailUrl'])
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            datasList = []
            for res in res_list:
                datas = RouVideo.parseResponse(response=res)
                if datas is not None:
                    datasList.extend(datas)
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                # with ThreadPoolExecutor(1) as tp:
                for data in datasList:
                    downloadM3u8.downloadOfm3u8(data)


def downloadOne():
    RouVideo.data_list = []
    url = input('例如：https://rou.video/v/ckvknyuih001211g43tc310h1\n输入视频播放页地址：')
    res = RouVideo.response(url)
    if res.status_code == 200:
        RouVideo.parseResponse(res)
        if len(RouVideo.data_list) > 0:
            downloadM3u8.downloadOfm3u8(RouVideo.data_list[0])


def downloadSearch():
    RouVideo.data_list = []
    word = input('输入你要添加的搜索词：')
    url = 'https://rou.video/search?q=' + word
    detaiLUrlList = RouVideo.getDetailUrl(url, pages=5)
    detaiLUrlList = [i for i in detaiLUrlList if len(re.compile(word).findall(i['title'])) > 0]
    res_list = []
    for row in detaiLUrlList:
        res = RouVideo.response(url=row['detailUrl'])
        if res is not None:
            res_list.append(res)
    if len(res_list) > 0:
        datasList = []
        for res in res_list:
            datas = RouVideo.parseResponse(response=res)
            if datas is not None:
                datasList.extend(datas)
        if len(datasList) > 0:
            # dict的去重
            datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
            print("抓取的视频列表长度：" + str(len(datasList)))
            print('开始下载视频>>>')
            # with ThreadPoolExecutor(1) as tp:
            for data in datasList:
                downloadM3u8.downloadOfm3u8(data)


def main():
    while True:
        num = input('选择下载单个视频请输入1\n选择批量下载视频列表请输入2\n选择下载固定搜索词的批量下载功能请输入3\n选择退出请输入q\n')
        if num == '1':
            downloadOne()
        elif num == '2':
            rouVideoDownload()
        elif num == '3':
            downloadSearch()
        elif num == 'q':
            break
        else:
            print('输入错误，请重新输入\n')


if __name__ == '__main__':
    PATHTSDIR = r'E:\tsAvolTv'
    PATH_DIR = r'G:\ghs\未分类'
    main()
