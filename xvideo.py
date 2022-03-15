import re
import time

from Crypto.Cipher import AES
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from configXvideo import *
from tools import *


class downloadM3u8(object):
    cryptor = ''
    tq = ''
    PATH_DIR = ''
    PATHTSDIR = ''
    @staticmethod
    def createDir(PATH_DIR):
        pathList = PATH_DIR.split('\\')
        path_dir = ''
        for i in range(0, len(pathList)):
            if i == 0:
                path_dir = pathList[0]
            else:
                path_dir = path_dir + '\\' + pathList[i]
                if not os.path.exists(path_dir):
                    os.mkdir(path_dir)

    @classmethod
    def get_cryptor(cls, url_m3u8):
        """
        获取解密对象
        :param url_m3u8:
        :return:
        """
        headers = {
            'user-agent': random.choice(user_agent_list)
        }
        url_qianzui = '/'.join(url_m3u8.split('.m3u8')[0].split('/')[:-1]) + '/'
        response = requests.get(url=url_m3u8, headers=headers)
        m3u8_txt = response.text
        ts_list = []
        url_key = ''
        for line in m3u8_txt.split('\n'):
            if 'URI' in line:
                url_key = url_qianzui + re.compile('URI="(.*)"').findall(line)[0]
            elif '.ts' in line:
                ts_list.append(url_qianzui + line)
        if len(url_key) == 0:
            return ts_list
        else:
            headers = {
                'user-agent': random.choice(user_agent_list)
            }
            key_byte = requests.get(url=url_key, headers=headers).content
            cls.cryptor = AES.new(key_byte, AES.MODE_CBC)
            return cls.cryptor, ts_list

    @classmethod
    def download_1(cls, ts_url):
        """
        下载方式1
        :param ts_url:
        :return:
        """
        if '?' in ts_url:
            name_ts = ts_url.split('?')[0]
        try:
            name_ts = name_ts.split('/')[-1]
        except:
            name_ts = ts_url.split('/')[-1]
        if not os.path.exists(cls.PATHTSDIR + '\\' + name_ts):
            ts = get_ts(ts_url, acount=0)
            if ts is not None:
                ts = ts.content
                ts_open = cls.cryptor.decrypt(ts)
                with open(cls.PATHTSDIR + '\\' + name_ts, 'wb') as wt:
                    wt.write(ts_open)
                cls.tq.update(1)
        else:
            cls.tq.update(1)

    @classmethod
    def download_2(cls, ts_url):
        if '?' in ts_url:
            name_ts = ts_url.split('?')[0]
        try:
            name_ts = name_ts.split('/')[-1]
        except:
            name_ts = ts_url.split('/')[-1]
        if not os.path.exists(cls.PATHTSDIR + '\\' + name_ts):
            ts = get_ts(ts_url, acount=0)
            if ts is not None:
                ts = ts.content
                # name_ts = name_ts.split('.')[0]
                # ts_open = cryptor.decrypt(ts)
                # dict_ts[name_ts]= ts_open
                with open(cls.PATHTSDIR + '\\' + name_ts, 'wb') as wt:
                    wt.write(ts)
                    # print(name_ts)
                    cls.tq.update(1)
        else:
            cls.tq.update(1)

    @staticmethod
    def response(url):
        """
        获取网页
        :param url:
        :return:
        """
        headers = HEADERS
        res = requests.get(url=url, headers=headers)
        return res

    @classmethod
    def downloadOfm3u8(cls, data):
        videoName = data['videoName']
        url_m3u8 = data['url_m3u8']
        cls.PATH_DIR = data['PATH_DIR']
        cls.PATHTSDIR = data['PATHTSDIR']
        videoName = videoName.replace(':', '_').replace('/', '_').replace('!', '_').replace('?', '_').replace('|','_').replace('*', '_').replace('\n', '').replace('.','_')
        cls.createDir(cls.PATH_DIR)
        cls.createDir(cls.PATHTSDIR)
        print(videoName+'下载中...')
        path_name = cls.PATH_DIR + '\\' + videoName + '.ts'
        dataList = []
        if len(videoName) > 0 and len(url_m3u8) > 0:
            data = {
                "path_name": path_name,
                "url_m3u8": url_m3u8
            }
            dataList.append(data)
        # while True:
        #     videoName = input('输入番号名称：').replace(':', '_').replace('/', '_').replace('!', '_').replace('?', '_').replace(
        #         '|',
        #         '_').replace(
        #         '*', '_').replace('\n', '')
        #     path_name = PATH_DIR + '\\' + videoName + '.ts'
        #     url_m3u8 = input('输入m3u8地址：')
        #     if len(videoName) > 0 and len(url_m3u8) > 0:
        #         data = {
        #             "path_name": path_name,
        #             "url_m3u8": url_m3u8
        #         }
        #         dataList.append(data)
        #     else:
        #         break
        if len(dataList) > 0:
            for data in dataList:
                start_time = int(time.time())
                path_name = data["path_name"]
                url_m3u8 = data["url_m3u8"]
                if not os.path.exists(path_name.replace('.ts', '.mp4')) and not os.path.exists(path_name):
                    tuple_test = cls.get_cryptor(url_m3u8)
                    # if len(list(tuple_test)) < 3:
                    if type(tuple_test) is tuple:
                        cls.cryptor, ts_list = tuple_test

                        # tq = tqdm(total=len(ts_list))
                        # ts_list = [yuMing + '/'.join(m3u8_.split('/')[:-1]) + '/' + i.split('/')[-1] for i in ts_list]
                        cls.tq = tqdm(total=len(ts_list))
                        list_ts_file = ''
                        while len(list_ts_file) < len(ts_list):
                            with ThreadPoolExecutor(10) as tp:
                                for ts_url in ts_list:
                                    tp.submit(cls.download_1, ts_url)
                                list_ts_file = os.listdir(cls.PATHTSDIR)
                        cls.tq.close()
                        print('ts下载完成')
                    elif type(tuple_test) is list:
                        ts_list = tuple_test
                        list_ts_file = ''

                        # ts_list = [yuMing + '/'.join(m3u8_.split('/')[:-1]) + '/' + i.split('/')[-1] for i in ts_list]
                        cls.tq = tqdm(total=len(ts_list))
                        while len(list_ts_file) < len(ts_list):
                            with ThreadPoolExecutor(4) as tp:
                                for ts_url in ts_list:
                                    tp.submit(cls.download_2, ts_url)
                                    list_ts_file = os.listdir(cls.PATHTSDIR)
                        cls.tq.close()
                        print('ts下载完成')

                    list_ts_file = os.listdir(cls.PATHTSDIR)
                    if len(list_ts_file) >0:#过滤掉m3u8返回错误的情况
                        # 弄掉'?'
                        if '?' in ts_list[0]:
                            ts_list = [i.split('?')[0] for i in ts_list if '?' in i]
                        with open(path_name, 'ab') as ab:
                            for i in [j.split('/')[-1] for j in ts_list]:
                                with open(cls.PATHTSDIR + '\\' + i, 'rb') as rb:
                                    ab.write(rb.read())
                            print(path_name + '合并完成')
                        for j in [cls.PATHTSDIR + '\\' + i for i in list_ts_file]:
                            # print(j)
                            os.remove(j)
                        print('ts删除完成')
                        end_time = int(time.time())
                        time_all = end_time - start_time
                        print('执行时间为：' + str(time_all) + 's')
            fanhao_zhangma(cls.PATH_DIR)


if __name__ == '__main__':
    PATHTSDIR = r'E:\tsAvolTv'
    PATH_DIR = r'G:\ghs\未分类'
    videoName = input('输入番号名称：').replace(':', '_').replace('/', '_').replace('!', '_').replace('?', '_').replace('|','_').replace('*', '_').replace('\n', '')
    url_m3u8 = input('输入m3u8地址：')
    data = {
        'videoName': videoName,
        'url_m3u8': url_m3u8,
        'PATH_DIR': PATH_DIR,
        'PATHTSDIR': PATHTSDIR
    }
    downloadM3u8.downloadOfm3u8(data=data)
