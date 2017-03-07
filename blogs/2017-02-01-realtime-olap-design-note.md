---
layout: post
category : datascience
tags : [bigdata,search,develop]
title: Big Data RealTime OLAP Design Note
---

大数据实时OLAP设计 Note
------------------------------------------------------------

Big Data Analysis Product = Data Visualization + OLAP(SQLonHadoop(Impala)/Spark) + Big Data Storage(Greenplum/HDFS/Kudu) 

Lambda架构作为最常见的实时数据处理框架,通过离线查询+流式处理方式实现实时数据查询的需求。但是如果是基于大数据实时的OLAP查询该如何实现呢?
多维数据分析的复杂度决定了我们需要寻找Lambda框架的开源OLAP数据分析解决方案。Druid作为有过实际生产场景应用的MOLAP引擎,可深入研究

#### Lambda实时查询架构

Big Data:Principles and best practices of scalable realtime

* a.Kafka+Storm+NoSQL实时处理设计

* b.SparkSQL计算引擎

* c.Impala通用实时OLAP查询

* d.PrestoDB



#### MOLAP设计(From Druid)

MOLAP是多维数据组织的OLAP实现,将细节数据和聚合后的数据均保存在cube中，所以以空间换效率，查询时效率高
Druid-OLAP引擎研究
OLAP与SearchEngine的差异

#### ROLAP设计(From Mondrian)

当前NewBI是基于ROLAP(关系型数据库OLAP抽象),从数据存储角度看非CUBE数据结构存储。因此当我们需要进行深度CUBE分析时,性能较差。
ROLAP优化方式考虑创建索引视图而不创建表,实现逻辑CUBE数据集

#### 大数据OLAP详细设计

- 多维OLAP查询设计(基于抽象逻辑模型的关联查询)
- Aggregation Query聚合查询与非聚合查询
- OLAP数据缓存设计
- 查询语义分析设计(复杂计算设计)

    ANTLR开源语法分析器.[介绍](http://www.ibm.com/developerworks/cn/java/j-lo-antlr/) <br />
    自动构造自定义语言的识别器(recognizer),编译器(parser),和解释器(translator)的框架 <br />
    Lucene中的语义分析比较:JavaCC+jflex

- 影响OLAP性能的因素
- 大数据实时OLAP设计
- 多维查询表达式MDX(Mutil Dimensional Expressions) 

[NewBI OLAP Design](http://wiki.yunat.com/pages/viewpage.action?pageId=47520652)
