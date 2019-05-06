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

#### III.SQL Engine Thinking

常量折叠、函数变换、表达式转换、函数类型推断、常量推断、语义去重等功能, 以生成最优的执行计划。

#### 1.Calcite

#### 2.Druid SQL Parser

- [Druid SQL Parser](https://github.com/alibaba/druid/wiki/SQL-Parser)

#### 3.PrestoDB代码详解

跨数据源整合查询

- [Presto-OLAP引擎](2017-04-03-olap-distributed-presto-practice-note.md)

#### 4.Stream SQL in Flink

Flink 实现了流式处理和批量处理，并在这基础上进一步提供了 Table API 和 SQL 的支持。 其 Table API 和 SQL 基本上实现了之前提到的物化视图增量更新算法。特别地，Flink 还使用了 Apache Calcite 提供的 SQL 解析和优化模块来执行相关任务。

_增量SQL查询算法_

增量SQL查询则意味着我们可以只依赖源数据的改变量，局部地执行查询并更新原来的结果。使用增量模型， 我们往往可以得到更快的执行方案。很显然，Stream SQL 执行就是增量SQL查询：新到达的数据就是在一张“源数据表” 当中新加入的数据项。

	Stream SQL是物化视图维护问题的一个子问题。

_SQL优化与执行规划_

_物化视图增量维护的简单算法(代数算法)_

	对物化视图进行增量维护的最简单算法就是从根算子开始，将其左右两颗子树作为整体看作“似表(Table-Like)”。
	在增量 SQL 查询中，当一个表的内容改变， 我们希望这些表将内容的修改表示成包含增加的行和减少的行的增量表(Delta Table)的形式
	α(T+ΔT)=α(T)+Q(T,ΔT)。 这里 α 代表一个算子，T 是基表，ΔT 是增量表，Q 是一个以 T 和 ΔT 为参数的查询

_查询放大问题及其解决思路_

	1.确保处理过程当中的行唯一性
	2.使得算子保存额外的内部状态
	3.使用近似计算-HyperLogLog
	4.限制或扩充语义

_修改放大问题及其解决思路(最为复杂)_

	1.延迟刷新
	2.限制/扩充语义

_可自我维护性(Self-maintainability)_

_物化视图维护算法增量地执行SQL_

分布式系统中的流式计算

	1.绝对时钟(Absolute Clock)问题-使用事件驱动(Event-Driven)模型来处理
	2.时间倾斜(Time Skew)问题:用水印(Watermark)来处理。水印就是根据消息的事件时间来决定一条消息应该被处理还是被丢弃的标记
	3.在实现严格单次发送(Exactly-Once Delivery)的系统中， 正确管理水印对于防止移除之后仍可能被查询到的条目非常重要

_激发器、水印、窗口和句点_

对于激发器、水印、窗口和句点这些概念，十分建议进一步阅读如下文章和论文:

- Stream 101: The world beyond batch
- Stream 102: The world beyond batch
- The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing

_Stream Join 的语义_

	1.Stream 与纯静态表 Join。这里的纯静态表的内容不会改变，因此 Join 的实现只是在 Stream 端对每个消息在静态表内进行查询
	2.Stream 与动态表的快照 Join。动态表的内容可能会出现增删改等情况，这里的 Join 的语义是， 当对流当中的某个消息实施 Join ，相当于查询了动态表在那一时刻的快照
	3.Stream 与 Stream Join，操作的两边都是 Stream，这种情况最为复杂也很难实现，在之后将会进一步介绍


#### IV.Deep SQL Engine Design


