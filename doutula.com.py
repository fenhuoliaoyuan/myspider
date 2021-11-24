from lxml import etree
import random
import requests
import os
# session = requests.Session()



with open('ips.txt', 'r',encoding='utf-8') as rt:
    ips = [i.replace("'",'"') for i in rt.read().split('\n')]
    # for i in ips:
    #     print(i)
with open('UA头.txt', 'r') as ua:
    user_agent_list = [i.replace('\n', '') for i in ua.readlines()]
# i = 0
# while i < 10:
#     headers = {
#         'user-agent': random.choice(user_agent_list),
#         'Cookie': '_agep=1635826284; _agfp=c2c6b3e6c1243c44587796625fd736e1; _agtk=ff38fcbe9eb655733fc45152ad676f66; BAIDU_SSP_lcr=https://www.baidu.com/link?url=I9sT4pEcSxSAOWVHC00hSxUNJ6hDUKg14DKhJpCl1nqvvUcBTJg7PEc_J_xXKPNu&wd=&eqid=b6d05f4a000087a5000000066180ba63; Hm_lvt_2fc12699c699441729d4b335ce117f40=1635826284,1635826385; XSRF-TOKEN=eyJpdiI6IlpseDhzMzlRejBtQmlqa1YxcVFyaHc9PSIsInZhbHVlIjoiSG1McFVsZjhvcWYyQVE4TTh4MGxYQ2pBWmRYbEdGV1VOTmFYK3h1cFZrSmtCSW1IZEVuMklaSmN3QXREOG0xcCIsIm1hYyI6IjYxYzMwYThjZmE3ZmI2OGRkYmE1YzQ4ODUzMjZmOWNmMDgyYWJmZTg0YzY1NDNlNmU1YjgxMWVkMTNlNDBiMzUifQ%3D%3D; doutula_session=eyJpdiI6IjhKdUd6Qk1Rbjd6NVF5UTVieUhLWkE9PSIsInZhbHVlIjoiemJ5c200YmRKQnF1OW5reVY4XC9kbkdFbFBFXC8xNmF5QnJhVmdPZFR1d3J6T0JHbTRiOXY0U1BIS0lkVHE4WjJmIiwibWFjIjoiYjY0YjgwYmJlNTYzMDUwODUwNmI0ODZkOThjMjEyMDI0MGIzMzZkNjdkMTI5MTI0ZWI0M2YxOWIwYzc5ODJjZSJ9; Hm_lpvt_2fc12699c699441729d4b335ce117f40=1635859871'
#     }
#     proxies = random.choice(ips)
#     try:
#         session.get(url='https://www.doutula.com', headers=headers, proxies=proxies, timeout=10)
#     except:
#         print('重试中')
#         i += 1
#     else:
#         i = 10

class Doutula():
    def __init__(self):
        self.path_root = r'F:\doutula'
        if not os.path.exists(self.path_root):
            os.mkdir(self.path_root)

    def get_page_text(self, url, acount):
        ip = random.choice(ips)
        proxies = {
            'https':'http://'+ip,
            'http':'http://'+ip
        }
        # print(proxies)
        try:
            headers = {
                'user-agent': random.choice(user_agent_list),
                'Referer': 'https://www.doutula.com/photo/list/'
              }
            page_text = requests.get(url=url, headers=headers,proxies=proxies)
            if page_text.status_code != 200:
                raise ValueError
        except:
            if acount == 10:
                return
            acount += 1
            Doutula.get_page_text(self,url, acount)
        else:
            return page_text

    def response(self, url):

        response = Doutula.get_page_text(self,url=url, acount=0)
        if response is not None:
            return response

    def get_url_detail_list(self, response):
        if response is not None:
            page_text = response.text
            tree = etree.HTML(page_text)
            url_detail_list = tree.xpath('//a[@class="col-xs-6 col-sm-3"]/@href')
            if len(url_detail_list) > 0:
                return url_detail_list

    def get_url_img(self, url_detail):
        response = Doutula.response(self,url_detail)
        if response is not None:
            page_text = response.text
            tree = etree.HTML(page_text)
            url_img = tree.xpath('//img[@referrerpolicy="no-referrer"]/@src')
            if len(url_img) > 0:
                return url_img[0]

    def save_img(self, url_img):
        img_name = url_img.split('/')[-1]
        response = Doutula.response(self,url_img)
        if response is not None:
            img = response.content
            with open(self.path_root + '\\' + img_name, 'wb') as ww:
                ww.write(img)
                print(img_name + '下载完成')


def main(url):
    Dt = Doutula()
    print('开始下载{}'.format(url))
    response = Dt.response(url=url)
    url_detail_list = Dt.get_url_detail_list(response)
    for url_detail in url_detail_list:
        url_img = Dt.get_url_img(url_detail)
        Dt.save_img(url_img)
if __name__ == '__main__':
    # from concurrent.futures import ThreadPoolExecutor
    # with ThreadPoolExecutor(1) as tp:
    #     for page in range(1, 201):
    #         url = 'https://www.doutula.com/photo/list/?page={}'.format(page)
    #         tp.submit(main,url)
    main('https://www.doutula.com/photo/list/?page=1')