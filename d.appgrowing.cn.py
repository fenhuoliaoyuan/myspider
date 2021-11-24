from pprint import pprint

from config import *
import requests
import json
url = 'https://d.appgrowing.cn/api/material?mtype=201&query=欢友&isExact=false&order=-_score&startDate=2021-08-20&endDate=2021-11-17&limit=10&page=1'
# 'https://d.appgrowing.cn/api/material?mtype=201&query=%E6%AC%A2%E5%8F%8B&isExact=false&order=-_score&startDate=2021-08-20&endDate=2021-11-17&limit=10&page=1'
def get_page_text(url,acount):
    proxies = random.choice(ips)
    # print(proxies)
    try:
        headers = {
            'user-agent': random.choice(user_agent_list),
            # 'referer': 'https://d.appgrowing.cn/leaflet/list?mtype=201&query=%E4%BA%A4%E5%8F%8B&viewType=material&isExact=false&order=-_score&startDate=2021-08-20&endDate=2021-11-17&limit=10&page=1'
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
        get_page_text(url,acount)
    else:
        return page_text
headers = {
	'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'accept-encoding' : 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
	'cache-control' : 'no-cache',
	'cookie' : '_ga=GA1.1.453621669.1637245519; _ga_JSV1PSDCPB=GS1.1.1637245518.1.0.1637245522.0; AG_Token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmNjY1NTFmLTA3OWItMzdjNC04MDIzLTI4M2EyZjBiZWM2ZiIsImFjYyI6NDc2Njg2LCJleHAiOjE2Mzk4Mzc0ODEsImFjY291bnRfc2Vzc2lvbiI6ImIwYzA2OGE4ZDM1Njg1YTgzY2Q4Y2IyYWU1YzU2ZjIzIiwiaWF0IjoxNjM3MjQ1NTI1fQ.gjZ4L5hDiVomWkvF1iP4wDZEEj8lVxK5Bdg1Rh2uz4w; Today_Logged_In=1; ph_oEY7uwNI-BrLK7aN1Al8D1-abXKFEeENlm9zn5gOvzM_posthog=%7B%22distinct_id%22%3A%22476686%22%2C%22%24device_id%22%3A%2217d334961a928-0a84c03d6f2df6-57b1a33-e1000-17d334961aa63d%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fauth.youcloud.com%2F%22%2C%22%24initial_referring_domain%22%3A%22auth.youcloud.com%22%2C%22%24referrer%22%3A%22https%3A%2F%2Fd.appgrowing.cn%2Fleaflet%2Flist%22%2C%22%24referring_domain%22%3A%22d.appgrowing.cn%22%2C%22app_release%22%3A%22v4.1.3-ag-data%22%2C%22%24session_recording_enabled%22%3Afalse%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24user_id%22%3A%22476686%22%7D',
	'pragma' : 'no-cache',
	'sec-ch-ua' : '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
	'sec-ch-ua-mobile' : '?0',
	'sec-ch-ua-platform' :'"Windows"',
	'sec-fetch-dest' : 'document',
	'sec-fetch-mode' : 'navigate',
	'sec-fetch-site' : 'none',
	'sec-fetch-user' : '?1',
	'upgrade-insecure-requests' : '1',
	'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
import re
# page_text = get_page_text(url=url,acount=0)
page_text= requests.get(url=url,headers=headers).text
NewResponse = re.sub(r"\\","",page_text)

page_text = json.dumps(NewResponse.encode('utf-8').decode("unicode_escape"))
# page_text.encoding = 'utf-8'
pprint(page_text)
# print(page_text['data'][0]['materialList'][0]['url'])