---
layout: post
category : technology
tags : [datascience,bigdata,architect]
title: Big Data Research1 - Develop Design
---

## 大数据研究2之数据分析处理
------------------------------------------------------------

### Hadoop MapReduce

### Spark for Big Data Development

[Spark大数据计算引擎](https://github.com/terrytang0905/TT_Tech_Space/blob/resource/blogs/2017-03-29-spark-bigdata-arch-note.md)

Spark作为Lambda Architecture一体化解决方案:

- Batch Layer,HDFS+Spark Core,实时增量数据加载到HDFS中,使用SparkCore批量处理全量数据
- Speed Layer,SparkStreaming处理实时的增量数据,以较低的时延生成实时数据
- Serving Layer,HDFS+SparkSQL/Impala,存储Batch Layer和Speed Layer整合完的数据视图,提供低时延的即席查询功能

### Flink Streaming Solution




### BigData Principles and BestPractices of Scalable RealtimeDataSystems






### X.Ref


[Hadoop2.6.0](http://hadoop.apache.org/docs/r2.6.0/)