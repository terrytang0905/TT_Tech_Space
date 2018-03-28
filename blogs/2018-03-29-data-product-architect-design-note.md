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
- 用户行为分析
	定向人群与行为交叉筛选
- 人群画像分析


### II.架构设计维度

1.数据采集-爬虫&Scrapy
2.实时数据处理-SparkStreaming/Storm
3.海量源数据存储-CDH&HDFS
4.基础数据分析-Hive/Spark&SparkSQL/Impala/Presto
5.数据ETL-Kettle
数据同步-Sqoop/DataX/gphdfs
6.深度数据分析-Greenplum/Python/Tensorflow
深度学习与人工智能
7.系统数据存储-PostgreSQL
8.产品应用架构-J2EE&微服务/PHP
9.数据BI&可视化-永洪BI/E-Charts/D3.js
10.产品性能优化
数据结构/ETL/缓存/业务架构/数据更新
11.常规问题-数据产品
数据验证/数据完整性/数据冲突/样本异常/性能问题

[大数据研究之架构技术](2017-07-27-bigdata-research-architect-menu.md)

### III.产品价值维度

1.内容榜单+内容分类
2.内容流量分析
3.人群筛选+对应内容榜单