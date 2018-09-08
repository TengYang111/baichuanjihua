# -*- coding: utf-8 -*-
import json
import re
from newspaper import Article
from scrapy.http import Request
from em_report.spiders.base.baseSpider import baseSpider


class souhuqiche_qcxwSpider(baseSpider):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'SUV=1804261740089768; gidinf=x099980109ee0ddc4bbacf42500021335b5d2d33198c; beans_mz_userid=RlLBf0VlSR39; IPLOC=CN4401; vjuids=-391bdd7e4.16598205c08.0.dfef638b1c25a; vjlast=1535855582.1535855582.30; t=1535855880866; ipcncode=CN990000; sohu_user_ip=223.74.34.11',
        'Referer': 'http://auto.sohu.com/qichexinwen.shtml',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    name = "souhucar"
    allowed_domains = ["http://auto.sohu.com/qichexinwen.shtml"]
    start_urls = ['http://auto.sohu.com/qichexinwen.shtml']

    def parse(self, response):
        for page in range(1, 3):
            # 此url是在js中找到的，打开之后有我们需要爬取的新闻url的部分信息，修改pagenumber后面的数字相当于加载的页面数，现在爬取的是1和2页，相当于下拉出了两页的新闻
            url = 'http://news.auto.sohu.com/MP/apiV2/profile/newsListAjax?callback=jQuery18306649521815151875_1535893492220&xpt=cWljaGVjaGFndWFuQHNvaHUuY29t&pageNumber=' + str(
                page) + '&pageSize=20&_=1535893505045'
            yield Request(url, dont_filter=True, headers=self.headers, callback=self.parse_get_url)

    def parse_get_url(self, response):
        select = re.compile(r'\w+[(](.*)[)]')  # 由于打开的url不是json的标准格式，所以需要用正则将里面小括号后面的内容全部拿出来
        res = select.findall(response.text)[0]
        block_json = json.loads(res)  # 加载json数据，自己百度json.loads
        # print(block_json['data'])
        content = re.compile(r'\\\"newsid\\\"\:(.*?)[,]')
        ids = content.findall(block_json['data'])
        for id in ids:
            news_url = 'http://www.sohu.com/a/' + str(id) + '_430289'  # 新闻url构造
            yield Request(news_url, dont_filter=True, callback=self.parse_detail,meta={'url':news_url})

    def parse_detail(self, response):
        # 新闻链接
        news_url = response.meta['url']

        # 标题
        title = response.xpath('//div[@class="article-box l"]/h3/text()|//h1/text()').extract()
        if title:
            news_title = ''
            for t in title:
                news_title += t.strip()
        else:
            news_title = ''

        # 发布时间
        publish_time = response.xpath('//span[@class="l time"]/text()').extract_first()
        if publish_time != None:
            year = publish_time[0:4]
            month = publish_time[5:7]
            day = publish_time[8:10]
            juti_time = publish_time[-8:]
            publish_time = year + month + day + ' ' + juti_time
        else:
            publish_time = response.xpath('//span[@class="time"]/text()').extract_first()
            year = publish_time[0:4]
            month = publish_time[5:7]
            day = publish_time[8:10]
            juti_time = publish_time[-5:]
            publish_time = year + month + day + ' ' + juti_time + ':' + '00'

        #标签
        d = response.xpath('//span[@class="r tag"]/a/text()').extract()
        if d != []:
            news_tags = ','.join(d).strip('\r\n')
        else:
            news_tags = ''

        # 正文
        '''可以考虑下使用文章密度算法来快速解析文章正文'''
        a = Article(response.meta['url'], language='zh')  # Chinese
        a.download()
        a.parse()
        news_content = a.text

        # 图片的链接
        image_names = []
        image_urls = response.xpath('//p[@class="ql-align-center"]/img/@data-src|//p[@style="text-align: center;"]/img/@data-src').extract()
        if image_urls == []:
            image_urls = ''
        else:
            image_urls = image_urls
            # 图片的名称
            for i in range(len(image_urls)):
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


        yield self.getItem(id='songtengteng',
                               news_url = news_url,
                               website_name = '搜狐',
                               website_block = '汽车',
                               news_title = news_title,
                               publish_time = publish_time,
                               news_author = '搜狐汽车',
                               news_tags = news_tags,
                               news_content = news_content,
                               image_urls=image_urls,
                               image_names=image_names,
                               )

# def parse_artical(self, response):  # 具体文章解析
    #     ID = 'songtengteng'
    #
    #     # 新闻链接
    #     news_url = response.meta['url']
    #
    #     #新闻标题
    #     news_title = response.xpath('//h3[class="article-title"]/text()').extract_first()
    #     if news_title != None:
    #         news_title = news_title.strip()
    #
    #     # 发布时间
    #     publish_time = response.xpath('//span[@class="l time"]/text()').extract_first()
    #     year = publish_time[0:4]
    #     month = publish_time[5:7]
    #     day = publish_time[8:10]
    #     juti_time = publish_time[-8:]
    #     publish_time = year + month + day + ' ' + juti_time + ':' + '00'
    #
    #     # 正文
    #     '''可以考虑下使用文章密度算法来快速解析文章正文'''
    #     a = Article(response.meta['url'], language='zh')  # Chinese
    #     a.download()
    #     a.parse()
    #     news_content = a.text
    #
    #     #标签
    #     d = response.xpath('//span[@class="r tag"]/a/text()').extract()
    #     if d != []:
    #         news_tags = ','.join(d).strip('\r\n')
    #     else:
    #         news_tags = ''
    #
    #     #图片的链接
    #     image_names = []
    #     image_urls = response.xpath('//p[@class="ql-align-center"]/img/@data-src').extract()
    #     if image_urls == []:
    #         image_urls = ''
    #     else:
    #         image_urls = image_urls
    #         # 图片的名称
    #         for i in range(len(image_urls)):
    #             if i >=0 and i<10:
    #                 image_name = news_title + '_000' + str(i)
    #                 image_names.append(image_name)
    #             elif i>=10 and i <100:
    #                 image_name = news_title + '_00' + str(i)
    #                 image_names.append(image_name)
    #             elif i>=100 and i <1000:
    #                 image_name = news_title + '_0' + str(i)
    #                 image_names.append(image_name)
    #             else:
    #                 image_name = news_title + str(i)
    #                 image_names.append(image_name)
    #
    #     yield self.getItem(id = ID,
    #                        news_url = news_url,
    #                        website_name = '搜狐',
    #                        website_block = '汽车',
    #                        news_title = news_title,
    #                        publish_time = publish_time,
    #                        news_author = '搜狐汽车',
    #                        news_tags = news_tags,
    #                        news_content = news_content,
    #                        image_urls=image_urls,
    #                        image_names=image_names,
    #                        )
    #
    #
