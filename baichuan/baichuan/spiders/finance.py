# -*- coding: utf-8 -*-
# !/usr/bin/python
import scrapy
import time
import os
import random
from bs4 import BeautifulSoup
from scrapy.http import Request
from baichuan.items import BaichuanItem
from selenium import webdriver
import sys

reload(sys)
sys.setdefaultencoding("utf-8")#转换编码
base ="C:\Users\ME\Desktop\Python project\pachong\scrapy\\baichuan/" #存放文件分类的最基础目录

class FinanceSpider(scrapy.Spider):
    name = 'finance'
    # 添加不同的网站的域名
    allowed_domains = ['www.sohu.com']
    # 起始url为新浪财经的首页,必须是列表格式，如start_urls = [ 'http://www.itcast.cn/', ]
    bash_url =  'http://business.sohu.com/'


    def start_requests(self):
        #构造不同大板块的url，并且使用判断句排除掉经营管理这个版块
        for a in range(994,999):#为了方便调试可以将999设置成996，只检验一个版块
            if a ==995:
                continue#如果是995，就跳出循环，继续下一个循环
            url = self.bash_url +str(a)
            yield Request(url,self.parse)#调用parse函数

    def parse(self,response):
        items = []#创建一个空列表，用来存储匹配到的数据
        post_urls = response.css(".box-cur p a::attr(href)").extract()#小版块的url
        post_names = response.css('.box-cur p a::text').extract()#小版块的名字
        website_name = response.css('.box-cur h4 a::text').extract()#大板块的名字
        for a in range(len(website_name)):
            file_name = base + website_name[a]
            # 创建主目录
            if (not os.path.exists(file_name)):
                os.makedirs(file_name)
            for b in range(len(post_names)):
                item = BaichuanItem()#实例化一个对象
                second_file_name = file_name + '/' + post_names[b]#创建副目录
                if (not os.path.exists(second_file_name)):
                    os.makedirs(second_file_name)
                post_url = 'http:' + post_urls[b]#构造小板块的url
                print post_url #用来验证post_url
                item['website_name'] = website_name[0]
                item['post_url'] = post_url
                item['post_name'] = post_names[b]
                item['path'] = second_file_name
                items.append(item)
        #print items#验证字典元素是否正确
        for item in items:#易错点：输出的url都是一样的
            #print item
            #print item['post_url']
            '''多了一个meta这么一个字典，这是Scrapy中传递额外数据的方法。因我们还有一些其他内容需要在下一个页面中才能获取到。'''
            yield Request(url=item['post_url'], callback=self.parse_news, meta={'item_1': item})

    def parse_news(self,response):
        '''
        错误： Filtered offsite request to 'www.sohu.com': <GET http://www.sohu.com/tag/67280>
        原因：allow domain没有加入www.sohu.com
        '''
        # 在小版块中获得新闻链接
        item_1 = response.meta['item_1']#获得上一个函数的字典


        items = []#定义一个新字典，用来存放数据
        # print item_1
        news_urls = response.css('h4 a::attr(href)').extract()#所有的新闻url
        browser = webdriver.Chrome()#定义一个具体browser对象
        browser.get(item_1['post_url'])
        for i in range(1, 10):#时间可以调节多一点啊
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            for d in range(len(news_urls)):
                news_url = 'http:' + news_urls[d]
                #print news_url
                if True:
                    item = BaichuanItem()
                    item['website_name'] = item_1['website_name']
                    item['post_url'] = item_1['post_url']
                    item['post_name'] = item_1['post_name']
                    item['path'] = item_1['path']
                    item['news_url'] = news_url
                    items.append(item)
            #print items
            for item in items:
                yield Request(url=item['news_url'], meta={'item_2': item}, callback=self.parse_detail)


    def parse_detail(self,response):
        #具体页面信息的抓取
        item = response.meta['item_2']
        #print item
        bs = BeautifulSoup(response.text, 'lxml')
        # print bs
        # print response.meta['url']
        # print response.meta[website_block]
        #获取作者
        news_author = bs.find('h4')
        if news_author ==None:#没有作者设置为'None'
            news_author = 'None'
        else:
            news_author = news_author.find('a').get_text()
        # print news_author

        #获取发布时间
        publish_time = bs.find('span',attrs={'class':'time'})
        if publish_time ==None:
            publish_time='None'
        else:
            publish_time=publish_time.get_text()
            second = random.randrange(60)
            publish_time = publish_time + ':' + str(second)

        #获取抓捕时间
        date = str(time.strftime("%Y-%m-%d"))
        currentTime = str(time.strftime("%H:%M:%S"))
        crawl_time = date + ' ' + currentTime
        #print crawl_time

        #获取标签
        c_news =[]
        news_tags = bs.find('span',attrs={'class','tag'})
        if news_tags ==None:
            news_tags = 'None'
        else:
            news_tags = news_tags.find_all('a')
            for i in news_tags:
                '''错误：ResultSet' object is not callable'''
                ii = i.get_text()
                c_news.append(ii)
        #print len(news_tags)
        #print type(news_tags)
        #print news_tags
        #print c_news
        news_tag =  ','.join(c_news)
        #print news_tag

        #获取标题
        news_title = bs.find('p',attrs={'data-role':'original-title'})
        if news_title ==None:
            news_title='None'
        else:
            news_title = news_title.get_text()
        #print(news_title)

        #获取正文
        article_contentText=bs.find('article',attrs={'class':'article'})
        if article_contentText ==None:
            article_contentText = 'None'
        else:
            [d.extract() for d in article_contentText('div')]  # 去掉其他多余的部分
            news_content = article_contentText.text.encode('utf-8')
            # print news_content

        # 将我们导入的item文件进行实例化，用来存储我们的数据。
        item['name_id'] = 'song-teng-teng'
        #print item['name_id']
        item['website_name'] = str(item['website_name'])
        item['website_block'] = item['post_name']
        item['news_url'] = item['post_url']
        item['news_author'] = news_author
        #print item['news_author']
        item['publish_time'] = publish_time
        #print item['publish_time']
        item['crawl_time'] = crawl_time
        #print item['crawl_time']
        item['news_tags'] = news_tag
        #print item['news_tags']
        item['news_title'] = news_title
        #print item['news_title']
        item['news_content'] =news_content
        #print item['news_content']
        yield item#yield 是用来提交提取到数据或者提交一个请求

