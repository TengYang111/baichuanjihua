# -*- coding: utf-8 -*-
import requests
from scrapy.http import Request
from newspaper import Article
from em_report.spiders.base.baseSpider import baseSpider

start_time= '2018-05-16 16:30' #如果第一次爬取，将此时间作为基准时间。

class TechFhSpider(baseSpider):
    name = 'keji'
    allowed_domains = ['tech.ifeng.com']

    def start_requests(self):
        bash_url = 'http://tech.ifeng.com/listpage/803/'
        last_url = '/list.shtml'
        for i in range(100):  # 页面按照改变页数翻页，100页肯定足够，加了判断
            url = bash_url + str(i + 1) + last_url
            if requests.get(url).status_code != 403:
                yield Request(url, self.parse)
            else:
                break

    def parse(self, response):  # 每个页面所有新闻列表链接
        news_urls = response.xpath('//a[@class = "t_css"]/@href').extract()
        for news_url in news_urls:
            yield Request(news_url,self.parse_artical, meta = {'url':news_url},dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']

        #新闻标题
        news_title = response.xpath('//h1/text()').extract_first().strip()

        # 作者
        news_author = response.xpath('//span[@class = "ss03"]/text()').extract_first()

        # 发布时间
        publish_time = response.xpath('//span[@class = "ss01"]/text()').extract_first()
        year = publish_time[0:4]
        month = publish_time[5:7]
        day = publish_time[8:10]
        juti_time = publish_time[-8:]
        publish_time = year + month + day + ' ' + juti_time

        # 正文
        '''可以考虑下使用文章密度算法来快速解析文章正文'''
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        # 数据源链接
        request_url = response.meta['url']
        yield self.getItem(id = ID,
                           news_url = news_url,
                           website_name = '凤凰网科技',
                           website_block = '互联网',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_content = news_content,
                           )


