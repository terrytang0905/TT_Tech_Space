---
layout: post
category : datascience
tags : [bigdata, framework, develop]
title: SQL Optimizer Design Note
---

## 查询优化器设计研究
-------------------------------------------

### Apache Calcite数据框架

### 数据库查询优化器分析

1._SQLite优化器_

		使用Nested嵌套联接
		[N最近邻居](https://www.sqlite.org/queryplanner-ng.html) 贪婪算法

	2._DB2优化器_

		使用所有可用的统计，包括线段树(frequent-value)和分位数统计(quantile statistics)。
		使用所有查询重写规则(含物化查询表路由，materialized query table routing),除了在极少情况下适用的计算密集型规则。
		使用动态编程模拟联接
			有限使用组合内关系（composite inner relation）
			对于涉及查找表的星型模式，有限使用笛卡尔乘积
		考虑宽泛的访问方式，含列表预取(list prefetch,注:我们将讨论什么是列表预取),index ANDing(注:一种对索引的特殊操作),和物化查询表路由。
		默认的，DB2 对联接排列使用受启发式限制的动态编程算法。

	默认的，DB2 对联接排列使用受启发式限制的动态编程算法。	

	3._Genetic Query Optimizer - PostgerSQL_

[geqo_postgreSQL](https://www.postgresql.org/docs/current/static/geqo-intro.html)

	The normal PostgreSQL query optimizer performs a near-exhaustive search over the space of alternative strategies. It can take an enormous amount of time and memory space when the number of joins in the query grows large. This makes the ordinary PostgreSQL query optimizer inappropriate for queries that join a large number of tables.

	genetic algorithm(GA) & GEQO 

### 大数据查询优化器

_GPORCA(Pivotal Query Optimizer) - Greenplum/HWQA_

![PQC-OrcaArch](_includes/Orca_arch.png)

The Pivotal Query Optimizer leverages a multi-core scheduler that can distribute individual optimization tasks across multiple cores to speed up the optimization process.

GPORCA also enhances Greenplum Database query performance tuning in the following areas:

	- Dynamic Partition Elimination(Queries against partitioned tables)
	- SubQuery Unnesting(Queries that contain subqueries)
		* Removing Unnecessary Nesting
		* Subquery Decorrelation
		* Conversion of Subqueries into Joins
	- Common Table Expressions(CTE-Queries that contain a common table expression)

GPORCA also includes these optimization enhancements:

	- Improved join ordering
	- Join-Aggregate reordering
	- Sort order optimization
	- Data skew estimates included in query optimization

- [PQO_Doc](https://content.pivotal.io/blog/greenplum-database-adds-the-pivotal-query-optimizer)

_Legacy Query Optimizer - Greenplum/PostgreSQL_

	Append-only Columnar Scan

### SparkSQL Catalyst优化器

![SparkCatalyst](_includes/spark_sql_catalyst.jpg)

Catalyst这部分代码完成的是从SQL到Optimized Logical Plan，后面的Physical Planning则位于｀sql/core｀下面。大概有这么几个组件需要展开细看：ParserAnalyzer(with Catalog)Optimizer和Catalyst具有类似功能的是Apache Calcite，像Hive, Phoenix都有在用Calcite，折腾完Catalyst，可以去看一看两者的异同。如果要快速理解Catalyst，我建议从 @连城 的项目 [liancheng/spear](https://link.zhihu.com/?target=https%3A//github.com/liancheng/spear) 入手，完整地阅读一遍，相信会有很多收获。



### Hive SQL Optimizer


