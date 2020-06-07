---
layout: post
category : bigdata
tags : [bigdata, tech, solution]
title: Big Data Research Note - LakeHouse
---

## 大数据研究-计算存储优化解决方案
---------------------------------------------------


大数据存储，我们能想到的技术有很多，比如HDFS，以及在HDFS上的列式存储技术Apache Parquet，Apache ORC，还有以KV形式存储半结构化数据的Apache HBase和Apache Cassandra。但因为众所周知的以下原因:

- HDFS:使用列式存储格式Apache Parquet，Apache ORC，适合离线分析，不支持单条纪录级别的update操作，随机读写性能差
- HBASE:可以进行高效随机读写，却并不适用于基于SQL的数据分析方向，大批量数据获取时的性能较差。

我们需要以下技术特性:

- 事务支持：企业内部许多数据管道通常会并发读写数据。对ACID事务支持确保了多方可使用SQL并发读写数据。
- 模式执行和治理（Schema enforcement and governance）：LakeHouse应该有一种可以支持模式执行和演进、支持DW模式的范式（如star/snowflake-schemas）。该系统应该能够推理数据完整性，并具有健壮的治理和审计机制。
- 计算与存储分离+高可用:这意味着存储和计算使用单独的集群，因此这些系统能够支持更多用户并发和更大数据量。一些现代数据仓库也具有此属性。
- 离线加速查询能力
- 高效随机读写/OLAP分析查询
- Update/Deleta数据更新能力
- 行存与列存混合优化存储(资源优化/高压缩比)
- 支持从非结构化数据到结构化数据的多种数据类型：LakeHouse可用于存储、优化、分析和访问许多数据应用所需的包括图像、视频、音频、半结构化数据和文本等数据类型。
- 支持各种工作负载：包括数据科学、机器学习以及SQL和分析。可能需要多种工具来支持这些工作负载，但它们底层都依赖同一数据存储库。
- 批流一体


### I.Apache Hudi

[Apache Hudi](https://github.com/apache/hudi)=Hadoop Upserts anD Incrementals

* 读取优化的表（Read Optimized Table）和近实时表（Near-Realtime Table）。

- 可插拔式的索引支持快速Upsert / Delete。
- 事务提交/回滚数据。
- 支持捕获Hudi表的变更进行流式处理。
- 支持Apache Hive，Apache Spark，Apache Impala和Presto查询引擎。
- 内置数据提取工具，支持Apache Kafka，Apache Sqoop和其他常见数据源。
- 通过管理文件大小，存储布局来优化查询性能。
- 基于行存快速提取模式，并支持异步压缩成列存格式。
- 用于审计跟踪的时间轴元数据。

Hudi使得能在hadoop兼容的存储之上存储大量数据，同时它还提供两种原语，使得除了经典的批处理之外，还可以在数据湖上进行流处理。这两种原语分别是：

* Update/Delete记录：Hudi使用细粒度的文件/记录级别索引来支持Update/Delete记录，同时还提供写操作的事务保证。查询会处理最后一个提交的快照，并基于此输出结果。
* 变更流：Hudi对获取数据变更提供了一流的支持：可以从给定的时间点获取给定表中已updated/inserted/deleted的所有记录的增量流，并解锁新的查询姿势（类别）。
* 准实时表：使用列存储和行存储以提供对实时数据的查询


#### 存储类型

我们看一下 Hudi 的两种存储类型：

    - 写时复制（copy on write）：仅使用列式文件（parquet）存储数据。在写入/更新数据时，直接同步合并原文件，生成新版本的基文件（需要重写整个列数据文件，即使只有一个字节的新数据被提交）。此存储类型下，写入数据非常昂贵，而读取的成本没有增加，所以适合频繁读的工作负载，因为数据集的最新版本在列式文件中始终可用，以进行高效的查询。
    - 读时合并（merge on read）：使用列式（parquet）与行式（avro）文件组合，进行数据存储。在更新记录时，更新到增量文件中（avro），然后进行异步（或同步）的compaction，创建列式文件（parquet）的新版本。此存储类型适合频繁写的工作负载，因为新记录是以appending 的模式写入增量文件中。但是在读取数据集时，需要将增量文件与旧文件进行合并，生成列式文件。

    Tips: Hudi做的事情就是将批处理（copy-on-write storage）和流计算（merge-on-read storage）作业整合，并将计算结果存储在Hadoop中。对于Spark应用程序，依靠其同意的DAG模型可以将融入了Hudi库与Spark/Spark Steaming作业天然整合。对于非Spark处理系统（例如：Flink，Hive），处理过程可以在各自的系统中完成，然后以Kafka Topics 或者HDFS中间文件的形式发送到Hudi表中。


#### 视图

在了解这两种存储类型后，我们再看一下Hudi支持的存储数据的视图（也就是查询模式）：

	-	读优化视图（Read Optimized view）：直接query 基文件（数据集的最新快照），也就是列式文件（如parquet）。相较于非Hudi列式数据集，有相同的列式查询性能
    - 增量视图（Incremental View）：仅query新写入数据集的文件，也就是指定一个commit/compaction，query此之后的新数据。
    - 实时视图（Real-time View）：query最新基文件与增量文件。此视图通过将最新的基文件（parquet）与增量文件（avro）进行动态合并，然后进行query。可以提供近实时的数据（会有几分钟的延迟）

在以上3种视图中，“读优化视图”与“增量视图”均可在“写时复制”与“读时合并”的存储类型下使用。而“实时视图“仅能在”读时合并“模式下使用。

存储类型  | 支持的视图 
-------- |----------
 写时复制 | 读优化 + 增量 
 读时合并 | 读优化 + 增量 + 近实时 

 

#### 时间轴

最后介绍一下 Hudi 的核心 —— 时间轴。

Hudi 会维护一个时间轴，在每次执行操作时（如写入、删除、合并等），均会带有一个时间戳。通过时间轴，可以实现在仅查询某个时间点之后成功提交的数据，或是仅查询某个时间点之前的数据。这样可以避免扫描更大的时间范围，并非常高效地只消费更改过的文件（例如在某个时间点提交了更改操作后，仅query某个时间点之前的数据，则仍可以query修改前的数据）。

 

### II.Spark DeltaLake

**Delta Lake特性**

- 支持ACID事务
- 可扩展的元数据处理
- 统一的流、批处理API接口
- 更新、删除数据，实时读写（读是读当前的最新快照）
- 数据版本控制，根据需要查看历史数据快照，可回滚数据
- 自动处理schema变化，可修改表结构

**Delta Lake目前的不足**

- 更新操作很重，更新一条数据和更新一批数据的成本可能是一样的，所以不适合一条条的更新数据
- 新数据的方式是新增文件，会造成文件数量过多，需要清理历史版本的数据，version最好不要保存太多
- 乐观锁在多用户同时更新时并发能力较差，更适合写少读多的场景（或者only append写多更新少场景）

### III.Apache Kudu

[Apache Kudu](https://kudu.apache.org/)在更新更及时的基础上实现更快的数据分析

Kudu不但提供了行级的插入、更新、删除API，同时也提供了接近Parquet性能的批量扫描操作。使用同一份存储，既可以进行随机读写，也可以满足数据分析的要求。

#### 1.Kudu总览

Tables和Schemas

从用户角度来看，Kudu是一种存储结构化数据表的存储系统。在一个Kudu集群中可以定义任意数量的table，每个table都需要预先定义好schema。每个table的列数是确定的，每一列都需要有名字和类型，每个表中可以把其中一列或多列定义为主键。这么看来，Kudu更像关系型数据库，而不是像HBase、Cassandra和MongoDB这些NoSQL数据库。不过Kudu目前还不能像关系型数据一样支持二级索引。
Kudu使用确定的列类型，而不是类似于NoSQL的“everything is byte”。这可以带来两点好处：

     - 确定的列类型使Kudu可以进行类型特有的编码。
     - 可以提供 SQL-like 元数据给其他上层查询工具，比如BI工具。

**读写操作**

用户可以使用 Insert，Update和Delete API对表进行写操作。不论使用哪种API，都必须指定主键。但批量的删除和更新操作需要依赖更高层次的组件（比如Impala、Spark）。Kudu目前还不支持多行事务。
而在读操作方面，Kudu只提供了Scan操作来获取数据。用户可以通过指定过滤条件来获取自己想要读取的数据，但目前只提供了两种类型的过滤条件：主键范围和列值与常数的比较。由于Kudu在硬盘中的数据采用列式存储，所以只扫描需要的列将极大地提高读取性能。

**一致性模型**

Kudu为用户提供了两种一致性模型。默认的一致性模型是snapshot consistency。这种一致性模型保证用户每次读取出来的都是一个可用的快照，但这种一致性模型只能保证单个client可以看到最新的数据，但不能保证多个client每次取出的都是最新的数据。另一种一致性模型external consistency可以在多个client之间保证每次取到的都是最新数据，但是Kudu没有提供默认的实现，需要用户做一些额外工作。
为了实现external consistency，Kudu提供了两种方式：

     - 在client之间传播timestamp token。在一个client完成一次写入后，会得到一个timestamp token，然后这个client把这个token传播到其他client，这样其他client就可以通过token取到最新数据了。不过这个方式的复杂度很高。
     - 通过commit-wait方式，这有些类似于Google的Spanner。但是目前基于NTP的commit-wait方式延迟实在有点高。不过Kudu相信，随着Spanner的出现，未来几年内基于real-time clock的技术将会逐渐成熟。

#### 2.Kudu的架构

与HDFS和HBase相似，Kudu使用单个的Master节点，用来管理集群的元数据，并且使用任意数量的Tablet Server节点用来存储实际数据。可以部署多个Master节点来提高容错性。

Kudu架构图


***Master***

Kudu的master节点负责整个集群的元数据管理和服务协调。它承担着以下功能：

作为catalog manager，master节点管理着集群中所有table和tablet的schema及一些其他的元数据。
作为cluster coordinator，master节点追踪着所有server节点是否存活，并且当server节点挂掉后协调数据的重新分布。
作为tablet directory，master跟踪每个tablet的位置。

**Catalog Manager**

Kudu的master节点会持有一个单tablet的table——catalog table，但是用户是不能直接访问的。master将内部的catalog信息写入该tablet，并且将整个catalog的信息缓存到内存中。随着现在商用服务器上的内存越来越大，并且元数据信息占用的空间其实并不大，所以master不容易存在性能瓶颈。catalog table保存了所有table的schema的版本以及table的状态（创建、运行、删除等）。

**Cluster Coordination**

Kudu集群中的每个tablet server都需要配置master的主机名列表。当集群启动时，tablet server会向master注册，并发送所有tablet的信息。tablet server第一次向master发送信息时会发送所有tablet的全量信息，后续每次发送则只会发送增量信息，仅包含新创建、删除或修改的tablet的信息。
作为cluster coordination，master只是集群状态的观察者。对于tablet server中tablet的副本位置、Raft配置和schema版本等信息的控制和修改由tablet server自身完成。master只需要下发命令，tablet server执行成功后会自动上报处理的结果。

**Tablet Directory**

因为master上缓存了集群的元数据，所以client读写数据的时候，肯定是要通过master才能获取到tablet的位置等信息。但是如果每次读写都要通过master节点的话，那master就会变成这个集群的性能瓶颈，所以client会在本地缓存一份它需要访问的tablet的位置信息，这样就不用每次读写都从master中获取。
因为tablet的位置可能也会发生变化（比如某个tablet server节点crash掉了），所以当tablet的位置发生变化的时候，client会收到相应的通知，然后再去master上获取一份新的元数据信息。

**Tablet存储**

在数据存储方面，Kudu选择完全由自己实现，而没有借助于已有的开源方案。tablet存储主要想要实现的目标为：

	- 快速的列扫描。
	- 低延迟的随机读写。
	- 一致性的性能。

**RowSets**

在Kudu中，tablet被细分为更小的单元，叫做RowSets。一些RowSet仅存在于内存中，被称为MemRowSets，而另一些则同时使用内存和硬盘，被称为DiskRowSets。任何一行未被删除的数据都只能存在于一个RowSet中。
无论任何时候，一个tablet仅有一个MemRowSet用来保存最新插入的数据，并且有一个后台线程会定期把内存中的数据flush到硬盘上。
当一个MemRowSet被flush到硬盘上以后，一个新的MemRowSet会替代它。而原有的MemRowSet会变成一到多个DiskRowSet。flush操作是完全同步进行的，在进行flush时，client同样可以进行读写操作。

**MemRowSet**

MemRowSets是一个可以被并发访问并进行过锁优化的B-tree，主要是基于MassTree来设计的，但存在几点不同：

	- Kudu并不支持直接删除操作，由于使用了MVCC，所以在Kudu中删除操作其实是插入一条标志着删除的数据，这样就可以推迟删除操作。
	- 类似删除操作，Kudu也不支持原地更新操作。
	- 将tree的leaf链接起来，就像B+-tree。这一步关键的操作可以明显地提升scan操作的性能。
	- 没有实现字典树（trie树），而是只用了单个tree，因为Kudu并不适用于极高的随机读写的场景。

与Kudu中其他模块中的数据结构不同，MemRowSet中的数据使用行式存储。因为数据都在内存中，所以性能也是可以接受的，而且Kudu对在MemRowSet中的数据结构进行了一定的优化。

**DiskRowSet**

当MemRowSet被flush到硬盘上，就变成了DiskRowSet。当MemRowSet被flush到硬盘的时候，每32M就会形成一个新的DiskRowSet，这主要是为了保证每个DiskRowSet不会太大，便于后续的增量compaction操作。Kudu通过将数据分为base data和delta data，来实现数据的更新操作。Kudu会将数据按列存储，数据被切分成多个page，并使用B-tree进行索引。除了用户写入的数据，Kudu还会将主键索引存入一个列中，并且提供布隆过滤器来进行高效查找。

**Compaction**

为了提高查询性能，Kudu会定期进行compaction操作，合并delta data与base data，对标记了删除的数据进行删除，并且会合并一些DiskRowSet。

**分区**

和许多分布式存储系统一样，Kudu的table是水平分区的。BigTable只提供了range分区，Cassandra只提供hash分区，而Kudu提供了较为灵活的分区方式。当用户创建一个table时，可以同时指定table的的partition schema，partition schema会将primary key映射为partition key。一个partition schema包括0到多个hash-partitioning规则和一个range-partitioning规则。通过灵活地组合各种partition规则，用户可以创造适用于自己业务场景的分区方式。


### IV.Apache CarbonData

[Apache CarbonData](https://github.com/apache/carbondata)是一个支持索引和物化视图的ACID数据湖的数据存储(计算与存储分离)优化解决方案

- 索引和物化视图能力：

详单查询：二级索引、BloomFilter索引、Lucene索引、空间索引、Segment级别MINMAX索引，实现PB级别秒级详单查询；
复杂查询：物化视图、时序聚合、分桶索引，实现复杂查询秒级响应；
海量索引管理：分布式内存索引缓存、并支持索引内存预加载；

- 数据湖能力：

历史数据无缝迁移：支持对Parquet、ORC、CarbonData数据进行统一元数据管理，PB级别Parquet、ORC数据秒级迁移CarbonData；
历史数据加速：为Parquet、ORC、CarbonData构建统一物化视图；
异构计算融合：对接Flink、Hive、Presto、PyTorch、TensorFlow，实现“一份数据到处访问”；

- ACID能力：

Insert、Update和Delete性能增强，支持Merge语法


下面我们首先介绍CarbonData的愿景，其次通过示例介绍CarbonData的索引、物化视图、数据湖能力和ACID能力。

前言
如下表所示，业界在EB级别存储的数据库可选方案主要包含Nosql数据、Hadoop生态数据仓库等，但都有其明显的不足。

可选方案	优势	不足
HBase、ES、Kudu、MPP等	快	贵
Spark、Hive等	成本低	慢
​ ​ ​ ​ ​ ​ 首先，以HBase服务、MongoDB服务或者ElasticSearch服务为代表的Nosql数据库，虽然也可以支持快速的复杂SQL查询，但是这些服务均不支持存储与计算分离，为了满足PB/EB级别存储的需求，往往我们需要启动更多的计算节点，消耗更多的CPU和存储成本，同时还要付出更多的运维成本，计算和存储的紧密耦合也意味着更低的计算和存储利用率。例如HBase服务，单台RegionServer可维护不超过10TB的数据，面对10PB的数据存储时，需要1000台计算节点部署RegionServer，其所面对的金钱成本和运维成本都十分高昂。
​ ​ ​ ​ ​ ​ 其次，以Spark on Parquet、Hive on ORC为代表的Hadoop生态数据仓库解决方案，支持将数据放在对象存储服务上，但是没有对数据构建高效的索引，使得明细数据查询或者复杂查询都很慢。假设如下几种场景：1）查询过去一年某用户的行为轨迹，当没有针对用户构建索引时，只能暴力扫描过去一整年的数据，测试中需要7天才能完成，2）Join类的复杂查询同样如此，无索引情况下，只能对数据暴力扫描，极大限制了查询速度。
​ ​ ​ ​ ​ ​ 由上可见，Nosql数据库虽然具有较好的数据索引机制，但是“太贵”，传统的Hadoop生态数据仓库将数据放在对象存储上，但是“太慢”，这两者各自的局限性，使得我们进行EB级别数据仓库选型时，面临着这一个鱼与熊掌不可兼得的选择题。

​ 为了能够像关系型数据库一样可以高效执行复杂SQL查询，又可以像NoSQL数据库一样，构建高效索引，最后，可以和Spark/Hive一样，享受高度可扩展性的数据并行处理、利用近乎无限的低成本的对象存储资源，满足这种“又方便又快又便宜”的任性就是CarbonData的使命。

接下来的内容，我们将重点介绍如何体验CarbonData 2.0 RC2中的索引、物化视图、ACID能力。

一、快速安装CarbonData
准备1台Linux弹性云服务器

下载快速安装脚本
```
curl -k -O http://carbondata-publish.obs.myhuaweicloud.com/quick_start_carbondata.sh
```

启动sparksql和carbondata
```
source quick_start_carbondata.sh
```

二、CarbonData索引和物化视图

CarbonData 2.0 提供了丰富的索引能力，笔者总结了CarbonData提供的不同索引能力和适用场景。如下表所示。

| 索引类型  | 	适用场景	          | 效果             |
| 排序索引  |	带有排序键过滤的查询     | 秒级主键精确查询   |
| 二级索引  | 带有二级索引键过滤的查询 | 	秒级非主键精确查询 | 
| 物化视图  | Join、GroupBy、OrderBy等复杂查询	| 复杂查询秒级响应 | 
| 时序索引	| 时序聚合	| 秒级时序聚合 | 
| 空间索引	| 空间检索	| 秒级空间精确过滤 | 
| BloomFilter索引	|  带有高基数列过滤的查询	|  高基数列快速过滤 | 
| Lucene索引	  | 多维检索	|  秒级多维索引  | 

下面我们给出在CarbonData中构建索引的语法示例。

* 构建排序键索引，语法举例如下：

```
CREATE TABLE person(id STRING, age INT, country STRING, timestamp timestamp, address STRING, skill STRING) 
STORED AS carbondata 
TBLPROPERTIES('sort_scope'='GLOBAL_SORT','sort_columns'='id, age');
```

* 构建二级索引，语法举例如下：

```
CREATE INDEX person_si_country_age on table person(country, age) AS 'carbondata';
```

* 构建物化视图，基于复杂查询构建物化视图的语法举例如下：
```
CREATE MATERIALIZED VIEW person_countid_gb_country
AS SELECT country,count(id) FROM person GROUP BY country;
```
* 构建时序索引，语法举例如下：
```
CREATE MATERIALIZED VIEW person_countid_gb_timeseries AS
SELECT timeseries(timestamp, 'minute'),count(id)
FROM person 
GROUP BY timeseries(timestamp, 'minute');
```
* BloomFilter索引，语法举例如下：
```
CREATE INDEX person_bf_address
ON TABLE person (address)
AS 'bloomfilter'
PROPERTIES ('BLOOM_SIZE'='640000', 'BLOOM_FPP'='0.00001');
```
* Lucene索引，语法举例如下：
```
CREATE INDEX person_luc_skill
ON TABLE person (skill)
AS 'lucene';
```
* 加载数据
```
INSERT INTO person VALUES 
('c001', '23', 'china', '2016-02-23 09:01:30','china sz','computer design'),
('c003', '23', 'japan', '2016-02-23 08:01:30','japan to','sport speech'),
('c002', '23', 'india', '2016-02-23 07:01:30','india mm','draw write');
```
* 查询数据
```
//利用排序索引查询
SELECT * FROM person WHERE id = 'c001';

//利用二级索引查询
SELECT * FROM person WHERE country = 'china' and age = 23;

//利用物化视图进行查询
SELECT country,count(id) FROM person GROUP BY country;

//利用时序索引进行查询
SELECT timeseries(timestamp, 'minute'),count(id)
FROM person 
GROUP BY timeseries(timestamp, 'minute');

//利用BloomFilter索引进行查询
SELECT * FROM person WHERE address = 'china sz';

//利用Lucene索引进行查询
SELECT * FROM person WHERE TEXT_MATCH('skill:*computer*')
```

三、数据湖

CarbonData在体现性能优势的同时，需要回答如何将历史数据搬迁到CarbonData的问题，CarbonData 2.0交出了如下的答卷：

- 1）历史Parquet、ORC数据如何导入CarbonData？

支持通过"add segment"的方式，实现CarbonData对Parquet、ORC数据进行统一纳管。实现PB级别历史数据秒级迁移。

- 2）如何对历史Parquet、ORC数据构建索引？

支持对CarbonData、Parquet、ORC构建统一物化视图。实现PB级别数据复杂查询秒级响应。

下面主要通过示例演示以上两个功能：
	
	1.Parquet文件如何无缝导入CarbonData; 
	2.如何对Parquet数据构建物化视图。

Parquet文件导入CarbonData
首先，构建一张Parquet表，并写入数据。

```
CREATE TABLE parquet_table(id STRING, age INT, country STRING, timestamp timestamp, address STRING, skill STRING) 
STORED AS parquet;

INSERT INTO parquet_table VALUES 
('c004', '23', 'kor', '2016-02-22 09:01:30','kor ab','design'),
('c005', '23', 'russia', '2016-02-21 08:01:30','russia mo','game'),
('c006', '23', 'india', '2016-02-23 07:01:30','india sc','travel');
```

其次，将Parquet文件元数据导入CarbonData，语法示例如下。这里path需要替换为真实parquet表路径，路径信息可以通过describe formatted parquet_table查询得到。

```
ALTER TABLE person ADD SEGMENT options('path'='{$parquet_table_location}','format'='parquet');
```
最后，查询CarbonData表。最终可以发现CarbonData表中已经可以查询到Parquet表的数据。
```
SELECT * FROM person;
```
为Parquet表构建物化视图
```
CREATE MATERIALIZED VIEW parquet_table_countid_gb_country
AS SELECT country,count(id) FROM parquet_table GROUP BY country;
```
利用物化视图进行查询
```
SELECT country,count(id) FROM parquet_table GROUP BY country;
```
三、ACID

CarbonData 2.0中深度优化了UPDATE、DELETE性能，并支持了Merge语法。

数据更新，语法示例如下：
```
UPDATE person SET age = '24' WHERE id = c001;
```
数据删除，语法示例如下：
```
DELETE FROM person WHERE id = c002;
```
数据Merge，支持批量查询、更新、删除。[语法可参考](https://github.com/apache/carbondata/blob/master/examples/spark/src/main/scala/org/apache/carbondata/examples/CDCExample.scala)


结语
CarbonData提供了一种新的融合数据存储方案，以一份数据同时支持多种应用场景，EB级别数据规模，查询性能秒级响应。可以看出CarbonData目前的架构和想法都十分先进.



### V.AliCloud Hologres


