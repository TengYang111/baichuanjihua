# -*- coding: utf-8 -*-
import requests
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class InformationFhSpider(baseSpider):
    name = 'gundong'
    allowed_domains = ['tech.163.com']
    start_urls = ['http://tech.163.com/special/000915BE/iPhoneAPP.html']

    def start_requests(self):
        for i in range(1,11):
            if i == 1:
                website_url = self.start_urls[0]
            elif i == 10:
                website_url = 'http://tech.163.com/special/000915BE/iPhoneAPP_10.html'
            else:
                website_url = 'http://tech.163.com/special/000915BE/iPhoneAPP_0' + str(i) + '.html'
            if requests.get(website_url).status_code != 403:
                yield Request(website_url, self.parse_news,dont_filter=True)
            else:
                break

    def parse_news(self,response):#这个函数做的是获取新闻的url
        news_urls = response.xpath('//ul[@class="list_f14d"]/li/a/@href').extract()
        for i in range(len(news_urls)):
            news_url = news_urls[i]
            yield Request(news_url,self.parse_content,meta = {'url':news_url},dont_filter=True)

    def parse_content(self,response):
        #这个函数是用来解析新闻页面的
        ID = 'songtengteng'

        # 文章url
        news_url = response.meta['url']

        # 文章标题
        news_title = response.xpath('//h1/text()').extract_first()

        #文章正文
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text


        # 发布时间
        publish_time = response.xpath('//div[@class="post_time_source"]/text()').extract_first().lstrip().rstrip()
        if publish_time != None:
            publish_time = publish_time[:19]
        year = publish_time[:4]
        month = publish_time[5:7]
        day = publish_time[8:10]
        publish_time = year + month + day + ' ' + publish_time[-8:]

        #作者
        news_author = response.xpath('//div[@class="post_time_source"]/a/text()').extract_first()

        #获取文章的图片和名称
        image_urls = []
        image_names = []
        image_urls1 = response.xpath('//p[@class="f_center"]/img/@src').extract()
        if image_urls1 != []:
            image_urls = image_urls1
            for i in range(len(image_urls)):
                if i <10 and i>=0:
                    image_name = news_title + '000' + str()
                    image_names.append(image_name)
                elif i <100 and i>=10:
                    image_name = news_title + '00' + str()
                    image_names.append(image_name)
                elif i <1000 and i>=100:
                    image_name = news_title + '0' + str()
                    image_names.append(image_name)
                else:
                    image_name = news_title + str()
                    image_names.append(image_name)

        yield self.getItem(id = ID,
                           news_url = news_url,
                           website_name = '网易科技',
                           website_block = '滚动频道',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_content = news_content,
                           image_urls = image_urls,
                           image_names = image_names,
                           )

