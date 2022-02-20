import requests
from lxml import etree
import config
import random



headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
ips = config.ips
def get_page_text(url,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        page_text = requests.get(url=url, headers=headers,proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        if acount == 10:
            # print()
            return
        acount += 1
        get_page_text(url,acount)
    else:
        return page_text

def get_page_text_detail(url_detail,acount):
    proxies = random.choice(ips)
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        page_text_detail = requests.get(url=url_detail, headers=headers,proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        if acount == 10:
            return
        acount += 1
        get_page_text_detail(url_detail,acount)
    else:
        return page_text_detail

def get_m3u8(m3u8_url,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        m3u8 = requests.get(url=m3u8_url,headers=headers,proxies=proxies)
        if m3u8.status_code == 200 or m3u8.status_code == 503:
            m3u8 = m3u8.text
        else:
            raise ValueError
    except:

        ips.remove(proxies)
        print('删除连接超时Ip---{}-get_m3u8'.format(proxies))
        if acount == 20:
            return
        acount += 1
        get_m3u8(m3u8_url,acount)
    else:
        return m3u8

def get_ts(url_ts_,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        ts = requests.get(url=url_ts_, proxies=proxies,headers=headers)
        if ts.status_code != 200:
            raise ValueError
    except:
        if acount == 10:
            return
        acount += 1
        get_ts(url_ts_,acount)
    else:
        return ts
def get_url_detail_list(a,b):
    url_detail_lists = []
    for page in range(a,b+1):
        URL = 'https://cableav.tv/playlist/gIukReynhD7/page/%d/'%page
        page_text = get_page_text(url=URL,acount=0)
        if page_text:
            # page_text = requests.get(url=URL,headers=headers)
            tree1 = etree.HTML(page_text.text)
            user_name = tree1.xpath('//h1/text()')[0]
            cun1 = config.conn.sadd('cableav_user_name',user_name)
            if cun1 == 1:
                config.conn.zadd('cableav_user_url',URL,1)
            url_detail_list = tree1.xpath('//h3[@class="entry-title h3 post-title"]/a/@href')
            url_detail_lists += url_detail_list
    return url_detail_lists
    # print('开始遍历--{}'.format(user_name))
def get_mian(url_detail):
    url_detail_set = config.conn.sadd('cableav_url_detail', url_detail)
    if url_detail_set == 1:
        config.conn.srem('cableav_url_detail', url_detail)
        # url = 'https://cableav.tv/r98IzG0aF5a/?playlist=54487'
        #     page_text_detail = requests.get(url=url_detail,headers=headers)
        page_text_detail = get_page_text_detail(url_detail=url_detail, acount=0)
        if page_text_detail:
            tree = etree.HTML(page_text_detail.text)
            name_video = tree.xpath('/html/head/title/text()')[0]
            # “?”、“、”、“╲”、“/”、“*”、““”、“”“、“<”、“>”、“|”
            # name_video = 'agja?gag|gjg'
            for i in ['?', '\\', '/', '*', '<', '>', '|']:
                if i in name_video:
                    name_video = name_video.replace(i, '')
            path_video = 'F:\cableav' + '\\' + name_video + '.mp4'
            url_m3u8 = tree.xpath('///html/head/meta[4]/@content')[0]
            name_video_set = config.conn.sadd('name_video_set',name_video)
            config.conn.sadd('cableav_url_m3u8', url_m3u8)
            if name_video_set == 1:
                config.conn.srem('name_video_set', name_video)
                config.conn.srem('cableav_url_m3u8', url_m3u8)
                m3u8 = get_m3u8(m3u8_url=url_m3u8, acount=0)
                if m3u8:
                    print('得到{}'.format(url_m3u8))
                    ts_list = []
                    for line in m3u8.split('\n'):
                        if 'ts' in line:
                            url_ts = '/'.join(url_m3u8.split('/')[:-1]) + '/' + line
                            ts_list.append(url_ts)
                    print('开始下载{}.mp4'.format(name_video))
                    # t1 = tqdm(total=ts_list)
                    for url_ts in ts_list:
                        ts_set = config.conn.sadd('cableav_ts_url', url_ts)
                        if ts_set == 1:
                            config.conn.srem('cableav_ts_url', url_ts)
                            ts = get_ts(url_ts_=url_ts, acount=0)
                            if ts:
                                # ts = requests.get(url=url_ts, headers=headers)
                                with open(path_video, 'ab') as mf:
                                    mf.write(ts.content)
                                    # t1.update(1)
                                    config.conn.sadd('cableav_ts_url', url_ts)
                    # t1.close()
                    config.conn.sadd('cableav_url_m3u8', url_m3u8)
                    config.conn.sadd('cableav_url_detail', url_detail)
                    config.conn.sadd('name_video_set', name_video)
                    print('{}.mp4下载完成'.format(name_video))
if __name__ == '__main__':
    # print(len(get_url_detail_list(1, 3)))
    # print(get_url_detail_list(1,3))
    url_detail_list = get_url_detail_list(1,8)
    if len(url_detail_list):
        print('开始下载{}个视频'.format(len(url_detail_list)))
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(10) as tp:
            for url_detail in url_detail_list:
                tp.submit(get_mian,url_detail)

