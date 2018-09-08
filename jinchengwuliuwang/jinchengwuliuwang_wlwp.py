# -*- coding: utf-8 -*-
import requests
import time
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class JinchengwuliuSpider(baseSpider):
    name = 'wuliuwangping'
    allowed_domains = ['http://info.jctrans.com']

    def start_requests(self):
        bash_url = 'http://info.jctrans.com/xueyuanpd/trans_comment/default'
        last_url = '.shtml'
        for i in range(1,20):#20
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
        news = response.xpath('//*[@id="main"]/div[2]/div[1]/div/p[2]/span/text()').extract()
        for i in range(len(news_urls)):
            if i > len(news):
                news_url = 'http://info.jctrans.com' + news_urls[i]
                publish_time = publish_times[i]
                yield Request(news_url,self.parse_artical, meta = {'url':news_url,'publish_time':publish_time},dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']

        #新闻标题
        news_title = response.xpath('//title/text()').extract_first().strip('\r\n ')[:-11]

        news_author = response.xpath('//*[@id="content"]/p[5]/text()').extract_first().strip('\r\n ')[-2:]
        if news_author == None:
            news_author = ''

        #发布时间：
        publish_time1 = response.meta['publish_time'].strip('\r\n ')[1:-1] + ':' + '00'
        publish_time = publish_time1[0:4] + publish_time1[5:7] +publish_time1[8:10] + ' ' +publish_time1[-8:]

        # 正文
        '''可以考虑下使用文章密度算法来快速解析文章正文'''
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        #标签
        d = response.xpath('//div[@class="pl"]/a/span/u/text()|//*[@id="new_container"]/div/div[1]/div[3]/div[4]/p[2]/text()').extract()
        if d != []:
            news_tags = ','.join(d[2:]).strip('\r\n')
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
                           website_block = '物流网评',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_tags = news_tags,
                           news_content = news_content,
                           image_urls=image_urls,
                           image_names=image_names,
                           )


