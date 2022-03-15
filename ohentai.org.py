import re
from lxml import etree
from down_from_url import down_from_url
from 类库 import get_page_text
from concurrent.futures import ThreadPoolExecutor

yuMing = 'https://ohentai.org/'
class OhentaiOrg():
    @staticmethod
    def getVideoDetailUrlList(url):
        page_text = get_page_text(url=url,acount=0)
        if page_text is not None:
            page_text = page_text.text
            tree = etree.HTML(page_text)
            videoDetailUrlList = tree.xpath('//div[@class="videobrick"]/a[@class="interlink"][1]/@href')
            videoDetailUrlList = [yuMing+i for i in videoDetailUrlList]
            # print(videoDetailUrl)
            return videoDetailUrlList
    @staticmethod
    def getVideoURLTitleAndMp4List(videoDetailUrlList):
        VideoURLTitleAndMp4List = []
        for videoDetailUrl in videoDetailUrlList:
            page_text = get_page_text(url=videoDetailUrl, acount=0)
            if page_text is not None:
                page_text = page_text.text
                tree = etree.HTML(page_text)
                title = tree.xpath('//h1[@class="title"]/text()')[0].strip()
                videoURLMp4 = re.compile('''\{"file"\:\"(.*?)\"\}''').findall(page_text)
                if len(videoURLMp4)>0:
                    VideoURLTitleAndMp4List.append(title+'##'+videoURLMp4[0])
                    print(title+'##'+videoURLMp4[0])
        return VideoURLTitleAndMp4List

if __name__ == '__main__':
    url = 'https://ohentai.org/sery_video.php?seryid=MjY0OQ=='
    videoDetailUrlList = OhentaiOrg.getVideoDetailUrlList(url)
    videoURLTitleAndMp4List = OhentaiOrg.getVideoURLTitleAndMp4List(videoDetailUrlList)
    with ThreadPoolExecutor(8) as tp:
        for videoURLTitleAndMp4 in videoURLTitleAndMp4List:
            tp.submit(down_from_url,videoURLTitleAndMp4)



