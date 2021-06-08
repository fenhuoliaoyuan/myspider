import requests
from requests.exceptions import RequestException
import json
from urllib.parse import urlencode
import pymongo
import numpy as np
import time
from config import collection
import random
# 构建headers,从这个列表里随机获取header
url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
header = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'user_trace_token=20210504130856-9e4e3980-98a3-407a-b647-7a1312b51f73; _ga=GA1.2.1206761504.1620104936; LGUID=20210504130857-49d05329-0044-4256-8736-9ef69a2908b9; LG_LOGIN_USER_ID=bb63f893c38af975a2dcce326fe4b040313ba55d3ef680752c0c7a9a5ed686ce; LG_HAS_LOGIN=1; RECOMMEND_TIP=true; index_location_city=%E5%B9%BF%E5%B7%9E; WEBTJ-ID=2021062%E4%B8%8B%E5%8D%887:42:45194245-179cc88766d57-0e600fdc62f06-f7f1939-921600-179cc88766e3f7; sensorsdata2015session=%7B%7D; JSESSIONID=ABAAAECABFAACEA7BFBBF15266887A1B2B34B6B49ECE947; gate_login_token=b3d228fc2f7dfd30985ef17391ab7fcd97e0c49199cb8a95673a35dac5b753bb; _putrc=0D64C97147F9A51F123F89F2B170EADC; login=true; unick=%E6%9D%8E%E4%BC%9F%E5%90%89; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; privacyPolicyPopup=false; EDUJSESSIONID=ABAAAECABCAAACDD09D6634D1DF3E0A87E8B5B6D76C7867; user-finger=507c7f71c53694a19838341d0a75cc8c; smidV2=202106022109396c66e6e1df2b449030b69b7b10a897b500b94fc90151fc6f0; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WHJMrwNw1k/HC1NdButFFLXPxcdXCJ08ny0X5JzfnplQTJXNc2HryrY9Fyy3pTB/ZrxLJIuLmPYFL93MVq1CmHgQ9lttDn+n6dCW1tldyDzmQI99+chXEirHBcMCrF5db9lCUKKcsmkSqmJzoPeggwzYmmmXo8LlTkQE5YcNLqNriNYPfoOP/bo5r5oTms6dUHR45uFj1+G2KFKr33wxFMe8Vg+5pExYXkEB3O8mIIi3CqnqlbtXI1rfoRz4IyNXPe5685hmEETs%3D1487582755342%22%7D%2C%7B%22channel%22%3A2%2C%22thirdDeviceId%22%3A%22140%23zaXDnzPszzPEezo23zvs4pN8s7aJqe/BXdDB4Ol5nlF7Rr4/QVLQ+dCkbumpfiRvqVMKt6hqzzn6axrAciszzBVNbjvqlQzx2DD3VthqzFng2XU+llfzzPziVWFnlT8I1wba7X53xYYCTdkWsdWE5CTH83TmqZ5i6ePaeMrfG7vEx/YfiVRzj0rBxppfgSMWq5JqKV/xVZZZq7CeXSlbphyU7soxWzRfLku1IkM+RTudn5DptgiQopkeKfRMg9oNumjDY9gZqmbXeyTeeK1pZhv9cCSmLXAQI4IAwLBdRy/qIxMZylwYflUAKVeQFpsLhLzRY4vrXCy6y2aDey1GVDwV/gqc6eqfWMW0dUeyFq61WUOZk2UAVnqT5GsOAXxsiYoEju+6+VmuqLenlra9q3wKd3YCfBDMI50ZnRThP1P5qv6LA1XeUfti86sdGOhvmMrHvPTz/SKdauCURVb2erdBbC5nURvObMQSKTwAco3Zg9yQXhoIvLrmxgciYhIzLFnfFzec0bgnqoSNL5v1PbP3DCtod+SlwSwCwKy66yoqDta2SLI8v7yga5ZtRGJlmJzOxD/Ua0MVl0TqnAM9PcM2XckOeqqK919Ahnb7WWEFaXyH3GGPSW7EGzS08zFstZKL7caayLX+KMH5wOS+4wuTHYLBibnibH15D7x7xX3MWQP+7gpqlsdASlcecz7P+u3EZYN5JReHxF1tjmbO/MLJVvpNd6Gbl3Uy52acOOQ1dQ3U3caH2YVElYDdy2G2REuo0M6CFztSsIrqPQYZynDIL27S3n1h9kU1kPqo/j8GrwcLvRWmieRpu7drsYPf6eV9MkmDWTTZuUk9kBxM+ZPz/f8jxQWR7Ua8VXeFqQ60253r0ZCyoDxqVbL+NH5eWyETAPLUtWtaCqGOpHEGYUMc7UL4DQNcHet+GRg/cM0jrbcDBuRpNHc43zUA6Gi8q4H2+rvLQEuJyNKeruVAT1Llzm+wCRA2huvvBjp/Fkv7Du/9Uv/4PuE6a6TAUQs/FB2iTipCmL6YStPhPGaNWDjXhosuDO60u9cjmBvj/WPT+kxb%2Cundefined%22%7D%5D; TG-TRACK-CODE=search_code; __lg_stoken__=088c1af26be2838d1d573674410bf147c36f22f38531e139182256f11ce15abfbb27d595556441969b654d562307c3bd2e976350ea133ae893516e36ead67dc61c23dce19fee; _gid=GA1.2.1211680189.1623061783; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1622634166,1623138711; _gat=1; LGSID=20210608155152-30d98c5a-b878-415a-b121-ad6a8b3eb920; PRE_UTM=m_cf_cpt_baidu_pcbt; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fother.php%3Fsc.a00000aoFcBktLjyrBy7agfocxEPobkY7MlxyQpxXIe%5FAwP6Dub4ntD7-SNDN6i0%5FKqsHVbk4HNOl1xMetUt1ePMYzZJFbTNKAa1iy%5FUnLKRDC1bIUsnKztW9GOhLmil9A29epCDcvXk-L3FU4cfKkDDPEjFIq-uVHwJCO1d780N9ANf-qiOkyepMPwvgX6xyd%5FN%5FNObko0%5FD3vrD0wKIgg-sKKv.7Y%5FNR2Ar5Od663rj6tJQrGvKD77h24SU5WudF6ksswGuh9J4qt7jHzk8sHfGmYt%5FrE-9kYryqM764TTPqKi%5FnYQZHuukL0.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqs2v4%5FsKdTvNzgLw4TARqn0K9u7qYXgK-5Hn0IvqzujL0oUhY0ZFWIWYk0ZNzU7qGujYkPHcLPjD3rjDd0Addgv-b5HDYn1n3Pjfz0AdxpyfqnHDsnjRsP100UgwsU7qGujYknWcLnsKsI-qGujYs0A-bm1dcHbc0TA-b5Hf0mv-b5H6Y0APzm1YzPj0YPs%26ck%3D7724.8.58.335.75.376.153.161%26dt%3D1623138705%26wd%3D%25E6%258B%2589%25E9%2592%25A9%26tpl%3Dtpl%5F12273%5F25609%5F21806%26l%3D1527418815%26us%3DlinkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E6%25258B%25259B%2525E8%252581%252598%2525E3%252580%252591%2525E5%2525AE%252598%2525E6%252596%2525B9%2525E7%2525BD%252591%2525E7%2525AB%252599%252520-%252520%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E9%2525AB%252598%2525E8%252596%2525AA%2525E5%2525A5%2525BD%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E4%2525B8%25258A%2525E6%25258B%252589%2525E5%25258B%2525BE%21%2526linkType%253D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm%5Fsource%3Dm%5Fcf%5Fcpt%5Fbaidu%5Fpcbt; __SAFETY_CLOSE_TIME__21308400=1; SEARCH_ID=02df2acbdb08455babf374f9702b04f7; X_HTTP_TOKEN=562f4ee7d6490da71088313261a7d7d9e14d6f5ef1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2221308400%22%2C%22%24device_id%22%3A%2217935c7ac65b52-016a6874dcc481-d7e1739-921600-17935c7ac66a79%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22m_cf_cpc_baidu_pc%22%2C%22%24latest_utm_campaign%22%3A%22distribution%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2291.0.4472.77%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22first_id%22%3A%2217935c7ac65b52-016a6874dcc481-d7e1739-921600-17935c7ac66a79%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1623138802; LGRID=20210608155403-3f6fca8e-eebc-4cc0-a42b-7e6e3d5e739a',
    'referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

# 构建请求链接
# def make_url(page):
#
#     url = u'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false' + urlencode(data)
#     return url

url= 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
# 请求每一页的链接，根据页数和header列表长度的余数随机取header的值
def get_index_page(url,page):
    data = {
        'first': 'false',
        'pn': page,
        'kd': '爬虫',
        'sid': 'e1f135c9b49541e2903352eb183b3a81'
    }
    try:
        reponse = requests.post(url, headers=header, data=data)
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        print('请求职位列表页错误')
        return None
# 解析列表页
def parse_job_page(response):
    result = json.loads(response)
    if result:
        jobs = result['content']['positionResult']['result']
        for job in jobs:
            company_name = job['companyFullName']
            city = job['city']
            financ = job['financeStage']
            job_name = job['positionName']
            job_year = job['workYear']
            job_createtime = job['createTime']
            job_salary = job['salary']
            job_data = {
                'company_name': company_name,
                'city': city,
                'financ': financ,
                'job_name': job_name,
                'job_year': job_year,
                'job_createtime': job_createtime,
                'job_salary': job_salary
            }
            if job_data:
                save_to_mongo(job_data)
# 保存到mongoDB数据库
def save_to_mongo(result):
    if collection.insert(result):
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
