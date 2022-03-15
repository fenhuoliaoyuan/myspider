import os
import random
import re
from lxml import etree
import requests
from concurrent.futures import ThreadPoolExecutor
from configRiSite import *

if not os.path.exists(PATH_DIR):
    os.mkdir(PATH_DIR)
class RiSite(object):

    data_list = []
    @staticmethod
    def getDetailUrl(url,pages):
        """
        获取详情页地址和标题
        :param url:
        :param pages:
        :return:
        """
        detaiLUrlList  = []
        for page in range(1,int(pages)+1):
            URL = url + 'page/'+str(page)+ '/'
            res = requests.get(URL,headers=HEADERS)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath('//*[@id="main"]/div[1]/article')
                for article in articleList:
                    detailUrl = article.xpath('./a/@href')
                    title = article.xpath('./a/@title')
                    if len(detailUrl)>0 and len(title)>0:
                        dataDetailUrl = {
                            'detailUrl': detailUrl[0],
                            'title':title[0]
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
            videoTitle = tree.xpath('//h1[@class="entry-title"]/text()')
            videoUrl = re.compile('source src=\"(.*?)\"').findall(pageText)
            if len(videoTitle)>0 and len(videoUrl)>0:
                data = {
                    'videoTitle': videoTitle[0],
                    'videoUrl': videoUrl[0]
                }

                cls.data_list.append(data)
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
    # 'https://ri1.site/category/%e7%90%b3%e7%90%b3-jamiebabe/'
    url = input('输入链接地址：')
    pages = input('输入下载的页数：')
    detaiLUrlList = RiSite.getDetailUrl(url=url,pages=pages)
    if len(detaiLUrlList) > 0:
        res_list = []
        for row in detaiLUrlList:
            res = RiSite.response(url=row['detailUrl'])
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            datasList = []
            for res in res_list:
                datas = RiSite.parseResponse(response=res)
                if datas is not None:
                    datasList.extend(datas)
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                with ThreadPoolExecutor(2) as tp:
                    for data in datasList:
                        tp.submit(RiSite.saveToFile, data)


if __name__ == '__main__':
    main()
