import random
import re
import time
from pprint import pprint

from lxml import etree
from toolSpankbang import *
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}


class Spankbang(object):
    data_list = []
    URL = ''

    @classmethod
    def getDetailUrl(cls, url, pages):
        """
        获取详情页地址和标题
        :param url:
        :param pages:
        :return:
        """
        detaiLUrlList = []
        for page in range(1, int(pages) + 1):
            # for page in range(1, 2):
            cls.URL = url + '/videos?o=new&page={}'.format(page)
            # URL = url

            res = requests.get(cls.URL, headers=HEADERS)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath('//a[@class="n"]')
                for article in articleList:
                    detailUrl = article.xpath('./@href')
                    title = article.xpath('./text()')
                    if len(detailUrl) > 0 and len(title) > 0:
                        dataDetailUrl = {
                            'detailUrl': 'https://jp.spankbang.com' + detailUrl[0],
                            'title': title[0]
                        }
                        detaiLUrlList.append(dataDetailUrl)
        return detaiLUrlList

    @classmethod
    def response(cls, url):
        """
        获取网页
        :param url:
        :return:
        """
        proxies = random.choice(ips)
        res = requests.get(url=url, headers=HEADERS)
        return res

    @classmethod
    def parseResponse(cls, response):
        """
        解析response
        :param response:
        :return:
        """
        try:
            if response is not None:
                pageText = response.text
                tree = etree.HTML(pageText)
                videoTitle = tree.xpath('//div[@class="left"]/h1/text()')
                videoUrl_list = re.compile("(https://vdownload.*?)']").findall(pageText)
                # 去重，排序，挑选最高画质
                videoUrl_list = list(set(videoUrl_list))
                key_list = [re.compile('/\d+-(.*?)\.mp4').findall(i)[0].replace('k','000').replace('p','') for i in videoUrl_list]
                dict_data = {}
                for i in range(0,len(videoUrl_list)):
                    dict_data[key_list[i]] = videoUrl_list[i]
                keys = sorted([int(i) for i in dict_data.keys()])
                if len(videoTitle) > 0 and len(videoUrl_list) > 0:
                    data = {
                        'videoName': videoTitle[0],
                        'videoUrl': dict_data[str(keys[-1])],
                    }

                    cls.data_list.append(data)
        except:
            print(response.url)


def download_all():
    Spankbang.data_list = []
    # 'https://onebookcms.com/tags/ba0204559d2fab3059f5a22bca91954a/'
    url = input('输入链接地址：')
    pages = input('输入下载的页数：')
    detaiLUrlList = Spankbang.getDetailUrl(url=url, pages=pages)
    if len(detaiLUrlList) > 0:
        res_list = []
        for row in detaiLUrlList:
            time.sleep(2)
            print(row['detailUrl']+'解析中......')
            res = Spankbang.response(url=row['detailUrl'])
            if res.status_code == 200:
                print(row['detailUrl']+'响应成功!')
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            for res in res_list:
                Spankbang.parseResponse(response=res)
            datasList = Spankbang.data_list
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                pprint(datasList)
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                with ThreadPoolExecutor(4) as tp:
                    for data in datasList:
                        tp.submit(down_from_url, data)
                # for data in datasList:
                #     down_from_url(data)


def download_one():
    url = input('输入链接地址：')
    Spankbang.data_list = []
    res = Spankbang.response(url=url)
    Spankbang.parseResponse(res)
    if len(Spankbang.data_list) > 0:
        down_from_url(Spankbang.data_list[0])


def main():
    while True:
        num = input('选择下载单个视频请请输入1\n选择下载用户全部视频请输入2\n选择退出请输入q\n')
        if num == '1':
            download_one()
        elif num == '2':
            download_all()
        elif num == 'q':
            break
        else:
            print('输入错误，请重新输入\n')


if __name__ == '__main__':
    main()
