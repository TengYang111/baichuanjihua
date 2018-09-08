# -*- coding: utf-8 -*-
import re
import random
from scrapy import Request
from newspaper import Article
from em_report.spiders.base.baseSpider import baseSpider

class CarpeopleSpider(baseSpider):
    name = 'renmingwang_yuanchuang'
    allowed_domains = ['edu.people.com.cn']
    start_urls = ['http://edu.people.com.cn/GB/367001/index.html']

    def parse(self,response):
        for a in range(1,11):
            block_url = self.start_urls[0][:-5]+str(a)+'.html'
            yield Request(url = block_url, callback = self.parse_news)

    def parse_news(self, response):#获得所有新闻的URl
        news_urls = response.xpath('//ul[@class = "list_16 mt10"]/li/a/@href').extract()
        block_name = response.xpath('/html/body/div[6]/div[1]/div[1]/a[3]/text()').extract_first()
        for news_url in news_urls:
            news_url = self.start_urls[0] + news_url
            yield Request(news_url,self.parse_content, meta = {'url':news_url,'block_name':block_name},dont_filter=True)
    #
    def parse_content(self, response):

        # 作爬取者名称
        ID = ' songtengteng '

        # 站点名称
        website_name = '人民网教育'

        # 版块
        website_block = response.meta['block_name']

        # 新闻链接
        news_url = response.meta['url']

        # 作者
        news_author = response.xpath('//div[@class="box01"]/div[@class="fl"]/a/text()').extract_first()

        # 发布时间
        a = random.randint(1, 61)
        if a >= 0 and a < 10:
            a = '0' + str(a)
        else:
            a = str(a)
        ptime_temp = re.search(u"(20\d+)年(\d+)月(\d+)日(\d+):(\d+)", response.text)
        ptime = ''
        for i in range(1, 7):
            if i < 3:
                ptime = ptime + ptime_temp.group(i) + '-'
            if i == 3:
                ptime = ptime + ptime_temp.group(i) + ' '
            if i > 3 and i < 6:
                ptime = ptime + ptime_temp.group(i) + ':'
            if i == 6:
               publish_time = ptime[0:4] + ptime[5:7] +ptime[8:10] + ' ' + ptime[11:13] + ':'+ ptime[14:16] + ':'+ a

        # 新闻标题
        news_title = response.xpath('//h1/text()').extract()[0].lstrip().rstrip()

        # 正文
        '''可以考虑下使用文章密度算法来快速解析文章正文'''
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        # 图片的链接
        image_names = []
        image_urls = []
        image_urls1 = response.xpath(
            '//p[@style="text-align: center;"]/img/@src|//*[@id="rwb_zw"]/p/img/@src').extract()
        if image_urls1 == []:
            image_urls = []
        else:
            # 图片的名称
            for i in range(len(image_urls)):
                image_url = 'http://edu.people.com.cn' + image_urls1[i]
                image_urls.append(image_url)
                if i >= 0 and i < 10:
                    image_name = news_title + '_000' + str(i)
                    image_names.append(image_name)
                elif i >= 10 and i < 100:
                    image_name = news_title + '_00' + str(i)
                    image_names.append(image_name)
                elif i >= 100 and i < 1000:
                    image_name = news_title + '_0' + str(i)
                    image_names.append(image_name)
                else:
                    image_name = news_title + str(i)
                    image_names.append(image_name)

        yield self.getItem(id = ID,
                           news_url = news_url,
                           website_name = website_name,
                           website_block = website_block,
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_tags = '',
                           news_content = news_content,
                           image_urls=image_urls,
                           image_names=image_names,
                           )
