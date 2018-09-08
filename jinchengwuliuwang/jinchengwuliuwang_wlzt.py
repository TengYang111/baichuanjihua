# -*- coding: utf-8 -*-
import requests
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class JinchengwuliuSpider(baseSpider):
    name = 'wuliuzhuanti'
    allowed_domains = ['http://info.jctrans.com']

    def start_requests(self):
        bash_url = 'http://info.jctrans.com/zhuanti/wlrd/default'
        last_url = '.shtml'
        for i in range(1,15):#15
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
        for i in range(len(news_urls)):
            news_url = news_urls[i]
            yield Request(news_url,self.parse_news,dont_filter=True)

    def parse_news(self,response):
        news_urls = response.xpath('//h3/a/@href').extract()
        for news_url in news_urls:
            news_url = 'http://info.jctrans.com' + news_url
            yield Request(news_url,self.parse_artical, meta = {'url':news_url},dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']

        #新闻标题
        news_title = response.xpath('//h1/text()').extract_first().strip('\r\n ')

        a = response.xpath('//span[@class="tit02"]/text()').extract_first()
        if a == None:
            b = response.xpath('//p[@class="source"]/text()').extract()
            # 作者
            if b != []:
                if len(b[3].strip().split(' ')) == 3:
                    news_author = b[3].strip().split(' ')[2].strip('\r\n ')
                else:
                    news_author = ''
                # 发布时间
                publish_time = b[3].strip().split(' ')[0]+' '+b[3].strip().split(' ')[1]
                year = publish_time[0:4]
                month1 = publish_time[6:7]
                if month1 == '-':
                    month = '0' + publish_time[5:6]
                    day1 = publish_time[8:9]
                    if day1 == ' ':
                        day = '0' + publish_time[7:8]
                    else:
                        day = publish_time[7:9]
                else:
                    month = publish_time[5:7]
                    day1 = publish_time[9:10]
                    if day1 == ' ':
                        day = '0' + publish_time[8:9]
                    else:
                        day = publish_time[8:10]
                hour = publish_time[-8:-7]
                if hour == ' ':
                    hour = '0' + hour
                juti_time = publish_time[-7:]
                publish_time = year + month + day + ' ' + hour + juti_time
        else:
            # 作者
            news_author = a.split(' ')[2]
            if news_author == None:
                news_author = ''
            # 发布时间
            publish_time = a.split(' ')[0] + ' ' + a.split(' ')[1]
            year = publish_time[0:4]
            month1 = publish_time[6:7]
            if month1 == '-':
                month = '0' + publish_time[5:6]
                day1 = publish_time[8:9]
                if day1 == ' ':
                    day = '0' + publish_time[7:8]
                else:
                    day = publish_time[7:9]
            else:
                month = publish_time[5:7]
                day1 = publish_time[9:10]
                if day1 == ' ':
                    day = '0' + publish_time[8:9]
                else:
                    day = publish_time[8:10]
            hour = publish_time[-8:-7]
            if hour == ' ':
                hour = '0' + hour
            juti_time = publish_time[-7:]
            publish_time = year + month + day + ' ' + hour + juti_time

        # 正文
        '''可以考虑下使用文章密度算法来快速解析文章正文'''
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        #标签
        d = response.xpath('//div[@class="pl"]/a/span/u/text()').extract()
        if d != []:
            news_tags = ','.join(d[2:]).strip('\r\n')
        else:
            d1 = response.xpath('//p[@class="key"]/text()').extract()
            news_tags = ''.join(d1)

        #图片
        image_urls1 = response.xpath('//p[@align="center"]/img/@src').extract()
        image_urls = []
        image_names = []
        if image_urls1 != []:
            for i in range(len(image_urls1)):
                image_url = 'http://info.jctrans.com' + image_urls1[i]
                image_urls.append(image_url)
                if i>=0 and i <10:
                    image_title = news_title + '000' + str(i)
                    image_names.append(image_title)
                else:
                    image_title = news_title + '00' + str(i)
                    image_names.append(image_title)

        yield self.getItem(id = ID,
                           news_url = news_url,
                           website_name = '锦程物流网',
                           website_block = '物流专题',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_tags = news_tags,
                           news_content = news_content,
                           image_urls = image_urls,
                           image_names=image_names,
                           )


