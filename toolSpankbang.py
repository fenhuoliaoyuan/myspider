from tqdm import tqdm  # 进度条模块
import os
import requests

pathDir = r'G:\ghs\jav_pmv'


def get_ips():
    with open('ips.txt', 'r', encoding='utf-8') as rd:
        ips = []
        for line in [i.replace('\n', '') for i in rd.readlines()]:
            ip = {
                'http': 'http://' + line,
                # 'https': 'http://' + line
            }
            ips.append(ip)
        # pprint(ips)
        return ips


ips = get_ips()
# proxies = random.choice(ips)



def formatStr(str):
    return str.replace('!', ' ').replace('^', ' ').replace('*', ' ').replace('?', ' ').replace('\n', ' ').replace('<',
                                                                                                                  ' ').replace(
        '>', ' ').replace('|', ' ').replace('/', '').replace('"', ' ').replace('.', ' ').strip()


def down_from_url(data):
    headers = {
        'accept': '*/*',
        # 'accept-encoding': 'identity;q=1, *;q=0',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'range': 'bytes=0-',
        'referer': 'https://jp.spankbang.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'video',
        # 'sec-fetch-mode': 'no-cors',
        # 'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    try:
        # urlAndDstList = urlAndDst.split('##')
        url = data['videoUrl']
        dst = pathDir + '\\' + formatStr(data['videoName']) + '.mp4'
        # 设置stream=True参数读取大文件
        response = requests.get(url, headers=headers, stream=True)
        # 通过header的content-length属性可以获取文件的总容量
        # file_size = int(response.headers['content-length'])
        if 'Content-Range' in response.headers.keys():
            file_size = int(response.headers['Content-Range'].split('-')[-1].split('/')[0])
            if os.path.exists(dst):
                # 获取本地已经下载的部分文件的容量，方便继续下载，如果不存在就从头开始下载。
                first_byte = os.path.getsize(dst)
            else:
                # first_byte = 0
                first_byte = 0
            # 如果大于或者等于则表示已经下载完成，否则继续
            if first_byte >= file_size:
                return file_size
            # 避免连接中断
            while first_byte < file_size:
                try:
                    headers['range'] = "bytes=%d-%d" % (first_byte, file_size)
                    # header = {"Range": "bytes=%d-%d" % (first_byte, file_size)}
                    # header = dict(header, **headers)
                    pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
                    req = requests.get(url, headers=headers, stream=True)
                    with open(dst, 'ab') as f:
                        # 每次读取一个1024个字节
                        for chunk in req.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                pbar.update(1024)
                except:
                    pbar.close()
                    if os.path.exists(dst):
                        # 获取本地已经下载的部分文件的容量，方便继续下载，如果不存在就从头开始下载。
                        first_byte = os.path.getsize(dst)
                else:
                    pbar.close()
                    if os.path.exists(dst):
                        # 获取本地已经下载的部分文件的容量，方便继续下载，如果不存在就从头开始下载。
                        first_byte = os.path.getsize(dst)

    except:
        down_from_url(data=data)


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    dataNU = []
    while True:
        videoName = formatStr(input("影片名："))
        videoUrl = input('mp4地址：')
        if len(videoName) > 0 and len(videoUrl) > 0:
            data = {
                'videoName': videoName,
                'videoUrl': videoUrl
            }
            dataNU.append(data)
        else:
            break
    if len(dataNU) > 0:
        with ThreadPoolExecutor(10) as tp:
            for data in dataNU:
                tp.submit(down_from_url, data)
