from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
from lxml import etree
import requests
import random
from 爬虫小项目 import config
import time
from selenium.webdriver.common.action_chains import ActionChains


class get_img():
    def __init__(self):
        self.url = config.zhihu_url
        self.username = config.username
        self.password = config.password
        self.path_root = config.path_root
    def get_bro(self):

        # os.system(r'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"')
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # debuggerAddress调试器地址
        chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"  # 驱动
        bro = webdriver.Chrome(chrome_driver, options=chrome_options)
        return bro
    def get_img(self):
        bro = self.get_bro()
        headers = {
            'user-agent': random.choice(config.get_ua()),
        }
        bro.get(url=self.url)
        click_used_password = bro.find_element_by_xpath('//div[@class="SignFlow-tab"]')
        click_used_password.click()
        time.sleep(2)
        # pass
        input_name = bro.find_element_by_xpath('//input[@name="username"]')
        input_name.send_keys(self.username)
        time.sleep(2)
        input_password = bro.find_element_by_xpath('//input[@name="password"]')
        input_password.send_keys(self.password)
        time.sleep(2)
        click_login = bro.find_element_by_xpath('//button[@type="submit"]')
        click_login.click()
        time.sleep(2)
        # 批量抓取验证图片
        # i = 0
        # while i<100:
        #     page_text = bro.page_source
        #     tree = etree.HTML(page_text)
        #     url_img = tree.xpath('//img[@class="yidun_bg-img"]/@src')[0]
        #     name_img = url_img.split('/')[-1]
        #     path_img = 'C:\github\zhihu\验证码图片' + '\\' + name_img
        #     if not os.path.exists(path_img):
        #         img = requests.get(url_img,headers=headers).content
        #         with open(path_img,'wb') as fp:
        #             fp.write(img)
        #             print('{}下载成功'.format(name_img))
        #     time.sleep(2)
        #     button_shuaxin = bro.find_element_by_xpath('//div[@class="yidun_refresh"]')
        #     button_shuaxin.click()
        #     time.sleep(2)
        #     i += 1
        page_text = bro.page_source
        tree = etree.HTML(page_text)
        url_img = tree.xpath('//img[@class="yidun_bg-img"]/@src')[0]
        name_img = url_img.split('/')[-1]
        path_root = self.path_root
        path_img = path_root + '\\' + name_img
        if not os.path.exists(path_img):
            img = requests.get(url_img, headers=headers).content
            with open(path_img, 'wb') as fp:
                fp.write(img)
                print('{}下载成功'.format(name_img))
                return path_img,bro
    def get_slide_locus(self, distance):
        distance += 8
        v = 0
        m = 0.3
        # 保存0.3内的位移
        tracks = []
        current = 0
        mid = distance * 4 / 5
        while current <= distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            s = v0 * m + 0.5 * a * (m ** 2)
            current += s
            tracks.append(round(s))
            v = v0 + a * m
        # 由于计算机计算的误差，导致模拟人类行为时，会出现分布移动总和大于真实距离，这里就把这个差添加到tracks中，也就是最后进行一步左移。
        # tracks.append(-(sum(tracks) - distance * 0.5))
        # tracks.append(10)
        return tracks
    def slide_verification(self,distance,bro):
        # distance,bro = self.get_img()
        locus = self.get_slide_locus(distance)
        ActionChains(bro).click_and_hold(bro.find_element_by_xpath('//div[@class="yidun_slider"]')).perform()
        # 模拟人的滑动
        for loc in locus:
            time.sleep(0.5)
            ActionChains(bro).move_by_offset(loc, random.randint(-5, 5)).perform()
            ActionChains(bro).context_click(bro.find_element_by_xpath('//div[@class="yidun_slider"]'))
        # 释放鼠标
        ActionChains(bro).release(on_element=bro.find_element_by_xpath('//div[@class="yidun_slider"]')).perform()



class baidu_login:
    def __init__(self,ak,sk):
        self.ak = ak
        self.sk = sk
    def get_access_token(self):
        # encoding:utf-8
        import requests

        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(self.ak,self.sk)
        response = requests.get(host)
        if response:
            # print(response.json())
            # print(response.json()['access_token'])
            return response.json()['access_token']
    def recongnize(self,access_token,img_file,api_url):
        """
        EasyDL 物体检测 调用模型公有云API Python3实现
        """

        import json
        import base64
        import requests
        """
        使用 requests 库发送请求
        使用 pip（或者 pip3）检查我的 python3 环境是否安装了该库，执行命令
          pip freeze | grep requests
        若返回值为空，则安装该库
          pip install requests
        """

        # 目标图片的 本地文件路径，支持jpg/png/bmp格式
        # IMAGE_FILEPATH = "【您的测试图片地址，例如：./example.jpg】"
        IMAGE_FILEPATH = img_file
        # 可选的请求参数
        # threshold: 默认值为建议阈值，请在 我的模型-模型效果-完整评估结果-详细评估 查看建议阈值
        PARAMS = {"threshold": 0.6}

        # 服务详情 中的 接口地址
        # MODEL_API_URL = "【您的API地址】"
        MODEL_API_URL = api_url

        # 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
        # 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
        ACCESS_TOKEN = access_token
        API_KEY = self.ak
        SECRET_KEY = self.sk

        print("1. 读取目标图片 '{}'".format(IMAGE_FILEPATH))
        with open(IMAGE_FILEPATH, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_str = base64_data.decode('UTF8')
        print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
        PARAMS["image"] = base64_str

        if not ACCESS_TOKEN:
            print("2. ACCESS_TOKEN 为空，调用鉴权接口获取TOKEN")
            auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials" \
                       "&client_id={}&client_secret={}".format(API_KEY, SECRET_KEY)
            auth_resp = requests.get(auth_url)
            auth_resp_json = auth_resp.json()
            ACCESS_TOKEN = auth_resp_json["access_token"]
            print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
        else:
            print("2. 使用已有 ACCESS_TOKEN")

        print("3. 向模型接口 'MODEL_API_URL' 发送请求")
        request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
        response = requests.post(url=request_url, json=PARAMS)
        response_json = response.json()
        # response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
        # print("结果:\n{}".format(response_str))
        return response_json["results"][0]["location"]["left"]
if __name__ == '__main__':
    img = get_img()
    path_img,bro = img.get_img()
    baidu_login = baidu_login(config.ak,config.sk)
    access_token = baidu_login.get_access_token()
    img_lelf = baidu_login.recongnize(access_token,path_img,api_url=config.baidu_api_url)
    # print(img_lelf)
    img.slide_verification(distance=img_lelf,bro=bro)
