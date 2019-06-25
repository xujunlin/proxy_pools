import pymongo
from pymongo import errors
import random



class Mongo_save(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['proxypool']
        self.proxies = self.db['proxies']
        self.proxies.ensure_index('proxy', unique=True)

    def insert_proxy(self, proxy):
        try:
            self.proxies.insert_one(proxy)
        except pymongo.errors.DuplicateKeyError:
            pass

    def delete_proxy(self, proxy):
        self.proxies.delete_one(proxy)

    def update_proxy(self, proxy, value):
        self.proxies.update_one(proxy, {'$': value})

    def get_proxy(self, count):
        proxies = self.proxies.find({}, limit=count)
        return [proxy['proxy'] for proxy in proxies]

    def get_random_proxy(self):
        proxies= self.proxies.find({})
        return random.choice([proxy['proxy'] for proxy in proxies])

    def get_fastest_proxy(self):
        proxies = self.proxies.find({}).sort('delay')
        return [[proxy['proxy'] for proxy in proxies]][0][0]

if __name__ == '__main__':
    m = Mongo_save()
    i = m.get_fastest_proxy()
    print(i)