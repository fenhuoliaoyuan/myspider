import requests
import re
import execjs

url = 'https://g0527.91p47.com/view_video.php?viewkey=76856b3ce848bab86d0a'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'cookie': '__utmz=50351329.1620127544.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 91username=c129F%2BTyLiYr%2BNpWec169n%2B9pZvVlb5r%2FzSHeYAzwf8LBBP8hMuodTIqEg; __utmc=50351329; watch_times=0; CLIPSHARE=uebu5cijc5frjlbv9v3ibfeuoa; level=7; cf_clearance=86efd21db8ea13371e93fa1f2e125ff7d776c1d1-1624286837-0-150; __utma=50351329.1431892130.1620127544.1624278463.1624286839.33; __utmb=50351329.0.10.1624286839; __cf_bm=9184724fc8f7c776731d5301e2d2e7286517c136-1624286838-1800-AWfx+kCgiKw1QGhh8jN2DFvKZjNEA1S3Zz8x1bTUYf1s8eedq4s1Vcal3axLvYpwQ9k+VbfMzASDrLIZyB9BEBaDE6IekPtLh7REM6L4NhNYkBMWMxCNEgFUoLEL2KlEoQ=='
}
page_detail_response = requests.get(url=url,headers=headers)
page_detail_response.encoding = page_detail_response.apparent_encoding
page_detail_text = page_detail_response.text
st_yuanma = re.compile('strencode2\("(.*?)"\)').findall(page_detail_text)[0]
note = execjs.get()
# ctx = node.compile(open('./steam.js',encoding='utf-8').read())
ctx = note.compile(open('91porn_mp4地址_st值逆向.js',encoding='utf-8').read())

# 执行js函数
funcName = 'get_st("{}")'.format(st_yuanma)
st_ = ctx.eval(funcName)
# print(st)
st = re.compile("src=\'(.*)\' type").findall(st_)[0]
print(st)
