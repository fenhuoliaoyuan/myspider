from 爬虫小项目.config import conn

video = conn.smembers('url_video')
for i in list(video)[1:1000]:
    i_str = bytes.decode(i)
    conn.srem('url_video', i_str)
    print(i_str+'删除成功')
