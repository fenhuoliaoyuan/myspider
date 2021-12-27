import re
from lxml import etree
from down_from_url import down_from_url
from 类库 import get_page_text
from concurrent.futures import ThreadPoolExecutor

# yuMing = 'https://ohentai.org/'
yuMing = ''
class OhentaiOrg():
    @staticmethod
    def getVideoDetailUrlList():
        videoDetailUrlListAll = []
        for page in range(1, 4):
            url = 'https://hentaiworld.tv/3d/page/{}/'.format(page)
            page_text = get_page_text(url=url,acount=0)
            if page_text is not None:
                page_text = page_text.text
                tree = etree.HTML(page_text)
                videoDetailUrlList = tree.xpath('//div[@class="display-all-posts-background"]/a/@href')
                videoDetailUrlList = [yuMing+i for i in videoDetailUrlList]
                videoDetailUrlListAll.extend(videoDetailUrlList)
                # print(videoDetailUrl)
        return videoDetailUrlListAll
    @staticmethod
    def getVideoURLTitleAndMp4List(videoDetailUrlList):
        VideoURLTitleAndMp4List = []
        for videoDetailUrl in videoDetailUrlList:
            page_text = get_page_text(url=videoDetailUrl, acount=0)
            if page_text is not None:
                page_text = page_text.text
                tree = etree.HTML(page_text)
                title = tree.xpath('//h1[@class="entry-title"]/text()')[0].strip().replace('.','_').replace(':','').replace('!','').replace('?','').replace('*','')
                videoURLMp4 = re.compile('''<source src=\'(.*?)\' type='video/mp4'>''').findall(page_text)
                a = 1
                while title in [i.split('##')[0] for i in VideoURLTitleAndMp4List]:
                    title = title[::-1].replace(str(a-1),'',1)[::-1]
                    title = title + str(a)
                    a = a + 1
                if len(videoURLMp4)>0:
                    VideoURLTitleAndMp4List.append(title+'##'+videoURLMp4[0])
                    print(title+'##'+videoURLMp4[0])
        return VideoURLTitleAndMp4List

if __name__ == '__main__':
    # for page in range(1,4):
    #     url = 'https://hentaiworld.tv/3d/page/{}/'.format(page)
    videoDetailUrlList = OhentaiOrg.getVideoDetailUrlList()
    print(len(videoDetailUrlList))
    videoURLTitleAndMp4List = OhentaiOrg.getVideoURLTitleAndMp4List(videoDetailUrlList)
    with ThreadPoolExecutor(10) as tp:
        for videoURLTitleAndMp4 in videoURLTitleAndMp4List:
            tp.submit(down_from_url, videoURLTitleAndMp4)



