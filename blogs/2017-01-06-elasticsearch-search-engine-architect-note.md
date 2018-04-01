---
layout: post
category : datascience
tags : [search, bigdata, develop]
title: Distributed Search Engine Architect - ElasticSearch 
---

## ElasticSearch - Distributed SearchEngine Architect
------------------------------------------------------

#### Concepts

- Near Realtime (NRT)
- Cluster
- Node
- Index
- Document
- Shards & Replicas

	Sharding is important for two primary reasons:
	- It allows you to horizontally split/scale your content volume
	- It allows you to distribute and parallelize operations across shards (potentially on multiple nodes) thus increasing performance/throughput

	Replication is important for two primary reasons:
	- It provides high availability in case a shard/node fails. For this reason, it is important to note that a replica shard is never allocated on the same node as the original/primary shard that it was copied from.
	- It allows you to scale out your search volume/throughput since searches can be executed on all replicas in parallel.


#### About ElasticSearch v6

- [ElasticSearch SearchAPI](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html)

- [PostgreSQL to ElasticSearch](https://gocardless.com/blog/syncing-postgres-to-elasticsearch-lessons-learned/)