---
layout: post
category : bigdata
tags : [datascience,bigdata,architect]
title: Big Data Research Note - Data Process Design
---

## 大数据研究-数据处理计算
-------------------------------------------------------------

### 大数据开发框架

HDFS - 分布式文件系统
MapReduce - 分布式计算框架
Yarn - 分布式集群资源调度框架

框架在架构设计上遵循一个重要的设计原则叫“依赖倒转原则”，IOC依赖倒转原则是高层模块不能依赖低层模块，它们应该共同依赖一个抽象，这个抽象由高层模块定义，由低层模块实现。


### Hadoop MapReduce

![MapReduce](_includes/mapreduce.jpg)

Shuffle过程是指 Mapper 产生的直接输出结果，经过一系列的处理，成为最终的
Reducer 直接输入数据为止的整个过程。这是 mapreduce 的核心过程。该过程可以分为两 个阶段:

	- Mapper端的Shuffle:由 Mapper 产生的结果并不会直接写入到磁盘中，而是先存 储在内存中，当内存中的数据量达到设定的阀值时，一次性写入到本地磁盘中。并同时进行 sort(排序)、combine(合并)、partition(分片)等操作。其中，sort 是把 Mapper 产 生的结果按照 key 值进行排序;combine 是把 key 值相同的记录进行合并;partition 是把数据均衡的分配给 Reducer。
	- Reducer端的Shuffle:由于 Mapper 和 Reducer 往往不在同一个节点上运行，所以Reducer 需要从多个节点上下载 Mapper 的结果数据，并对这些数据进行处理，然后才能 被 Reducer 处理。

1. MapReduce 计算框架中负责计算任务调度的 JobTracker 对应 HDFS 的 NameNode 的角色，只不过一个负责计算任务调度，一个负责存储任务调度。

2. MapReduce 计算框架中负责真正计算任务的 TaskTracker 对应到 HDFS 的 DataNode 的角色，一个负责计算，一个负责管理存储数据。

	Tips:
	考虑到“Data_Local”，一般地，将NameNode和JobTracker部署到同一台机器上， 各个DataNode和TaskNode也同样部署到同一台机器上。

### Spark for Big Data Development

Spark可以作为Kappa架构的一种实现,以解决Lambda Architecture一体化所存在问题:

- [Spark大数据计算引擎](2017-03-29-spark-bigdata-arch-note.md)

### Realtime Streaming Computeing

- [实时流式数据计算](2018-05-31-bigdata-stream-compute-research-note.md)

### ElasticSearch Solution

- [ElasticSearch全文检索](2017-01-06-elasticsearch-search-engine-architect-note.md)



### X.Ref


- [Hadoop2.6.0](http://hadoop.apache.org/docs/r2.6.0/)

