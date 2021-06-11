# 遇到js混淆，可以使用google自带的反混淆即在设置项将Source选项Search in anonymous and content scripts打开，就会出现js算法代码
# 网站地址：https://passport.kongzhong.com/
import re
import requests
import execjs
import time

url_dc = 'https://sso.kongzhong.com/ajaxLogin?j=j&jsonp=j&service=https://passport.kongzhong.com/&_=1623420164013'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Referer': 'https://passport.kongzhong.com/',
    'Host': 'sso.kongzhong.com'
}
params = {
    'j': 'j',
    'jsonp': 'j',
    'service': 'https://passport.kongzhong.com/',
    '_': time.time()
}
page_text_dc = requests.get(url=url_dc,headers=headers, params=params).text
dc = re.findall('"dc":"(.*?)",',page_text_dc,re.S)[0]
# print(dc)

node = execjs.get()
ctx = node.compile(open('zhanhuohuyu.js',encoding='utf-8').read())
funcName = 'getPwd("{0}","{1}")'.format('12345678',dc)
password = ctx.eval(funcName)
print(password)