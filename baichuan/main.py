# -*- coding: utf-8 -*-
'''
本文件是用来给pycharm调试的文件，如果没有这个文件，PC无法调试scrapy的一些文件
'''
from scrapy import cmdline
name ='finance'
cmd = 'scrapy crawl {0}{1}'.format(name,'')
cmdline.execute(cmd.split())
# from scrapy.cmdline import execute
# import os
# import sys
# #因为每次要输入副目录很麻烦，通过调用这两个模块，能够快速找到main文件的副目录
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# #print os.path.dirname(os.path.abspath(__file__))
# #添加完命令之后，我们在项目下的Spyder的爬虫文件就可以设置断点进行调试了
# execute(['scrapy','crawl','finance'])