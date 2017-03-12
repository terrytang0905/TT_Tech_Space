---
layout: post
category : datascience
tags : [bigdata,database,develop]
title: BigTable&HBase Analysis Note
---

BigTable & HBase Analysis Note
------------------------------------------------------------


### BigTable原理


### HBase 深度研究

HBase是按照BigTable模型实现的,是一个稀疏的,分布式的,持久化的,多维的映射,由行键,列键和时间戳索引。

Table -> RowKey -> Column Family(Column data/Timestamp/Version) = Value

SortedMap<RowKey,List<SortedMap<Column,List<Value,Timestamp>>>>

BigTable和HBase的典型使用场景是webtable,存储从互联网中抓取网页。
行数据的存取操作是原子的(atomic),可以读写任意数目的列。目前为止不支持跨行事务与跨表事务,和绝大多数NoSQL数据库一致


#### HBase自动分区-autosharding

HBase中扩展与负载均衡的基本单元称为region,region本质上是以行键排序的连续存储的区间。HBase中的region等同于数据库分区中用的
范围划分(range partition)。

* Region Server与Region分布 

按照HBase和现在的硬件能力,每台服务器的最佳加载数量差不多还是10-1000,但每个region的最佳大小是1GB-2GB。

#### 简单数据模型&存储API

数据存储在存储文件(store file)中,称为HFile,HFile中存储的是经过排序的键值映射结构。文件内部由连续的块组成,块的索引信息存储在文件尾部。
每个HFile都有一个块索引。首先,在内存的块索引进行二分查询(已排序数据结构)。
存储文件通常保存于HDFS,作为HBase的存储层。



### Ref

