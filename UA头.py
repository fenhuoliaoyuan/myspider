def get_ua_list():
    with open(r'C:\pachon\study_documents\爬虫小项目\UA头.txt','r',encoding='utf-8') as ua:
        return [{'User-Agent':i.replace('\n','')} for i in ua.readlines()]
if __name__ == '__main__':
    ua_list = get_ua_list()
    print(ua_list)