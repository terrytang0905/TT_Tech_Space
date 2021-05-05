---
layout: post
category : bigdata
tags : [datascience,bigdata,architect]
title: Big Data Research Note - DataProcess Design
---

## 大数据研究-数据处理-通用开发
-------------------------------------------------------------

### I.大数据处理框架

* 无边界数据与有边界数据
* TimeDomain(EventTime/ProcessingTime)
* 批处理与流处理

#### Data Workflow

Workflow Design Pattern

![workflow](_includes/data_workflow.png)

**复制模式(Copier Pattern)**

	复制模式通常是将单个数据处理模块中的数据,完整地复制到两个或更多的数据处理模块中,然后再由不同的数据处理模块进行处理。

**过滤模式(Filter Pattern)**

	过滤模式的作用是过滤掉不符合特定条件的数据。

**分离模式(Splitter Pattern)**


**合并模式(Joiner Pattern)**


**发布/订阅模式(Publish/Subscribe Pattern)**

发布/订阅模式指的是消息的发送方可以将消息异步地发送给一个系统中不同组件,而无需知道接收方是谁.

![sub_rev_message_pattern](_includes/sub_rev_message_pattern.png)

_发布/订阅模式样例:_

![sub_rev_data_distrubte](_includes/sub_rev_data_distrubte.png)

_发布/订阅模式的优缺点:_

	- 松耦合(Loose Coupling):消息的发布者和消息的订阅者在开发的时候完全不需要事先知道对方的存在,可以独立地进行开发。
	- 高伸缩性(High Scalability):发布 / 订阅模式中消息队列可以独立的作为一个数据存储中心存在。在分布式环境中,是消息队列,可以扩展至上千个服务器中.
	- 系统组件间通信更加简洁:因为不需要为每一个消息的订阅者准备专门的消息格式,只需要知道消息队列中保存消息格式,发布者就可以按照这个格式发送消息,订阅者也只需按照此格式接收消息。

	Tips:订阅推送方式解决多端数据应用需求

- [Kafka分布式消息队列](2017-01-10-bigdata-research-dataprocess-kafka-note.md)

### II.BatchProcess-Hadoop MapReduce

HDFS - 分布式文件系统
MapReduce - 分布式计算框架
Yarn - 分布式集群资源调度框架

框架在架构设计上遵循一个重要的设计原则叫“依赖倒转原则”，IOC依赖倒转原则是高层模块不能依赖低层模块，它们应该共同依赖一个抽象，这个抽象由高层模块定义，由低层模块实现。

![MapReduce](_includes/mapreduce.jpg)

Shuffle过程是指 Mapper 产生的直接输出结果，经过一系列的处理，成为最终的
Reducer 直接输入数据为止的整个过程。这是 mapreduce 的核心过程。该过程可以分为两 个阶段:

	- Mapper端的Shuffle:由 Mapper 产生的结果并不会直接写入到磁盘中，而是先存 储在内存中，当内存中的数据量达到设定的阀值时，一次性写入到本地磁盘中。并同时进行 sort(排序)、combine(合并)、partition(分片)等操作。其中，sort 是把 Mapper 产 生的结果按照 key 值进行排序;combine 是把 key 值相同的记录进行合并;partition 是把数据均衡的分配给 Reducer。
	- Reducer端的Shuffle:由于 Mapper 和 Reducer 往往不在同一个节点上运行，所以Reducer 需要从多个节点上下载 Mapper 的结果数据，并对这些数据进行处理，然后才能 被 Reducer 处理。

1. MapReduce 计算框架中负责计算任务调度的 JobTracker 对应 HDFS 的 NameNode 的角色，只不过一个负责计算任务调度，一个负责存储任务调度。

2. MapReduce 计算框架中负责真正计算任务的 TaskTracker 对应到 HDFS 的 DataNode 的角色，一个负责计算，一个负责管理存储数据。

		Tips:考虑到“Data_Local”，一般地，将NameNode和JobTracker部署到同一台机器上， 各个DataNode和TaskNode也同样部署到同一台机器上。

### III.BatchProcess-Spark

Spark可以作为Kappa架构的一种实现,以解决Lambda Architecture一体化所存在问题:

- [Spark大数据计算引擎](2017-03-29-spark-bigdata-arch-note.md)

- [Spark性能优化](2018-11-23-spark-performance-tuning-note.md)

### IV.Streaming Compute 

- [实时计算数据框架](2017-07-29-bigdata-research-dataprocess-realtime-framework.md)

- [流式数据处理技术](2018-05-31-bigdata-research-dataprocess-stream-compute.md)

### V.BatchProcess-ETL

### VI.Next Generation DataProcess

- [ElaticSearch搜索架构](2017-01-06-elasticsearch-search-engine-architect-note.md)
- ClickHouse



### X.Ref


- [Hadoop2.6.0](http://hadoop.apache.org/docs/r2.6.0/)

