# -*- coding: utf-8 -*-
import requests
import time
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class JinchengwuliuSpider(baseSpider):
    name = 'maoyixinwen'
    allowed_domains = ['http://info.jctrans.com']

    def start_requests(self):
        bash_url = 'http://info.jctrans.com/newspd/myxw/default'
        last_url = '.shtml'
        for i in range(1,19):#19
            if i == 1:
                url = bash_url + last_url
            else:
                url = bash_url + '_' + str(i) + last_url
            if requests.get(url).status_code != 403:
                yield Request(url, self.parse)
            else:
                break

    def parse(self, response):  # 每个页面所有新闻列表链接
        news_urls = response.xpath('//div[@class="liebiao2_left"]/p/a/@href').extract()
        publish_times = response.xpath('//div[@class="liebiao2_left"]/p/span[2]/text()').extract()
        for i in range(len(news_urls)):
            news_url = 'http://info.jctrans.com' + news_urls[i]
            publish_time = publish_times[i]
            yield Request(news_url,self.parse_artical, meta = {'url':news_url,'publish_time':publish_time},dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']

        #新闻标题
        news_title = response.xpath('//title/text()').extract_first()[:-11]

        # 作者
        news_author = response.xpath('//p[@class="source"]/text()').extract()[1].strip()[12:].strip()
        if news_author == None:
            news_author = ''

        # 发布时间
        publish_time = response.meta['publish_time']
        year = publish_time[1:5]
        month = publish_time[6:8]
        day = publish_time[9:11]
        juti_time = publish_time[-6:-1]
        publish_time = year + month + day + ' ' + juti_time + ':' + '00'

        # 正文
        '''可以考虑下使用文章密度算法来快速解析文章正文'''
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        #标签
        d = response.xpath('//p[@class="key"]/text()').extract()
        if d != []:
            news_tags = ','.join(d[1:]).strip('\r\n')
        else:
            news_tags = ''

        #获取文章的图片和名称
        image_urls = []
        image_names = []
        image_urls1 = response.xpath('//p[@style="text-align: center;"]/img/@src|//div[@class="zz_leftneirong4" ]/p/img/@src').extract()
        if image_urls1 != []:
            for i in range(len(image_urls1)):
                image_url = 'http://info.jctrans.com' + image_urls1[i]
                image_urls.append(image_url)
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
                           website_name = '锦程物流网',
                           website_block = '贸易新闻',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_tags = news_tags,
                           news_content = news_content,
                           image_urls=image_urls,
                           image_names=image_names,
                           )


