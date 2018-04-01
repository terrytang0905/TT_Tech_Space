---
layout: post
category : thinking
tags : [thinking,product,datascience]
title: DataProduct Architect Design Note
---

### I.产品设计维度

1.数据清洗-识别数据规则&异常数据

基于已标记范例的学习:有监督的学习

2.数据处理-数据分类与详细信息

3.数据仓库-有效分类行为数据开发
数据银行

4.数据分析

- 分类数据排名分析
- 流量数据分析
- 历史数据趋势分析

	1.识别数据规则
	2.数据分类与详细信息
	3.有效分类行为数据采集
	4.分类数据排名
	5.流量数据分析
	历史数据趋势分析
	6.基于分类数据的行为预测分析
	用户行为分析 / 人群画像分析

5.数据挖掘&人工智能

- 基于分类数据的行为预测分析
- [用户行为分析](2017-05-30-postgresql-best-practice-note.md)
- 人群画像分析

	1.路由用户画像数据
	2.Looklike 全流量用户视频数据
	3.放大 全流量用户IMEI/MAC

- [大数据分析思路](2015-11-08-bigdata-analysis-thinking.md)

### II.架构设计维度

- [大数据研究之架构组成](2017-07-27-bigdata-research-architect-build.md)

1.数据采集-爬虫&Scrapy

2.实时数据处理-SparkStreaming/Storm

3.海量源数据存储-CDH&HDFS

- [大数据存储架构](2017-01-22-bigdata-database-architect-research-note.md)

4.大数据处理

- 基础数据分析技术 -Hive/Spark&SparkSQL/Impala/Presto
- [大数据研究1-大数据SQL](2017-07-28-bigdata-research1-sql-design.md)
- [大数据研究2-数据分析处理](2017-07-28-bigdata-research2-bigdata-development.md)
- [ElaticSearch搜索架构](2017-01-06-elasticsearch-search-engine-architect-note.md)
- ETL数据处理 -Kettle
- 数据同步 -Sqoop/DataX/gphdfs
- 数据质量分析

5.深度数据分析-Greenplum/Python/Tensorflow

- [Greenplum最佳实践](2017-05-28-greenplum-best-practice-note.md)
- [机器学习&Python数据挖掘](2017-10-16-ml-python-data-analysis-note.md)

6.系统数据存储-PostgreSQL

- [PostgreSQL最佳实践](2017-05-30-postgresql-best-practice-note.md)

7.产品应用架构-J2EE&微服务/PHP

8.数据BI&可视化-永洪BI/E-Charts/D3.js

9.产品性能优化

	数据结构/ETL/缓存/业务架构/数据更新

10.常规问题-数据产品

	数据验证/数据完整性/数据冲突/样本异常/性能问题


### III.产品价值维度

1.内容榜单分析+内容分类

2.内容流量分析

3.人群筛选+对应内容榜单

4.搜索-推荐-广告

5.[计算广告](2017-05-30-postgresql-best-practice-note.md)

