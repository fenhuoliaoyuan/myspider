import requests
from lxml import etree
import os


if not os.path.exists('./5g影院_图片/'):
    os.mkdir('./5g影院_图片/')
acounts = 0
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}
for page in range(1,88):
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++第{}页抓取开始'.format(page))
    URL = 'https://5gunw.xyz/h/tupian/list_6_%d.html'%page
    page_text = requests.get(url=URL,headers=headers).text
    tree = etree.HTML(page_text)
    li_lst = tree.xpath('//li[@class="pin"]')
    for li in li_lst:
        url_detail = 'https://5gunw.xyz' + li.xpath('./a/@href')[0]
        name_img_qianzui = li.xpath('./p/a/text()')[0]
        page_text_detail = requests.get(url=url_detail, headers=headers).text
        tree_0 = etree.HTML(page_text_detail)
        img_list = tree_0.xpath('//div[@class="bf_js"]/img')
        number = 0
        for img in img_list:
            url_img = img.xpath('./@src')[0]
            number += 1
            name_img = name_img_qianzui + '_' + str(number) + '.jpg'
            path_img = './5g影院_图片/' + name_img
            if os.path.exists(path_img):
                acounts += 1
                print('第{}个文件{}--{}已存在跳过'.format(acounts,name_img,page))
                continue
            else:
                try:
                    img_content = requests.get(url=url_img, headers=headers).content
                except:
                    print('加载过慢')
                else:
                    with open(path_img, 'wb') as fp:
                        fp.write(img_content)
                        acounts += 1
                        print('第{}个文件{}下载成功--{}'.format(acounts, name_img,page))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++第{}页抓取完成'.format(page))