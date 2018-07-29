# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
import codecs
import jieba
from gensim import corpora
from gensim import models
from collections import defaultdict
from gensim import similarities
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
big_shuzu = []
path1 = r"C:\Users\ME\Desktop\Python project\pachong\scrapy\baichuan4\证券时报网".encode('gbk')

for root,dirs,files in os.walk(path1):
	print(root.decode('gbk').encode('utf-8'))#输出根目录
	# print dirs
	# print files
	# for dir in dirs:#输出文件夹的名字
	# 	print(os.path.join(root, dir).decode('gbk').encode('utf-8'))
	for fp in files:
		# print(os.path.join(root, fp))
		if fp == None:
			print ('None')
		else:
			# print(os.path.join(root, fp).decode('gbk').encode('utf-8'))
			path = os.path.join(root, fp)
			with open(path) as f:
				'''
				使用python的时候经常会遇到文本的编码与解码问题，其中很常见的一种解码错误如题目所示，下面介绍该错误的解决方法，将‘gbk’换成‘utf-8’也适用。
				（1）、首先在打开文本的时候，设置其编码格式，如：open(‘1.txt’,encoding=’gbk’)；
				（2）、若（1）不能解决，可能是文本中出现的一些特殊符号超出了gbk的编码范围，可以选择编码范围更广的‘gb18030’，如：open(‘1.txt’,encoding=’gb18030’)；
				（3）、若（2）仍不能解决，说明文中出现了连‘gb18030’也无法编码的字符，可以使用‘ignore’属性进行忽略，如：open(‘1.txt’,encoding=’gb18030’，errors=‘ignore’)；
				（4）、还有一种常见解决方法为open(‘1.txt’).read().decode(‘gb18030’,’ignore’)
							'''
				lines = [line.strip() for line in f.readlines()]
				# print (lines)
				corpora_documents = []
				# 分词处理
				for item_text in lines:
					item_seg = list(jieba.cut(item_text))
					# print item_seg

					'''建立停用词'''
					# stopwords = {}.fromkeys(['。', '：', '，',' ','《','》','、',' ','（','）','“','”','；','\n'])
					buff = []
					with codecs.open(r'C:\Users\ME\Desktop\Python project\stop.txt') as fp:
						for ln in fp:
							el = ln[:-2]
							buff.append(el)
					stopwords = buff
					for word in item_seg:
						if word not in stopwords and len(word) > 1:
							# print word
							corpora_documents.append(word)
				# print corpora_documents
				# 生成字典和向量语料
				dictionary = corpora.Dictionary([corpora_documents])
				# print(dictionary)
				# print 'dfs:', dictionary.dfs  # 字典词频，{单词id，在多少文档中出现}
				# print('num_docs:', dictionary.num_docs)  # 文档数目
				# print('num_pos:', dictionary.num_pos)  # 所有词的个数
				# word_id_dict = dictionary.token2id  # {词:id}
				# print 'word_id_dict:'
				# print len(word_id_dict)
				# for k in word_id_dict.keys():
				# kuozhan(corpora_documents)
				big_shuzu.append(corpora_documents)
				# print big_shuzu
				dictionary.add_documents(big_shuzu)  # 词典扩展
				print('num_docs:', dictionary.num_docs)  # 文档数目
				print('num_pos:', dictionary.num_pos)  # 所有词的个数
				# dict.add_documents(dictionary)
				dictionary.save('ths_dict.dict')  # 保存生成的词典
				dictionary = corpora.Dictionary.load('ths_dict.dict')  # 加载

				# 处理corporate以及model
				# 通过下面一句得到语料中每一篇文档对应的稀疏向量（这里是bow向量）
				corpus = [dictionary.doc2bow(text) for text in big_shuzu]
				# 向量的每一个元素代表了一个word在这篇文档中出现的次数
				# print(corpus)
				corpora.MmCorpus.serialize('ths_corpuse.mm', corpus)  # 将生成的语料保存成MM文件
				corpus = corpora.MmCorpus('ths_corpuse.mm')  # 加载
				# corpus是一个返回bow向量的迭代器。下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
				tfidf_model = models.TfidfModel(corpus)
				corpus_tfidf = tfidf_model[corpus]
				# 使用for循环查看model中的内容
				# for item in corpus_tfidf:
				# 	print(item)
				corpus_tfidf.save("ths_tfidf.model")  # 保存成model格式
				corpus_tfidf = models.TfidfModel.load("ths_tfidf.model")  # 加载
				# print(tfidf_model.dfs)


