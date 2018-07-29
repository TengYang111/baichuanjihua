# -*- coding: utf-8 -*-
# !/usr/bin/python
import scrapy
import time
from bs4 import BeautifulSoup
from scrapy.http import Request
from baichuan2.items import Baichuan2Item

class InsuranceSpider(scrapy.Spider):
    name = 'insurance'
    allowed_domains = ['insurance.cngold.org/']
    bash_url = 'http://insurance.cngold.org/'

    def start_requests(self):
        #构造不同板块的url
        base = ['jgdt/','gsdt/','cxdt/']#调试时候记得改数字，加快调试效率
        for i in range(3):
            url = self.bash_url + base[i]
            # print url
            yield Request(url,self.parse)#调用parse函数

    def parse(self, response):
        items = []  # 创建一个空列表，用来存储匹配到的数据
        website_name = response.css('h1 a span::text').extract_first()#大板块的名字
        # print website_name
        big_name = response.css('.title h2::text').extract_first()  # 小版块的名字
        # print big_name
        first_url = response.css('.fl a[class]::attr(href)').extract_first()  # 小版块的url
        # print first_url
        str1 = response.css('.last a::attr(href)').extract_first()[-13:-9]
        # print str1
        urls = []
        for a in range(1, 12):  # 调试时候记得改数字，加快调试效率
            if a == 1:
                url = first_url
            else:
                url = first_url + 'list_' + str1 + '_' + str(a) + '.html'
            urls.append(url)
        # print urls
        item = Baichuan2Item()  # 实例化一个对象
        item['website_name'] = website_name
        item['first_url'] = urls
        item['big_name'] = big_name
        items.append(item)
        # print items
        for item in items:
            for b in range(11):  # 调试时候记得改数字，加快调试效率
                # print item['first_url'][b]
                yield Request(item['first_url'][b], callback=self.parse_two, meta={'item_1': item}, dont_filter=True)

    def parse_two(self, response):
        # 获得所有新闻的url
        items = []
        item_1 = response.meta['item_1']
        # print item_1
        news_urls = response.css('.tit a::attr(href)').extract()
        # print news_urls
        for c in range(len(news_urls)):
            news_url = news_urls[c]
            if True:
                item = Baichuan2Item()
                item['website_name'] = item_1['website_name']
                item['first_url'] = item_1['first_url']
                item['big_name'] = item_1['big_name']
                item['news_url'] = news_url
                items.append(item)
        # print items
        for item in items:
            # print item
            yield Request(item['news_url'], callback=self.parse_detail, meta={'item_2': item}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item_2']
        items = []
        # print item_2
        bs = BeautifulSoup(response.text, 'lxml')
        # 新闻链接
        news_url = item['news_url']
        # print news_url

        # 新闻标题
        news_title = bs.find_all('h1')[1].get_text()
        # print news_title

        code_span = bs.find('div', attrs={'class': 'article-info'}).find_all('span')
        # print code_span

        # 新闻作者
        if len(code_span) == 3:
            news_author = code_span[1].get_text()[3:]
        else:
            news_author = code_span[0].get_text()
        # print news_author

        # 新闻发布时间
        if len(code_span) == 3:
            publish_time = code_span[2].get_text()
        else:
            publish_time = code_span[1].get_text()
        # print publish_time

        # 新闻抓取时间
        date = str(time.strftime("%Y-%m-%d"))
        currentTime = str(time.strftime("%H:%M:%S"))
        crawl_time = date + ' ' + currentTime
        # print crawl_time

        # 新闻自带标签
        tags = []
        news_tags = bs.find('div', attrs={'class': 'article_con'}).find_all('a')
        for d in range(len(news_tags)):
            tags.append(news_tags[d].get_text())
        # print tags
        news_tags = ','.join(tags)
        # print news_tags

        # 新闻正文
        news = []
        news_content = bs.find('div', attrs={'class': 'article_con'}).find_all('p')
        for e in range(len(news_content)):
            news.append(news_content[e].get_text())
        news_content = '\n'.join(news)
        # print news_content

        # 将我们导入的item文件进行实例化，用来存储我们的数据。
        item['id'] = '宋腾腾'
        print item['id']
        item['website_name'] = item['website_name']
        print item['website_name']
        item['website_block'] = item['big_name']
        print item['website_block']
        item['news_url'] = item['news_url']
        print item['news_url']
        item['news_author'] = news_author
        print item['news_author']
        item['publish_time'] = publish_time
        print item['publish_time']
        item['crawl_time'] = crawl_time
        print item['crawl_time']
        item['news_tags'] = news_tags
        print item['news_tags']
        item['news_title'] = news_title
        print item['news_title']
        item['news_content'] = news_content
        print item['news_content']

        yield item  # yield 是用来提交提取到数据或者提交一个请求
