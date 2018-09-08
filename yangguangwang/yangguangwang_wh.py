# -*- coding: utf-8 -*-
import requests
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class YangguangwangSpider(baseSpider):
    name = 'yangguangwang_wh'
    allowed_domains = ['www.cnr.cn']

    def start_requests(self):
        bash_url = 'http://www.cnr.cn/chanjing/wenhua/'
        last_url = '.html'
        for i in range(1, 100):  # 100
            if i == 1:
                url = bash_url
            else:
                url = bash_url + 'index_' + str(i) + last_url
            if requests.get(url).status_code != 403:
                yield Request(url, self.parse)
            else:
                break

    def parse(self, response):  # 每个页面所有新闻列表链接
        news_urls = response.xpath('//div[@class="text"]/strong/a/@href').extract()
        for i in range(len(news_urls)):
            news_url = news_urls[i]
            yield Request(news_url, self.parse_artical, meta={'url': news_url}, dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']


        # 新闻标题
        news_title = response.xpath('//h2/text()').extract_first()


        # 作者
        a = response.xpath('//div[@class="source"]/span[2]/text()').extract_first()
        if a == None:
            news_author = ''
        else:
            news_author = a[3:]

        # 发布时间
        publish_time = response.xpath('//div[@class="source"]/span[1]/text()').extract_first()
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

        # 标签
        news_tags = ''


        #图片
        image_urls1 = response.xpath('//p[@align="center"]/img/@src').extract()
        image_names1 = response.xpath('//p[@align="center"]/text()').extract()
        image_urls = []
        image_names = []
        if image_urls1 != []:
            if image_names1 != []:
                for i in range(len(image_urls1)):
                    image_url = news_url[:-25] + image_urls1[i]
                    image_urls.append(image_url)
                    image_title = image_names1[i]
                    image_names.append(image_title)
            else:
                for i in range(len(image_urls1)):
                    image_url = news_url[:-25] + image_urls1[i]
                    image_urls.append(image_url)
                    if i >= 0 and i < 10:
                        image_title = news_title + '000' + str(i)
                    elif i >= 10 and i < 100:
                        image_title = news_title + '00' + str(i)
                    elif i >= 100 and i < 1000:
                        image_title = news_title + '0' + str(i)
                    else:
                        image_title = news_title + str(i)
                    image_names.append(image_title)

        yield self.getItem(id=ID,
                           news_url=news_url,
                           website_name='央广网',
                           website_block='文化',
                           news_title=news_title,
                           publish_time=publish_time,
                           news_author=news_author,
                           news_tags=news_tags,
                           news_content=news_content,
                           image_urls=image_urls,
                           image_names=image_names
                           )




