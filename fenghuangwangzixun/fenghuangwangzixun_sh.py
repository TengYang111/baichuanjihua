from scrapy import Request
import time
from newspaper import Article
from em_report.spiders.base.baseSpider import baseSpider

class InformationFhSpider(baseSpider):
    name = 'shehui'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/listpage/7837/']

    def start_requests(self):
        day = time.strftime("%Y%m%d")[-2:]
        year = time.strftime("%Y%m%d")[0:4]
        month = time.strftime("%Y%m%d")[4:6]
        date = int(day)
        if date > 5:#可以调节大小
            for j in range(date-5,date+1):
                website_url = self.start_urls[0] + year + month + str(j) + '/1/rtlist.shtml'
                yield Request(website_url, self.parse_news)
        else:
            for j in range(0,date+1):
                website_url = self.start_urls[0] + year + month + str(j) + '/1/rtlist.shtml'
                #如果数字想要调大一点，那么月份就要发生变换
                yield Request(website_url, self.parse_news)

    def parse_news(self,response):#这个函数做的是获取新闻的url
        news_urls = response.xpath('//div[@class ="main"]/div[@class = "left"]/div[@class="newsList"]/ul/li/a/@href').extract()
        for i in range(len(news_urls)):
            news_url = news_urls[i]
            yield Request(news_url,self.parse_content,meta = {'url':news_url})

    def parse_content(self,response):
        #这个函数是用来解析新闻页面的
        ID = 'songtengteng'

        news_url = response.meta['url']

        news_title = response.xpath('//h1/text()').extract_first()

        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        # 发布时间
        publish_time = response.xpath('//*[@id="artical_sth"]/p/span[1]/text()|//div[@class="yc_tit"]/p/span/text()').extract_first().lstrip().rstrip()
        year = publish_time[:4]
        month = publish_time[5:7]
        day = publish_time[8:10]
        publish_time = year + month + day + ' ' + publish_time[-8:]

        news_author = response.xpath('//*[@id="artical_sth"]/p/span[3]/span/a/text()|//span[@class="ss03"]/text()|//div[@class="yc_tit"]/p/a/text()').extract_first()

        #获取文章的图片和名称
        image_urls = []
        image_names = []
        image_urls1 = response.xpath('//p[@class="detailPic"]/img/@src').extract()
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
                           website_name = '凤凰网资讯',
                           website_block = '社会',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_content = news_content,
                           image_urls=image_urls,
                           image_names=image_names,
                           )

