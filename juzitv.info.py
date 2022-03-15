import requests
import os
import random
from lxml import etree
import re
from Crypto.Cipher import AES
from base64 import b64decode
import 类库
from 类库 import get_ts, get_page_text, get_page_text_detail, get_m3u8
from concurrent.futures import ThreadPoolExecutor
from 爬虫小项目 import config

ips = config.ips
headers_list = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"},
    {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"},
    {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
    {'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
]


def get_href_list(start_page, end_page, URL):
    url_detail_list = []
    for page in range(int(start_page), int(end_page) + 1):
        # URL = 'https://www.mdr18.xyz/index.php/vod/type/id/101/page/%d.html'%page
        # URL = 'https://mdr18.pw/index.php/vod/search/page/1/wd/%E5%86%AF%E9%9B%AA.html'
        # URL = 'https://www.mdr18.pw/index.php/vod/search/page/{}/wd/%E6%9D%8E%E5%AE%97%E7%91%9E.html'.format(page)
        # https://mdr18.pw/index.php/vod/search/page/2/wd/%E5%A4%8F%E6%99%B4%E5%AD%90.html
        URL_0 = 'https://www.juzitv.info/index.php/vod/search/page/'
        URL_1 = str(page) + '/wd/' + URL.split('/')[-1]
        URL = URL_0 + URL_1
        # URL = URL + '&page={}'.format(page)
        page_text = get_page_text(url=URL, acount=0)
        if page_text:
            page_text = page_text.text
            tree = etree.HTML(page_text)
            href_list = ['https://www.juzitv.info' + href for href in tree.xpath('//div[@class="entry-title"]/a/@href')]
            url_detail_list.extend(href_list)
    return url_detail_list


def download(url_detail):
    def get_m3u8_(m3u8_url, acount):
        try:

            headers = {
                'user-agent': random.choice(config.user_agent_list),
                # 'referer': 'https://www.mdr18.xyz/',
                # 'origin': 'https://www.mdr18.xyz'
            }
            if 'www.foxmaxke.xyz' in m3u8_url:
                headers = {
                    'user-agent': random.choice(config.user_agent_list),
                    'origin': 'https://www.juzitv.info',
                    'referer': 'https://www.juzitv.info/',
                    # ':authority': 'www.foxmaxke.xyz'
                }

            proxies = random.choice(ips)
            m3u8 = requests.get(url=m3u8_url, headers=headers, proxies=proxies)
            if m3u8.status_code != 200:
                raise ValueError
        except:
            # ips.remove(proxies)
            # print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
            if acount == 20:
                return
            acount += 1
            get_m3u8_(m3u8_url, acount)
        else:
            return m3u8

    def get_url_m3u8(url_detail):
        page_detail = get_page_text_detail(url_detail=url_detail, acount=0)
        if page_detail is not None:
            page_detail_text = page_detail.text
            tree = etree.HTML(page_detail_text)
            title = tree.xpath('/html/head/title/text()')[0]
            print('------------------------开始下载{}------------------------'.format(title + '.mp4'))
            title = title.replace('.', '#').replace('*', '#').replace(':', '#').replace('/', '#').split('-')[0]
            path_mp4 = path_root + '\\' + title + '.mp4'
            url_m3u8 = re.compile('var urls = "(.*?)";').findall(page_detail_text)
            if len(url_m3u8)!=0:
                url_m3u8 = url_m3u8[0]
            # url_m3u8_ = re.compile('<source src="(.*?)" type').findall(page_detail_text)[0]
            m3u8_base64 = re.compile('"url":"(.*?)","url_next"').findall(page_detail_text)
            # url = 'aHR0cHM6Ly93d3cuZm9ybWF4MjMueHl6LzIwMjEwNzE4LzdvZ0c4SEJ0L2luZGV4Lm0zdTgO0O0O'
            import base64
            url_m3u8 = bytes.decode(base64.b64decode(m3u8_base64[0]),encoding='unicode_escape')
            url_m3u8 = re.compile('(.*?u8)').findall(url_m3u8)[0]
            print(url_m3u8)
            # url_m3u8_64 = m3u8_base64[0][:64]
            # weibu = m3u8_base64[0][64:]
            # import base64
            # toubu = bytes.decode(base64.b64decode(url_m3u8_64))
            # # URL = base64.b64decode(url)
            # # URL_ = bytes.decode(URL)
            # # print(URL_)
            # # 麻豆
            # weibu = re.compile('(.*?u8)').findall(bytes.decode(base64.b64decode(weibu), encoding='unicode_escape'))
            # if len(weibu) != 0:
            #     weibu = weibu[0]
            # else:
            #     weibu = ''
            # # m3u8_qianzui = ''.join(re.compile('.*/').findall(toubu))
            # # if 'vip' in m3u8_qianzui:
            # #     url_m3u8 = m3u8_qianzui + 'index.m3u8'
            # # else:
            # #     url_m3u8 = m3u8_qianzui + 'index.m3u8'
            # url_m3u8 = toubu + weibu
            # if 'huishenghuo888888' in url_m3u8:
            #     url_m3u8 = url_m3u8.replace('https://video.huishenghuo888888.com', 'https://d3b4hd2s3d140t.cloudfront.net')
            m3u8_text = get_m3u8_(m3u8_url=url_m3u8, acount=0)
            if m3u8_text is not None:
                m3u8_text = m3u8_text.text
                # url_m3u8_ = url_m3u8.replace('/index.m3u8','') + m3u8_text.split('\n')[-2]
                url_m3u8_ = 'https://www.formax23.xyz' + m3u8_text.split('\n')[-2]
                if 'www.lbbf9.com' in url_m3u8:
                    url_m3u8_ = 'https://www.lbbf9.com' + m3u8_text.split('\n')[-2]
                elif 'fhbf9' in url_m3u8:
                    url_m3u8_ = 'https://vip2.fhbf9.com' + m3u8_text.split('\n')[-2]
                elif 'foxmaxkc' in url_m3u8:
                    url_m3u8_ = 'https://www.foxmaxkc.xyz' + m3u8_text.split('\n')[-2]
                elif 'video' in url_m3u8:
                    url_m3u8_ = url_m3u8.replace('index.m3u8', '') + m3u8_text.split('\n')[-1]
                elif 'cloudfront' in url_m3u8:
                    url_m3u8_ = url_m3u8.replace('index.m3u8', '') + m3u8_text.split('\n')[-1]
                elif 'vip2.lbbf9' in url_m3u8:
                    url_m3u8_ = 'https://vip2.lbbf9.com' + m3u8_text.split('\n')[-2]
                elif 'https://lbbf9.com' in url_m3u8:
                    url_m3u8_ = 'https://lbbf9.com'+m3u8_text.split('\n')[-2]
                elif 'www.foxmaxke.xyz' in url_m3u8:
                    url_m3u8_ = 'https://www.foxmaxke.xyz'+m3u8_text.split('\n')[-2]
                print('m3u8地址：'+url_m3u8_)
            return url_m3u8_, path_mp4

    def get_cryptor(url_m3u8):
        # url_m3u8 = 'https://kingdom-b.alonestreaming.com/hls/LABUvA1N2MSC7uTh8Fi1Pg/1634916782/16000/16665/16665.m3u8'

        # if 'vip' in url_m3u8:
        #     headers = {
        #         'Host': 'vip2.lbbf9.com',
        #         'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        #         'Sec-Fetch-Site': 'cross-site',
        #         'Sec-Fetch-Mode': 'cors',
        #         'Sec-Fetch-Dest': 'empty',
        #         'Origin': 'https://www.mdr69.info',
        #         'Pragma': 'no-cache',
        #         'Referer': 'https://www.mdr69.info/',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        #
        #     }
        #     response = requests.get(url=url_m3u8, headers=headers)
        # else:
        response = requests.get(url=url_m3u8, headers=random.choice(headers_list))
        m3u8_txt = response.text
        # print()
        jpg_list = []
        url_key = ''
        for line in m3u8_txt.split('\n'):
            # print(line)
            if 'URI' in line:
                # url_key = url_qianzui + re.compile('URI="(.*)"').findall(line)[0]
                URI = re.compile('URI="(.*)"').findall(line)
                if len(URI) != 0:
                    url_key = url_qianzui + URI[0]
                    if 'vip2.lbbf9' in url_m3u8:
                        url_key = 'https://vip2.lbbf9.com' + URI[0]
                        print('url_key地址：' + url_key)
                # iv = b64decode(re.compile('IV=(.*)').findall(line)[0])
                # print(url_key)
            elif 'jpg' in line:
                jpg_list.append(line)
            # elif 'ts' in line and 'lbbf9' in url_m3u8:
            #     jpg_list.append('https://lbbf9.com' + line)
            # elif 'ts' in line and 'vip' in url_m3u8:
            #     jpg_list.append(url_qianzui + line)
            elif 'ts' in line and 'video' in url_m3u8:
                jpg_list.append(url_m3u8.replace('index.m3u8', '') + line)
            elif 'ts' in line and 'cloudfront' in url_m3u8:
                jpg_list.append(url_m3u8.replace('index.m3u8', '') + line)
            elif 'ts' in line and 'vip2.lbbf9' in url_m3u8:
                jpg_list.append('https://vip2.lbbf9.com' + line)
            elif 'ts' in line and 'www.lbbf9.com' in url_m3u8:
                jpg_list.append('https://www.lbbf9.com'+line)
            elif 'ts' in line and 'https://lbbf9.com' in url_m3u8:
                jpg_list.append('https://lbbf9.com'+line)
        print('ts长度：'+str(len(jpg_list)))
        if len(url_key) == 0:
            return jpg_list
        else:
            key_byte = requests.get(url=url_key, headers=random.choice(headers_list)).content
            cryptor = AES.new(key_byte, AES.MODE_CBC)
            return cryptor, jpg_list

    def download_1(ts_url):
        name_ts = ts_url.split('/')[-1]
        if not os.path.exists(ts_dir + '\\' + name_ts):
            ts = get_ts(ts_url, acount=0)
            if ts is not None:
                ts = ts.content

                # name_ts = name_ts.split('.')[0]
                ts_open = cryptor.decrypt(ts)
                # dict_ts[name_ts]= ts_open
                with open(ts_dir + '\\' + name_ts, 'wb') as wt:
                    wt.write(ts_open)
                    print(name_ts)
                # with open('./jable_第一个mp4.mp4', 'ab') as fp:
                #     fp.write(ts_open)
                #     print('{}下载成功'.format(name_ts))

    def download_2(jpg_url):
        name_jpg = jpg_url.split('/')[-1]
        if not os.path.exists(ts_dir + '\\' + name_jpg):
            ts = get_ts(jpg_url, acount=0)
            if ts is not None:
                ts = ts.content
                # name_ts = name_ts.split('.')[0]
                # ts_open = cryptor.decrypt(ts)
                # dict_ts[name_ts]= ts_open
                with open(ts_dir + '\\' + name_jpg, 'wb') as wt:
                    wt.write(ts)
                    print(name_jpg)

    # for url_detail in url_detail_list:
    url_m3u8, path_mp4 = get_url_m3u8(url_detail)
    print('获取m3u8')
    if not os.path.exists(path_mp4):
        ts_dir = path_mp4.split('.mp')[0]
        print('创建目录{}'.format(ts_dir))
        if not os.path.exists(ts_dir):
            os.mkdir(ts_dir)
        list_ts_file = ''
        url_qianzui = url_m3u8.replace('index.m3u8', '')
        if 'vip' in url_m3u8:
            url_qianzui = url_m3u8.split('com')[0] + 'com'
        # 'https://2xingav.com/video/m3u8/20a770ddca8b5b14dc545e5a2277feb9dddb720a.m3u8?video_server=lacdn'
        # 'https://c.s1c.xyz/videos/20a770ddca8b5b14dc545e5a2277feb9dddb720a/p00015.ts'
        # url_m3u8 = url_qianzui + '9442.m3u8'
        if len(list(get_cryptor(url_m3u8))) == 2:
            cryptor, ts_list = get_cryptor(url_m3u8)
            while len(list_ts_file) < len(ts_list):
                with ThreadPoolExecutor(100) as tp:
                    for ts_url in ts_list:
                        tp.submit(download_1, ts_url)
                    list_ts_file = os.listdir(ts_dir)
            print('ts下载完成')
        else:
            ts_list = get_cryptor(url_m3u8)
            while len(list_ts_file) < len(ts_list):
                with ThreadPoolExecutor(100) as tp:
                    for ts_url in ts_list:
                        tp.submit(download_2, ts_url)
                        list_ts_file = os.listdir(ts_dir)
            print('ts下载完成')
        # dict_ts = sorted(dict_ts)
        # with open('第一个MP4.mp4','ab') as rb:
        #     for i in dict_ts:
        #         rb.write(dict_ts[i])
        #         print(i+'写入成功')
        # list_ts_file = os.listdir('./测试')
        # path_name = r'番号\JUL-285 處男的我愛上了知性美女三浦步美為她獻上我的童子之身 三浦歩美.mp4'
        with open(path_mp4, 'ab') as ab:
            for i in ts_list:
                with open(ts_dir + '\\' + i.split('/')[-1], 'rb') as rb:
                    ab.write(rb.read())
            print(path_mp4 + '合并完成')
        for j in [ts_dir + '\\' + i for i in list_ts_file]:
            # print(j)
            os.remove(j)
        os.rmdir(ts_dir)
        print('ts删除完成,ts目录删除完成')
        end_time = int(time.time())
        time_all = end_time - start_time
        print('执行时间为：' + str(time_all) + 's')


if __name__ == '__main__':
    import time

    path_root = r'F:\国产av\Princessdolly'
    if not os.path.exists(path_root):
        os.mkdir(path_root)
    start_time = int(time.time())
    # 使用搜索所得页地址，获取href_list
    url = 'https://www.juzitv.info/index.php/vod/search/page/2/wd/Princessdolly.html'
    url_detail_list = get_href_list(1, 1, url)
    with ThreadPoolExecutor(10) as ttp:
        for url_detail in url_detail_list[2:]:
            ttp.submit(download, url_detail)
