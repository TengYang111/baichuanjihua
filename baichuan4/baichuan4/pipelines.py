# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import codecs
import os

class Baichuan4Pipeline(object):
    def process_item(self, item, spider):
        file_name1 = item['news_title']
        file_name1 += ".txt"
        file_name = r"C:\Users\ME\Desktop\Python project\pachong\scrapy\baichuan4/" + '证券时报网'
        # 创建主目录
        if (not os.path.exists(file_name)):
            os.makedirs(file_name)
        third_file_name = file_name + '/' + item['website_block'] # 创建副副目录
        if (not os.path.exists(third_file_name)):
            os.makedirs(third_file_name)
        path = third_file_name

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

