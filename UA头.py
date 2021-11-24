from 爬虫小项目.config import user_agent_list
with open('UA头.txt','a',encoding='utf-8') as ua:
    for i in user_agent_list:
        ua.write(i+'\n')