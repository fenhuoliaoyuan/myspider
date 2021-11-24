from 爬虫小项目.config import conn

for i in conn.smembers('ts_url'):
    a = bytes.decode(i)
    m = a.split('/')[-1]
    m = m.replace('.ts', '')
    print(m)
    conn.sadd('ts_url', m)
    conn.srem('ts_url', a)
