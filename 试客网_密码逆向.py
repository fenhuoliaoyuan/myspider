import execjs
import requests
from lxml import etree
import re

url_mian = 'http://login.shikee.com'
# url_getkey = 'http://login.shikee.com/getkey?v=9696d8085bbec4073dca8fa79e9eb11c'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}
page_text_mian = requests.get(url=url_mian,headers=header).text
tree = etree.HTML(page_text_mian)
url_get_key = url_mian + tree.xpath('/html/body/script[4]/@src')[0]
# print(url_get_key)
ex = 'var rsa_n = "(.*)"'
page_text_gekey = requests.get(url=url_get_key,headers=header).text
rsa_n = re.findall(ex,page_text_gekey,re.S)[0]
# print(rsa_n)
node = execjs.get()
ctx = node.compile(open('./shikewang.js',encoding='utf-8').read())
funcname = "getPwd('{0}','{1}')".format('12345678',rsa_n)
pwd = ctx.eval(funcname)
print(pwd)


