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
- Runtime code generation using LLVM is one of the techniques employed extensively by Impala's backend to improve execution times.
- In order to perform data scans from both disk and memory at or near hardware speed,Impala uses an HDFS feature called short-circuit local reads to bypass the DataNode protocol when reading from local disk.
- HDFS caching allows Impala to access memory-resident data at memory bus speed and also saves CPU cycles as there is no need to copy data blocks and/or checksum them.
- Impala supports most popular file formats:Avro,RC,Sequence,TEXTFILE and Parquet.Recommend using Apache Parquet because Parquet offer both high compression and scan efficency.
-Compared to YARN resource management,Impala support mixed-workload resource management through a single mechanism that supports both the low latency decision making of admission control & Llama for Low-Latency Application Master, and the cross-framework support of YARN.

#### Impala Architect

Impala is massively-parallel query execution engine,which runs on hundreds of machines in existing Hadoop clusters.

![Impala Architecture](_includes/Impala_arch.png).

Impala daemon(impalad)
Statestore daemon(statestored)
Catalog daemon(catalogd)


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
