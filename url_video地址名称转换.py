from 爬虫小项目.config import conn

for i in conn.smembers('url_video'):
    a = bytes.decode(i)
    if a == 'mr':
        conn.srem('url_video', a)
        print('删除一个')
    else:
        m = a.split('=')[-1]
        print(m)
        conn.sadd('url_video', m)
        conn.srem('url_video', a)