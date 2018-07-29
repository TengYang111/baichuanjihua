# -*- coding: utf-8 -*-
# !/usr/bin/python
import scrapy
import time
import os
import jieba
import codecs
from bs4 import BeautifulSoup
from scrapy.http import Request
from baichuan3.items import Baichuan3Item
from gensim import corpora
from gensim import models
from collections import defaultdict


base =r"C:\Users\ME\Desktop\Python project\pachong\scrapy\baichuan3/"

class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['//stock.stcn.com/']
    bash_url = 'http://stock.stcn.com/'

    def start_requests(self):
        # 构造不同板块的url
        base = ['xingu/', 'zhuli/', 'bankuai/','dapan/']  # 调试时候记得改数字，加快调试效率
        big_shuzu = []
        for i in range(4):
            url = self.bash_url + base[i] + 'index.shtml'
            # print url
            yield Request(url, self.parse, meta={'big_shuzu': big_shuzu,'url':url})  # 调用parse函数

    def parse(self, response):
        big_shuzu = response.meta['big_shuzu']
        items = []  # 创建一个空列表，用来存储匹配到的数据
        website_name = response.css('.weizhi span a::text').extract_first()  # 大板块的名字
        # print website_name
        big_name = response.css('.a_title span::text').extract_first()  # 小版块的名字
        # print big_name
        first_url = response.meta['url'][:-11]  # 小版块的url
        # print first_url
        file_name = base + website_name
        # 创建主目录
        if (not os.path.exists(file_name)):
            os.makedirs(file_name)
        second_file_name = file_name + '/' + big_name  # 创建副目录
        if (not os.path.exists(second_file_name)):
            os.makedirs(second_file_name)
        urls = []
        for a in range(1, 21):  # 调试时候记得改数字，加快调试效率
            url = first_url + str(a) + '.shtml'
            urls.append(url)
        #print urls
        item = Baichuan3Item()  # 实例化一个对象
        item['website_name'] = website_name
        item['first_url'] = urls
        item['big_name'] = big_name
        item['path'] = second_file_name
        items.append(item)
        # print items
        for item in items:
            for b in range(20):  # 调试时候记得改数字，加快调试效率
                # print item['first_url'][b]
                yield Request(item['first_url'][b], callback=self.parse_two, meta={'item_1': item,'big_shuzu1':big_shuzu}, dont_filter=True)

    def parse_two(self, response):
        # 获得所有新闻的url
        items = []
        big_shuzu = response.meta['big_shuzu1']
        item_1 = response.meta['item_1']
        # print item_1
        news_urls = response.css('.tit a::attr(href)').extract()
        #print news_urls
        for c in range(len(news_urls)):
            news_url = news_urls[c]
            if True:
                item = Baichuan3Item()
                item['website_name'] = item_1['website_name']
                item['first_url'] = item_1['first_url']
                item['big_name'] = item_1['big_name']
                item['path'] = item_1['path']
                item['news_url'] = news_url
                items.append(item)
        # print items
        for item in items:
            #print item
            yield Request(item['news_url'], callback=self.parse_detail, meta={'item_2': item,'big_shuzu1':big_shuzu}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item_2']
        items = []
        # print item_2
        bs = BeautifulSoup(response.text, 'lxml')
        big_shuzu1 = response.meta['big_shuzu1']
        # 新闻链接
        news_url = item['news_url']
        # print news_url

        code_div = bs.find('div',attrs={'class':'intal_tit'})
        # 新闻标题
        news_title = code_div.find('h2').get_text()
        # print news_title

        # 新闻作者
        news_author = code_div.find('div',attrs={'class':'info'}).get_text()[21:]
        # print news_author

        # 新闻发布时间
        publish_time = code_div.find('div',attrs={'class':'info'}).get_text()[0:16]
        # print publish_time

        # 新闻抓取时间
        date = str(time.strftime("%Y-%m-%d"))
        currentTime = str(time.strftime("%H:%M:%S"))
        crawl_time = date + ' ' + currentTime
        # print crawl_time

        # # 新闻自带标签
        # tags = []
        # news_tags = bs.find('div', attrs={'class': 'article_con'}).find_all('a')
        # for d in range(len(news_tags)):
        #     tags.append(news_tags[d].get_text())
        # # print tags
        # news_tags = ','.join(tags)
        # # print news_tags

        # 新闻正文
        news = []
        news_content = bs.find('div',attrs={'class':'txt_con'}).find_all('p')
        for e in range(len(news_content)):
            news.append(news_content[e].get_text())
        news_content = '\n'.join(news)
        # print news_content

        # 将我们导入的item文件进行实例化，用来存储我们的数据。
        item['name_id'] = '宋腾腾'
        # print item['name_id']
        item['website_name'] = item['website_name']
        # print item['website_name']
        item['website_block'] = item['big_name']
        # print item['website_block']
        item['news_url'] = item['news_url']
        # print item['news_url']
        item['news_author'] = news_author
        # print item['news_author']
        item['publish_time'] = publish_time
        # print item['publish_time']
        item['crawl_time'] = crawl_time
        # print item['crawl_time']
        # item['news_tags'] = news_tags
        # print item['news_tags']
        item['news_title'] = news_title
        # print item['news_title']
        item['news_content'] = news_content
        # print item['news_content']
        items.append(item['news_title'])
        items.append(item['news_content'])
        items.append(item['news_url'])
        #print items
        #print items[2]
        # yield item  # yield 是用来提交提取到数据或者提交一个请求
        yield Request(items[2],callback=self.natural_language_processing,meta={'title':items[0],'content':items[1],'big_shuzu':big_shuzu1},dont_filter=True)

    def natural_language_processing(self, response):
        # 对所抓取的预料进行自然语言处理
        title = response.meta['title']
        # print title
        content = response.meta['content']
        # print content
        big_shuzu = response.meta['big_shuzu']
        raw_documents = []
        raw_documents.append(title)
        raw_documents.append(content)
        # print raw_documents
        #print raw_documents[0]
        #print raw_documents[1]
        corpora_documents = []
        # 分词处理
        for item_text in raw_documents:
            item_seg = list(jieba.cut(item_text))
            # print item_seg

            '''''建立停用词'''
            # stopwords = {}.fromkeys(['。', '：', '，',' ','《','》','、',' ','（','）','“','”','；','\n'])
            buff = []
            with codecs.open(r'C:\Users\ME\Desktop\Python project\stop.txt') as fp:
                for ln in fp:
                    el = ln[:-2]
                    buff.append(el)
            stopwords = buff
            for word in item_seg:
                if word not in stopwords and len(word) > 1:
                    #print word
                    corpora_documents.append(word)
        big_shuzu.append(corpora_documents)
        # print corpora_documents
        dictionary = corpora.Dictionary([corpora_documents])
        # print(dictionary)
        # print 'dfs:', dictionary.dfs  # 字典词频，{单词id，在多少文档中出现}
        print 'num_docs:', dictionary.num_docs  # 文档数目
        print 'num_pos:', dictionary.num_pos  # 所有词的个数
        # word_id_dict = dictionary.token2id  # {词:id}
        # print 'word_id_dict:'
        # print len(word_id_dict)
        # for k in word_id_dict.keys():
        # kuozhan(corpora_documents)

        # print big_shuzu
        dictionary.add_documents(big_shuzu)  # 词典扩展
        print 'num_docs:', dictionary.num_docs  # 文档数目
        print 'num_pos:', dictionary.num_pos  # 所有词的个数
        # dict.add_documents(dictionary)
        dictionary.save('ths_dict.dict')  # 保存生成的词典
        dictionary = corpora.Dictionary.load('ths_dict.dict')  # 加载
        # 通过下面一句得到语料中每一篇文档对应的稀疏向量（这里是bow向量）
        corpus = [dictionary.doc2bow(text) for text in [corpora_documents]]
        # 向量的每一个元素代表了一个word在这篇文档中出现的次数
        # print(corpus)
        corpora.MmCorpus.serialize('ths_corpuse.mm', corpus)  # 保存生成的语料
        corpus = corpora.MmCorpus('ths_corpuse.mm')  # 加载

        # corpus是一个返回bow向量的迭代器。下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
        tfidf_model = models.TfidfModel(corpus)
        corpus_tfidf = tfidf_model[corpus]

        # 查看model中的内容
        for item in corpus_tfidf:
            print(item)
        corpus_tfidf.save("ths_tfidf.model")
        corpus_tfidf = models.TfidfModel.load("ths_tfidf.model")
        #print(tfidf_model.dfs)