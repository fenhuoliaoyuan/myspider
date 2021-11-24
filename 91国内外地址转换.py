from config import conn

users_videos_list_url = conn.smembers('91users_videos_list_url')
for users_videos_list_ in users_videos_list_url:
    # print(users_videos_list_)
    URL = bytes.decode(users_videos_list_)
    url = 'https://g0527.91p47.com/' + URL.split('/')[-1]
    conn.sadd('91users_videos_list_url_guonei',url)



