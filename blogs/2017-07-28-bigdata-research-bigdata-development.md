---
layout: post
category : technology
tags : [datascience,bigdata,architect]
title: Big Data Research Note - Data Process Design
---

## 大数据研究-数据分析处理
------------------------------------------------------------

### Hadoop MapReduce

### Spark for Big Data Development

Spark作为Lambda Architecture一体化解决方案:

- Batch Layer,HDFS+Spark Core,实时增量数据加载到HDFS中,使用SparkCore批量处理全量数据
- Speed Layer,SparkStreaming处理实时的增量数据,以较低的时延生成实时数据
- Serving Layer,HDFS+SparkSQL/Impala,存储Batch Layer和Speed Layer整合完的数据视图,提供低时延的即席查询功能

- [Spark大数据计算引擎](2017-03-29-spark-bigdata-arch-note.md)

### Flink Streaming Solution

- [Flink流式处理](2018-05-31-flink-research-note.md)


### ElasticSearch Solution

- [ElasticSearch全文检索](2017-01-06-elasticsearch-search-engine-architect-note.md)


### BigData Principles and BestPractices of Scalable RealtimeDataSystems






### X.Ref


[Hadoop2.6.0](http://hadoop.apache.org/docs/r2.6.0/)