import M3u8Onebookcms
from M3u8Onebookcms import *
from lxml import etree
import time

PATHTSDIR = r'E:\tsAvolTv'
PATH_DIR = r'G:\ghs\国产'


class OneBookcms(object):
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
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                # 'cookie': 'PHPSESSID=o1e3vqo70kf1n42vmlbgrff5rr; kt_referer=https%3A%2F%2Fwww.google.com.hk%2F; kt_qparams=id%3D9429%26dir%3D8461f8b15d011f8472bd7849ec070e9e; kt_ips=91.238.103.147; kt_tcookie=1; kt_is_visited=1; _ga=GA1.2.6983639.1647056768; _gid=GA1.2.2058903063.1647056768',
                'referer': url,
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            params = {
                'mode': 'async',
                'function': 'get_block',
                'block_id': 'list_videos_common_videos_list',
                'sort_by': 'post_date',
                'from': page,
                '_': int(time.time()),
            }
            res = requests.get(URL, headers=HEADERS, params=params)
            if res.status_code == 200:
                pageText = res.text
                tree = etree.HTML(pageText)
                articleList = tree.xpath('//div[@class="item  "]')
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
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': 'PHPSESSID=o1e3vqo70kf1n42vmlbgrff5rr; kt_referer=https%3A%2F%2Fwww.google.com.hk%2F; kt_qparams=id%3D9429%26dir%3D8461f8b15d011f8472bd7849ec070e9e; kt_ips=91.238.103.147; kt_tcookie=1; kt_is_visited=1; _ga=GA1.2.6983639.1647056768; _gid=GA1.2.2058903063.1647056768',
            # 'referer': url,
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        }
        # proxies = random.choice(ips)
        HEADERS = {
            'user-agent': random.choice(user_agent_list)
        }
        res = requests.get(url=url, headers=HEADERS,proxies=random.choice(ips))
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
            videoTitle = tree.xpath('//div[@class="headline"]/h1/text()')
            videoUrl = re.compile('file:\"(.*?)\",').findall(pageText)
            if len(videoTitle) > 0 and len(videoUrl) > 0:
                data = {
                    'videoName': videoTitle[0],
                    'url_m3u8': videoUrl[0],
                    'PATH_DIR': PATH_DIR,
                    'PATHTSDIR': PATHTSDIR
                }

                cls.data_list.append(data)
                return cls.data_list


def main():
    # 'https://onebookcms.com/tags/ba0204559d2fab3059f5a22bca91954a/'
    url = input('输入链接地址：')
    pages = input('输入下载的页数：')
    detaiLUrlList = OneBookcms.getDetailUrl(url=url, pages=pages)
    if len(detaiLUrlList) > 0:
        res_list = []
        for row in detaiLUrlList:
            res = OneBookcms.response(url=row['detailUrl'])
            if res is not None:
                res_list.append(res)
        if len(res_list) > 0:
            datasList = []
            for res in res_list:
                datas = OneBookcms.parseResponse(response=res)
                if datas is not None:
                    datasList.extend(datas)
            if len(datasList) > 0:
                # dict的去重
                datasList = [dict(t) for t in set([tuple(d.items()) for d in datasList])]
                print("抓取的视频列表长度：" + str(len(datasList)))
                print('开始下载视频>>>')
                # with ThreadPoolExecutor(1) as tp:
                for data in datasList:
                    M3u8Onebookcms.downloadM3u8.downloadOfm3u8(data)


if __name__ == '__main__':
    PATHTSDIR = r'E:\tsAvolTv'
    PATH_DIR = r'G:\ghs\国产\杏吧'
    main()
