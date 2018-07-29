# -*- coding: utf-8 -*-
# !/usr/bin/python
import scrapy
import time
import random
from bs4 import BeautifulSoup
from scrapy.http import Request
from baichuan4.items import Baichuan4Item


class FinanceSpider(scrapy.Spider):
    name = 'stcn'
    allowed_domains = ['finance.stcn.com/']
    base1 = 'http://'
    base2 = '.stcn.com/'

    def start_requests(self):
        # 构造不同板块的url
        base = ['stock', 'company', 'finance','kuaixun']  # 调试时候记得改数字，加快调试效率
        for i in range(4):
            url = self.base1 + base[i] + self.base2
            #print url
            yield Request(url, self.parse, meta={'url':url,'i':i})  # 调用parse函数

    def parse(self, response):
        url1 = response.meta['url']
        #print url1
        i = response.meta['i']
        #print i

        #有小版块就得到小板块的url，没就构建新的url
        if i == 3:
            url = url1 + 'list/kxyb.shtml'
            print (url)
            yield Request(url,self.parse_two,meta={'url':url}, dont_filter=True)
        elif i == 0:
            a = response.css('.a_title a::attr(href)').extract()
            for aa in range(5):
                if aa ==3:
                    continue
                else:
                    url = url1 + a[aa]
                    print(url)
                    yield Request(url, self.parse_two, meta={'url': url}, dont_filter=True)
        elif i == 1:
            c = response.css('.a_title a::attr(href)').extract()
            for cc in range(3):
                if cc == 2:
                    continue
                else:
                    url = url1 + c[cc]
                    print(url)
                    yield Request(url, self.parse_two, meta={'url': url}, dont_filter=True)
        elif i == 2:
            b = response.css('.a_title a::attr(href)').extract()
            for bb in b:
                url = url1 + bb
                print(url)
                yield Request(url, self.parse_two, meta={'url': url}, dont_filter=True)

    def parse_two(self,response):
        #获得所有页面的链接
        url1 = response.meta['url']
        print (url1)
        for i in range(21):
            if i == 1:
                yemian_url = url1
                yield Request(yemian_url, self.parse_three, meta={'url': url1}, dont_filter=True)
            else:
                yemian_url = url1[:-11] + str(i) +'.shtml'
                yield Request(yemian_url, self.parse_three, meta={'url': url1}, dont_filter=True)

    def parse_three(self,response):
        #得到所有文章的url
        article_urls = response.css('.tit a::attr(href)').extract()
        for article_url in article_urls:
            #print article_url
            yield Request(article_url,self.parse_detail,meta={'url': article_url}, dont_filter=True)

    def parse_detail(self,response):
        #得到文章的正文和标题
        item = {}
        url = response.meta['url']
        # title = response.css('.intal_tit h2::text').extract()
        # #print title
        # content = response.css('.txt_con p::text').extract()
        # # for content in content:
        # # print content

        # 得到中版块名字
        website_block = response.css('.website a::text').extract()[1]
        # print website_block

        # 得到小版块名字
        website_block2 = response.css('.website a::text').extract()[2]
        # print website_block2

        bs = BeautifulSoup(response.text, 'lxml')

        code_div = bs.find('div', attrs={'class': 'intal_tit'})
        # 新闻标题
        news_title = code_div.find('h2').get_text()
        # print news_title

        code_div2 = code_div.find('div').get_text()
        # 新闻作者
        news_author = code_div2[20:]
        # print news_author

        # 新闻发布时间
        publish_time = code_div2[:16]
        second = random.randrange(60)
        publish_time = publish_time + ':' + str(second)
        # print publish_time

        # 新闻抓取时间
        date = str(time.strftime("%Y-%m-%d"))
        currentTime = str(time.strftime("%H:%M:%S"))
        crawl_time = date + ' ' + currentTime
        # print crawl_time

        # 新闻自带标签
        tags = []
        tags.append(website_block)
        tags.append(website_block2)
        # print tags
        news_tags = ','.join(tags)
        # print news_tags

        # 新闻正文
        news = []
        news_content = bs.find('div', attrs={'class': 'txt_con'}).find_all('p')
        for e in range(len(news_content)):
            news.append(news_content[e].get_text())
        news_content = '\n'.join(news)
        # print news_content

        # 将我们导入的item文件进行实例化，用来存储我们的数据。
        item['id'] = '宋腾腾'
        print (item['id'])
        item['website_name'] = website_block
        print (item['website_name'])
        item['website_block'] = website_block2
        print (item['website_block'])
        item['news_url'] = url
        print (item['news_url'])
        item['news_author'] = news_author
        print (item['news_author'])
        item['publish_time'] = publish_time
        print (item['publish_time'])
        item['crawl_time'] = crawl_time
        print (item['crawl_time'])
        item['news_tags'] = news_tags
        print (item['news_tags'])
        item['news_title'] = news_title
        print (item['news_title'])
        item['news_content'] = news_content
        print (item['news_content'])


        yield item