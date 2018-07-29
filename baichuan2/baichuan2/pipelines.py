# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class Baichuan2Pipeline(object):
    def process_item(self, item, spider):
        file_name1 = item['news_title']
        file_name1 += ".txt"
        file_name = r"C:\Users\ME\Desktop\Python project\pachong\scrapy\baichuan2/" + item['website_name']
        # 创建主目录
        if (not os.path.exists(file_name)):
            os.makedirs(file_name)
        second_file_name = file_name + '/' + item['website_block']  # 创建副目录
        if (not os.path.exists(second_file_name)):
            os.makedirs(second_file_name)
        path = second_file_name
        fp = codecs.open(path+'/'+file_name1, 'w')
        fp.write('id : ' + item['id'] + '\n')
        fp.write('website_name : ' + item['website_name'] + '\n')
        fp.write('website_block : ' + item['website_block'] + '\n')
        fp.write('news_url : ' + item['news_url'] + '\n')
        fp.write('news_author : ' + item['news_author'] + '\n')
        fp.write('publish_time : ' + item['publish_time'] + '\n')
        fp.write('crawl_time : ' + item['crawl_time'] + '\n')
        fp.write('news_tags : ' + item['news_tags'] + '\n')
        fp.write('news_title : ' + item['news_title'] + '\n')
        fp.write('news_content : ' + item['news_content'] )
        fp.close()
        return item

class InsertRedis(object):
    def __init__(self):
        self.Redis = RedisOpera('insert')
    def process_item(self,item,spider):
        self.Redis.write(item['news_url'])
        return item