---
layout: post
category : bigdata
tags : [search, bigdata, develop]
title: Distributed Search Engine Architect - ElasticSearch 
---

## Elasticsearch - Distributed SearchEngine Architect
-------------------------------------------------------------

CurrVersion:6.3

#### Concepts

Elasticsearch is a distributed RESTful search engine built for the cloud. Features include:

- Distributed and Highly Available Search Engine.

	Each index is fully sharded with a configurable number of shards.
	Each shard can have one or more replicas.
	Read / Search operations performed on any of the replica shards.

- Multi Tenant.

	Support for more than one index.
	Index level configuration (number of shards, index storage, …).

- Various set of APIs

	HTTP RESTful API
	Native Java API.
	All APIs perform automatic node operation rerouting.

- Document oriented

	No need for upfront schema definition.
	Schema can be defined for customization of the indexing process.

- Reliable, Asynchronous Write Behind for long term persistency.
- (Near) Real Time Search.
- Built on top of Lucene

	Each shard is a fully functional Lucene index
	All the power of Lucene easily exposed through simple configuration / plugins.

- Per operation consistency

	Single document level operations are atomic, consistent, isolated and durable.

- Shards & Replicas

	Sharding is important for two primary reasons:
	- It allows you to horizontally split/scale your content volume
	- It allows you to distribute and parallelize operations across shards (potentially on multiple nodes) thus increasing performance/throughput

	Replication is important for two primary reasons:
	- It provides high availability in case a shard/node fails. For this reason, it is important to note that a replica shard is never allocated on the same node as the original/primary shard that it was copied from.
	- It allows you to scale out your search volume/throughput since searches can be executed on all replicas in parallel.

#### 数据同步

1.Logstash数据采集

![Logstash](_includes/logstash.png)

Logstash JDBC input 

2.[PostgreSQL to ElasticSearch](https://gocardless.com/blog/syncing-postgres-to-elasticsearch-lessons-learned/)


#### Elasticsearch Tuning

#### A.[Tune for indexing speed](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html)

- 使用bulk请求
- 使用并行workers/threads来发送数据到ES
- 增加刷新频率index.refresh_interval
- 在初始加载时禁用刷新和复制
- 禁用swap内存交换
- 分配至少一半的内存到文件系统Cache
- 使用自建ids
- 使用更快的硬件
- 索引buffer size=indices.memory.index_buffer_size
- 禁用_field_names

#### B.[Tune for searching speed](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html)

- 分配内存到filesystem cache
- 选择性能高硬件(IOPS高的磁盘,废话一句)
- Document模型
- 搜索尽可能少的field字段
- 预索引数据pre-index data
- Mapping映射
- Search rounded dates
- [强制merge只读索引](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-forcemerge.html)
- 开启global ordinals
- 开启filesystem cache(index.store.preload)
- 映射标识符为keyword
- 使用Index sorting来加速连接
- 使用preference来优化缓存
- Replicas复制可提高throughput

#### Elasticsearch-Hadoop

Elasticsearch对接Hadoop

- [Elasticsearch-Hadoop](https://www.elastic.co/cn/products/hadoop)

#### ElasticSearch v6 API

- [Elasticsearch SearchAPI](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html)



