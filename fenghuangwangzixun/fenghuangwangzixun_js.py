from scrapy import Request
from newspaper import Article
from em_report.spiders.base.baseSpider import baseSpider

class InformationFhSpider(baseSpider):
    name = 'junshi'
    allowed_domains = ['news.ifeng.com']
    bash_url = 'http://news.ifeng.com/listpage/16874/'
    last1_url = '/1/list.shtml'

    def start_requests(self):
        # 军事板块按照页码翻页
        for k in range(1,11):#可以调节数字
            website_url = self.bash_url + str(k) +self.last1_url
            yield Request(website_url, self.parse_news,dont_filter=True)

    def parse_news(self,response):#这个函数做的是获取新闻的url
        news_urls = response.xpath('//div[@class="box_list clearfix"]/h2/a/@href').extract()
        for news_url in news_urls:
            if news_url != None:
                yield Request(news_url,self.parse_content,meta = {'url':news_url}, dont_filter=True)

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
        publish_time = response.xpath('//*[@id="artical_sth"]/p/span[1]/text()|//div[@class="yc_tit"]/p/span/text()').extract_first()
        if publish_time != None:
            publish_time = publish_time.lstrip().rstrip()
            year = publish_time[:4]
            month = publish_time[5:7]
            day = publish_time[8:10]
            publish_time = year + month + day + ' ' + publish_time[-8:]
            news_author = response.xpath(
                '//*[@id="artical_sth"]/p/span[3]/span/a/text()|//span[@class="ss03"]/text()|//div[@class="yc_tit"]/p/a/text()').extract_first()
            if news_author != None:
                news_author = news_author.lstrip().rstrip()
            else:
                news_author = ''
            # 获取图片的url和名称
            image_urls = []
            image_names = []
            image_urls1 = response.xpath('//p[@class="detailPic"]/img/@src').extract()
            for i in range(len(image_urls1)):
                if image_urls1[i] != None:
                    image_url = image_urls1[i]
                    image_urls.append(image_url)
                    if i < 10 and i >= 0:
                        image_name = news_title + '_000' + str(i)
                        image_names.append(image_name)
                    elif i < 100 and i >= 10:
                        image_name = news_title + '_00' + str(i)
                        image_names.append(image_name)
                    elif i < 1000 and i >= 100:
                        image_name = news_title + '_0' + str(i)
                        image_names.append(image_name)
                    else:
                        image_name = news_title + str(i)
                        image_names.append(image_name)
        else:
            publish_time = response.xpath('//div[@class = "titL"]/p/span/text()').extract_first()
            year = publish_time[:4]
            month = publish_time[5:7]
            day = publish_time[8:10]
            publish_time = year + month + day + ' ' + publish_time[-5:] + ':00'
            news_author = ''
            # 获取图片的url和名称
            image_urls = []
            image_names = []
            image_urls1 = response.xpath('//div[@class="picWin swiper-container"]/img/@src').extract()
            for i in range(len(image_urls1)):
                if image_urls1[i] != None:
                    image_url = 'http:'+image_urls1[i]
                    image_urls.append(image_url)
                    if i < 10 and i >= 0:
                        image_name = news_title + '_000' + str(i)
                        image_names.append(image_name)
                    elif i < 100 and i >= 10:
                        image_name = news_title + '_00' + str(i)
                        image_names.append(image_name)
                    elif i < 1000 and i >= 100:
                        image_name = news_title + '_0' + str(i)
                        image_names.append(image_name)
                    else:
                        image_name = news_title + str(i)
                        image_names.append(image_name)

        yield self.getItem(id = ID,
                           news_url = news_url,
                           website_name = '凤凰网',
                           website_block = '军事',
                           news_title = news_title,
                           publish_time = publish_time,
                           news_author = news_author,
                           news_content = news_content,
                           image_names = image_names,
                           image_urls = image_urls
                           )
