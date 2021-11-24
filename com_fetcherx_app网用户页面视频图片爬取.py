from selenium import webdriver
from lxml import etree
from time import sleep
import requests
import os
import time
import random
from selenium.webdriver.chrome.options import Options
headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"},
    {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"},
    { 'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
    {'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
    { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
]
url = 'https://app.fetcherx.com/user/cIMUOA5DZ'# https://app.fetcherx.com/user/4YGvcqxr1
# header = random.choice(headers_list)
# #动态获取cookie
# # url_main_page = 'https://bbs6.unr1.xyz/2048/thread.php?fid-29-type-9-page-1.html'
# # header = random.choice(headers_list)#随机挑选头部，进行UA伪装
# # session = requests.Session()#创建Session对象
# # session.get(url_main_page,headers=header)#捕获且存储cookie
# if not os.path.exists('./'):
#     os.mkdir('./杂动图')
# url = 'https://bbs6.unr1.xyz/2048/thread.php?fid-29-type-8-page-71.html"'
# 在使用selenium进行自动化测试中我们有时会遇到这样的情况：
# 我们需要手动打开浏览器，进入到所需的页面，执行一些手动任务，如输入表单、输入验证码，登陆成功后，然后再开始运行自动化脚本。
# 这种情况下如何使用selenium来接管先前已打开的浏览器呢？
# 这里给出Google Chrome浏览器的解决方案。
# 我们可以利用Chrome DevTools协议。它允许客户检查和调试Chrome浏览器。
# 打开cmd，在命令行中输入命令：
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
#       对于-remote-debugging-port值，可以指定任何打开的端口。
#       对于-user-data-dir标记，指定创建新Chrome配置文件的目录。它是为了确保在单独的配置文件中启动chrome，不会污染你的默认配置文件。
#       还有，不要忘了在环境变量中PATH里将chrome的路径添加进去。
# 此时会打开一个浏览器页面，我们输入百度网址，我们把它当成一个已存在的浏览器：
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# # 谷歌浏览器安装目录下执行
# # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
# # 在打开的浏览器中输入 www.baidu.com
#
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# driver = webdriver.Chrome(chrome_driver, options=chrome_options)
# # 输出百度一下你就知道  表示接管成功了
# print(driver.title)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  #debuggerAddress调试器地址
chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"#驱动
bro = webdriver.Chrome(chrome_driver, options=chrome_options)
# 输出百度一下你就知道  表示接管成功了
# print(bro.title)
# bro = webdriver.Chrome(executable_path='./goolequdong/chromedriver.exe')

bro.get(url)
sleep(1)
btn = bro.find_element_by_xpath('//*[@id="mat-tab-content-0-0"]/div/div[1]/div')
btn.click()#点击按钮
sleep(2)
a = bro.switch_to.alert     #  新方法，切换alert
# a = driver.switch_to_alert()   #  老方法，切换alert
print(a.text)                    # 获取弹窗上的文本
a.accept()                       # 确认，相当于点击[确定]按钮
# a.dismiss()
# sleep(2)
# #滑动到页面底部
# bro.switch_to.default_content()
# js4 = "arguments[0].scrollIntoView();"
# div = bro.find_element_by_xpath('//*[@id="mat-tab-content-0-0"]/div/div[2]/div[10]')
# bro.execute_script(js4, div)#自动观看动
# bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')#向下滚动
# sleep(2)
# bro.get(url)
# js = "var q=document.documentElement.scrollTop=10000"
# bro.execute_script(js)
temp_height = 0
while True:
    # 循环将滚动条下拉
    bro.execute_script("window.scrollBy(0,1000)")
    # sleep一下让滚动条反应一下
    time.sleep(5)
    # 获取当前滚动条距离顶部的距离
    check_height = bro.execute_script(
        "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
    # 如果两者相等说明到底了
    if check_height == temp_height:
        break
    temp_height = check_height
    print(check_height)
page_text = bro.page_source
tree = etree.HTML(page_text)
# 所有详情页地址列表
div_list = tree.xpath('//*[@id="mat-tab-content-0-0"]/div/div[2]/div')#//*[@id="mat-tab-content-0-0"]/div/div[2]/div[294]
# /div[1]/a/@href
# detail_page_url_list = []
for div in div_list:
    detail_page_url = 'https://app.fetcherx.com' + div.xpath('./div[1]/a/@href')[0]
    # print(detail_page_url)
    # detail_page_url_list.append(detail_page_url)#将解析到的地址放入数组中
    bro.get(detail_page_url)
    sleep(1)
    # /html/body/app-root/app-timeline/div/div[3]/div[1]/div
    # / html / body / app - root / app - timeline / div / div[3] / div[1] / div#
    btn = bro.find_element_by_xpath('/html/body/app-root/app-timeline/div/div[3]/div[1]/div')
    btn.click()  # 点击按钮
    sleep(2)

    a = bro.switch_to.alert  # 新方法，切换alert
    # a = driver.switch_to_alert()   #  老方法，切换alert
    print(a.text)  # 获取弹窗上的文本
    a.accept()  # 确认，相当于点击[确定]按钮

    temp_height = 0
    while True:
        # 循环将滚动条下拉
        bro.execute_script("window.scrollBy(0,1000)")
        # sleep一下让滚动条反应一下
        time.sleep(5)
        # 获取当前滚动条距离顶部的距离
        check_height = bro.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        # 如果两者相等说明到底了
        if check_height == temp_height:
            break
        temp_height = check_height
        print(check_height)
    page_text_1 = bro.page_source
    tree_1 = etree.HTML(page_text_1)
    div_list_1 = tree_1.xpath('/html/body/app-root/app-timeline/div/div[3]/app-bookmark-list/div/div')
    for div_1 in div_list_1:
        # detail_page_url_1 = div_1.xpath('./app-bookmark-preview/div/div/div[1]')
        # print('{}/app-bookmark-preview/div/div/div[1]'.format(div_1))

        print('/html/body/app-root/app-timeline/div/div[3]/app-bookmark-list/div/div[%d]/ap'
                                          'p-bookmark-preview/div/div/div[1]'%(div_list_1.index(div_1)+1))
        btn_1 = bro.find_element_by_xpath('/html/body/app-root/app-timeline/div/div[3]/app-bookmark-list/div/div[%d]/ap'
                                          'p-bookmark-preview/div/div/div[1]'%(div_list_1.index(div_1)+1))
        btn_1.click()


        #返回上一页层
        btn_2 = bro.find_element_by_xpath('//*[@id="mat-dialog-4"]/app-media-dialog/div[2]/app-bookmark-info/div/mat-card/mat-card-header[1]/div[1]/img')
        btn_2.click()
        sleep(2)










