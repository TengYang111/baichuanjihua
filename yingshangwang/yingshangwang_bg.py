from scrapy import Request
import random
from newspaper import Article
from em_report.spiders.base.baseSpider import baseSpider

class winshangspider(baseSpider):
	name = "baoguang"
	allowed_domains = ["winshang.com"]
	start_urls = ['http://news.winshang.com/list-1305.html']

	def parse(self, response):#爬取每个版块的url
		for j in range(1,1000):#测试错误时把数字调小  1000
			website_url = self.start_urls[0][:-5] + '/page-' + str(j) + '.html'
			yield Request(website_url,self.parse_news, dont_filter=True)

	def parse_news(self,response):#构建不同版块的所有页面的url
		news_urls = response.xpath('//div[@class="fzywtt"]/a/@href').extract()
		for news_url in news_urls:
			yield Request(news_url,self.parse_content,meta = {'url':news_url}, dont_filter=True)

	def parse_content(self,response):
		#对每个页面进行解析
		ID = 'songtengteng'

		news_url = response.meta['url']


		news_tag = response.xpath('//div[@class="newskey"]//strong//a/text()').extract()
		news_tags = ','.join(news_tag)

		news_title = response.xpath('//h1/text()').extract_first()

		a = Article(response.meta['url'], language='zh')  # Chinese
		a.download()
		a.parse()
		news_content = a.text


		# 发布时间
		a = random.randint(1, 61)
		if a >= 0 and a < 10:
			a = '0' + str(a)
		else:
			a = str(a)
		publish_time = response.xpath('//div[@class="nly"]/span/text()').extract_first()
		if publish_time != None:
			publish_time = publish_time.lstrip().rstrip()
		else:
			publish_time = response.xpath('/html/body/div[11]/div[2]/div[4]/text()[2]').extract_first()
		year = publish_time[:4]
		month = publish_time[5:7]
		day = publish_time[8:10]
		hour = publish_time[11:13]
		minute = publish_time[14:16]
		publish_time = year + month + day + ' ' + hour + ':' + minute + ':' + a

		news_author = response.xpath('//*[@id="form1"]/div[10]/div[2]/div[1]/span[2]/text()').extract_first()[3:]

		image_urls = []
		image_names = []
		yield self.getItem(id = ID,
		                   news_url = news_url,
		                   website_name = '赢商网',
		                   website_block = '曝光',
		                   news_title = news_title,
		                   publish_time = publish_time,
		                   news_author = news_author,
		                   news_tags = news_tags,
		                   news_content = news_content,
						   image_urls=image_urls,
						   image_names=image_names,
						   )