# URL = 'https://www.xvideos.com/video63108659/the_ryujin_hip_trend_pmv'
# //*[@id="video-player-bg"]/script[4](m3u8)
# //*[@id="main"]/h2(title)
import requests
import os
from lxml import etree
import random
import re
from time import sleep

headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"},
    { 'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
    {'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
    { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
]
# if not os.path.exists('./X站视频下载/'):  # 创建文件目录
#     os.mkdir('./X站视频下载/')
acounts = 0
for page in range(2):
    print('========第{}页爬取开始========'.format(page+1))
    if page == 0:
        URL = 'https://www.xvideos.com/channels/hmjmtokyo/videos/best'
    else:
        URL = 'https://www.xvideos.com/channels/hmjmtokyo/videos/best/{}'.format(page)
    # url = 'https://www.xvideos.com/video63108659/the_ryujin_hip_trend_pmv'
    session = requests.Session()  # 创建Session对象
    session.get(URL, headers=random.choice(headers_list))  # 捕获且存储cookie
    # 获取主页源码
    response_page_main = session.get(URL,headers=random.choice(headers_list)).text#.encode('iso-8859-1').decode('gbk')# print(res.
    sleep(random.randint(1,2))
    tree = etree.HTML(response_page_main)
    user_name = tree.xpath('//*[@id="video_60472487"]/div[2]/p[2]/span/span[3]/a/span/text()')[0]
    # 获取详情页div表
    url_detail_page_list = tree.xpath('//div[@class="mozaique cust-nb-cols"]/div')#//*[@id="tabVideos"]/div[1]/div[4]
    while url_detail_page_list == []:#防止网络问题拿到空列表
        print("正在重连")
        response_page_main = session.get(URL, headers=random.choice(
            headers_list)).text  # .encode('iso-8859-1').decode('gbk')# print(res.
        tree = etree.HTML(response_page_main)
        url_detail_page_list = tree.xpath('//div[@class="mozaique cust-nb-cols"]/div')#//*[@id="tabVideos"]/div[1]/div[4]/divclass="mozaique cust-nb-cols"
        user_name = tree.xpath('//*[@id="video_60472487"]/div[2]/p[2]/span/span[3]/a/span/text()')[0]
    # print(url_detail_page_list)
    # 遍历详情页div表取出详情页地址
    for url_detail_page in url_detail_page_list:
        url_detail_page_0 = url_detail_page.xpath('./div[@class="thumb-under"]//a/@href')[0]#/html/body/div[1]/div[4]/div[3]
        # /div[2]/div[2]/div[1]/div[4]/div/div[1]/div[1]/div/a/img
        url_detail_page_0 = re.findall('\d{8}/.*',url_detail_page_0,re.S)[0]
        # print(url_detail_page_0)
        url_detail_0 = 'https://www.xvideos.com/video' +url_detail_page_0 #详情页地址
        response_url_detail_0 = session.get(url_detail_0,headers=random.choice(headers_list)).text#详情页源码
        tree = etree.HTML(response_url_detail_0)
        # print(url_detail_0)
        title_video = tree.xpath('//*[@id="main"]/h2/text()')[0]#视频标题
        # print(title_video)
        # title_video = title_video.replace('&sol;','_')[0]
        # title_video = title_video.replace(' ','_')[0]
        # print(title_video)
        if not os.path.exists('./X站视频下载/{}/'.format(user_name)):  # 创建文件目录
            os.mkdir('./X站视频下载/{}/'.format(user_name))
        path_video = './X站视频下载/{}/'.format(user_name) + title_video +'.mp4' #视频地址
        if os.path.exists(path_video):#过滤已经下过的视频
            print('文件{}.mp4已存在'.format(title_video))
            acounts +=1
        else:
            url_VideoHLS_m3u8_list = tree.xpath('//*[@id="video-player-bg"]/script[4]/text()')#m3u8文本
            # print(url_VideoHLS_m3u8)
            # print(url_VideoHLS_m3u8_list)
            ex = "'(https://hls.*?m3u8.*?)'"
            ex_00 = ".*(https?.*?.m3u8)"
            for line in url_VideoHLS_m3u8_list:#遍历文本，观察到m3u8地址有两种匹配形式
                # print(line)
                # url_VideoHLS_m3u8 = re.findall(ex,line,re.S)[0]
                if re.findall(ex,line,re.S) ==[]:
                    url_VideoHLS_m3u8 = re.findall(ex_00,line,re.S)[0]#获得m3u8地址
                else:
                    url_VideoHLS_m3u8 = re.findall(ex,line,re.S)[0]
            text_m3u8_geshi = session.get(url_VideoHLS_m3u8,headers=random.choice(headers_list)).text.split('\n')#发现是一个真正视频m3u8的text
            ex_0 = '(http.*/)hls'
            m3u8_qianzui = re.findall(ex_0,url_VideoHLS_m3u8,re.S)[0]#真实m3u8的前缀

            url_m3u8_list = {}
            for line_1 in text_m3u8_geshi:#遍历文本挑选格式
                if 'hls-1080' in line_1:
                    url_ts = m3u8_qianzui + line_1
                    url_m3u8_list['1080'] = url_ts
                    continue
                elif 'hls-720' in line_1:
                    url_ts = m3u8_qianzui + line_1
                    url_m3u8_list['720'] = url_ts
                    continue
                elif 'hls-480' in line_1:
                    url_ts = m3u8_qianzui + line_1
                    url_m3u8_list['480'] = url_ts
                    continue
            acounts_0 = 0
            if '1080' in url_m3u8_list.keys():
                text_m3u8_list = session.get(url=url_m3u8_list['1080'], headers=random.choice(headers_list)).text.split('\n')
                ts_list = []#用来装ts的列表
                for line_2 in text_m3u8_list:
                    if 'ts' in line_2:
                        ts_list.append(line_2)
                print('========第{}个视频{}.mp4（1080p）下载开始========'.format(acounts + 1, title_video))
                for ts in ts_list:
                    ts_finally = m3u8_qianzui + ts
                    ts = session.get(ts_finally, headers=random.choice(headers_list)).content
                    with open(path_video, 'ab') as fp:
                        fp.write(ts)
                        acounts_0 += 1
                        print('第{}个{}.ts下载成功'.format(acounts_0, title_video))
                acounts += 1
                print('========第{}个视频{}.mp4（1080p）下载成功========'.format(acounts, title_video))
                continue
            elif '720' in url_m3u8_list.keys():
                text_m3u8_list = session.get(url=url_m3u8_list['720'], headers=random.choice(headers_list)).text.split(
                    '\n')
                ts_list = []  # 用来装ts的列表
                for line_2 in text_m3u8_list:
                    if 'ts' in line_2:
                        ts_list.append(line_2)
                print('========第{}个视频{}.mp4（720p）下载开始========'.format(acounts + 1, title_video))
                for ts in ts_list:
                    ts_finally = m3u8_qianzui + ts
                    ts = session.get(ts_finally, headers=random.choice(headers_list)).content
                    with open(path_video, 'ab') as fp:
                        fp.write(ts)
                        acounts_0 += 1
                        print('第{}个{}.ts下载成功'.format(acounts_0, title_video))
                acounts += 1
                print('========第{}个视频{}.mp4（720p）下载成功========'.format(acounts, title_video))
                continue
            elif '480' in url_m3u8_list.keys():
                text_m3u8_list = session.get(url=url_m3u8_list['480'], headers=random.choice(headers_list)).text.split(
                    '\n')
                ts_list = []  # 用来装ts的列表
                for line_2 in text_m3u8_list:
                    if 'ts' in line_2:
                        ts_list.append(line_2)
                print('========第{}个视频{}.mp4下载开始（480p）========'.format(acounts + 1, title_video))
                for ts in ts_list:
                    ts_finally = m3u8_qianzui + ts
                    ts = session.get(ts_finally, headers=random.choice(headers_list)).content
                    with open(path_video, 'ab') as fp:
                        fp.write(ts)
                        acounts_0 += 1
                        print('第{}个{}.ts下载成功'.format(acounts_0, title_video))
                acounts += 1
                print('========第{}个视频{}.mp4下载成功（480p）========'.format(acounts, title_video))
                continue
    print('========第{}页爬取成功========'.format(page+1))