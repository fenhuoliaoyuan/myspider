import requests
import os
import re
from lxml import etree
import random
import config
from time import sleep
from tqdm import tqdm
from config import conn
from proxies import proxies
import random
import execjs


def get_page_text_jiajin(url_jiajin_, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)

        page_text_jiajin = session.get(url=url_jiajin_, headers=headers, proxies=proxies)
        if page_text_jiajin.status_code != 200:
            raise ValueError
        page_text_jiajin = page_text_jiajin.text
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_jiajin(url_jiajin_, acount)
    else:
        return page_text_jiajin


def get_page_text_jiajin_(url_jiajin_detail, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_jiajin_ = session.get(url=url_jiajin_detail, headers=headers, proxies=proxies)
        if page_text_jiajin_.status_code != 200:
            raise ValueError
        page_text_jiajin_ = page_text_jiajin_.text
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_page_text_jiajin'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_jiajin_(url_jiajin_detail, acount)
    else:
        return page_text_jiajin_


def get_page_text(url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text = session.get(url=url, headers=headers, proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
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


def get_page_text_detail(url_detail, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 3:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        page_text_detail = session.get(url=url_detail, headers=headers, proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        acount += 1
        # print('重试中...')
        get_page_text_detail(url_detail, acount)
    else:
        return page_text_detail


def get_m3u8(m3u8_url, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 2:
        #     session.get(url='https://g0527.91p47.com', headers=headers, proxies=proxies)
        m3u8 = session.get(url=m3u8_url, headers=headers, proxies=proxies)
        if m3u8.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 5:
            # print('该视频地址应该为mp4,跳过')
            return
        acount += 1
        # print('重试中...')
        get_m3u8(m3u8_url, acount)
    else:
        return m3u8


def get_ts(url_ts_, acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        ts = session.get(url=url_ts_, proxies=proxies, headers=headers)
        if ts.status_code != 200:
            raise ValueError
    except:
        # ips.remove(proxies)
        # config.conn_1.srem('ip_proxies', proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_ts'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            # print()
            return
        # if acount == 2:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        acount += 1
        # print('重试中...')
        get_ts(url_ts_, acount)
    else:
        return ts


def get_mp4(url_video_mp4, acount):
    try:
        proxies = random.choice(ips)
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        # if acount == 10:
        #     session.get(url='https://g0527.91p47.com/index.php', headers=headers, proxies=proxies)
        # print(proxies)
        mp4 = session.get(url=url_video_mp4, headers=headers, proxies=proxies)
        if mp4.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # config.conn_1.srem('ip_proxies',proxies['http'])
        # print('redis删除无用IP成功-{}'.format(proxies['http']))
        # print('删除连接超时Ip---{}-get_mp4'.format(proxies))
        # print('ip池中ip个数还有{}'.format(len(ips)))
        if acount == 10:
            return
        acount += 1
        # print('重试中...')
        get_mp4(url_video_mp4, acount)
    else:
        return mp4


user_agent_list = config.get_ua()

# proxies =[{'http': 'http://' + '3.211.65.185:80',},
#           {'http': 'http://' + '173.192.128.238:9999'}]

URL_list = []


# ips = proxies.Proxy()
def get_ips():
    ips_ = config.conn_ip
    # IPs = ips_.smembers('ip_proxies_good')
    IPs = ips_.smembers('ip_proxies_1')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        # ips__.append({'http': ip,'https':'https://'+ip.split('/')[-1]})
        # ips__.append({'https': 'https://' + ip.split('/')[-1]})
        ips__.append({'http': ip})
    return ips__


ips = get_ips()
# 加精页面获取，获取用户视频列表地址

session = requests.Session()

i = 0
while i < 10:
    headers = {
        'user-agent': random.choice(user_agent_list),
    }
    proxies = random.choice(ips)
    try:
        session.get(url='https://0819.91p30.com/index.php', headers=headers, proxies=proxies, timeout=10)
    except:
        print('重试中')
        i += 1
    else:
        i = 10


def get_jiajin(a, b):
    # n = 0
    m = 0
    for page_jiajin in range(a, b + 1):
        print('第{}页解析'.format(page_jiajin))
        url_jiajin_ = 'https://0819.91p30.com/v.php?category=rf&viewtype=basic&page={}'.format(page_jiajin)
        # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
        page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
        if page_text_jiajin is not None:
            tree = etree.HTML(page_text_jiajin)
            div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
            for div in div_list:
                url_jiajin_detail = div.xpath('./a/@href')[0]
                # page_text_jiajin_ = requests.get(url=url_jiajin_detail,headers=headers).text
                page_text_jiajin_ = get_page_text_jiajin_(url_jiajin_detail, acount=0)
                if page_text_jiajin_ is not None:
                    tree__ = etree.HTML(page_text_jiajin_)
                    title = tree__.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0]
                    if title != 'guolifeng_513':
                        # // *[ @ id = "wrapper"] / div[1] / div[3] / div / div / div[1] / div / text()[2]
                        # user_name = conn.sadd('user_name',title)
                        # user_name = conn.zadd('user_name_', title, n)
                        user_name = conn.sadd('UN', title)
                        # n += 1
                        if user_name == 1:
                            URL__ = 'https://0819.91p30.com/' + \
                                    tree__.xpath('//*[@id="videodetails-content"]/span[@class="title"]/a[1]/@href')[0]
                            # URL_list.append(URL__)
                            print('第{}页用户视频列表获取成功----{}---更新用户{}'.format(page_jiajin, URL__, title))
                            # conn.zadd('91users_videos_list_url_guonei_', URL__, m)
                            conn.sadd("91jingxuan",URL__)
                            m += 1
                    else:
                        print(title)


# while True:
#     URL = input('例如：https://g0527.91p47.com/uvideos.php?UID=56b32VuYds27p8V4IB3ddGnmR6CJalE4c8iZB0EafCnNNLur&type=public \n输入你要添加的下载用户视频列表视频地址(若没有点击回车) :')
#     if URL != '':
#         URL_list.append(URL)
#     else:
#         # URL = 'https://www.91porn.com/uvideos.php?UID=2ee6XCROiUEaLyheXVbVFIS837SG5erMPqdjHgwim8GV5qhp&type=public'
#         break
# for URL_ in URL_list:
#     conn.sadd('91users_videos_list_url_guonei',URL_)
# users_videos_list_url = conn.smembers('91users_videos_list_url_guonei')
# users_videos_list_url = conn.zrange("91users_videos_list_url_guonei_",0,-1)
# users_videos_list_url = conn.zrange("91users_videos_list_url_guonei_",350,400)

# ips = proxies.Proxy()
# users_videos_list_url = ['https://g0527.91p47.com/uvideos.php?UID=2dc6hCnoYlNicZCARkrArfszQtI1dLL1oEQRyTrWMjHtxRtx&type=public']
# print('===================================================开始遍历{}个用户的视频列表'.format(len(users_videos_list_url)))
def main(users_videos_list_):
    # print(users_videos_list_)
    # ips = proxies.Proxy()
    # URL = 'https://0316.workarea2.live/' + bytes.decode(users_videos_list_).split('/')[-1]
    URL = 'https://0819.91p30.com/' + bytes.decode(users_videos_list_).split('/')[-1]


    # URL = users_videos_list_
    print('===================================================开始遍历\n{}'.format(URL))
    # from selenium.webdriver.chrome.options import Options
    # from selenium import webdriver
    # chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # debuggerAddress调试器地址
    # chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"  # 驱动
    # bro = webdriver.Chrome(chrome_driver, options=chrome_options)
    # bro.get(URL)
    # start_page = input('输入你要下载的起始页码 ：')
    # end_page = input('输入你要下载的结束页码 ：')
    start_page = 1
    end_page = 10
    # path_root = input('例如：C:\番号\91porn \n输入你要存储视频的根目录 ：')
    path_root = r'G:\ghs\91porn'
    if not os.path.exists(path_root):
        os.mkdir(path_root)
    for page in range(int(start_page), int(end_page) + 1):
        # print('===================================================第{}页下载开始'.format(page))
        url = '{}&page={}'.format(URL,page)
        # headers = config.get_ua()
        # page_text = requests.get(url=url,headers=headers)
        # page_text.encoding = page_text.apparent_encoding
        # page_text = page_text.text
        # user_name = re.compile('>?(.*?)公开视频').findall(page_text)
        page_text = get_page_text(url=url, acount=0)
        page_text.encoding = page_text.apparent_encoding
        page_text = page_text.text
        tree = etree.HTML(page_text)
        user_name_ = tree.xpath('//*[@id="wrapper"]/div[1]/div[1]/h4/text()')[0]
        user_name = re.compile('(.*?)Public Videos').findall(user_name_)[0].strip()
        path_root_ = path_root + '\\' + user_name + '\\'
        if not os.path.exists(path_root_):
            os.mkdir(path_root_)
        div_list = tree.xpath('//div[@class="well well-sm"]')

        # div_len = tqdm(total=len(div_list))
        # 解析视频列表
        for div in div_list:
            url_detail = div.xpath('./a/@href')[0]
            title = div.xpath('./a/span/text()')[0]
            title = title.replace('?', '')
            title = title.replace(':', '')
            title = title.replace('!', '')
            title = title.replace('|', '')
            title = title.replace('*', '')
            path_mp4 = path_root_ + user_name + title + '.mp4'
            # mp4_title = conn.sadd('mp4_title',title)
            # if mp4_title == 0:
            #     print('{}.mp4已存在'.format(title))
            # else:
            # print('有新数据更新...')
            url_detail_test = conn.sadd('url_video', url_detail)
            if url_detail_test == 0:
                continue
            else:
                print('有新数据更新...')
                # 删除键值
                conn.srem('url_video', url_detail)
                print('==================================================={}.mp4下载开始---{}'.format(title, user_name))
                # page_text_detail = requests.get(url=url_detail, headers=headers)
                # page_text_detail.encoding = page_text_detail.apparent_encoding
                # page_text_detail = page_text_detail.text
                page_text_detail = get_page_text_detail(url_detail, acount=0).text
                # 对MP4或m3u8地址进行解密

                try:
                    st_yuanma = re.compile('strencode2\("(.*?)"\)').findall(page_text_detail)[0]
                except:
                    print('解密失败,正则匹配错误,转拼凑m3u8地址')
                    tree_ = etree.HTML(page_text_detail)
                    # UID = tree_.xpath('//div[@id=VID]/text()')[0]
                    # 获取m3u8
                    VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]

                    m3u8_url = 'https://cdn.91p07.com//m3u8/{}/{}.m3u8'.format(VID, VID)
                    print(m3u8_url)
                    m3u8 = get_m3u8(m3u8_url, acount=0)
                    # m3u8 = requests.get(url=m3u8_url, headers=headers).text
                    # 提取ts地址
                    if m3u8 is not None:
                        if m3u8.status_code == 200:
                            m3u8 = m3u8.text
                            ts_list = []
                            for ts_ in m3u8.split('\n'):
                                if 'ts' in ts_:
                                    url_ts = 'https://cdn.91p07.com//m3u8/{}/'.format(VID) + ts_
                                    ts_list.append(url_ts)
                            # print('ts数量为{}'.format(len(ts_list)))
                            pbar = tqdm(total=len(ts_list))
                            for url_ts_ in ts_list:
                                # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                                ts_url = conn.sadd('ts_url', url_ts_)
                                # 返回1即插入成功，返回零即该url已存在
                                if ts_url == 0:
                                    # print('该ts数据已经下载')
                                    pbar.update(1)
                                    continue
                                else:
                                    # 删除刚刚插入的值
                                    conn.srem('ts_url', url_ts_)
                                    ts = get_ts(url_ts_, acount=0)
                                    # ts = requests.get(url=url_ts_, headers=headers).content
                                    if ts.status_code == 200:
                                        with open(path_mp4, 'ab') as fp:
                                            fp.write(ts.content)
                                            # 写入成功再添加值
                                            conn.sadd('ts_url', url_ts_)
                                            pbar.update(1)
                            pbar.close()
                            # 该视频下载完成后添加键值
                            conn.sadd('url_video', url_detail)
                            conn.sadd('url_video_m3u8', m3u8_url)


                else:
                    print('解密成功')
                    note = execjs.get()
                    # ctx = node.compile(open('./steam.js',encoding='utf-8').read())
                    ctx = note.compile(open('91porn_mp4地址_st值逆向.js', encoding='utf-8').read())

                    # 执行js函数
                    funcName = 'get_st("{}")'.format(st_yuanma)
                    st_ = ctx.eval(funcName)
                    # print(st)
                    st = re.compile("src=\'(.*)\' type").findall(st_)[0]
                    if 'mp4' in st:
                        # 以mp4格式进行传输
                        # 对mp4地址继续解密
                        # try:
                        #     st_yuanma = re.compile('strencode2\("(.*?)"\)').findall(page_text_detail)[0]
                        # except:
                        #     print('正则匹配错误')
                        # else:
                        #     note = execjs.get()
                        #     # ctx = node.compile(open('./steam.js',encoding='utf-8').read())
                        #     ctx = note.compile(open('91porn_mp4地址_st值逆向.js', encoding='utf-8').read())
                        #
                        #     # 执行js函数
                        #     funcName = 'get_st("{}")'.format(st_yuanma)
                        #     st_ = ctx.eval(funcName)
                        #     # print(st)
                        #     st = re.compile("src=\'(.*)\' type").findall(st_)[0]
                        url_video_mp4 = 'https://cdn.91p07.com//mp43/' + st.split('/')[-1]
                        print(url_video_mp4)
                        test_mp4 = conn.sadd('url_video_mp4', url_video_mp4)
                        if test_mp4 == 1:
                            conn.srem('url_video_mp4', url_video_mp4)
                            tq = tqdm(total=1)
                            # mp4 = requests.get(url=url_video_mp4,headers=headers).content
                            mp4 = get_mp4(url_video_mp4, acount=0)

                            if mp4.status_code == 200:
                                with open(path_mp4, 'wb') as m:
                                    m.write(mp4.content)
                                    conn.sadd('url_video_mp4', url_video_mp4)
                                    conn.sadd('url_video', url_detail)
                                    tq.update(1)
                                    tq.close()
                                    print('{}下载成功'.format(title))

                    # 视频以ts格式传输
                    elif 'm3u8' in st:
                        # if page_text_detail is not None:
                        #     if page_text_detail.status_code == 200:
                        #     page_text_detail.encoding = page_text_detail.apparent_encoding
                        #     page_text_detail = page_text_detail.text
                        tree_ = etree.HTML(page_text_detail)
                        # UID = tree_.xpath('//div[@id=VID]/text()')[0]
                        # 获取m3u8
                        VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]

                        m3u8_url = 'https://cdn.91p07.com//m3u8/{}/{}.m3u8'.format(VID, VID)
                        print(m3u8_url)
                        m3u8 = get_m3u8(m3u8_url, acount=0)
                        # m3u8 = requests.get(url=m3u8_url, headers=headers).text
                        # 提取ts地址
                        if m3u8 is not None:
                            if m3u8.status_code == 200:
                                m3u8 = m3u8.text
                                ts_list = []
                                for ts_ in m3u8.split('\n'):
                                    if 'ts' in ts_:
                                        url_ts = 'https://cdn.91p07.com//m3u8/{}/'.format(VID) + ts_
                                        ts_list.append(url_ts)
                                # print('ts数量为{}'.format(len(ts_list)))
                                pbar_0 = tqdm(total=len(ts_list))
                                for url_ts_ in ts_list:
                                    # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                                    ts_url = conn.sadd('ts_url', url_ts_)
                                    # 返回1即插入成功，返回零即该url已存在
                                    if ts_url == 0:
                                        # print('该ts数据已经下载')
                                        pbar_0.update(1)
                                        continue
                                    else:
                                        # 删除刚刚插入的值
                                        conn.srem('ts_url', url_ts_)
                                        ts = get_ts(url_ts_, acount=0)
                                        # ts = requests.get(url=url_ts_, headers=headers).content
                                        if ts.status_code == 200:
                                            with open(path_mp4, 'ab') as fp:
                                                fp.write(ts.content)
                                                # 写入成功再添加值
                                                conn.sadd('ts_url', url_ts_)
                                                pbar_0.update(1)
                                pbar_0.close()
                                # 该视频下载完成后添加键值
                                conn.sadd('url_video', url_detail)
                                conn.sadd('url_video_m3u8', m3u8_url)


if __name__ == '__main__':
    # UN_ = conn.zrange("user_name_",1,-1)
    # for u in list(UN_):
    #     conn.sadd("UN",u)
    #     print("{}转换成功".format(u))
    # get_jiajin(1,3)
    # users_videos_list_url = conn.smembers('91users_videos_list_url_guonei')
    # users_videos_list_url = conn.zrange("91users_videos_list_url_guonei_",0,-1)
    # users_videos_list_url = conn.zrange("91users_videos_list_url_guonei_", 1,-1)
    users_videos_list_url = conn.smembers("91jingxuan")

    # 转换
    # for i in list(users_videos_list_url):
    #     conn.sadd("91jingxuan",i)
    #     print("插入{}成功".format(i))
    # ips = proxies.Proxy()
    # users_videos_list_url = ['https://g0527.91p47.com/uvideos.php?UID=2dc6hCnoYlNicZCARkrArfszQtI1dLL1oEQRyTrWMjHtxRtx&type=public']
    print('===================================================开始遍历{}个用户的视频列表'.format(len(users_videos_list_url)))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(100) as tp:
        for users_videos_list_ in list(users_videos_list_url)[::-1]:
            tp.submit(main, users_videos_list_)
