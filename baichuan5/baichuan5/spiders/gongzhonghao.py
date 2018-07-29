# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json
import urllib
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from baichuan5.items import Baichuan5Item

class GongzhonghaoSpider(scrapy.Spider):
    name = "gongzhonghao"
    allowed_domains = ["mp.weixin.qq.com/"]
    start_urls = ['https://mp.weixin.qq.com/s?timestamp=1532500653&src=3&ver=1&signature=jXI*5FjzwIjiE70CEs7r-AXBK62ZbJbOXW1xEbtck6oIOW3PYoE7bj*JX9DeKQLykE5tXTK4YMmvrK8*RLnOZ5zUKdcP39YhX807nSdU3rTY4U2BOsABEae*cDfvridrXuaPAeAj8sjBY3DgM7sl8QNrDYpoZ8B9WcqEJew773w=']

    def parse(self, response):

        # # 版块
        # website_block = response.xpath('//*[@id="js_name"]/text()').extract_first().lstrip().rstrip()
        # # print(website_block)

        # 作者
        news_author = response.xpath('//*[@id="meta_content"]/span[2]/text()').extract_first()
        if news_author == None:
            pass
        else:
            print(news_author.lstrip())

        # # 发布时间
        # browser = webdriver.Chrome()
        # browser.get(self.start_urls[0])  # 这个就是chrome浏览器中的element的内容了
        # publish_time = browser.find_element_by_id('publish_time')
        # print(publish_time.text)
        # browser.close()
        hour = random.randint(0, 24)
        if hour < 10 and hour >= 0:
	        hour = '0' + str(hour)
        else:
	        hour = str(hour)
        # print(a)
        minute = random.randint(1, 60)
        if minute < 10 and minute >= 0:
	        minute = '0' + str(minute)
        else:
	        minute = str(minute)
        sec = random.randint(1, 60)
        if sec < 10 and sec >= 0:
	        sec = '0' + str(sec)
        else:
	        sec = str(sec)
        html = urllib.request.urlopen(self.start_urls[0] )  # 取网页源代码url
        page = html.read()
        p_time = re.search('var publish_time = "(.*?)"', str(page))
        publish_time = re.findall(r"\d{4}-\d{1,2}-\d{1,2}", str(p_time))[0]
        year = publish_time[:4]
        month = publish_time[5:7]
        day = publish_time[8:10]
        publish_time = year + month + day + ' ' + hour + ':' + minute + ':' + sec
        print(publish_time)
        # for p in publish_time:
        #     print(p)

        # 爬取时间
        date = str(time.strftime("%Y-%m-%d"))
        currentTime = str(time.strftime("%H:%M:%S"))
        crawl_time = date + ' ' + currentTime
        # print(crawl_time)

        # 新闻标题
        news_title = response.css('h2::text').extract_first().lstrip().rstrip()
        # print(news_title)

        # 正文  需要做一个判断，p标签是否含有span标签
        news_contents = response.xpath('//*[@id="js_content"]/p/text()| //*[@id="js_content"]//span/text()|//*[@id="js_content"]//strong/text()').extract()
        # print(news_contents)
        # if news_contents == []:
        #     print('文章只有图片，没有正文')
        #
        # else:
        for news_content in news_contents:
            print(news_content)
        #     pass

        # 数据源链接
        request_url =  response.css('.rich_media_tool a::attr(href)').extract_first()
        if request_url ==None:
            print('没有源链接')
        else:
            request_url = self.start_urls[0]  + request_url
            pass

        # 图片名称
        img_titles = response.xpath('//*[@id="js_content"]/p/span[@style = "color: rgb(136, 136, 136);"]/text()').extract()
        # print(len(img_titles))
        # print(img_titles)
        img_urls = response.css('img::attr(data-src)').extract()
        # print(img_urls)
        for a in range(len(img_urls)):
	        if len(img_titles) != 0:
		        if a >= 0 and a <= len(img_titles) - 1:
			        # 'item' + str(i) = {}
			        item = {}
			        if a < 10 and a >= 0:
				        item['图片标题000' + str(a)] = img_titles[a]
			        elif a < 100 and a >= 10:
				        item['图片标题00' + str(a)] = img_titles[a]
			        elif a < 1000 and a >= 100:
				        item['图片标题0' + str(a)] = img_titles[a]
			        else:
				        item['图片标题' + str(a)] = img_titles[a]
			        print(item)
		        else:
			        for b in range(len(img_titles), len(img_urls)):
				        item = {}
				        if b < 10 and b >= 0:
					        item['图片标题000' + str(b)] = news_title + ' ' + img_urls[b]
				        elif b < 100 and b >= 10:
					        item['图片标题00' + str(b)] = news_title + ' ' + img_urls[b]
				        elif b < 1000 and b >= 100:
					        item['图片标题0' + str(b)] = news_title + ' ' + img_urls[b]
				        else:
					        item['图片标题' + str(b)] = news_title + ' ' + img_urls[b]
				        print(item)
	        else:
		        item = {}
		        if a < 10 and a >= 0:
			        item['图片标题000' + str(a)] = news_title + ' ' + img_urls[a]
		        elif a < 100 and a >= 10:
			        item['图片标题00' + str(a)] = news_title + ' ' + img_urls[a]
		        elif a < 1000 and a >= 100:
			        item['图片标题0' + str(a)] = news_title + ' ' + img_urls[a]
		        else:
			        item['图片标题' + str(a)] = news_title + ' ' + img_urls[a]
		        print(item)



        item1 = {}
        # item2 = {}
        # 将我们导入的item文件进行实例化，用来存储我们的数据。
        item1['id'] = '爬虫小分队'
        # print(item1['id'])
        # item1['website_name'] = website_block
        # print(item1['website_name'])
        # item1['website_block'] = website_block
        # print(item1['website_block'])
        item1['news_url'] = self.start_urls[0]
        # print(item1['news_url'])
        item1['news_author'] = news_author
        # print(item['news_author'])
        item1['publish_time'] = publish_time
        # print(item['publish_time'])
        item1['crawl_time'] = crawl_time
        # print(item['crawl_time'])
        # item['news_tags'] = news_tags
        # print(item['news_tags'])
        item1['news_title'] = news_title
        # print(item['news_title'])
        item1['news_content'] = news_contents
        # print(item['news_content'])
        item1['request_url'] = request_url
        # print(item[request_url])

        # item2['id'] = '爬虫小分队'
        # print(item2['id'])
        # # item2['website_name'] = website_block
        # # print(item2['website_name'])
        # item2['website_block'] = website_block
        # print(item2['website_block'])
        # item2['news_url'] = self.start_urls[0]
        # print(item2['news_url'])
        # item2['news_author'] = news_author
        # print(item2['news_author'])
        # item2['publish_time'] = publish_time
        # print(item2['publish_time'])
        # item2['crawl_time'] = crawl_time
        # print(item2['crawl_time'])
        # item2['news_title'] = news_title
        # print(item2['news_title'])
        # # item2['news_content'] = news_contents
        # # print(item2['news_content'])
        # item2['img_urls'] = img_urls
        # print(item2['img_urls'])

        #
        # items = {}
        # for img_url in img_urls:
        #     items['img_url'] = img_url
        #     print(items['img_url'])
        #     yield items


        yield item1