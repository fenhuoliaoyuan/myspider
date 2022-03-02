import re

from xvideo import downloadM3u8
from lxml import etree
import requests
from configCableavTv import *

PATHTSDIR = r'E:\ts\CableavTv'
PATH_DIR = r'G:\ghs\CableavTv\Avove'


class CableavTv(object):
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
        print('正在获取视频详细页列表...')
        for page in range(1, int(pages) + 1):
            URL = url + 'page/'+str(page)+ '/'
            res = requests.get(URL, headers=HEADERS)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath('//h3[@class="entry-title h3 post-title"]')
                for article in articleList:
                    detailUrl = article.xpath('./a/@href')
                    title = article.xpath('./a/@title')
                    if len(detailUrl) > 0 and len(title) > 0:
                        dataDetailUrl = {
                            'detailUrl': detailUrl[0],
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
            pageText = response.text
            tree = etree.HTML(pageText)
            videoTitle = tree.xpath('/html/head/title/text()')
            # videoUrl = re.compile('source src=\"(.*?)\"').findall(pageText)
            # videoUrl = tree.xpath('/html/head/meta[4]/@content')
            videoUrls = re.compile('"source_file":"(.*?)"}').findall(pageText)
            videoUrl = videoUrls[-1].replace('\\','')
            if len(videoTitle) > 0 and len(videoUrl) > 0:
                data = {
                    'PATHTSDIR': PATHTSDIR,
                    'PATH_DIR': PATH_DIR,
                    'videoName': videoTitle[0].replace('- CableAV', '').strip(),
                    'url_m3u8': videoUrl
                }

                cls.data_list.append(data)
                return cls.data_list


def main():
    # 'https://cableav.tv/playlist/r111qLRtz8j/'
    url = input('输入链接地址：')
    pages = input('输入下载总页数：')
    detaiLUrlList = CableavTv.getDetailUrl(url=url,pages=pages)
    if len(detaiLUrlList) > 0:
        res_list = []
        for row in detaiLUrlList:
            res = CableavTv.response(url=row['detailUrl'])
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            datasList = []
            for res in res_list:
                datas = CableavTv.parseResponse(response=res)
                if datas is not None:
                    datasList.extend(datas)
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                for data in datasList:
                    downloadM3u8.tq = ''
                    downloadM3u8.downloadOfm3u8(data)


if __name__ == '__main__':
    PATHTSDIR = r'E:\ts\CableavTv'
    PATH_DIR = r'G:\ghs\CableavTv\虎牙主播 長腿兮兮 直播熱舞誘惑'
    main()
