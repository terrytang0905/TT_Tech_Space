---
layout: post
category : datascience
tags : [bigdata,search,develop]
title: Big Data RealTime OLAP Design Note
---

大数据实时OLAP设计 Note
--------------------------------------------------


### 大数据OLAP通用设计

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

设计多维查询表达式MDX。通过多维报表设计生成多维查询表达式MDX,在MDX通用结构底层下,转换成SQL解析器,实现多重情况下的复杂数据查询(实时查询+离线查询)。


#### ROLAP设计(From Mondrian)

当前NewBI是基于ROLAP(关系型数据库OLAP抽象),从数据存储角度看非CUBE数据结构存储。因此当我们需要进行深度CUBE分析时,性能较差。
ROLAP优化方式考虑创建索引视图而不创建表,实现逻辑CUBE数据集

#### MOLAP设计(From Druid)

MOLAP是多维数据组织的OLAP实现,将细节数据和聚合后的数据均保存在cube中，所以以空间换效率，查询时效率高
Druid-OLAP引擎研究
OLAP与SearchEngine的差异


