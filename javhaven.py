import os
import time
import requests
from tqdm import tqdm  # 进度条模块

headers = {
    'Connection': 'keep-alive',
    'Host': 'op153ff.dood.video',
    'Pragma': 'no-cache',
    'Referer': 'https://dood.la/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}
# pathDir = 'G:\\ghs\\hentaiworld.tv'
pathDir = r'G:\ghs\番号'


def down_from_url(urlAndDst):
    try:
        # urlAndDstList = urlAndDst.split('##')
        url = urlAndDst['videoUrl']
        dst = pathDir + '\\' + urlAndDst['videoName'] + '.mp4'
        # 设置stream=True参数读取大文件
        response = requests.get(url, headers=headers, stream=True)
        # 通过header的content-length属性可以获取文件的总容量
        file_size = int(response.headers['content-length'])
        if os.path.exists(dst):
            # 获取本地已经下载的部分文件的容量，方便继续下载，如果不存在就从头开始下载。
            first_byte = os.path.getsize(dst)
        else:
            first_byte = 0
        # 如果大于或者等于则表示已经下载完成，否则继续
        if first_byte >= file_size:
            return file_size
        header = {"Range": "bytes=%d-%d"%(first_byte,file_size)}
        header = dict(header,**headers)
        pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
        req = requests.get(url, headers=header, stream=True)
        with open(dst, 'ab') as f:
            # 每次读取一个1024个字节
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        return file_size
    except:
        return

if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    dataNU = []
    while True:
        videoName = input("名称")
        videoUrl = input('mp4地址')
        if len(videoName)>0 and len(videoUrl)>0:
            data = {
                'videoName':videoName,
                'videoUrl':videoUrl
            }
            dataNU.append(data)
        else:
            break
    if len(dataNU)>0:
        with ThreadPoolExecutor(10) as tp:
            for data in dataNU:
                tp.submit(down_from_url,data)
