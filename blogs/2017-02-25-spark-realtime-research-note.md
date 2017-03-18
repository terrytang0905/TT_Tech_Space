---
layout: post
category : datascience
tags : [bigdata,search,develop]
title: Spark Research Note
---

## Spark 实时计算Note
------------------------------------------------------------

Lambda架构作为最常见的实时数据处理框架,通过离线查询+流式处理方式实现实时数据查询的需求。但是如果是基于大数据实时的OLAP查询该如何实现呢?
多维数据分析的复杂度决定了我们需要寻找Lambda框架的开源OLAP数据分析解决方案。Druid作为有过实际生产场景应用的MOLAP引擎,可深入研究

#### Lambda实时查询架构

Big Data:Principles and best practices of scalable realtime

* a.Kafka+Storm+NoSQL实时处理设计

* b.SparkSQL计算引擎


