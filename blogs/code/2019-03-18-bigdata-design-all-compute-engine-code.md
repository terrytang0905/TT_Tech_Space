---
layout: post
category : bigdata
tags : [bigdata, framework, design]
title: BigDataDesign - All Compute Engine Code Design
---

## 大数据设计-分布式联合查询计算引擎
-----------------------------------------------------------

### I.需求分析与设计

分布式查询计算引擎

_1.核心Features设计_

	1.数据湖多数据源整合建模-Data Lake Analytics
	2.元数据模型抽象动态支持业务模型
	3.支持标准SQL语言标准
	4.OLAP/OLTP/ETL联合查询
	5.离线与实时大数据处理与计算优化
	6.边缘计算引擎

_2.核心问题整理_

	解决海量数据计算性能问题 - Spark&Flink
	解决数据检索与即席查询分析需求 - Elasticsearch
	解决数据库查询性能瓶颈的分布式内存 - Ingite
	解决通用联合查询分析需求落地 - Presto+定制OLAP平台

_3.相关技术文档_

- [分布式交互式查询](2017-04-04-olap-sqlonhadoop-research-note.md)

- [通用OLAP查询引擎设计](2017-02-01-bigdata-analytics-olap-query-engine-design-note.md)

- [查询优化器设计](2018-06-01-query-optimizer-design-note.md)


### II.Federated Query - Data Lake Analytics

使用标准SQL即可分析与集成对象存储、数据库(PostgreSQL/MySQL等)、NoSQL(TableStore等)数据源的数据

F1 Query=用一套系统解决所有 OLTP、OLAP、ETL需求.用一套系统访问数据中心里各种格式的数据

1. OLTP - 事务型交易执行（Centralized Execution）
2. OLAP - 分布式分析执行（Distributed Execution）
3. ETL - 批处理执行（Batch Execution）

分布式查询中的算子可以有多个实例(Instance)并行执行，每个实例负责其中一部分数据。

在 F1 Query 里这样一个数据分片被称为**Fragment**,在 Spark SQL 里叫**Partition**，在 Presto 里叫**Split**。

下面的例子是一个 Join-Aggregation-Sort 的查询，它分成了 4 个阶段：

	1. Scan(Clicks) 被分配给 1000 个 F1 Worker 上并行拉取数据，并根据每一行数据的 Hash(AdID) 发送给对应的 HashJoin 分片，即一般说的 shuffle 过程;
	2. Scan(Ads) 被分配给 200 个 F1 Worker 上并行拉取数据，并且也以同样的方式做 shuffle；
	3. HashJoin 及 PartialAggregation：根据 Join Key 分成了 1000 个并行任务，各自做 Join 计算，并做一次聚合；
	4. 最后，F1 Server 把各个分片的聚合结果再汇总起来，返回给客户端。

Presto具有的缺陷，F1 Query 分布式查询同样也有，比如：

	- 纯内存的计算方式，无法利用磁盘的存储空间，某些查询可能面临内存不足；
	- 没有 Fault-tolerance，对于一个涉及上千台 Worker 的查询，任何一台的重启都会导致查询失败。


#### Apache Lens-PrestoDB-F1 Query



#### Spark DeltaLake - Hudi


### III.Compute Engine详细

3.1.内存SQL查询 

Ignite

3.2.实时数据处理计算

Spark&Flink

基于上下文查询分析 
针对Mac维度流式计算SparkStreaming

3.3.Spark&MPP Usage

Greenplum-Spark Connector

3.4.Elasticsearch查询引擎

3.5.SQL Engine查询计算引擎 

PrestoDB

3.6.数据挖掘计算模块封装

	Greenplum_MADlib机器学习
	SparkMLlib

3.7.各组件间技术整合开发落地

	Spark-Greenplum Connector
	ES-Spark整合
	Presto-ES Connector
	通用SQL解析执行引擎

Presto-ROLAP查询性能瓶颈+OLAP引擎整合

### IV.SQL Query Core Engine Thinking

CodeGen

常量折叠、函数变换、表达式转换、函数类型推断、常量推断、语义去重等功能, 以生成最优的执行计划。

#### 1.Calcite

- [查询优化器设计](2018-06-01-query-optimizer-design-note.md)

#### 2.Druid SQL Parser

- [Druid SQL Parser](https://github.com/alibaba/druid/wiki/SQL-Parser)

#### 3.PrestoDB代码详解

- [Presto分布式OLAP](2017-04-03-olap-distributed-presto-practice-note.md)

#### 4.Flink计算引擎

- [Stream计算与Flink](2018-05-31-bigdata-research-dataprocess-stream-compute.md)


### V.Deep Compute&SQL Engine Design

- SQL Standard
- Data Adapters
- Query Parser
- Query Optimizer
- Stream SQL Compute

#### 5.1.QueryEngine内核优化

*5.1.1.Query性能差异与执行顺序*

1) Scan Query
2) Aggregation Query
3) Join Query

*5.1.2.混合大数据查询*

离线与实时大数据处理与计算优化

Greenplum-MPP数据查询+海量HDFS数据查询

*5.1.3.通用SQL数据解析Calcite*

- [Calcite 数据引擎]()

*5.1.4.分布式查询QueryOptimizer*

通用统一SQLEngine设计-Federated Query 

	- 统一元数据结构体系
	- 支持对通用元数据的查询计算分析
	- 支持多种原数据类型的移动计算(部署不同类型Worker,针对不同类型数据)
	- 合并计算结果输出

研究PrestoDB架构源码


*5.1.5.特定全文检索Index设计*

- OLAP与全文检索的组合应用(封装Lucene的Antlr函数)
- SQL-OLAP不支持复杂数据类型(array、struct、map)查询,要求数据输入Schema必须是平铺的。
- ES/Druid可以理解为一种支持复杂数据类型的OLAP数据库


#### 5.2.数据计算优化

- 增量SQL查询算法
- 内存计算规则
- Flink实时流式数据计算
- 预计算的内存存放(内存计算结果保存)
- 查询语义分析设计(复杂计算设计)

    ANTLR开源语法分析器.[介绍](http://www.ibm.com/developerworks/cn/java/j-lo-antlr/) <br />
    自动构造自定义语言的识别器(recognizer),编译器(parser),和解释器(translator)的框架 <br />
    Lucene中的语义分析比较:JavaCC+jflex

- 影响OLAP性能的因素

#### 5.3.数据结构优化

- 内存数据结构设计优化

**Apache Arrow**是一个内存数据结构,支持在不同数据源之间做快速高效的数据交换。

	-定义一个通用而高效的内存数据格式,方便数据查询引擎进行查询
	-定义了从上述格式中载入数据的格式.任何支持这个格式的系统,都可方便,高效地输入或输出这种格式

- AliORC设计

#### 5.4.查询引擎详细设计

#### 5.4.1.计算引擎开发 Spark&Flink

Ignite与Spark整合

Greenplum-Spark Connector: https://greenplum-spark.docs.pivotal.io/140/index.html

Spark&SparkStreaming

#### 5.4.2.全文检索微服务设计

Elasticsearch整合应用 

Elasticsearch性能调优

ES-Hadoop: https://www.elastic.co/products/hadoop

ES-Spark整合

#### 5.4.3.OLAP通用查询引擎开发(核心)

通用SQL解析执行-Calcite

Presto-ROLAP查询引擎

	presto-elasticsearch connector
	presto&Ignite connector
	HDFS Connector
	Greenplum Connector
	ES Connector
	Ignite Connector
	Kafka Connector

语义分析组件开发

查询解析相关

查询优化相关

#### 5.4.4.内存技术应用落地 

Ignite分布式内存库应用分析

	1.Ignite应用设计
	
	2.分布式数据库缓存层-MyBatis
	
	3.Hadoop加速器

