import os
from tqdm import tqdm

import requests


def get_mp4(url, video_name, path_dir):
    """下载mp4"""
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    path_name = path_dir + '\\' + video_name + '.mp4'
    if not os.path.exists(path_name):
        headers = {
            'range': 'bytes=447938560-',
            'referer': 'https://asianclub.tv/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'video',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers)
        file_size = int(res.headers.get('Content-Length'))  # 获取视频的总大小
        pbar = tqdm(total=file_size)  # 设置进度条的长度
        with open(path_name, 'ab') as wb:
            for chunk in res.iter_content(1024 * 1024 * 2):
                wb.write(chunk)
                pbar.set_description('正在下载中......')
                pbar.update(1024 * 1024 * 2)  # 更新进度条长度
            pbar.close()
        print(video_name + '.mp4下载成功')


if __name__ == '__main__':
    # while True:
    url = 'https://str17.vidoza.net/nvl4ctd4s4eeieno3ubrhw52heqkutxwee2i6na4425klwftxjs6h26je33q/v.mp4'
    video_name = 'ipz-390'
    ''
    path_dir = 'D:\hhh\未分类'
    # url = input('输入mp4地址：')
    # video_name = input('输入影片名：')
    # path_dir = r'F:\番号'
    get_mp4(url=url, video_name=video_name, path_dir=path_dir)
