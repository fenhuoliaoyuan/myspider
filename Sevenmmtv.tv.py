from M3u8SevenMmtv import *
PATHTSDIR = r'E:\tsAvolTv'
PATH_DIR = r'G:\ghs\未分类'
datas = []
while True:
    videoName = input('输入番号名称：').replace(':', '_').replace('/', '_').replace('!', '_').replace('?', '_').replace('|',
                                                                                                                 '_').replace(
        '*', '_').replace('\n', '')
    url_m3u8 = input('输入m3u8地址：')
    if len(videoName)==0 or len(url_m3u8)==0:
        break
    data = {
        'videoName': videoName,
        'url_m3u8': url_m3u8,
        'PATH_DIR': PATH_DIR,
        'PATHTSDIR': PATHTSDIR
    }
    datas.append(data)
for data in datas:
    downloadM3u8.downloadOfm3u8(data=data)