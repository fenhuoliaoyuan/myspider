import base64
import random
import re
import execjs
from lxml import etree
from xvideo import *
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}


class Pornhub(object):
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
            #     cls.URL = url + '/videos?page={}'.format(page)
            actress = re.compile('actor/(.*?)\?').findall(url)[0]
            id = re.compile('id=(\d+)').findall(url)[0]
            cls.URL = 'https://www.av01.tv/search/videos?actress={}&id={}&page={}'.format(actress, id, page)
            # cls.URL = url

            res = requests.get(cls.URL, headers=HEADERS)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath('//div[@class="well well-sm "]/a')
                for article in articleList:
                    detailUrl = article.xpath('./@href')
                    title = article.xpath('./span/text()')
                    if len(detailUrl) > 0 and len(title) > 0:
                        dataDetailUrl = {
                            'detailUrl': 'https://www.av01.tv' + detailUrl[0],
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
                videoTitle = tree.xpath('//h3[@class="hidden-xs big-m-t-0"]/text()')
                # 正则匹配js代码片段，执行得出url_m3u8_master
                # sc = re.compile('media_3;(.*?var media_4.*?;)').findall(pageText)[0]
                sc_list = re.compile('scriptElement.src = \'(.*?)\';').findall(pageText)
                if len(sc_list) > 0:
                    url_js = 'https://www.av01.tv' + sc_list[0]
                    headers = {
                        'accept': '*/*',
                        # 'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                        # 'cookie': 'AVS=8382b92b2e15a91dfe2351161992bc45; _ga=GA1.2.491254759.1641899968',
                        'referer': response.url,
                        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'script',
                        'sec-fetch-mode': 'no-cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
                    }
                    req_js = requests.get(url=url_js, headers=headers)
                    if req_js.status_code == 200:
                        url_m3u8_master_text= req_js.text
                        url_m3u8_master_text = re.compile('base64,(.*?)\',').findall(url_m3u8_master_text)
                        if len(url_m3u8_master_text) > 0:
                            url_m3u8_master_text = bytes.decode(base64.b64decode(url_m3u8_master_text[0]))
                            url_m3u8_list = []
                            for line in url_m3u8_master_text.split('\n'):
                                if 'index' in line:
                                    url_m3u8_list.append(line)
                            if len(videoTitle) > 0 and len(url_m3u8_list) > 0:
                                data = {
                                    'videoName': videoTitle[0],
                                    'url_m3u8': url_m3u8_list[-1],
                                    'PATH_DIR': PATH_DIR,
                                    'PATHTSDIR': PATHTSDIR
                                }

                                cls.data_list.append(data)
        except:
            print(response.url)


def download_all():
    Pornhub.data_list = []
    # 'https://cn.pornhub.com/model/nicolove'
    url = input('例如：https://www.av01.tv/actor/%E6%B2%B3%E5%8C%97%E5%BD%A9%E8%8A%B1?id=232\n输入链接地址：')
    pages = input('输入下载的页数：')
    detaiLUrlList = Pornhub.getDetailUrl(url=url, pages=pages)
    if len(detaiLUrlList) > 0:
        res_list = []
        for row in detaiLUrlList:
            time.sleep(1)
            print('标题：' + row['title'])
            print(row['detailUrl'] + '解析中......')
            res = Pornhub.response(url=row['detailUrl'])
            if res.status_code == 200:
                print(row['detailUrl'] + '响应成功!')
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            for res in res_list:
                Pornhub.parseResponse(response=res)
            datasList = Pornhub.data_list
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                pprint(datasList)
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                # with ThreadPoolExecutor(4) as tp:
                #     for data in datasList:
                #         tp.submit(downloadM3u8.downloadOfm3u8, data)
                for data in datasList:
                    downloadM3u8.downloadOfm3u8(data)


def download_one():
    url = input('例如：https://www.av01.tv/video/64293/ssis-361-1%E3%81%8B%E6%9C%88%E3%81%AE%E7%A6%81%E6%AC%B2%E3%82%92%E7%B5%8C%E3%81%A6-%E6%9C%AC%E8%83%BD%E3%81%AE%E3%81%BE%E3%81%BE%E8%B2%AA%E3%82%8A-%E7%84%A6%E3%82%89%E3%81%95%E3%82%8C-%E3%82%A4%E3%82%AD%E3%81%BE%E3%81%8F%E3%82%8B-%E6%B1%82%E6%84%9B%E3%82%AA%E3%83%BC%E3%82%AC%E3%82%BA%E3%83%A0%E4%BA%A4%E5%B0%BE-%E6%B2%B3%E5%8C%97%E5%BD%A9%E8%8A%B1\n输入链接地址：')
    Pornhub.data_list = []
    res = Pornhub.response(url=url)
    Pornhub.parseResponse(res)
    if len(Pornhub.data_list) > 0:
        downloadM3u8.downloadOfm3u8(Pornhub.data_list[0])


PATHTSDIR = r'E:\ts\tsAv01'
PATH_DIR = r'G:\ghs\番号\骑兵'


def main():
    while True:
        num = input('设置好PATHTSDIR和PATH_DIR的路径目录值\n选择下载单个视频请请输入1\n选择下载用户全部视频请输入2\n选择退出请输入q\n')
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
