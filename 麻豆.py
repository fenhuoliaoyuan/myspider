import os
import requests
from lxml import etree
import re
from Crypto.Cipher import AES
import binascii
from base64 import b64decode,b64encode
from Crypto.Random import get_random_bytes

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.7'
                  '7 Safari/537.36'
}
# url = 'http://mdtv008.com/latestVideo/10203/1/?type=10203'
if not os.path.exists('./麻豆/'):
    os.mkdir('./麻豆/')
# session = requests.Session()
# session.get(url,headers=headers)
# page_text = session.get(url,headers=headers)
# page_text.encoding = 'utf-8'
# page_text = page_text.text
# # print(page_text.text)
# tree = etree.HTML(page_text)
# div_list = tree.xpath('//*[@id="pane-10203"]/div/div')
# for div in div_list:
#     url_detail = 'http://mdtv008.com' +  div.xpath('./div/a/@href')[0]#//*[@id="pane-10203"]/div/div[1]/div/a
#     name_video = div.xpath('./div/h1/text()')[0].replace('/','_')
#     # name_video= name_video.replace('/','_')
#     # print(name_video)
#     path_video = './麻豆预告片/' + name_video + '.mp4'
#     if os.path.exists(path_video):
#         print('文件{}.mp4已存在'.format(name_video))
#         continue
#     # else:
url = 'https://gw.izcqzih.cn/api/app/media/m3u8/av/ev/kw/a1/8z/6c6108b5a25e4b289fb9d6b1faef264c'
m3u8_txt = requests.get(url=url,headers=headers).text
# url_key = re.compile('URI="")
ts_list = []
for line in m3u8_txt.split('\n'):
    # print(line)
    if 'URI' in line:
        url_key = 'https://gw.izcqzih.cn' + re.compile('URI="(.*)"').findall(line)[0]
        # print(url_key)
    elif 'ts' in line:
        ts_list.append(line)
# iv = get_random_bytes(16)
# iv = b64encode(cipher.iv).decode('utf-8')
key_byte = requests.get(url=url_key,headers=headers).content
# key_byte = binascii.b2a_hex(key_byte)

cryptor = AES.new(key_byte,AES.MODE_CBC)
i = 1
for ts_url in ts_list:
    ts = requests.get(url=ts_url,headers=headers).content
    if len(key_byte):
        name_ts = ts_url.split('/')[-1]
        ts_open = cryptor.decrypt(ts)
        # with open('./麻豆/clip_%d'%i,'wb') as ft:
        #     ft.write(ts_open)
        #     print('正在下载clip_%d'%i)
        #     i += 1
        with open('./麻豆/第一个mp4.mp4', 'ab') as fp:
            fp.write(ts_open)
            print('{}下载成功'.format(name_ts))






