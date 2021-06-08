import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

db = client.lagou
collection = db['spider']

db_Tencent = client.Tencent
spider_tencent = db_Tencent['spider_tencent']
# MONGO_URL : ''