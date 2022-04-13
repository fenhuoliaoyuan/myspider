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
        for page in range(0, int(pages)):
            # for page in range(1, 2):
            cls.URL = url + '/videos/new/{}'.format(page)
            # cls.URL = url
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Host': 'www.xvideos.com',
                'Origin': 'https://www.xvideos.com',
                'Referer': url,
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            }
            res = requests.get(cls.URL, headers=headers)
            if res.status_code == 200:
                articleList = res.json()['videos']
                for article in articleList:
                    detailUrl = article['u']
                    title = article['t']
                    if len(detailUrl) > 0 and len(title) > 0:
                        dataDetailUrl = {
                            'detailUrl': 'https://www.xvideos.com' + detailUrl,
                            'title': title
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
                videoTitle = tree.xpath('//h2[@class="page-title"]/text()')
                sc_list = re.compile('setVideoHLS\(\'(.*?)\'\);').findall(pageText)
                if len(sc_list) > 0:
                    url_m3u8_master = sc_list[0]
                    req_master = requests.get(url=url_m3u8_master, headers=HEADERS)
                    url_m3u8_list = []
                    url_qianzui_m3u8 = '/'.join(url_m3u8_master.split('.m3u8')[0].split('/')[:-1]) + '/'
                    for line in req_master.text.split('\n'):
                        if 'm3u8' in line:
                            url_m3u8_list.append(url_qianzui_m3u8 + line)
                    keys_list = [re.compile('-(\d+)p').findall(i)[0] for i in url_m3u8_list]
                    dist_ = {}
                    for i in range(len(keys_list)):
                        dist_[keys_list[i]] = url_m3u8_list[i]
                    keys_list = sorted([int(i) for i in keys_list])
                    url_m3u8 = dist_[str(keys_list[-1])]
                    if len(videoTitle) > 0 and len(url_m3u8_list) > 0:
                        data = {
                            'videoName': videoTitle[0],
                            'url_m3u8': url_m3u8,
                            'PATH_DIR': PATH_DIR,
                            'PATHTSDIR': PATHTSDIR
                        }

                        cls.data_list.append(data)
        except:
            print(response.url)


def download_all():
    Pornhub.data_list = []
    # 'https://www.xvideos.com/profiles/letankorea'
    url = input('例如：https://www.xvideos.com/profiles/letankorea\n输入链接地址：')
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


def createDir(PATH_DIR):
    pathList = PATH_DIR.split('\\')
    path_dir = ''
    for i in range(0, len(pathList)):
        if i == 0:
            path_dir = pathList[0]
        else:
            path_dir = path_dir + '\\' + pathList[i]
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)


def download_one():
    url = input('例如：https://www.xvideos.com/video61596603/_-_2\n输入链接地址：')
    Pornhub.data_list = []
    res = Pornhub.response(url=url)
    Pornhub.parseResponse(res)
    if len(Pornhub.data_list) > 0:
        downloadM3u8.downloadOfm3u8(Pornhub.data_list[0])


PATHTSDIR = r'E:\ts\Xvideos'
# PATH_DIR = r'G:\ghs\Pornhub\NicoLove'
PATH_DIR = r'H:\ghs\Xvideos'
createDir(PATH_DIR)
createDir(PATHTSDIR)


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
