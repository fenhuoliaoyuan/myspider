import execjs
import os
import requests
from lxml import etree
import re
import random
import config
import time
from tqdm import tqdm




headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
ips = config.ips
def get_page_text(url,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        page_text = requests.get(url=url, headers=headers,proxies=proxies)
        if page_text.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print('删除连接超时Ip---{}-get_page_text'.format(proxies))
        if acount == 10:
            # print()
            return
        acount += 1
        get_page_text(url,acount)
    else:
        return page_text

def get_page_text_detail(url_detail,acount):
    proxies = random.choice(ips)
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        page_text_detail = requests.get(url=url_detail, headers=headers,proxies=proxies)
        if page_text_detail.status_code != 200:
            raise ValueError
    except:
        ips.remove(proxies)
        # print('删除连接超时Ip---{}-get-page_text_detail'.format(proxies))
        if acount == 10:
            return
        acount += 1
        get_page_text_detail(url_detail,acount)
    else:
        return page_text_detail


def get_img(url_img,acount):
    try:
        headers = {
            'user-agent': random.choice(config.user_agent_list)
        }
        proxies = random.choice(ips)
        img = requests.get(url=url_img, proxies=proxies,headers=headers)
        if img.status_code != 200:
            raise ValueError
    except:
        if acount == 10:
            return
        acount += 1
        get_img(url_img,acount)
    else:
        return img
# key加密部分
def get_key(num1):
    node = execjs.get()
    ctx = node.compile(open('H漫画js_key加密.js',encoding='utf-8').read())
    function_Name = 'Encrypt("{}")'.format(num1)
    key = ctx.eval(function_Name)
    return key
def get_url_list(URL):
    # URL = 'https://www.mhdao.xyz/?page.currentPage=2&orderType=3&subjectName=&filmName='
    page_text = get_page_text(url=URL,acount=0)
    if page_text is not None:
        page_text = page_text.text
        url_list_ = re.compile("window.open\('(.*?)'\)").findall(page_text)
        url_list = []
        for url_ in url_list_:
            url = 'https://www.mhdao.xyz' + url_
            url_list.append(url)
        return url_list
# get_url_list(URL='')
def get_url_detail_list(url):
    # url = 'https://www.mhdao.xyz/manhua/info/1559.html'
    page_text = get_page_text(url=url,acount=0)
    if page_text is not None:
        page_text = page_text.text
        tuple_list = re.compile('''onclick="getInfo\('(.*?)','(.*?)'\)"''').findall(page_text)
        tree = etree.HTML(page_text)
        Title = tree.xpath('/html/head/title/text()')[0].replace('/','#')
        num_list = []
        for tuple_ in tuple_list:
            num0,num1 = tuple_
            num_list.append(num1)
        url_detail_list = []
        for num2 in num_list:
            key = get_key(num1=num2)
            url_detail = 'https://www.mhdao.xyz/play?linkId={}&bookId={}&key={}'.format(num2,num0,key)
            url_detail_list.append(url_detail)
        return url_detail_list,Title

# url = 'https://www.mhdao.xyz/manhua/info/1559.html'
# url_detail_list = get_url_detail_list(url)
def get_tuple(url_detail):
    page_text_detail = get_page_text_detail(url_detail=url_detail, acount=0)
    if page_text_detail is not None:
        page_text_detail = page_text_detail.text
        tree = etree.HTML(page_text_detail)
        title = tree.xpath('/html/head/title/text()')[0].replace('/','#')
        path_root_ = path_root + '\\' + title
        if not os.path.exists(path_root_):
            os.mkdir(path_root_)
        img_list = tree.xpath('//*[@id="imgList"]/img')
        url_img_list = []
        for img_ in img_list:
            url_img = 'https://www.mhdao.xyz' + img_.xpath('./@src')[0]
            url_img_list.append(url_img)
        jishu = 0
        # tuple_list = []
        for url_img_ in url_img_list:
            name_img = str(jishu) + '.jpg'
            path_img = path_root_ + '\\' + name_img
            jishu += 1
            config.conn.sadd('hman_img_list',path_img+',,,'+url_img_)
            print('尝试插入--{}'.format(path_img+',,,'+url_img_))
            # tuple_list.append(path_img+',,,'+url_img_)
        # print()
        # return tuple_list
def save(tuple_):
    # tuple_ = "jjaghgjiaij97175757577,,,2771777"
    path_img,url_img = tuple(tuple_.split(',,,'))
    # print(path_img)
    if os.path.exists(path_img):
        pass
    else:
        img = get_img(url_img=url_img, acount=0)
        if img is not None:
            with open(path_img, 'wb') as mf:
                mf.write(img.content)
            print('{}下载成功'.format('_'.join(path_img.split('\\')[-2:])))
# main(url_detail_list)
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    path_roots = r'E:\H漫画'
    if not os.path.exists(path_roots):
        os.mkdir(path_roots)
    for page in range(1,1):
        URL = 'https://www.mhdao.xyz/?page.currentPage=%d&orderType=3&subjectName=&filmName='%page
        url_list = get_url_list(URL=URL)
        if url_list is not None:
            print('线程池开启')
            with ThreadPoolExecutor(100) as tp:
                for url in url_list:
                    try:
                        tuple__ = get_url_detail_list(url=url)
                        if type(tuple__) is tuple:
                            url_detail_list, Title = tuple__
                            path_root = path_roots + '\\' + Title
                            if not os.path.exists(path_root):
                                os.mkdir(path_root)

                            for url_detail in url_detail_list:
                                tp.submit(get_tuple,url_detail)
                            # print('{}下载完成'.format(Title))
                    except:
                        pass
            print('线程池关闭')
        print('第{}页图片链接和内存地址存储完毕'.format(page))
    with ThreadPoolExecutor(50) as tp0:
        list_img = config.conn.smembers('hman_img_list')
        for img_ in list(list_img)[::-1]:
            tuple_ = bytes.decode(img_)
            tp0.submit(save,tuple_)