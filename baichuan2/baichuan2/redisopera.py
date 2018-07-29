# -*- coding: utf-8 -*-
import redis
import time
from scrapy import log
from newscrawl.util import RedisCollection

class RedisOpera:
    def __init__(self,stat):
        log.msg('init redis %s connection!!!!!!!!!!!!!!!!!!!!!!!!!' %stat,log.INFO)
        self.r = redis.Redis(host='localhost',port=6379,db=0)

    def write(self,values):
        # print self.r.keys('*')
        collectionname = RedisCollection(values).getCollectionName()
        self.r.sadd(collectionname,values)
    def query(self,values):
        collectionname = RedisCollection(values).getCollectionName()
        return self.r.sismember(collectionname,values)