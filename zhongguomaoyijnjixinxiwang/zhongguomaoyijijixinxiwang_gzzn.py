# -*- coding: utf-8 -*-
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class GpjSpider(baseSpider):
    name = 'gzzn'
    allowed_domains = ['gpj.mofcom.gov.cn']
    start_urls = [
                  'http://gpj.mofcom.gov.cn/article/bu/',
                  ]
    url = 'http://gpj.mofcom.gov.cn'

    def parse(self, response):
        #构造不同版块下的页面url
        url = self.start_urls[0]
        yield Request(url, self.parse_news,meta={'url':self.url})

    def parse_news(self,response):
    #获取所有页面的所有新闻url
        news_urls = response.xpath('//*[@id="leftList"]/div[2]/dl/dd/ul/li/a/@href').extract()
        for i in range(len(news_urls)):
            news_url = response.meta['url'] + news_urls[i]
            yield Request(news_url,self.parse_content,meta={"url":news_url})

    def parse_content(self,response):
        #这个函数用作新闻的具体解析

        ID = 'songtengteng'

        website_name = '商务部贸易救济调查局'

        # 网站板块
        website_block = response.xpath("//div[@class='position']/a[2]/text()").extract_first()

        news_url = response.meta['url']

        # 作者
        news_author_list = response.xpath('//script')
        if len(news_author_list) != 0:
            news_author = news_author_list.re('v.{2}\ss.{4}e\s=\s\"[\u4e00-\u9fa5]+\"')[0][13:].replace('"','')
        else:
            news_author = '商务部贸易救济调查局'

        # 新闻发布时间，统一格式：YYYY MM DD HH:Mi:SS           v.{2}\stm\s=\s\".*\"
        publish_time = response.xpath('//script').re('v.{2}\stm\s=\s\".*\"')[0][9:].replace('"','')
        year = publish_time[0:4]
        month = publish_time[5:7]
        day = publish_time[8:10]
        juti_time = publish_time[-8:]
        publish_time = year + month + day + ' ' + juti_time

        # 新闻自带标签
        news_tags = response.xpath('//script').re('v.{2}\sc.+e\s=\s\"[\u4e00-\u9fa5]+\"')[0][14:].replace('"','')

        # 新闻标题
        news_title = response.xpath('//h3/text()').extract_first()

        # 新闻正文
        a = Article(response.url, language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        #获取文章的图片和名称
        image_urls = []
        image_names = []
        image_urls1 = response.xpath('//p[@class="detailPic"]/img/@src|//div[@class="article_con"]/center/img/@src|//p[@style="text-align: center"]/img/@src').extract()
        if image_urls1 != []:
            image_urls = image_urls1
            for i in range(len(image_urls)):
                if i <10 and i>=0:
                    image_name = news_title + '_000' + str(i)
                    image_names.append(image_name)
                elif i <100 and i>=10:
                    image_name = news_title + '_00' + str(i)
                    image_names.append(image_name)
                elif i <1000 and i>=100:
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
                           news_tags = news_tags,
                           news_content = news_content,
                           image_urls=image_urls,
                           image_names=image_names,
                           )
