import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

# 首先，实现方法 get_page() 来加载单个 Ajax 请求的结果。其中唯一变化的参数就是 offset，所以我们将它当作参数传递，实现如下：
# 这里我们用 urlencode() 方法构造请求的 GET 参数，然后用 requests 请求这个链接，如果返回状态码为 200，则调用 response 的
# json() 方法将结果转为 JSON 格式，然后返回。
def get_page(offset):
    params = {
        'keyword': '街拍美女',
        'pd': 'atlas',
        'source': 'search_subtab_switch',
        'dvpf': 'pc',
        'aid': '4916',
        'page_num': '1',
        'rawJSON': '1',
        'search_id': '202105222157220102121921344017BC5B'
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)#urlencode:将一个由两个元素组成的元组的字典或序列
    # 编码为URL查询字符串。如果查询arg中的任何值是sequence且doseq为true，则每个序列元素都将转换为单独的参数。如果查询arg
    # 是一个序列对于两个元素的元组，输出中参数的顺序将与输入中参数的顺序相匹配。
    try:#反正响应异常
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

# 接下来，再实现一个解析方法：提取每条数据的 image_detail 字段中的每一张图片链接，将图片链接和图片所属的标题一并返回，此时
# 可以构造一个生成器。实现代码如下：
def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_detail')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }

# 接下来，实现一个保存图片的方法 save_image()，其中 item 就是前面 get_images() 方法返回的一个字典。在该方法中，首先根据
# item 的 title 来创建文件夹，然后请求这个图片链接，获取图片的二进制数据，以二进制的形式写入文件。图片的名称可以使用其内容
# 的 MD5 值，这样可以去除重复。相关代码如下：
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')
# 最后，只需要构造一个 offset 数组，遍历 offset，提取图片链接，并将其下载即可：

def main(offset):
    json = get_page(offset)#返回json文件
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()