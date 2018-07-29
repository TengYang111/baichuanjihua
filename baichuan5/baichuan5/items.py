# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Baichuan5Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()#爬虫作者
    website_name = scrapy.Field() #站点名称
    website_block = scrapy.Field() #版块
    news_url = scrapy.Field() #新闻链接
    news_author = scrapy.Field() #作者
    publish_time = scrapy.Field() #发布时间
    crawl_time = scrapy.Field() #爬取时间
    news_tags = scrapy.Field() #标签
    news_title = scrapy.Field() #新闻标题
    news_content = scrapy.Field() #正文
    request_url = scrapy.Field() #数据源链接
    img_title = scrapy.Field() #图片名称
    img_url = scrapy.Field() #图片链接