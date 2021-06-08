import requests
from requests.exceptions import RequestException
import json
from urllib.parse import urlencode
import pymongo
import numpy as np
import time
from config import spider_tencent
import random
# 构建headers,从这个列表里随机获取header
url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1623148314085&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

# 构建请求链接
# def make_url(page):
#
#     url = u'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false' + urlencode(data)
#     return url
# 请求每一页的链接，根据页数和header列表长度的余数随机取header的值
def get_index_page(url,page):
    params = {
        'timestamp': time.time(),
        'countryId': '',
        'cityId': '',
        'bgIds': '',
        'productId': '',
        'categoryId': '',
        'parentCategoryId': '',
        'attrId': '',
        'keyword': '',
        'pageIndex': page,
        'pageSize': 10,
        'language': 'zh-cn',
        'area': 'cn'
    }
    try:
        response = requests.get(url, headers=header,params=params)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求职位列表页错误')
        return None
# 解析列表页
def parse_job_page(response):
    result = json.loads(response)
    if result:
        jobs = result["Data"]["Posts"]
        for job in jobs:
            ProductName = job["ProductName"]
            LocationName = job[ "LocationName"]
            CategoryName = job[ "CategoryName"]
            RecruitPostName = job[ "RecruitPostName"]
            Responsibility = job['Responsibility']
            LastUpdateTime = job['LastUpdateTime']
            PostURL= job['PostURL']
            job_data = {
                'ProductName' : ProductName,
                'city' : LocationName,
                'CategoryName' : CategoryName,
                'job_name' : RecruitPostName,
                'Responsibility' : Responsibility,
                'LastUpdateTime' : LastUpdateTime,
                'PostURL' : PostURL
            }
            if job_data:
                save_to_mongo(job_data)
# 保存到mongoDB数据库
def save_to_mongo(result):
    if spider_tencent .insert(result):
        print('存储到mongoDB成功', result)
        return True
    return False

# 用np.random.rand()生成随机数用来sleep模拟人访问的操作,抓取前三页
def main():
    for page in range(1, 3 + 1):
        time.sleep(np.random.rand() * 20)
        response = get_index_page(url,page)
        if response:
            parse_job_page(response)


if __name__ == '__main__':
    main()
