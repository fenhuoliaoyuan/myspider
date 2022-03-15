import os
import re

import requests
from lxml import etree
import random
from 爬虫小项目.config import ips, user_agent_list, session


def get_page_text(url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': random.choice(user_agent_list),
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8'
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text = requests.get(url=url, headers=headers)
        if page_text.status_code != 200:
            raise ValueError
    except:
        # ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text(url, acount)
    else:
        return page_text


def download(page):
    url = 'http://t66y.com/thread0806.php?fid=2&search=&page={}.html'.format(page)#无码
    # url= 'https://rewrfsrewr.xyz/forum-37-{}.html'.format(page)#有码
    # url = 'https://bbs6.unr1.xyz/2048/thread.php?fid-15-page-{}.html'.format(page)  # 国内原创
    # url = 'https://rewrfsrewr.xyz/forum-103-{}.html'.format(page)  # 中文字幕
    # url = 'https://rewrfsrewr.xyz/forum-106-{}.html'.format(page)  # 91国产合集
    page_text = get_page_text(url=url, acount=0)
    if page_text is not None:
        page_text = page_text.text
        tree = etree.HTML(page_text)
        href_list = ['http://t66y.com/' + i for i in tree.xpath('//*[@id="tbody"]/tr/td[2]/h3/a/@href')]
        for href in href_list:
            # href = 'https://bbs6.unr1.xyz/2048/state/p/15/2111/4577630.html'
            page_text_0 = get_page_text(url=href, acount=0)
            if page_text_0 is not None:
                try:
                # page_text_0.encoding = page_text_0.apparent_encoding
                    page_text_0.encoding = 'gbk'
                    page_text_0 = page_text_0.text
                    tree_0 = etree.HTML(page_text_0)
                    # torrent_page_url = tree_0.xpath('//*[@id="read_tpc"]/a/@href')
                    torrent_name = tree_0.xpath('//html/head/title/text()')[0]
                    # print(torrent_name)
                    torrent_page_url = re.compile('href="http://www\.rmdown\.com/link\.php\?hash=(.*?)">').findall(page_text_0)
                    torrent_name = str(torrent_name).replace('/','').replace('.','')
                    # magnet = re.compile('(magnet.*?)<').findall(page_text_0)



                    path_torrent = r'F:\种子\无码' + '\\' + torrent_name.replace('/', '').replace('|','').replace('亞洲無碼原創區 | 草榴社區 - t66y com','') + '.txt'
                    # path_torrrent = r'F:\种子\有码' + '\\' + comment.replace('/', '_') + '.torrent'
                    # path_torrent = r'F:\种子\国产原创' + '\\' + torrent_name + '.torrent'
                    # path_torrent = r'F:\种子\高清中文字幕' + '\\' + comment.replace('/', '_') + '.torrent'
                    # path_torrent = r'F:\种子\91国产合集' + '\\' + torrent_name
                    if len(torrent_page_url)>0:
                        # print(torrent_page_url)
                        torrent_page_url = torrent_page_url[0][3:]
                        if not os.path.exists(path_torrent) :
                            with open(path_torrent,'w') as tx:
                                tx.write('magnet:?xt=urn:btih:'+torrent_page_url)
                                print('magnet:?xt=urn:btih:'+torrent_page_url)
                        # if len(magnet) > 0:
                        #     magnet = magnet[0]
                        #     with open('F:\种子\国产原创\{}.txt'.format(torrent_name),'w',encoding='utf-8') as txt:
                        #         txt.write(magnet)
                        #         print(torrent_name + magnet)
                        # if len(torrent_page_url) > 0:
                        #     torrent_page_url = torrent_page_url[0]
                            # page_text_1 = get_page_text(url=torrent_page_url, acount=0)
                            # if page_text_1 is not None:
                            #     page_text_1 = page_text_1.text
                            #     tree = etree.HTML(page_text_1)
                            # torrent_url = 'https://www.rmdown.com/download.php/' + torrent_page_url.split('=')[
                            #     -1] + '.torrent'
                            # torrent = get_page_text(url=torrent_url, acount=0)
                            # if torrent is not None:
                            #     torrent = torrent.content
                            #     with open(path_torrent, 'wb') as tr:
                            #         tr.write(torrent)
                            #         print(torrent_name + "下载完成")
                except:
                    print('............................................................')



if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(1) as tp:
        # 无码
        for page in range(1, 1723):
        # 有码
        # for page in range(1,1001):
        # 国产原创
        # for page in range(1,2):
            # 高清中文字幕
            # for page in range(1, 556):
            # 91国产合集
            # for page in range(1,22):
            tp.submit(download, page)
