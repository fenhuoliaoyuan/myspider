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


def main():
    # 'https://rou.video/t/%E6%9D%8F%E5%90%A7'
    url = input('输入链接地址：')
    pages = input('输入下载的页数：')
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


if __name__ == '__main__':
    PATHTSDIR = r'E:\tsAvolTv'
    PATH_DIR = r'G:\ghs\国产\杏吧'
    main()
