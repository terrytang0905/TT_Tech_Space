---
layout: post
category : bigdata
tags : [bigdata,olap,architect]
title: Big Data Analytics Note - BigData Compute Engine Code Design
---

## 大数据查询分析-分布式查询计算引擎Code设计
-----------------------------------------------------------

### I.需求分析与设计

_1.核心Features设计_

	1.数据湖多数据源整合建模
	2.元数据模型抽象动态支持业务模型
	5.OLAP联合查询与边缘计算
	6.离线与实时大数据处理与计算优化

- [分布式交互式查询](2017-04-04-olap-sqlonhadoop-research-note.md)

- [通用OLAP查询引擎设计](2017-02-01-bigdata-analytics-olap-query-engine-design-note.md)

- [查询优化器设计](2018-06-01-sql-optimizer-design-note.md)

#### II.Federated Query - Data Lake Analytics

使用标准SQL即可分析与集成对象存储、数据库(PostgreSQL/MySQL等)、NoSQL(TableStore等)数据源的数据

F1 Query=用一套系统解决所有 OLTP、OLAP、ETL需求.用一套系统访问数据中心里各种格式的数据

1. OLTP - 单机执行（Centralized Execution）
2. OLAP - 分布式执行（Distributed Execution）
3. ETL - 批处理执行（Batch Execution）

分布式查询中的算子可以有多个实例（Instance）并行执行，每个实例负责其中一部分数据。在 F1 Query 里这样一个数据分片被称为 Fragment，在 Spark SQL 里叫 Partition，在 Presto 里叫 Split。

下面的例子是一个 Join-Aggregation-Sort 的查询，它分成了 4 个阶段：

	1. Scan(Clicks) 被分配给 1000 个 F1 Worker 上并行拉取数据，并根据每一行数据的 Hash(AdID) 发送给对应的 HashJoin 分片，即一般说的 shuffle 过程;
	2. Scan(Ads) 被分配给 200 个 F1 Worker 上并行拉取数据，并且也以同样的方式做 shuffle；
	3. HashJoin 及 PartialAggregation：根据 Join Key 分成了 1000 个并行任务，各自做 Join 计算，并做一次聚合；
	4. 最后，F1 Server 把各个分片的聚合结果再汇总起来，返回给客户端。

Presto 具有的缺陷，F1 Query 分布式查询同样也有，比如：

	- 纯内存的计算方式，无法利用磁盘的存储空间，某些查询可能面临内存不足；
	- 没有 Fault-tolerance，对于一个涉及上千台 Worker 的查询，任何一台的重启都会导致查询失败。

#### III.SQL Engine Design

#### Calcite



#### IV.Stream SQL in Flink

增量SQL查询则意味着我们可以只依赖源数据的改变量，局部地执行查询并更新原来的结果。使用增量模型， 我们往往可以得到更快的执行方案。很显然，Stream SQL 执行就是增量SQL查询：新到达的数据就是在一张“源数据表” 当中新加入的数据项。

		Stream SQL是物化视图维护问题的一个子问题。

- SQL优化与执行规划
- 物化视图增量维护的简单算法
- 查询放大问题及其解决思路
- 修改放大问题及其解决思路
- 可自我维护性(Self-maintainability)

#### V.PrestoDB代码详解

跨数据源整合查询

- [Presto-OLAP引擎](2017-04-03-olap-distributed-presto-practice-note.md)

#### VI.Spark Query

