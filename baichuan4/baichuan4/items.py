# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Baichuan4Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website_name = scrapy.Field()
    big_name = scrapy.Field()
    first_url = scrapy.Field()
    file_name = scrapy.Field()
    news_url = scrapy.Field()
    #爬虫作者
    id = scrapy.Field()
    #网站名
    website_name = scrapy.Field()
    #网站板块
    website_block = scrapy.Field()
    #新闻链接
    news_url = scrapy.Field()
    #新闻作者
    news_author = scrapy.Field()
    #新闻发布时间
    publish_time = scrapy.Field()
    #新闻抓取时间
    crawl_time = scrapy.Field()
    #新闻自带标签
    news_tags=scrapy.Field()
    #新闻标题
    news_title=scrapy.Field()
    #新闻正文
    news_content=scrapy.Field()