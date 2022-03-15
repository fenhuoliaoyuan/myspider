from 爬虫小项目.config import ips
with open('ips.txt','a',encoding='utf-8') as tt:
    for i in ips:
        tt.write(i['http'].replace('http://','')+'\n')
