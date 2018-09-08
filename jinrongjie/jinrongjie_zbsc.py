# -*- coding: utf-8 -*-
import requests
import time
import re
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class JinrongjieSpider(baseSpider):
    name = 'zibenshichang'
    allowed_domains = ['http://finance.jrj.com/']

    def start_requests(self):#还有种是按照月份来构造的，这里只爬取前十页
        bash_url = 'http://finance.jrj.com.cn/list/zbsc'
        last_url = '.shtml'
        for i in range(1,11):
            if i == 1:
                url = bash_url + last_url
            else:
                url = bash_url + '-' + str(i) + last_url
            if requests.get(url).status_code != 403:
                yield Request(url, self.parse)
            else:
                break

    def parse(self, response):  # 每个页面所有新闻列表链接
        news_urls = response.xpath('//ul[@class="list2"]/li/a/@href').extract()
        for news_url in news_urls:
            yield Request(news_url,self.parse_artical, meta = {'url':news_url},dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']

        #新闻标题
        news_title = response.xpath('//title/text()').extract_first()[:-9]

        # 作者
        news_author = response.xpath('//div[@class="titmain"]').re('author.*\>')
        if news_author == []:
            a = response.xpath('//div[@class="titmain"]').re('source.*\>')[0]
            news_author = re.search("([\u4e00-\u9fa5]|\d)+.*([\u4e00-\u9fa5]|\d)",a).group()
        else:
            b = response.xpath('//div[@class="titmain"]').re('author.*\>')[0]
            news_author = re.search("([\u4e00-\u9fa5]|\d)+.*([\u4e00-\u9fa5]|\d)", b).group()

        # 发布时间
        c = response.xpath('//div[@class="titmain"]').re('date.*\n.*')[0]
        publish_time = re.search("\d+.*\d", c).group()
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

        #标签
        d = response.xpath('//p[@class="keyword mt20"]').re('\<!.*k.*\>')
        if d != []:
            news_tags = re.findall("[\u4e00-\u9fa5]+",d[0])
            news_tags = ','.join(news_tags)
        else:
            news_tags = ''

        #图片的链接
        image_names = []
        image_urls = response.xpath('//div[@class="texttit_m1"]/p/img/@src|//div[@class="rich_media_content "]/p/img/@src').extract()
        if image_urls == []:
            image_urls = ''
        else:
            image_urls = image_urls
            # 图片的名称
            for i in range(len(image_urls)):
                if i >=0 and i<10:
                    image_name = news_title + '_000' + str(i)
                    image_names.append(image_name)
                elif i>=10 and i <100:
                    image_name = news_title + '_00' + str(i)
                    image_names.append(image_name)
                elif i>=100 and i <1000:
                    image_name = news_title + '_0' + str(i)
                    image_names.append(image_name)
                else:
                    image_name = news_title + str(i)
                    image_names.append(image_name)

        yield self.getItem(id = ID,
                           news_url = news_url,
                           website_name = '金融界资讯',
                           website_block = '资本市场',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_tags = news_tags,
                           news_content = news_content,
                           image_urls = image_urls,
                           image_names = image_names,
                           )

