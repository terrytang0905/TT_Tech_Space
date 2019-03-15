---
layout: post
category : bigdata
tags : [bigdata, database, analytics]
title: Database Research Note - Database Management for Analytics
---

## 大数据分析平台应用日志
--------------------------------------------------------

分析型数据平台研究主要是研究当前业内主流基于数据分析的大数据平台,整合MPP与Hadoop特性,来解决海量数据的分析查询性能问题。

### 核心能力定义

Access to Multiple Data Sources
Administration and Management
Advanced Analytics
Data Ingest(减少移动数据,增强移动计算)
Managing Large Volumes of Data
Optimized Performance (Traditional/Exploratory)
Flexible Scalability
Variety of Data Types
Workload Management(负载管理)
Traditional Use Support

Traditional Data Warehouse
Real-Time Data Warehouse(adhoc querying and data mining)
Logical Data Warehouse

	This use case manages data variety and volume of data for both structured and other content data types.

Context-Independent Data Warehouse

	This use case concerns new data values, variants of data form and new relationships. It supports search, graph and other capabilities for discovering new information models.


#### 1.Google BigQuery

基于Dremel的GoogleBigQuery

- Concept: distributed search engine design
- Dremel provides a high-level, SQL-like language to express ad hoc queries without translating them into MR job.
- Dremel uses a column-striped storage representation, which enables it to read less data from secondary storage and reduce CPU cost due to cheaper compression


1.A high-performance storage layer is critical for in situ data management.
2.Columnar storage proved successful for flat relational data but making it work for Google required adapting it to a nested data model.

Ref:

- [SQLonHadoop研究Note-Dremel](2017-04-04-olap-sqlonhadoop-research-note.md)
- [BigQuery](https://cloud.google.com/bigquery/)


#### 2.Huawei FusionInsight


华为FusionInsight大数据平台是集Hadoop生态发行版FusionInsight HD、大规模并行处理MPP数据库FusionInsight LibrA、大数据云服务(Hadoop、Hive、Spark、HBase、MPPDB、流计算等组件)于一体的融合数据处理与服务平台。它支持统一的SQL引擎,拥有端到端全生命周期的解决方案能力。除了以上能力外，还提供数据分析挖掘平台、数据服务平台，帮助用户实现从数据到知识，从知识到智慧的转换，进而帮助用户从海量数据中挖掘数据价值。它支持私有化部署，及华为公共云或合作伙伴的公共云环境中部署。 

此外华为FusionInsight大数据平台是根据行业客户需求进行优化的解决方案。为解决用户在具体场景下的问题，提供许多创新的技术能力，举几个例子：

	1是统一SQL服务。大数据技术中有很多能够利用SQL语言进行数据处理的组件，比如Hive、SparkSQL、Elk、MPPDB等，当用户对于这些组件进行业务开发时，需要对不同组件分别进行，造成很大的不便。FusionInsight提供统一SQL，对外业务界面只出现一个SQL开发管理界面，通过统一SQL的业务分发层进行业务分发，这样就简化了业务开发。同时，华为还提供了SQL on Hadoop引擎Elk，这个引擎完全兼容SQL 2003标准，无需修改测试脚本就可以通过TPC-DS测试，性能超过开源产品3倍。通过使用统一SQL技术，某大型保险公司实现了用大数据平台替代传统数仓，在复杂计算业务场景下，其性能提升了10-100倍。

	2是实时搜索。华为FusionInsight率先实现了对Hadoop平台与MPP-DB数仓平台的统一全文检索Elk，率先支持SQL on Solr接口，提升业务开发效率5倍以上，独创标签索引方案，提升搜索性能3-10倍。目前，实时搜索技术在平安城市和金融行业已经实现商用。在国内某省的平安城市项目中，百亿级规模数据集中查询，**实时搜索响应时间<3秒**。

	3是实时决策。与日常生活息息相关的很多业务是需要实时决策的，比如使用银行卡交易过程中的风险控制。由于传统技术处理速度的原因，往往只能实现事后风控。也就是说用户在刷卡完成后，银行才能够检查出来，刚才的交易是否有风险。这样对于银行和客户而言，都会有很大的风险存在。而华为FusionInsight实时决策平台，可以实现毫秒级复杂规则的风险检查，提供百万TIPS的业务处理能力，从而让风险控制从事后变为事中，并确保端到端的交易可在500毫秒内完成，不影响交易用户的体验。

	4是图分析技术。在生活中有很多时候是需要进行用户的关系分析来进行风险控制和业务处理的。如果我们的客户中有一个是VIP客户，那么他的朋友符合VIP客户条件的可能性就会很大。因此如果我们能够通过关系分析技术找到他的朋友圈，在针对他的朋友进行针对性营销，那么业务成功的可能性也就会大大增加。但是，传统的数据库技术在处理客户关系发现时很困难，某公司曾经做过一个测试，想在2000万客户中发现客户间的关系信息，但是一直无法算出来。但是用图分析技术就可以很好解决这一类问题。因为在图数据库中，用户就是点，用户关系就是边，发现用户关系就变成了发现点与点间需要几条边的问题。华为的分布式图数据库，能够实现万亿顶点百亿边的实时查询，从而很快发现用户关系。在某项目中，华为帮助客户实现了13.7亿条关系图谱数据，3层关系查询秒级响应，从而大大提高了业务响应的速度。


##### 华为Hadoop-FusionInsight HD

针对离线处理场景，FusionInsight HD由如下组件来实现：HDFS负责存储所有数据；Yarn负责调度在离线平台上运行的所有任务，从数据加工、数据挖掘到数据分析；Mapreduce和Hive专门处理离线的具体任务，其中Mapreduce/Spark处理非SQL类、Hive/Spark SQL处理SQL类.借助上述组件，再加上数据采集组件,即可完成离线处理。

	- 统一的SQL接口
	- FusionInsight SparkSQL
	- 完全自研的SQL引擎Elk
	- Apache CarbonData数据存储格式(基于SparkSQL,有索引的列式存储)
	- 多级租户管理功能
	- 对异构设备支持

Apache CarbonData文件格式的压缩率缩减与数据导入时间的延长

- [CarbonData数据格式](https://www.cnblogs.com/happenlee/p/9202236.html)

##### 华为MPPDB-FusionInsight LibrA
    
     FusionInsight LibrA是华为公司研发的OLAP(Online Analytical Processing)型数据库，旨在为您提供轻松、可靠的企业数仓、数据集市和大数据SQL结构化数据分析解决方案。
 
     FusionInsight LibrA采用MPP(Massive Parallel Processing)架构，支持行存储与列存储，提供PB(Petabyte，250字节)级别数据量的处理能力。在核心技术上较传统数据库有巨大优势，能够解决不同行业用户的数据分析性能问题，可以为超大规模数据分析提供高性价比的方案，并可用于支撑各类数据仓库系统、数据集市、BI(Business Intelligence)系统和决策支持系统。

FusionInsight LibrA关键特性：
 
	- 专业的TD、Oracle迁移工具:支持平滑迁移，业务敏捷上线。
	- 数据入库快:支持并行数据导入，日入库达数百TB。
	- 查询响应快:全并行计算引擎，满足PB级业务所需。行列混和存储引擎，同时满足点查、复杂分析等混合业务场景。
	- 扩展性强:扩容不中断业务，且扩容后，容量/性能线性增长。
	- 企业级高可用:独创的主+备+Handoff三重数据保护，协调节点多活设计，提供企业级可靠性保障。
	- 安全:全方位安全保证机制，为数据安全保驾护航。
	- 全文检索:支持标准SQL对文本进行模糊搜索，提供文本数据类“Google”功能。
	- SQL On Hadoop:无缝集成Hadoop，可通过标准SQL访问和处理Hadoop数据。



#### 3.Transwarp Data Hub

TDH主要提供6款核心产品:

	Transwarp Inceptor是大数据分析数据库
	Transwarp Slipstream是实时计算引擎
	Transwarp Discover专注于利用机器学习从数据提中取价值内容
	Transwarp Hyperbase用于处理非结构化数据
	Transwarp Search用于构建企业搜索引擎
	Transwarp Sophon则是支持图形化操作的深度学习平台


##### Transwarp Inceptor - OLAP SQL查询分析数据库

在Inceptor中，您可以使用常见的数据库对象,包括数据库(database),表(table),视图(view)和函数(function)。您可以使用Inceptor SQL、Inceptor PL/SQL以及Inceptor SQL PL来操作这些数据库对象。

Transwarp Inceptor是基于Spark的分析引擎，从下往上有三层架构：

	- 最下面是存储层，包含分布式内存列式存储（Transwarp Holodesk），可建在内存或者SSD上;
	- 中间层是Spark计算引擎层，星环做了大量的改进保证引擎有超强的性能和高度的健壮性;
    - 最上层包括一个完整的SQL 99和PL/SQL编译器、统计算法库和机器学习算法库，提供完整的R语言访问接口。

##### Inceptor执行计划:

对SQL语句的执行需要交给Inceptor计算引擎，Inceptor主要由两类节点组成：主节点Inceptor Server，以及计算节点Executor。SQL语句由Inceptor Server解析执行，生成执行计划，最终RDD的变换执行过程组成Transwarp Spark DAG，RDD中不同的partition合理的分配给不同的计算节点Executor，每个partition对应于一个计算子任务，由Executor执行具体的计算处理。

Inceptor Spark是重构自研下的定制Spark

##### Inceptor编程模型:

Inceptor提供两种编程模型：

	一是基于SQL的编程模型，用于常规的数据分析、数据仓库类应用市场；SQLParser支持SQL 99标准/支持PL/SQL扩展/支持部分SQL 2003标准
	SQL解析器支持HiveQL解析器、SQL标准解析器和PL/SQL解析器 混合切换
	二是基于数据挖掘编程模型，可以利用R语言或者Spark MLlib来做一些深度学习、数据挖掘等业务模型。

##### Inceptor SQL Optimizer

* 基于规则的优化器(Rule Based Optimizer)

	- 文件读取时过滤
	- 过滤条件前置
	- 超宽表的读取过滤
	- Shuffle Stage的优化与消除
	- Partition消除

* 基于成本的优化器(Cost Based Optimizer)

	- JOIN顺序调优
	- JOIN类型的选择
	- 并发度的控制

##### Inceptor 数据存储

- Inceptor中数据库对象的元数据保存在Inceptor Metastore中
- 数据库对象内的数据可以存放支持在：Holodesk表/HDFS/HBase/Hyperbase/RDBMS

* Holodesk特性

- OLAP Cube

		Holodesk支持在数据表中内建Cube，并在数据分析时有效的利用这些Cube信息来加速分析查询。目前对于10亿级别的数据量，Transwarp Inceptor结合Holodesk能够在4台X86 PC服务器组成集群上5s内完成实时聚合运算，与传统Cube的预先物化计算不同，Holodesk利用Cube信息实时计算，没有过滤条件以及统计粒度的限制，提供完整的OLAP能力。

- 索引

		Holodesk支持用户对数据列建立索引来加速查询，因此对精确查询能够做到亚秒级返回。另外Holodesk支持对多个列构建索引，并通过智能索引技术自动选择最高效的索引来执行物理计划，从而让SQL编程更加简单。

- 为SSD优化的存储模型

		为了给客户提供更高性价比的解决方案， Holodesk为SSD优化了存储模型，从而保证基于SSD的OLAP性能能够达到基于内存的性能80%以上，而成本降低到原有1/10。Inceptor是Hadoop业界首个和SSD深度优化的SQL执行引擎。

- 容错技术

		Transwarp Holodesk通过Zookeeper来管理元数据，从而避免因为单点故障而导致的数据丢失，数据checkpoint在HDFS中。服务在故障恢复之后，Holodesk能够通过Zookeeper中的信息自动重建数据与索引，因此有很高的可靠性。

- 线性扩展

		Holodesk中创建一个Cube额外消耗的时间和空间是固定的，创建多个Cube的开销是呈线性关系，同时Cube的数据也是分散保存在集群各个节点上。另外，通过对SSD的针对优化与支持，可以将分析容量从基于内存GB级扩展到基于SSD的TB级，同时分析性能与容量随着节点的个数近乎线性增长。


> Spark执行引擎稳定性问题


#### 4.Huawei FusionInsight vs Transwarp Inceptor



#### 5.Alibaba Cloud - MaxCompute


MaxCompute 主要服务于批量结构化数据的存储和计算，可以提供海量数据仓库的离线计算解决方案以及针对大数据的分析建模服务。

MaxCompute特点:

    - 大规模计算存储
    MaxCompute 适用于 100GB 以上规模的存储及计算需求，最大可达 EB 级别。
    - 多种计算模型
    MaxCompute 支持 SQL、MapReduce、Graph 等计算类型及 MPI 迭代类算法。
    - 强数据安全
    MaxCompute 已稳定支撑阿里全部离线分析业务7年以上，提供多层沙箱防护及监控。
    - 低成本
    与企业自建私有云相比，MaxCompute 的计算存储更高效，可以降低 20%-30% 的采购成本。

![MaxCompute逻辑架构](_includes/maxcomputer_arch.png)

![MaxCompute数据格式支持](_includes/maxcompute_datasource.png)

MaxComputer SQL Parser & SQL Optimizer

Ref:

[MaxCompute Ref](https://yq.aliyun.com/articles/78108)
[MaxCompute 2.0](https://yq.aliyun.com/articles/656158?spm=a2c4e.11153940.blogcont78108.63.4f88123cEqWDsN)

多个数据仓库产品功能重叠(HybridDB / AnalyticDB / MaxCompute)
缺少全球化的TechWriter,以支持非中国区客户

#### 6.GBase+Informix

GBase 8a


#### 技术思考

1.数据治理(数据清洗)的智能算法

例如:Cloudera Navigator(for data governance).国内的数据治理可能难度更多,更有本地化优化的空间

2.大数据查询优化器设计

Calcite -> Spark Catalyst -> Dremel查询优化

3.DataModel数据模型设计优化

面向Document的数据模型结构
```
message Document {
  required int64 DocId;
  optional group Links {
    repeated int64 Backward;
    repeated int64 Forward; }
  repeated group Name {
    repeated group Language {
      required string Code;
      optional string Country; }
    optional string Url; }}
```

5.数据存储结构设计

design memory and disk-based column store

Dremel NESTED COLUMNAR STORAGE

LSM数据结构

内存列式存储优化


6.distributed file system文件系统改造 

HDFS/GFS设计差异,定制化文件系统

例如:MapR Network File System (NFS)





