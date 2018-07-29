# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class BaichuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #大板块的url
    parent_url = scrapy.Field()
    #小板块的url
    post_url=scrapy.Field()
    #小版块的名字
    post_name=scrapy.Field()
    #路径
    path = scrapy.Field()
    #爬虫作者
    name_id=scrapy.Field()
    #网站名
    website_name=scrapy.Field()
    #网站板块
    website_block=scrapy.Field()
    #新闻链接
    news_url=scrapy.Field()
    #新闻作者
    news_author=scrapy.Field()
    #新闻发布时间
    publish_time=scrapy.Field()
    #新闻抓取时间
    crawl_time=scrapy.Field()
    #新闻自带标签
    news_tags=scrapy.Field()
    #新闻标题
    news_title=scrapy.Field()
    #新闻正文
    news_content=scrapy.Field()
