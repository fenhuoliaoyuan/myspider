from 转码 import fanhao_zhangma
import os
from concurrent.futures import ThreadPoolExecutor
def tschangetomp4():
    """91porn"""
    with ThreadPoolExecutor(10) as tp:
        path_dir_list = [r'G:\ghs\91porn' + '\\' + i for i in os.listdir(r'G:\ghs\91porn')]
        for path_dir in path_dir_list:
            tp.submit(fanhao_zhangma, path_dir)

if __name__ == '__main__':
    tschangetomp4()