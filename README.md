# baichuanjihua
参加训练营以来做过的项目代码
# baichuanjihua
参加训练营以来做过的项目代码
合规门户系统需要抓取的信息说明
优先抓取 一、二、三，网址仅供参考
一、股票名称及代码
背景：合规门户中很多地方需要用户填写股票名称或股票代码，因此需要
	  各个股票市场的证券名称和证券代码，包括 A/B/H股/港股
字段：证券名称、证券代码，市场类型（ A/B/H股/港股）
抓取频率：更新频次估计较低，每天早上8点抓取一次即可
参考 ： http://quote.eastmoney.com/stocklist.html
二、公告
	背景：需要上市公司的公告信息
	需要的主要字段：证券代码、证券名称或简称、
公告标题、公告内容的网址/公告内容(非必须)
	抓取频率：为及时得到最新公告，10分钟抓取一次

抓取A股/港股公告
A股：http://www.cninfo.com.cn/cninfo-new/index
新三板：http://www.neeq.com.cn/disclosure/announcement.html
港股：
http://www.hkexnews.hk/listedco/listconews/mainindex/SEHK_LISTEDCO_DATETIME_TODAY_C.HTM
三、停复牌信息
	需求：深沪停复牌
主要字段 ： 证券代码、证券名称或简称、停牌时间、复牌时间、停牌期限（非必须）、停牌原因（非必须）
	表中的数据增量更新，即复牌停牌肯定是在原有的停牌信息上更新，主要使用表中当前停牌的信息
抓取频率：每天早上8点半，13点
参考 ：http://three.cninfo.com.cn/new/commonUrl?url=disclosure/stopResumeTrading

四其它
监管信息
主要字段：来源（如证监会）、类型（如：证监会要闻/行政处罚）、标题、时间、文章地址、内容（非必须，正文）
抓取频率：每日9点、12点、4点


同花顺行业新闻抓取
1、获取同花顺行业代码industry_code
进入同花顺行业频道：http://q.10jqka.com.cn/thshy/

同花顺行业共有60多个类别，每个行业类别都有对应的行业代码，如半导体及元件的行业代码为881121

在http://q.10jqka.com.cn/thshy/页面可抓取到所有行业代码industry_code。

2、抓取同花顺各个行业新闻列表
进入同花顺各个行业的新闻列表页，如半导体行业新闻：
http://news.10jqka.com.cn/list/field/881121/index_1.shtml
注意：在网页上点击下一页链接会出错，请更改上述链接的页码访问，如第二页：http://news.10jqka.com.cn/list/field/881121/index_2.shtml

   在列表页中，抓取每篇新闻的链接：
 





3、遍历每篇新闻的链接，抓取新闻的标题和正文


4、将抓取的新闻保存到文章保存到本地硬盘
保存格式：（1）每个行业为一个文件夹，文件夹名称为行业名；（2）文章保存成TXT格式，文件名为文章标题，文章正文保存至TXT文件中。

代码示例：
创建文件夹：
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

# 在F盘创建文件夹
os.mkdir(u"F:\\半导体及元件")

创建并写文件：
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# 打开一个文件
fo = open(u"F:\\半导体及元件\\消费电子产业迭代迅猛.txt", "w")  
fo.write( "过去的五年，是全球消费电子技术大踏步发展、产品快……")
 
# 关闭打开的文件
fo.close()
open中的第二个参数“w”表示打开一个文件只用于写入，如果该文件已存在则将其覆盖，如果该文件不存在，创建新文件。
Write函数的参数为string，将string写入文件中。



作业：爬取10个行业，每个行业爬取3页新闻，按上述格式要求保存新闻。

Team1

1、
53	宏观经济	finance.cnr.cn/	央广网产经


2、
159	基础设施	info.jctrans.com/	锦程物流网



3、
97	通信&IT	finance.jrj.com.cn/	金融界财经



4、
163	养老产业	insurance.cngold.org/	金投网保险

5、
177	金融服务	finance.stcn.com/qihuo/index.shtml	证券时报网股市-期货
177	金融服务	finance.stcn.com/xintuo/index.shtml	证券时报网股市-信托
177	金融服务	finance.stcn.com/baoxian/index.shtml	证券时报网股市-保险
177	金融服务	finance.stcn.com/yxlc/index.shtml	证券时报网股市-银行
177	金融服务	finance.stcn.com/quanshang/index.shtml	证券时报网股市-券商
177	金融服务	company.stcn.com/cjnews/index.shtml	证券时报网股市-产经新闻
177	金融服务	company.stcn.com/gsxw/index.shtml	证券时报网股市-公司新闻
177	金融服务	stock.stcn.com/xingu/index.shtml	证券时报网股市-新股
177	金融服务	kuaixun.stcn.com/list/kxyb.shtml	证券时报网股市-研报
177	金融服务	stock.stcn.com/zhuli/index.shtml	证券时报网股市-主力动向
177	金融服务	stock.stcn.com/bankuai/index.shtml	证券时报网股市-板块
177	金融服务	stock.stcn.com/dapan/index.shtml	证券时报网股市-大盘


