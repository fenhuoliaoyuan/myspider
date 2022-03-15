# 需求：爬取雪球网中的咨询信息
# 分析；
# 1.判断爬取的咨询数据是否为动态加载的
# -相关的更多咨询数据是动态加载的，滚轮滑动到底部的时候会动态加载更多数据
# 2.定位到Ajax请求的数据包，提取出请求的URL，响应数据为JSON形式的数据
import requests
# from lxml import etree






headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safa'
              'ri/537.36'
# 'Cookie': 'acw_tc=2760820516212341962603831e836c9cbe34cd9014e3d8fa368da48afd8321; xq_a_token=385b836a045da45667afda72237fc969313f56f0; xqat=385b836a045da45667afda72237fc969313f56f0; xq_r_token=f04bf9be3f04ead615a88752d56293c4ae5eec0b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYyMzgxMTc5NywiY3RtIjoxNjIxMjM0MTg4MjE0LCJjaWQiOiJkOWQwbjRBWnVwIn0.W1Qri8Cfj-xyZx5vwvdZ_C-GFJjOoNgcPwpavlB1nA6CXn6WaYdovIYQ-iSFk7gCqSbzhJJWM0e7ryFV4GlWcrIb2qz3nEiMyl3svuLo9FC-FWKqNWl7yNXto98uty_OHhfbYaFfded1ZgRmkkrPDWVVQY9MUDy1M215jNYfnnHhKtFYrpb3wJm7LgjwrU1l-Z1WeLTBwqs9XYJas6pNtaqPF8v6ciYJOZhAVP0mBaV8YdJ6ZEBhC1d6_gX02jcv28qxe5Js2L-aHFbxwchlvmQiuzGbn3lXRluRqV1aMSopmOSr4h6t6cWvrfQYilSsMikqiD_DpCfRmBDKFMB0uQ; u=241621234196265; device_id=24700f9f1986800ab4fcc880530dd0ed; Hm_lvt_1db88642e346389874251b5a1eded6e3=1621234204; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1621235832'
}
url_mainpage = 'https://xueqiu.com/'
session = requests.Session()#创建Session对象
session.get(url_mainpage,headers=headers)#捕获且存储cookie


url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=204887&size=15'
data = {
'since_id': '-1',
'max_id': '204887',
'size': '15'
}
#携带cookie发起请求
# response = session.get(url=url,headers=headers).json()
# print(response)
response = session.post(url=url,headers=headers).content
# print(response)

