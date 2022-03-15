import os

from lxml import etree

from 爬虫小项目.config import get_page_text


def download(page):
    # url = 'https://rewrfsrewr.xyz/forum-36-{}.html'.format(page)#无码
    # url= 'https://rewrfsrewr.xyz/forum-37-{}.html'.format(page)#有码
    url= 'https://rewrfsrewr.xyz/forum-2-{}.html'.format(page)#国产原创
    # url = 'https://rewrfsrewr.xyz/forum-103-{}.html'.format(page)  # 中文字幕
    # url = 'https://rewrfsrewr.xyz/forum-106-{}.html'.format(page)  # 91国产合集
    page_text = get_page_text(url=url, acount=0)
    if page_text is not None:
        page_text = page_text.text
        tree = etree.HTML(page_text)
        href_list = ['https://rewrfsrewr.xyz/' + i for i in tree.xpath('//a[@class="s xst"]/@href')]
        for href in href_list:
            page_text_0 = get_page_text(url=href, acount=0)
            if page_text_0 is not None:
                page_text_0 = page_text_0.text
                tree_0 = etree.HTML(page_text_0)
                try:
                    torrent_url = tree_0.xpath('//p[@class="attnm"]/a/@href')[0]
                    torrent_name = tree_0.xpath('//p[@class="attnm"]/a/text()')[0]
                    comment = tree_0.xpath('//*[@id="thread_subject"]/text()')[0]
                except:
                    pass
                else:
                    # path_torrent = r'F:\种子\无码' + '\\' + comment.replace('/', '_') + '.torrent'
                    # path_torrrent = r'F:\种子\有码' + '\\' + comment.replace('/', '_') + '.torrent'
                    path_torrent = r'F:\种子\国产原创' + '\\' + comment.replace('/', '_') + '.torrent'
                    # path_torrent = r'F:\种子\高清中文字幕' + '\\' + comment.replace('/', '_') + '.torrent'
                    # path_torrent = r'F:\种子\91国产合集' + '\\' + torrent_name
                    if not os.path.exists(path_torrent):
                        torrent = get_page_text(url=torrent_url, acount=0)
                        if torrent is not None:
                            torrent = torrent.content
                            with open(path_torrent, 'wb') as tr:
                                tr.write(torrent)
                                print(torrent_name + "下载完成")


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(50) as tp:
        # 无码
        # for page in range(1, 674):
        # 有码
        # for page in range(1,1001):
        # 国产原创
        for page in range(1,680):
        # 高清中文字幕
        # for page in range(1, 556):
        # 91国产合集
        # for page in range(1,22):
            tp.submit(download, page)
