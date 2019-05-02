---
layout: post
category : bigdata
tags : [bigdata, framework, develop]
title: Big Data Research Note - Google Database Group
---

## 大数据研究-Google大数据解决方案
---------------------------------------------------

### Google大数据

#### BigTable - HBase - Dynamo


#### Dremel - OLAP

Dremel多层次查询树架构

#### F1 Query - OLTP/OLAP/ETL

#### Spanner - Cosmos - MaxCompute

Spanner有一种负责专门管理数据的spanserver，spanserver也是基于bigtable的tablet结构


#### 核心数据模型比较


Bigtable的Key-Value数据结构

Dremel嵌套列数据模型

Spanner数据目录结构 - 虚拟桶




#### Ref

- [分布式数据架构](2017-01-22-bigdata-research-database-architect.md)
- [Bigtable: A Distributed Storage System for Structured Data]
- [Dynamo: Amazon’s Highly Available Key-value Store]
- [Dremel: Interactive Analysis of Web-Scale Datasets]
- [F1: A Distributed SQL Database That Scales]
- [Online, Asynchronous Schema Change in F1]
- [F1 Query: Declarative Querying at Scale]
- [Spanner: Google’s Globally-Distributed Database]
- [Spanner: Becoming a SQL System]
- [GOOGLE分布式数据库技术演进研究--从Bigtable、Dremel到Spanner](https://blog.csdn.net/x802796/article/details/18802733)


