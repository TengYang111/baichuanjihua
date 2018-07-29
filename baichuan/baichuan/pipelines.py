# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class BaichuanPipeline(object):
    def process_item(self, item, spider):
        file_name = item['news_title']
        file_name += ".txt"
        fp = codecs.open(item['path']+'/'+file_name, 'w')
        fp.write('name_id : ' + item['name_id'] + '\n')
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
