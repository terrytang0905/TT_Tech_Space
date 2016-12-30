---
layout: post
category : datascience
tags : [search, bigdata, develop]
title: Network Crawler Scrapy Design
---

### Impala

#### Impala Feature:

Impala apply Hadoop standard components(Metastore,HDFS,HBase,YARN,Sentry)

- Impala is the highest performing SQL-on-Hadoop system,especially under multi-user workloads.(nearly three times on average for multi-user)
- Impala SQL doesn't support UPDATE or DELETE like Hive.Impala supports ALTER TABLE DROP PARTITION.
- A major challenge in the design of an MPP database that is intended to run on hundrens of nodes is the coordination and synchronization of cluster-wide metadata 

#### Impala Architect

Impala is massively-parallel query execution engine,which runs on hundreds of machines in existing Hadoop clusters.

![Impala Architecture](_includes/Impala_arch.png).

Daemon-Statestore-CatalogService


#### Impala SQL Optimizer:

Query parsing,semantic analysis and query planing/optimization
QueryPlan:HDFS/HBase scan,hash join,cross join,union,hash aggregation,sort,top-n and analysis evaluation
Code generation has a dramatic impact on performance - Speed up 5.7x
Runtime Code Generation
In order to perform data scans from both disk and memory at or near hardware speed,Impala uses an HDFS feature called short-circuit local reads to bypass the DataNode protocol when reading from local disk.
Avro,RC,Sequence,plain text,Parquet(Recommend)
Resource Management:YARN Llama

#### Physical schema design 

CREATE TABLE T (...) PARTITIONED BY (day int,month int) LOCATION '<hdfs-path>' STORED AS PARQUET;
We could build time PARTITION for source table as the extend time items.  


### Kudu





### Reference

- [Impala Documents](http://www.cloudera.com/documentation/enterprise/latest/topics/impala.html)
- [Impala Code](https://github.com/cloudera/Impala/wiki)
- [Impala Paper]()
