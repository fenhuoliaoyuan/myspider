import requests
from lxml import etree
import random
import config
import re
url = 'https://cn.pornhub.com/view_video.php?viewkey=ph60d3899c2cadb'
headers = {
            # 'accept-language': 'zh-CN',
            'user-agent': random.choice(config.user_agent_list),
        }
page_text = requests.get(url=url,headers=headers).text
tree = etree.HTML(page_text)
img_url = tree.xpath('//img[@id="videoElementPoster"]/@src')[0]
videoId = re.compile("videoId: (\d+),").findall(page_text)[0]
videoTitle = re.compile("videoTitle: '(.*?)'",).findall(page_text)[0]
videoDate = re.compile('videos/(.*?)/{}'.format(videoId)).findall(img_url)

videoDate = videoDate[0]
path_root = 'D:\无底洞\p站'
path_mp4 = path_root + '\\' + videoTitle + '.mp4'
m3u8_ = 'https://ev-h.phncdn.com/hls/videos/{}/{}/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_{}.mp4.urlset/index-f1-v1-a1.m3u8'.format(videoDate,videoId,videoId)
page_text_m3u8 = requests.get(url=m3u8_,headers=headers).text
# img_test = config.conn.sadd('Pornhub_img',img_url)
ts_list = []
for ts_ in page_text_m3u8.split('\n'):
    if 'ts' in ts_:
        ts_url = 'https://ev-h.phncdn.com/hls/videos/202106/23/390089331/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_390089331.mp4.urlset/' + ts_
        # img_test = config.conn.sadd('Pornhub_img',img_url)
        # ts_test = config.conn.sadd('Pornhub_ts',ts_)
        # if ts_test==1:
        #     ts_list
        ts_list.append(ts_url)
# print(ts_list)
# img = requests.get(img_url,headers=headers).content
with open(path_mp4,'ab') as fp:
    # fp.write(img)
    for ts__ in ts_list:
        ts = requests.get(url=ts__,headers=headers).content
        fp.write(ts)