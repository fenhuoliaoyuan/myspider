url= 'https://0316.workarea2.live/index.php'
import requests,random
from 爬虫小项目.config import user_agent_list
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'cookie': '__utmc=164493566; __utmz=164493566.1626284673.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); CLIPSHARE=ulabql9ahngja1j2nl9rg563v7; 91username=2662t%2FZjXPkp49gDS%2B8dALwQnlfMa8mhFF5mK%2FUiN7rksebuq78QPZZlZw; school=3953wHnzwza0Eped88DCiIF51tn5sao6WXYkORQ; level=8dedu9jnYbezwutsfpfdVbYH3u462qcOsNCQNMZT; cf_clearance=o33XO.EtK43nttnHGAZYoTbuGhhTDNiyaRC2xKhsBbw-1634697270-0-150; __utma=164493566.912930536.1626284673.1635857749.1635915768.51'
    }
res = requests.get(url,headers=headers)
print(res.text)