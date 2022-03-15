import requests
import os
import re
from lxml import etree
import config
from time import sleep
from tqdm import tqdm
from config import conn
import random
import execjs
from concurrent.futures import ThreadPoolExecutor
import time,eventlet

def get_page_text_jiajin(url_jiajin_, acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'Accept-Language': 'zh-CN',
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
            'Accept-Language': 'zh-CN',
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
            'Accept-Language': 'zh-CN',
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
        if mp4.status_code == 200 or mp4.status_code == 206:
            print('mp4文件获取正常')
        else:
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
    IPs = ips_.smembers('ip_proxies_good')
    # IPs = ips_.smembers('ip_proxies_1')
    ips__ = []
    for IP in IPs:
        ip = bytes.decode(IP)
        # ips__.append({'http': ip,'https':'https://'+ip.split('/')[-1]})
        # ips__.append({'https': 'https://' + ip.split('/')[-1]})
        ips__.append({
            'http': ip,
            # 'https':ip,
                      })
    return ips__




path_ffmpeg = r'C:\软件安装\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\ffmpeg-N-104495-g945b2dcc63-win64-lgpl\bin'
def get_user(a, b):
    # n = 0
    m = 0
    for page in range(a, b + 1):
        print('第{}页解析'.format(page))
        url_jiajin_ = 'https://0316.workarea2.live/v.php?category=rf&viewtype=basic&page={}'.format(page)
        # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
        page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
        if page_text_jiajin is not None:
            tree = etree.HTML(page_text_jiajin)
            div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
            for div in div_list:
                url_jiajin_detail = div.xpath('./a/@href')[0]
                user = div.xpath('./text()')[5]
                user = user.strip()
                path_ = r'G:\ghs\91porn' + '\\' + user
                if not os.path.exists(path_):
                    os.mkdir(path_)
                    print(user)
                # page_text_jiajin_ = requests.get(url=url_jiajin_detail,headers=headers).text
                page_text_jiajin_ = get_page_text_jiajin_(url_jiajin_detail, acount=0)
                if page_text_jiajin_ is not None:
                    tree__ = etree.HTML(page_text_jiajin_)
                    try:
                        title = tree__.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0]
                        if title != 'guolifeng_513':
                            # // *[ @ id = "wrapper"] / div[1] / div[3] / div / div / div[1] / div / text()[2]
                            # user_name = conn.sadd('user_name',title)
                            # user_name = conn.zadd('user_name_', title, n)
                            user_name = conn.sadd('UN', title)
                            # n += 1
                            if user_name == 1:
                                URL__ = 'https://0316.workarea2.live/' + \
                                        tree__.xpath('//*[@id="videodetails-content"]/span[@class="title"]/a[1]/@href')[
                                            0]
                                # URL_list.append(URL__)
                                print('第{}页用户视频列表获取成功----{}---更新用户{}'.format(page, URL__, title))
                                # conn.zadd('91users_videos_list_url_guonei_', URL__, m)
                                conn.sadd("91jingxuan", URL__)
                                m += 1
                        else:
                            print(title)
                    except:
                        print('没拿到用户名')





def get_jiajin(page_jiajin):
    print('第{}页解析'.format(page_jiajin))
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=ori&viewtype=basic&page={}'.format(page_jiajin)  # 91原创
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=hot&viewtype=basic&page={}'.format(page_jiajin)#当前最热
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=long&viewtype=basic&page={}'.format(page_jiajin)#10分钟以上
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=longer&viewtype=basic&page={}'.format(page_jiajin)#20分钟以上
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=top&viewtype=basic&page={}'.format(page_jiajin)#本月最热
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=md&viewtype=basic&page={}'.format(page_jiajin)#本月讨论
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=top&m=-1&viewtype=basic&page={}'.format(page_jiajin)#上月最热
    url_jiajin_ = yuming+'/v.php?next=watch&page={}'.format(page_jiajin)#最新视频页面
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=hd&viewtype=basic&page={}'.format(page_jiajin)#高清视频页面
    # url_jiajin_ = 'https://0316.workarea2.live/v.php?category=rf&viewtype=basic&page={}'.format(page_jiajin)
    # url_jiajin_ = yuming+'/v.php?category=mf&viewtype=basic&page={}'.format(page_jiajin)




    # page_text_jiajin = requests.get(url=url_jiajin_,headers=headers).text
    page_text_jiajin = get_page_text_jiajin(url_jiajin_=url_jiajin_, acount=0)
    if page_text_jiajin is not None:
        tree = etree.HTML(page_text_jiajin)
        div_list = tree.xpath('//*[@class="well well-sm videos-text-align"]')
        for div in div_list:
            url_jiajin_detail = div.xpath('./a/@href')[0]
            viewkey = re.compile('viewkey=(.*?)&page').findall(url_jiajin_detail)[0]
            user_name_ = div.xpath('./text()')[5]
            user_name_ = user_name_.strip().replace('.','')
            video_name_ = div.xpath('./a/span[@class="video-title title-truncate m-t-5"]/text()')[0].replace \
                        (':', '').replace('!', '').replace('|', '').replace('*', '').replace('?','').replace('[原创]','').strip()
            user_name_ = user_name_.strip()
            path_mp4 = r'G:\ghs\91porn' + '\\' + user_name_ + '\\' + user_name_ + video_name_ + '.mp4'
            if user_name_ in path_list:
                url_detail_test = conn.sadd('url_video', viewkey)
################################################################################################################
                def download_ts():
                    print('{}用户存在，开始下载视频{}\n视频地址：{}'.format(user_name_,video_name_, url_jiajin_detail))
                    # 删除键值
                    conn.srem('url_video', viewkey)
                    page_text_detail = get_page_text_detail(url_jiajin_detail, acount=0)
                    if page_text_detail is not None:
                        page_text_detail = page_text_detail.text
                        tree_ = etree.HTML(page_text_detail)
                        video_name = tree_.xpath('/html/head/title/text()')[0]
                        video_name = video_name.replace('?', '').replace('Chinese homemade video', '').strip().replace \
                            (':', '').replace('!', '').replace('|', '').replace('*', '').replace('[原创]','')
                        user_name = tree_.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0].replace('.','')
                        path_mp4 = r'G:\ghs\91porn' + '\\' + user_name + '\\' + user_name + video_name + '.ts'
                        # UID = tree_.xpath('//div[@id=VID]/text()')[0]t
                        VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]
                        if len(VID) == 0:
                            VID = re.compile('VID=(d+)').findall(page_text_detail)[0]
                        # m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
                        m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
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
                                        url_ts = 'https://ccn.killcovid2021.com//m3u8/{}/'.format(VID) + ts_
                                        ts_list.append(url_ts)
                                # print('ts数量为{}'.format(len(ts_list)))
                                pbar = tqdm(total=len(ts_list))
                                for url_ts_ in ts_list:
                                    ts_id = url_ts_.replace('.ts', '').split('/')[-1]
                                    # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                                    ts_url = conn.sadd('ts_url', ts_id)
                                    # 返回1即插入成功，返回零即该url已存在
                                    if ts_url == 0:
                                        # print('该ts数据已经下载')
                                        pbar.update(1)
                                        continue
                                    else:
                                        # 删除刚刚插入的值
                                        conn.srem('ts_url', ts_id)
                                        ts = get_ts(url_ts_, acount=0)
                                        # ts = requests.get(url=url_ts_, headers=headers).content
                                        if ts.status_code == 200:
                                            with open(path_mp4, 'ab') as fp:
                                                fp.write(ts.content)
                                                # 写入成功再添加值
                                                conn.sadd('ts_url', ts_id)
                                                pbar.update(1)
                                pbar.close()
                                eventlet.monkey_patch()  # 必须加这条代码
                                try:
                                    with eventlet.Timeout(15, False):
                                        try:
                                            os.chdir(path_ffmpeg)
                                            os.system("ffmpeg -i \"{}\" -acodec copy -vcodec copy -f mp4 \"{}\"".
                                                      format(path_mp4,path_mp4.replace(".ts",'.mp4')))
                                            if os.path.exists(path_mp4.replace(".ts",'.mp4')) and os.path.exists(path_mp4):
                                                os.remove(path_mp4)
                                                print("文件转换成mp4完成，删除ts完成")
                                            # 该视频下载完成后添加键值
                                        except:
                                            pass
                                except :
                                    if os.path.exists(path_mp4.replace(".ts", '.mp4')) and os.path.exists(path_mp4):
                                        os.remove(path_mp4.replace(".ts", '.mp4'))
                                        print("转换超时，删除废弃mp4完成")
                                    # 该视频下载完成后添加键值
                                    # print(Exception)
                                print(
                                    '————————————————————————————————————————视频{}---{}下载成功'.format(user_name_, video_name))
                                list_all.append(user_name_ + video_name)
                                conn.sadd('url_video', viewkey)
                        else:
                            print('该地址应该为mp4')
                            try:
                                st_yuanma = re.compile('strencode2\("(.*?)"\)').findall(page_text_detail)[0]
                                print('st={}'.format(st_yuanma))
                            except:
                                print("没拿到地址" + url_jiajin_detail)
                            else:
                                try:
                                    print('解密成功')
                                    note = execjs.get()
                                    # ctx = node.compile(open('./steam.js',encoding='utf-8').read())
                                    ctx = note.compile(open('91porn_mp4地址_st值逆向.js', encoding='utf-8').read())

                                    # 执行js函数
                                    funcName = 'get_st("{}")'.format(st_yuanma)
                                    st_ = ctx.eval(funcName)
                                    # print(st)
                                    st = re.compile("src=\'(.*)\' type").findall(st_)[0]
                                    # url_video_mp4 = 'https://cdn.workgreat14.live//mp43/' + st.split('/')[-1]
                                    url_video_mp4 = 'https://ccn.killcovid2021.com'+'//mp43/' + st.split('/')[-1]
                                    print(url_video_mp4)
                                    if not os.path.exists(path_mp4):
                                        tq = tqdm(total=1)
                                        # mp4 = requests.get(url=url_video_mp4,headers=headers).content
                                        mp4 = get_mp4(url_video_mp4, acount=0)

                                        if mp4.status_code == 200:
                                            with open(path_mp4.replace('ts', 'mp4'), 'wb') as m:
                                                m.write(mp4.content)
                                                tq.update(1)
                                                tq.close()
                                                print('{}'.format(user_name_ + video_name))
                                                list_all.append(user_name_ + video_name)
                                                conn.sadd('url_video', viewkey)
                                except:
                                    print('文件还未转换完成')
####################################################################################################################
                if url_detail_test == 0 and not os.path.exists(path_mp4) and not os.path.exists(path_mp4.replace('.mp4', '.ts')):
                    # viewkey插入失败，缺失mp4和ts
                    # 直接调用download
                    # ts, 先删除ts_url, 下载完再添加回去
                    print('0:0:0viewkey插入失败，缺失mp4和ts')
                    print('{}用户存在，开始下载视频{}\n视频地址：{}'.format(user_name_,video_name_, url_jiajin_detail))
                    # 删除键值
                    conn.srem('url_video', viewkey)
                    page_text_detail = get_page_text_detail(url_jiajin_detail, acount=0)
                    if page_text_detail is not None:
                        page_text_detail = page_text_detail.text
                        tree_ = etree.HTML(page_text_detail)
                        video_name = tree_.xpath('/html/head/title/text()')[0]
                        video_name = video_name = video_name.replace('?', '').replace('Chinese homemade video', '').strip().replace \
                            (':', '').replace('!', '').replace('|', '').replace('*', '').replace('[原创]','')
                        user_name = tree_.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0].replace('.','')
                        path_mp4 = r'G:\ghs\91porn' + '\\' + user_name + '\\' + user_name + video_name + '.ts'
                        # UID = tree_.xpath('//div[@id=VID]/text()')[0]t
                        VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]
                        if len(VID) == 0:
                            VID = re.compile('VID=(d+)').findall(page_text_detail)[0]
                        # m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
                        m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
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
                                        url_ts = 'https://ccn.killcovid2021.com//m3u8/{}/'.format(VID) + ts_
                                        ts_list.append(url_ts)
                                # print('ts数量为{}'.format(len(ts_list)))
                                pbar = tqdm(total=len(ts_list))
                                for url_ts_ in ts_list:
                                    ts_id = url_ts_.replace('.ts', '').split('/')[-1]
                                    # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                                    # ts_url = conn.sadd('ts_url', ts_id)
                                    # # 返回1即插入成功，返回零即该url已存在
                                    # if ts_url == 0:
                                    #     # print('该ts数据已经下载')
                                    #     pbar.update(1)
                                    #     continue
                                    # else:
                                    #     # 删除刚刚插入的值
                                    conn.srem('ts_url', ts_id)
                                    ts = get_ts(url_ts_, acount=0)
                                    # ts = requests.get(url=url_ts_, headers=headers).content
                                    if ts.status_code == 200:
                                        with open(path_mp4, 'ab') as fp:
                                            fp.write(ts.content)
                                            # 写入成功再添加值
                                            conn.sadd('ts_url', ts_id)
                                            pbar.update(1)
                                pbar.close()
                                eventlet.monkey_patch()  # 必须加这条代码
                                try:
                                    with eventlet.Timeout(15, False):
                                        try:
                                            os.chdir(path_ffmpeg)
                                            os.system("ffmpeg -i \"{}\" -acodec copy -vcodec copy -f mp4 \"{}\"".
                                                      format(path_mp4, path_mp4.replace(".ts", '.mp4')))
                                            if os.path.exists(path_mp4.replace(".ts", '.mp4')) and os.path.exists(
                                                    path_mp4):
                                                os.remove(path_mp4)
                                                print("文件转换成mp4完成，删除ts完成")
                                            # 该视频下载完成后添加键值
                                        except:
                                            pass
                                except:
                                    if os.path.exists(path_mp4.replace(".ts", '.mp4')) and os.path.exists(path_mp4):
                                        os.remove(path_mp4.replace(".ts", '.mp4'))
                                        print("转换超时，删除废弃mp4完成")

                                    # print(Exception)
                                # 该视频下载完成后添加键值
                                print(
                                    '————————————————————————————————————————视频{}---{}下载成功'.format(user_name_, video_name))
                                list_all.append(user_name_ + video_name)
                                conn.sadd('url_video', viewkey)
                        else:
                            print('该地址应该为mp4')
                            try:
                                st_yuanma = re.compile('strencode2\("(.*?)"\)').findall(page_text_detail)[0]
                                print('st={}'.format(st_yuanma))
                            except:
                                print("没拿到地址" + url_jiajin_detail)
                            else:
                                try:
                                    print('解密成功')
                                    note = execjs.get()
                                    # ctx = node.compile(open('./steam.js',encoding='utf-8').read())
                                    ctx = note.compile(open('91porn_mp4地址_st值逆向.js', encoding='utf-8').read())

                                    # 执行js函数
                                    funcName = 'get_st("{}")'.format(st_yuanma)
                                    st_ = ctx.eval(funcName)
                                    # print(st)
                                    st = re.compile("src=\'(.*)\' type").findall(st_)[0]
                                    # url_video_mp4 = 'https://cdn.workgreat14.live//mp43/' + st.split('/')[-1]
                                    url_video_mp4 = 'https://ccn.killcovid2021.com'+'//mp43/' + st.split('/')[-1]
                                    print(url_video_mp4)
                                    if not os.path.exists(path_mp4):
                                        tq = tqdm(total=1)
                                        # mp4 = requests.get(url=url_video_mp4,headers=headers).content
                                        mp4 = get_mp4(url_video_mp4, acount=0)

                                        if mp4.status_code == 200:
                                            with open(path_mp4.replace('ts', 'mp4'), 'wb') as m:
                                                m.write(mp4.content)
                                                tq.update(1)
                                                tq.close()
                                                print('{}'.format(user_name_ + video_name))
                                                list_all.append(user_name_ + video_name)
                                                conn.sadd('url_video', viewkey)
                                except:
                                    print('文件未转换完成')

                elif url_detail_test == 0 and not os.path.exists(path_mp4) and os.path.exists(path_mp4.replace('.mp4', '.ts')):
                # 已经下载完成
                    pass
                elif url_detail_test == 0 and os.path.exists(path_mp4) and not os.path.exists(path_mp4.replace('.mp4', '.ts')):
                # 已经下载完成
                    pass
                elif url_detail_test == 1 and not os.path.exists(path_mp4) and not os.path.exists(path_mp4.replace('.mp4', '.ts')):
                # 全新的文件，直接下载
                    print('1:0:0全新的文件，直接下载')
                    download_ts()
                elif url_detail_test == 0 and os.path.exists(path_mp4) and os.path.exists(path_mp4.replace('.mp4', '.ts')):
                # 文件重复，删除MP4（此时的mp4未解码）
                    print('0:1:1文件重复，删除MP4（此时的mp4未解码）')
                    os.remove(path_mp4)
                    print("文件重复删除"+path_mp4)
                elif url_detail_test == 1 and not os.path.exists(path_mp4) and os.path.exists(path_mp4.replace('.mp4', '.ts')):
                # ts没下完,直接下载
                    print('1:0:1','ts没下完,直接下载')
                    download_ts()
                elif url_detail_test == 1 and os.path.exists(path_mp4) and not os.path.exists(path_mp4.replace('.mp4', '.ts')):
                # mp4 没下完，直接下载（应该记得在代码中修改）
                    print('mp4 没下完，直接下载（应该记得在代码中修改）')
                    print('{}用户存在，开始下载视频{}\n视频地址：{}'.format(user_name_,video_name_, url_jiajin_detail))
                    # 删除键值
                    conn.srem('url_video', viewkey)
                    page_text_detail = get_page_text_detail(url_jiajin_detail, acount=0)
                    if page_text_detail is not None:
                        page_text_detail = page_text_detail.text
                        tree_ = etree.HTML(page_text_detail)
                        video_name = tree_.xpath('/html/head/title/text()')[0]
                        video_name = video_name = video_name.replace('?', '').replace('Chinese homemade video', '').strip().replace \
                            (':', '').replace('!', '').replace('|', '').replace('*', '').replace('[原创]','')
                        user_name = tree_.xpath('//*[@id="videodetails-content"]/div[2]/span[2]/a[1]/span/text()')[0].replace('.','')
                        path_mp4 = r'G:\ghs\91porn' + '\\' + user_name + '\\' + user_name + video_name + '.mp4'
                        # UID = tree_.xpath('//div[@id=VID]/text()')[0]t
                        VID = re.compile('id=VID.*?>(\d+)<').findall(page_text_detail)[0]
                        if len(VID) == 0:
                            VID = re.compile('VID=(d+)').findall(page_text_detail)[0]
                        # m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
                        m3u8_url = 'https://ccn.killcovid2021.com//m3u8/{}/{}.m3u8'.format(VID, VID)
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
                                        url_ts = 'https://ccn.killcovid2021.com//m3u8/{}/'.format(VID) + ts_
                                        ts_list.append(url_ts)
                                # print('ts数量为{}'.format(len(ts_list)))
                                pbar = tqdm(total=len(ts_list))
                                for url_ts_ in ts_list:
                                    ts_id = url_ts_.replace('.ts', '').split('/')[-1]
                                    # 往redis的ts_url 集合中插入数据，来去重（持久化去重）
                                    ts_url = conn.sadd('ts_url', ts_id)
                                    # 返回1即插入成功，返回零即该url已存在
                                    if ts_url == 0:
                                        # print('该ts数据已经下载')
                                        pbar.update(1)
                                        continue
                                    else:
                                        # 删除刚刚插入的值
                                        conn.srem('ts_url', ts_id)
                                        ts = get_ts(url_ts_, acount=0)
                                        # ts = requests.get(url=url_ts_, headers=headers).content
                                        if ts.status_code == 200:
                                            with open(path_mp4, 'ab') as fp:
                                                fp.write(ts.content)
                                                # 写入成功再添加值
                                                conn.sadd('ts_url', ts_id)
                                                pbar.update(1)
                                pbar.close()
                                eventlet.monkey_patch()  # 必须加这条代码
                                try:
                                    with eventlet.Timeout(15, False):
                                        try:
                                            os.chdir(path_ffmpeg)
                                            os.system("ffmpeg -i \"{}\" -acodec copy -vcodec copy -f mp4 \"{}\"".
                                                      format(path_mp4, path_mp4.replace(".ts", '.mp4')))
                                            if os.path.exists(path_mp4.replace(".ts", '.mp4')) and os.path.exists(
                                                    path_mp4):
                                                os.remove(path_mp4)
                                                print("文件转换成mp4完成，删除ts完成")
                                            # 该视频下载完成后添加键值
                                        except:
                                            pass
                                except:
                                    if os.path.exists(path_mp4.replace(".ts", '.mp4')) and os.path.exists(path_mp4):
                                        os.remove(path_mp4.replace(".ts", '.mp4'))
                                        print("转换超时，删除废弃mp4完成")
                                    # 该视频下载完成后添加键值
                                    # print(Exception)
                                # 该视频下载完成后添加键值
                                print(
                                    '————————————————————————————————————————视频{}---{}下载成功'.format(user_name_, video_name))
                                list_all.append(user_name_ + video_name)
                                conn.sadd('url_video', viewkey)
                                os.renames(path_mp4,path_mp4.replace('.mp4','.ts'))
                        else:
                            print('该地址应该为mp4')
                            try:
                                st_yuanma = re.compile('strencode2\("(.*?)"\)').findall(page_text_detail)[0]
                                print('st={}'.format(st_yuanma))
                            except:
                                print("没拿到地址" + url_jiajin_detail)
                            else:
                                try:
                                    print('解密成功')
                                    note = execjs.get()
                                    # ctx = node.compile(open('./steam.js',encoding='utf-8').read())
                                    ctx = note.compile(open('91porn_mp4地址_st值逆向.js', encoding='utf-8').read())

                                    # 执行js函数
                                    funcName = 'get_st("{}")'.format(st_yuanma)
                                    st_ = ctx.eval(funcName)
                                    # print(st)
                                    st = re.compile("src=\'(.*)\' type").findall(st_)[0]
                                    # url_video_mp4 = 'https://cdn.workgreat14.live//mp43/' + st.split('/')[-1]
                                    url_video_mp4 = 'https://ccn.killcovid2021.com'+'//mp43/' + st.split('/')[-1]

                                    print(url_video_mp4)
                                    if not os.path.exists(path_mp4):
                                        tq = tqdm(total=1)
                                        # mp4 = requests.get(url=url_video_mp4,headers=headers).content
                                        mp4 = get_mp4(url_video_mp4, acount=0)

                                        if mp4.status_code == 200:
                                            with open(path_mp4.replace('ts', 'mp4'), 'wb') as m:
                                                m.write(mp4.content)
                                                tq.update(1)
                                                tq.close()
                                                print('{}'.format(user_name_ + video_name))
                                                list_all.append(user_name_ + video_name)
                                                conn.sadd('url_video', viewkey)
                                    else:
                                        print('文件已存在 ')
                                        conn.sadd('url_video', viewkey)
                                except:
                                    print('文件未转换完成')
                    elif url_detail_test == 1 and os.path.exists(path_mp4) and os.path.exists(path_mp4.replace('.mp4', '.ts')):
                    # ts没下完，删除mp4文件
                        print('1:1:1ts没下完，删除mp4文件')
                        os.remove(path_mp4)
                        download_ts()
# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText
# def my_send_email(title,content_html,from_email,to_email):
#     # 邮件内容
#     message = MIMEText(content_html,'html','utf-8')
#     #邮件信息
#     message['Subject']=Header(title,'utf-8')
#     message['From'],message['To']=from_email,to_email
#
#     # 使用qq邮箱服务，发送邮件
#     smtpObj = smtplib.SMTP_SSL('smtp.qq.com',465)
#     smtpObj.login(from_email,'ftfuaelmflfcbdhj')
#     smtpObj.sendmail(from_email,[to_email],message.as_string())
#     smtpObj.quit()

if __name__ == '__main__':
    yuming = 'https://g1015.91p47.com'
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
            # session.get(url='https://0316.workarea2.live/index.php', headers=headers, proxies=proxies, timeout=10)
            session.get(url=yuming+'/index.php', headers=headers, proxies=proxies, timeout=10)
        except:
            print('重试中')
            i += 1
        else:
            i = 10

    path_list = os.listdir(r'G:\ghs\91porn')
    # get_user(1,1)
    while True:
        list_all = []
        with ThreadPoolExecutor(10) as tp:
            url_list = [i for i in list(range(1,50))]
            for page_jiajin in url_list:
                # a = random.choice(url_list)
                tp.submit(get_jiajin, str(page_jiajin))
                # url_list.remove(a)
        for i in list_all:
            print(i)
        print('更新视频个数为'+str(len(list_all)))

        from smtplib邮件通知 import my_send_email
        my_send_email("标题：91porn用户视频更新",
                      "<h1>更新视频个数为：{}<h1>更新的视频文件详情列表为：<br>{}".format(len(list_all),'<br>'.join(list_all)),
                      "2319423737@qq.com",
                      "2319423737@qq.com", )
        print('更新完成,邮件发送完成，等待八个小时继续更新...')
        sleep(3600*8)