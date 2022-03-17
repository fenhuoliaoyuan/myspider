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
            cls.URL = url + '/videos?page={}'.format(page)
            # cls.URL = url

            res = requests.get(cls.URL, headers=HEADERS)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath(
                    '//div[@class="profileVids"]/div[@class="videoSection clear-both"]//span[@class="title"]')
                for article in articleList:
                    detailUrl = article.xpath('./a/@href')
                    title = article.xpath('./a/@title')
                    if len(detailUrl) > 0 and len(title) > 0:
                        dataDetailUrl = {
                            'detailUrl': 'https://cn.pornhub.com' + detailUrl[0],
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
                videoTitle = tree.xpath('//span[@class="inlineFree"]/text()')
                # 正则匹配js代码片段，执行得出url_m3u8_master
                # sc = re.compile('media_3;(.*?var media_4.*?;)').findall(pageText)[0]
                sc_list = re.compile('(var ra.*?)flashvars').findall(pageText)
                if len(sc_list) > 0:
                    sc = sc_list[-2]
                    note = execjs.get()
                    # ctx = node.compile(open('./steam.js',encoding='utf-8').read())
                    ctx = note.compile(sc)

                    # 执行js函数
                    funcName = 'media_{}'.format(len(sc_list)-2)
                    url_m3u8_master = ctx.eval(funcName)
                    req_master = requests.get(url=url_m3u8_master, headers=HEADERS)
                    url_m3u8_list = []
                    url_qianzui_m3u8 = '/'.join(url_m3u8_master.split('.m3u8')[0].split('/')[:-1]) + '/'
                    for line in req_master.text.split('\n'):
                        if 'm3u8' in line:
                            url_m3u8_list.append(url_qianzui_m3u8 + line)
                    if len(videoTitle) > 0 and len(url_m3u8_list) > 0:
                        data = {
                            'videoName': videoTitle[0],
                            'url_m3u8': url_m3u8_list[0],
                            'PATH_DIR': PATH_DIR,
                            'PATHTSDIR': PATHTSDIR
                        }

                        cls.data_list.append(data)
        except:
            print(response.url)


def download_all():
    Pornhub.data_list = []
    # 'https://cn.pornhub.com/model/nicolove'
    url = input('例如：https://cn.pornhub.com/model/nicolove\n输入链接地址：')
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
    url = input('例如：https://cn.pornhub.com/view_video.php?viewkey=ph62042d99c2cc7\n输入链接地址：')
    Pornhub.data_list = []
    res = Pornhub.response(url=url)
    Pornhub.parseResponse(res)
    if len(Pornhub.data_list) > 0:
        downloadM3u8.downloadOfm3u8(Pornhub.data_list[0])

PATHTSDIR = r'E:\tsPornhub'
PATH_DIR = r'G:\ghs\Pornhub\NicoLove'
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
