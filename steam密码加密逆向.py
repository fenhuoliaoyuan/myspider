import execjs
import requests


url = 'https://store.steampowered.com/login/getrsakey/'
data = {
    'donotcache': 1623385390399,
    'username': '12345'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
}

response_json = requests.post(url=url,headers = headers,data=data).json()
mod = response_json['publickey_mod']
exp = response_json['publickey_exp']
# 实例化一个node对象
node = execjs.get()

# js源文件编译
ctx = node.compile(open('./steam.js',encoding='utf-8').read())

# 执行js函数
funcName = 'getPwd("{0}","{1}","{2}")'.format('123456',mod,exp)
pwd = ctx.eval(funcName)
print(pwd)