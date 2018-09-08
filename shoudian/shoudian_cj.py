# -*- coding: utf-8 -*-
import requests
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider

class ShoudianSpider(baseSpider):
    name = 'shoudian_cj'
    allowed_domains = ['shoudian.bjx.com.cn']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    start_urls = [
            'http://shoudian.bjx.com.cn/NewsList?id=85',
    ]

    def start_requests(self):
        bash_url = 'http://shoudian.bjx.com.cn/NewsList?id=85'
        last_url = '&page='
        for i in range(1,10):#10
            if i == 1:
                url = bash_url
            else:
                url = bash_url + last_url + str(i)
            url_code = requests.get(url,headers=self.headers).status_code
            if url_code != 403:
                yield Request(url,self.parse,meta={'url':url},headers=self.headers)
                print(url_code)
            else:
                break

    def parse(self, response):  # 每个页面所有新闻列表链接
        news_urls = response.xpath('//ul[@class="list_left_ul"]/li/a/@href').extract()
        publish_times = response.xpath('//ul[@class="list_left_ul"]/li/span/text()').extract()
        for i in range(len(news_urls)):
            news_url = news_urls[i]
            publish_time = publish_times[i]
            yield Request(news_url,self.parse_artical, meta = {'url':news_url,'publish_time':publish_time},dont_filter=True)

    def parse_artical(self, response):  # 具体文章解析
        print('hello')
        ID = 'songtengteng'

        # 新闻链接
        news_url = response.meta['url']
        print(news_url)

        #新闻标题
        news_title = response.xpath('//h1/text()').extract_first()

        # 作者
        news_author = response.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/text()[2]').extract_first()
        if news_author == None:
            news_author = ''
        else:
            news_author = news_author.strip()
        print(news_author)

        # 发布时间
        publish_time = response.meta['publish_time']
        year = publish_time[0:4]
        month = publish_time[5:7]
        day = publish_time[8:10]
        juti_time = response.xpath('').extract()
        publish_time = year + month + day + ' ' + juti_time

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
                           website_name = '北极星售电网',
                           website_block = '财经',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_tags = news_tags,
                           news_content = news_content,
                           image_urls=image_urls,
                           image_names=image_names,

                           )


