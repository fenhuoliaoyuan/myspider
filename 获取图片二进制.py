url = 'https://i1.hdslb.com/bfs/face/f75bf731289d97abb0e8f31aa037943748a31d1c.jpg@150w_150h.jpg'
# with open(path,'rb') as rb:
import requests
ct = requests.get(url).content
print()
