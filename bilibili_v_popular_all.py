import os
import re

from lxml import etree

import requests

dir_name = r'G:'
os.chdir(dir_name)
headers = {
    'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    # 'cookie': '_uuid=56AD6CAF-16BF-49A5-28A1-500D5935260A72708infoc; sid=jm22g21w; rpdid=|(k|k)JYJu~k0J'uYk|u|Rl|J; LIVE_BUVID=AUTO6016235994281872; route=; fingerprint_s=266eff96b0402d10a6f675c014cb1c19; CURRENT_QUALITY=80; DedeUserID=269363284; DedeUserID__ckMd5=ee1445cefa4ba98a; video_page_version=v_old_home; buvid_fp_plain=3DCE0F1B-EED0-4B1F-8824-4E326DCABBB1167622infoc; SESSDATA=ab3110d5%2C1653706934%2C9686d*b1; bili_jct=ecf27919109e67755c7b7138cd28b130; i-wanna-go-back=-1; b_ut=5; CURRENT_BLACKGAP=0; blackside_state=0; buvid4=AD50BD49-E0CB-E34A-C69B-9F82FBC5C1B602394-022012118-7wW9WxYI4As8abEmaUm6ZA%3D%3D; buvid3=3BFBC856-DAC1-4C3E-8CD4-04004A244B63148801infoc; fingerprint3=f009a3ecbe56ec046cdfce8e0d4b23de; fingerprint=decada5c5c47faedc2b7a198dacf6190; nostalgia_conf=-1; bsource=search_google; innersign=1; buvid_fp=9864bd2acf4232ce5c320a6432219d14; PVID=1; bp_video_offset_269363284=633319603925155800; bp_t_offset_269363284=633319603925155848; _dfcaptcha=d4cfec6838f3c2b750d50805abd107e1; CURRENT_FNVAL=4048; b_lsid=AAA3A9D1_17F4EEE649E',
    'origin': 'https://space.bilibili.com',
    # 'referer': 'https://space.bilibili.com/23606362/video?tid=0&page=1&keyword=&order=pubdate',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
}
data = []
for page in range(1, 5):
    URL = 'https://space.bilibili.com/23606362/video?tid=0&page=%d&keyword=&order=pubdate'
    url = 'https://api.bilibili.com/x/space/arc/search?' + 'mid=' + re.compile('.com/(.*?)/').findall(URL)[
        0] + '&ps=30&tid=0&pn=%d&keyword=&order=pubdate&jsonp=jsonp' % page
    req = requests.get(url=url, headers=headers)
    page_json = req.json()
    # data.list.vlist
    vlist = page_json['data']['list']['vlist']
    for li in vlist:
        bvid = li['bvid']
        title = li['title']
        URL_DETAIL = 'https://www.bilibili.com/video/' + bvid
        if len(URL_DETAIL) > 0:
            # url_video_cmd = 'yt-dlp -f \"/estvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best\" ' + URL_DETAIL
            url_video_cmd = 'yt-dlp ' + URL_DETAIL
            # os.system(url_video_cmd)
            data.append(url_video_cmd)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(1) as tp:
    for url_video_cmd in data:
        tp.submit(os.system,url_video_cmd)