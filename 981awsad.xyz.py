import re
import time

from Crypto.Cipher import AES
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from configAwsadXyz import *
from tools import *
if not os.path.exists(PATHTSDIR):
    os.mkdir(PATHTSDIR)
if not os.path.exists(PATH_DIR):
    os.mkdir(PATH_DIR)


def get_cryptor(url_m3u8):
    """
    获取解密对象
    :param url_m3u8:
    :return:
    """
    headers = {
        'user-agent': random.choice(user_agent_list)
    }
    url_qianzui = '/'.join(url_m3u8.split('/')[:-1]) + '/'
    url_qianzui = 'https://wetytrytuyu.com'
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
        cryptor = AES.new(key_byte, AES.MODE_CBC)
        return cryptor, ts_list


def download_1(ts_url):
    """
    下载方式1
    :param ts_url:
    :return:
    """
    name_ts = ts_url.split('/')[-1]
    if not os.path.exists(PATHTSDIR + '\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content
            ts_open = cryptor.decrypt(ts)
            with open(PATHTSDIR + '\\' + name_ts, 'wb') as wt:
                wt.write(ts_open)
            tq.update(1)
    else:
        tq.update(1)


def download_2(ts_url):
    name_ts = ts_url.split('/')[-1]
    if not os.path.exists(PATHTSDIR + '\\' + name_ts):
        ts = get_ts(ts_url, acount=0)
        if ts is not None:
            ts = ts.content
            # name_ts = name_ts.split('.')[0]
            # ts_open = cryptor.decrypt(ts)
            # dict_ts[name_ts]= ts_open
            with open(PATHTSDIR + '\\' + name_ts, 'wb') as wt:
                wt.write(ts)
                # print(name_ts)
                tq.update(1)
    else:
        tq.update(1)


def response(url):
    """
    获取网页
    :param url:
    :return:
    """
    headers = HEADERS
    res = requests.get(url=url, headers=headers)
    return res


if __name__ == '__main__':
    dataList = []
    while True:
        name = input('输入番号名称：').replace(':', '_').replace('/', '_').replace('!','_').replace('?','_').replace( '|', '_').replace('*', '_').replace('\n','')
        path_name = PATH_DIR + '\\' + name + '.ts'
        url_m3u8 = input('输入m3u8地址：')
        if len(name) > 0 and len(url_m3u8) > 0:
            data = {
                "path_name": path_name,
                "url_m3u8": url_m3u8
            }
            dataList.append(data)
        else:
            break
    if len(dataList) > 0:
        for data in dataList:
            start_time = int(time.time())
            path_name = data["path_name"]
            url_m3u8 = data["url_m3u8"]
            if not os.path.exists(path_name.replace('.ts', '.mp4')) and not os.path.exists(path_name):
                tuple_test = get_cryptor(url_m3u8)
                if len(list(tuple_test)) < 3:
                    cryptor, ts_list = tuple_test
                    if '?' in ts_list[0]:
                        ts_list = [i.split('?')[0] for i in ts_list if '?' in i]
                    # tq = tqdm(total=len(ts_list))
                    # ts_list = [yuMing + '/'.join(m3u8_.split('/')[:-1]) + '/' + i.split('/')[-1] for i in ts_list]
                    tq = tqdm(total=len(ts_list))
                    list_ts_file = ''
                    while len(list_ts_file) < len(ts_list):
                        with ThreadPoolExecutor(10) as tp:
                            for ts_url in ts_list:
                                tp.submit(download_1, ts_url)
                            list_ts_file = os.listdir(PATHTSDIR)
                    tq.close()
                    print('ts下载完成')
                else:
                    ts_list = tuple_test
                    list_ts_file = ''
                    if '?'in ts_list[0]:
                        ts_list = [i.split('?')[0] for i in ts_list if '?' in i]
                    # ts_list = [yuMing + '/'.join(m3u8_.split('/')[:-1]) + '/' + i.split('/')[-1] for i in ts_list]
                    tq = tqdm(total=len(ts_list))
                    while len(list_ts_file) < len(ts_list):
                        with ThreadPoolExecutor(10) as tp:
                            for ts_url in ts_list:
                                tp.submit(download_2, ts_url)
                                list_ts_file = os.listdir(PATHTSDIR)
                    tq.close()
                    print('ts下载完成')
                with open(path_name, 'ab') as ab:
                    for i in [j.split('/')[-1] for j in ts_list]:
                        with open(PATHTSDIR + '\\' + i, 'rb') as rb:
                            ab.write(rb.read())
                    print(path_name + '合并完成')
                for j in [PATHTSDIR + '\\' + i for i in list_ts_file]:
                    # print(j)
                    os.remove(j)
                print('ts删除完成')
                end_time = int(time.time())
                time_all = end_time - start_time
                print('执行时间为：' + str(time_all) + 's')
        fanhao_zhangma(PATH_DIR)
