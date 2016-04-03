---
layout: post
category : datascience
tags : [nosql,bigdata]
title: MongoDB Internal
---
{% include JB/setup %}

## MongoDB NoSQL商业化的开端

### MongoDB 背景

基于内容的数据存储方式
留言/日记/多媒体数据

### CAP & BASE 理论

没有Transaction的MongoDB
Two-phase commit(2PC)

### MongoDB 架构特点

1.data model from relational to document-based
capped collection
文档大小限制16M
2.embedded docs for speed
3.agile development with dynamic schemas
4.easier horizontal scalability because joins aren’t as important

Storage Engine (内存杀手的原因)
1.MMAP
它会把数据文件映射到内存中，如果是读操作，内存中的数据起到缓存的作用，如果是写操作，内存还可以把随机的写操作转换成顺序的写操作，总之可以大幅度提升性能。
2.WiredTiger
--wiredTigerCacheSizeGB (默认物理内存一半)
--syncdelay (同步延迟1分钟)
--wiredTigerCollectionBlockCompressor (snappy或zlib)

Journaling (WAL)

1.MongoDB使用MMAP(内存映射文件)并且每60秒向磁盘输出一次通知，这就意味着最大程度上你可能丢失60秒加上向硬盘输出通知这段时间内所有的数据。
2.The WiredTiger journal ensures that writes are persisted to disk between checkpoints.
WiredTiger uses checkpoints to flush data to disk by default every 60 seconds or after 2GB of data has been written.

内存

分布式
   主从模式
   ReplSet复制集
   	 The size of the oplog is configurable and by default is 5% of the available free disk space
   Sharding分片
   	不可以更改文件中的shard key
   	Range-based Sharding
   	Hash-based Sharding
   	Location-aware Sharding
   读写分离

### MongoDB 数据结构

BSON (Binary JSON). The BSON encoding extends the popular JSON (JavaScript Object Notation) representation to include additional types such as int, long, and floating point.

树状结构
1.1  单文档存储整根树(Full Tree in Signle Document)
1.2  (父连接)Parent Links
1.3  (子链接)Child Links
1.4  (祖先数组)Array of Ancestors
1.5  物化路径(Materialized Path[Full Path in Each Node])

### MongoDB 查询与聚合
强查询弱更新
- Key-value queries
- Range queries
- Geospatial queries
- Text Search
- Aggregation Framework
- MapReduce queries

findAndModify
update
upsert

$push
$pop
$pull


Index
- Unique Indexes
- Compound Indexes
- Array Indexes
- TTL Indexes.
- Geospatial Indexes
- Sparse Indexes
- Text Search Indexes

### MongoDB 性能限制
Because MongoDB provides in-memory performance, for most applications there is no need for a separate caching layer.

### MongoDB 3.0 新特性
>	WiredTiger特性  
>	支持文档级别并发控制  
>	支持对所有集合和索引进行Block压缩和前缀压缩(包括journal)  
>	通过storage.wiredTiger.engineConfig.cacheSizeGB可控制MongoDB所能使用的最大内存(该参数默认值为物理内存大小的一半)  

查看比较1: [MongoDB响应延迟](../_includes/MongoLatency.png).

查看比较2: [MongoDB并发量](../_includes/MongoDBOpsSec.png).

>	MMAPv1存储引擎优化
>	并发锁粒度由数据库级别锁提升为集合级别锁
>	抛弃了基于paddingFactor的自适应分配方式,基于usePowerOf2Sizes的预分配方式成为默认的文档空间分配方式

>	Replica Set 优化
>	复制集成员增长到50个。但能够投票的最大成员个数依然为7个
>	Primary节点StepDown处理方式变化

>	Sharded Clusters 优化
>	新增工具函数 sh.removeTagRange()
>	提供更可预测的Read Preference处理
>	为chunk迁移提供writeConcern设置
>	增加均衡器状态显示

### MongoDB 实践

### MongoDB ORM 设计


