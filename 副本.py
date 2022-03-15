import requests
import re
import os
from proxies import proxies_1
from lxml import etree
import random
from tqdm import tqdm



headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}
for page in range(1,136):
    print('====================================================第{}页下载开始'.format(page))
    url = 'https://www.yamei001.com/?s=pic/type/17/{}.html'.format(page)
    proxy = proxies_1.Proxy()
    page_text = requests.get(url=url,headers=headers,proxies=random.choice(proxy)).text
    tree = etree.HTML(page_text)
    a_list = tree.xpath('//h4[@class="artlist_title"]/a')
    for a in a_list:
        url_detail = 'https://www.yamei001.com' + a.xpath('./@href')[0]
        title = a.xpath('./@title')[0]
        path_img_ = 'C:\\番号\\ntqyfj_com' + '/' + title
        if not os.path.exists(path_img_):
            os.mkdir(path_img_)
        page_text_img = requests.get(url=url_detail,headers=headers,proxies= random.choice(proxy)).text
        a_id = re.compile('a_id=(\d+)').findall(page_text_img)[0]
        ajax_url = 'https://www.cmsapitpmt.com/pic.php/?a_id={}'.format(a_id)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++{}下载开始'.format(title))
        page_text_img_ajax = requests.get(url=ajax_url,headers=headers,proxies=random.choice(proxy)).text
        url_img_list = re.compile('(https:.*?jpg)').findall(page_text_img_ajax)
        pbar = tqdm(total=len(url_img_list))
        for url_img in url_img_list:
            name_img = url_img.split("/")[-1]
            path_img = path_img_ + "/" + name_img
            if os.path.exists(path_img):
                print('文件已存在')
                pbar.update(1)
                continue
            else:
                img = requests.get(url=url_img,headers=headers,proxies=random.choice(proxy)).content
                with open(path_img,'wb') as fp:
                    fp.write(img)
                    # print('{}下载成功'.format(name_img))
                    pbar.update(1)
        pbar.close()