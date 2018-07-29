# -*- coding: utf-8 -*-
import re
from scrapy import log
class RedisCollection(object):
    def __init__(self,OneUrl):
        self.collectionname = OneUrl
    def getCollectionName(self):
        # name = None
        if self.IndexAllUrls() is not None:
            name = self.IndexAllUrls()
        else:
            name = 'publicurls'
        # log.msg("the collections name is %s"(name),log.INFO)
        return name
    def IndexAllUrls(self):
        allurls = ['wooyun','freebuf']
        result = None
        for str in allurls:
            if re.findall(str,self.collectionname):
                result = str
                break
        return result