---
layout: post
category : bigdata
tags : [bigdata, tech, solution]
title: Big Data Research Note - Storage Layer
---

## 大数据研究-分布式文件存储格式
---------------------------------------------------


### I.基础数据存储格式


### II.Parquet

 a columnar storage format available to any project in the Hadoop ecosystem, regardless of the choice of data processing framework, data model or programming language.


### III.ORC

ORC: the smallest, fastest columnar storage for Hadoop workloads.

- ACID Support:Includes support for ACID transactions and snapshot isolation
- Built-in Indexes:Jump to the right row with indexes including minimum, maximum, and bloom filters for each column.
- Complex Types:Supports all of Hive's types including the compound types: structs, lists, maps, and unions

### IV.AliORC

**Row-based VS. Column-based**

对于文件存储而言，有两种主流的方式，即按行存储以及按列存储。所谓按行存储就是把每一行数据依次存储在一起，先存储第一行的数据再存储第二行的数据，以此类推。而所谓按列存储就是把表中的数据按照列存储在一起，先存储第一列的数据，再存储第二列的数据。而在大数据场景之下，往往只需要获取部分列的数据，那么使用列存就可以只读取少量数据，这样可以节省大量磁盘和网络I/O的消耗。此外，因为相同列的数据属性非常相似，冗余度非常高，列式存储可以增大数据压缩率，进而大大节省磁盘空间。因此，MaxCompute最终选择了列存。

### V.Avro

Apache Avro™ is a data serialization system.

Avro provides:

	- Rich data structures.
	- A compact, fast, binary data format.
	- A container file, to store persistent data.
	- Remote procedure call (RPC).
	- Simple integration with dynamic languages. Code generation is not required to read or write data files nor to use or implement RPC protocols. Code generation as an optional optimization, only worth implementing for statically typed languages.