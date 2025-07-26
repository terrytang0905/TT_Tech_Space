---
layout: post
category : bigdata
tags : [bigdata, framework, design]
title: BigDataDesign - Data Platform Arch Planning Note
---

## 大数据设计-数据平台架构规划落地
---------------------------------------------------

### 1.数据平台架构设计

基础架构

数据中台 

    - 计算与分析服务
    - DataLake&数据仓库

业务中台

业务前台

### 2.数据平台技术规划落地

数据采集与接入 - pc端/移动端加码+多数据源对接

数据脱敏与数据管理 - 数据资产与数据建模

数据标签仓库 - 用户标签

数据分析与数据挖掘 - 定制挖掘与机器学习

数据中台与系统搭建 - DMP-CDP-CRM平台

OLAP与数据可视化解决方案

大数据测评BigBench

#### 核心技术模块

分布式文件存储系统/K8s

分布式任务调度

数据管理与存储服务-多种数据库组合

数据计算/信息整合/机器学习/知识图谱

第三方应用整合服务

数据跨类搜索

#### 数据平台详细架构设计

数据接入/数据采集

数据预处理(清理与转换)-ETL/Kettle

	特征向量是什么? 例如TD-IDF中词频与权重
	数据降维:主成分分析和变量聚类 

为什么精准的数据样本非常重要? 好的食材是炒出好菜最基础也是最关键的一步
因此数据采集与数据清洗尤为重要

数据仓库设计-针对数据指标

	原始数据
	数据仓库数据
	应用聚合数据
	维度数据

分布式数据存储的选择


#### 数据平台技术选型

*  文件存储：Hadoop HDFS、Tachyon、GFS
*  PAAS: Kubernetes
*  资源管理：YARN、Mesos
*  离线计算：Hadoop MapReduce、Spark
*  流式、实时计算：Storm、Spark Streaming、Flink
*  K-V、NOSQL数据库：HBase、Redis、MongoDB、Cassandra
*  消息系统：Kafka、StormMQ、ZeroMQ、RabbitMQ
*  分析型数据仓库: Greenplum,Vertica
*  OLAP查询分析：Impala、Presto、Phoenix、SparkSQL、Drill、Kylin、Druid
*  分布式协调服务：Zookeeper,etcd
*  集群管理与监控：Ambari、Ganglia、Nagios、Cloudera Manager
*  数据挖掘、机器学习：Spark MLLib, PyTorch, Tenseflow
*  日志收集：Flume、Scribe、Logstash、Kibana
*  数据同步：Sqoop,DataX
*  任务调度：Oozie,Azkaban

HDFS/GFS

Greenplum/ElasticSearch/HBase/Redis/PostgreSQL

Spark/SparkMLlib/Flink

OLAP/SQLEngine/Federated Query/Data Lake Analytics

DMP&CDP->DataMart

DataProduct

### 3.数据平台核心目标

DataLake:数据管理与数据安全

数据能力平台输出

	1.数据安全规范
	2.标准数据能力字典
	3.标准用户特征标签列表
	4.基础内容数据库建设
	5.数据内容自动识别分类
	6.多数据源ID归一

数据挖掘与整合-数据资产转化

人工智能与知识图谱

#### 平台特征差异

* 运营商数据平台资源

* BATJ/头部媒体数据资源

* 网络视频数据资源

* 数据整合平台DMP/CDP/DataLake

#### 大数据变现

ROI模型(投入产出比)

业务效率提升

数据交易

产品数据集市


### 4.数据平台KPI考核

* 数据KPI考核核心

	- 数据源多样性(数量&质量)
	- 数据处理效率提升
	- 有效数据能力落地

* 数据KPI量化分析

	- 成本与营收

* 案例分析

第一方数据-公司自有

	- 交易数据
	- 用户行为数据

第三方数据合作

### 5.数据平台风险与瓶颈

#### 数据安全与隐私保护

1.数据采集端敏感数据匿名化
2.现有数据仓库字段加密处理
3.用户端隐私声明文档
4.上游数据源相关免责条款
5.外采数据需要和相关数据认证机构合作

### 6.数据平台与物联网的应用

边缘计算

### 7.数据平台未来十年

未来将是属于**基于云计算的数据平台**
