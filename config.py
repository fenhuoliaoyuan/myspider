import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.lagou
collection = db['spider']
# MONGO_URL : ''