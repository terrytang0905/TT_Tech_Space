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
- The key point of the impala design of an MPP database is how to run on hundrens of nodes is the coordination and synchronization of cluster-wide metadata.For example,up-to-date versions of the system catalog
- Designed a simple publish-subscribe service called the statestore to disseminate metadata changes to a set of subscribers,not establish a TCP connection or create synchronous RPCs(avoid network connection cost).
- Impala’s catalog service serves catalog metadata to Impala daemons via the statestore broadcast mechanism, and exe- cutes DDL operations on behalf of Impala daemons.
- The catalog service pulls information from third-party metadata stores (for example, the Hive Metastore or the HDFS Namenode), and aggregates that information into an Impala- compatible catalog structure.The default third-party metadata store is Hive Metastore and could be replaced by HBase.
- Impala supports inline views, uncorrelated and correlated subqueries (that are rewritten as joins), all variants of outer joins as well as explicit left/right semi- and anti-joins, and analytic window functions.
- Impala chooses whichever strategy is estimated to minimize the amount of data exchanged over the network, also exploiting existing data partitioning of the join inputs.The design is similar to Greenplum.
- Runtime code generation using LLVM is one of the techniques employed extensively by Impala's backend to improve execution times.
- In order to perform data scans from both disk and memory at or near hardware speed,Impala uses an HDFS feature called short-circuit local reads to bypass the DataNode protocol when reading from local disk.
- HDFS caching allows Impala to access memory-resident data at memory bus speed and also saves CPU cycles as there is no need to copy data blocks and/or checksum them.
- Impala supports most popular file formats:Avro,RC,Sequence,TEXTFILE and Parquet.Recommend using Apache Parquet because Parquet offer both high compression and scan efficency.
-Compared to YARN resource management,Impala support mixed-workload resource management through a single mechanism that supports both the low latency decision making of admission control & Llama for Low-Latency Application Master, and the cross-framework support of YARN.

#### Impala Architect

Impala is massively-parallel query execution engine,which runs on hundreds of machines in existing Hadoop clusters.

![Impala Architecture](_includes/Impala_arch.png).

> Impala daemon(impalad) <br/> 
> Statestore daemon(statestored) <br/>
> Catalog daemon(catalogd) <br/>
> Hive Metastore <br/>
> HDFS 

#### Impala SQL Query:

Query compilation process: Query parsing,semantic analysis and query planing/optimization

An executable query plan is constructed in two phases: (1) Single node planning and (2) plan parallelization and fragmentation.<br/>

	> 1)A non- executable single-node plan tree consists of HDFS/HBase scan,hash join,cross join,union,hash aggregation,sort,top-n and analysis evaluation.<br/>
	> 2)Takes the single-node plan as input and produces a distributed execution plan in order to to minimize data movement and maximize scan locality.<br/>
    All aggregation is currently executed as a local pre-aggregation followed by a merge aggregation operation.

The impala backend is written in C++ and uses code generation at runtime to produce e cient codepaths (with respect to instruction count) and small memory overhead.<br/>
Impala employs a partitioning approach for the hash join and aggregation operators.<br/>
When building the hash tables for the hash joins and there is reduction in cardinality of the build-side relation, impala constructs a Bloom-filter which is then passed on to the probe side scanner, implementing a simple version of a semi-join.

##### About Code Generation

Virtual function calls incur a large performance penalty and cost large runtime overheads.Impala uses code generation to replace the virtual function call with a call directly to the correct function, which can then be inlined.<br/>
JIT compilation has an effect similar to custom-coding a query. For example, it eliminates branches, unrolls loops, propagates constants, offsets and pointers, inlines functions.<br/>
Code generation has a dramatic impact on performance - Speed up 5.7x

* Runtime Code Generation *

In order to perform data scans from both disk and memory at or near hardware speed,Impala uses an HDFS feature called short-circuit local reads to bypass the DataNode protocol when reading from local disk.
Avro,RC,Sequence,plain text,Parquet(Recommend)

Resource Management:YARN Llama

#### Physical schema design 

CREATE TABLE T (...) PARTITIONED BY (day int,month int) LOCATION '<hdfs-path>' STORED AS PARQUET;
We could build time PARTITION for source table as the extend time items.  


### Kudu

hybrid architectures(HDFS+HBase)



### Reference

- [Impala Documents](http://www.cloudera.com/documentation/enterprise/latest/topics/impala.html)
- [Impala Code](https://github.com/cloudera/Impala/wiki)
- [Impala Paper]()
