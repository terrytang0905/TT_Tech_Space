---
layout: post
category : bigdata
tags : [bigdata,analytics,guide]
title: AliCloud MaxCompute Best Practice Note
---

## 阿里云MaxCompute-SaaS级智能数仓最佳实践
-------------------------------------------------------

#### MaxCompute最佳实践概述

#### 1.MaxCompute架构概述

#### 2.Data Modeling & Design-数据模型与设计

#### 3.MaxCompute 最佳实践&实操

#### 4.MaxCompute 生态与Functions

#### 5.云端大数据产品横向分析

[Google BigData&BigQuery](2019-05-01-bigdata-research-google-tech-solution.md)

**<u>Snowflake vs Redshift</u>**

Snowflake的核心产品能力: 完全存算分离/工作负载隔离/极致性能。但是随着Redshift RA3新集群的出现提供成本更低与更便捷的竞对产品方案,这一切是否会有改变？

Redshift RA3新集群开始全新支持计算与存储资源独立弹性伸缩。这从2013年AWS作为Game Changer,发布云端Redshift以来的第一次重大升级。Redshift产品本身基于ParAcell 数据库技术,它就是云平台之上的MPP数据库。总结上说,
Redshift是一个部署在云端的MPP数据库,能够处理TB级数据如同GB级,支持分析/管理数据,云原生,可在小时级内按需资源扩容,使用纯SQL,把这些能力放在一起,确实是个吸引人的创新产品。但是由于历史的局限,导致Redshift主要以On-Premise(本地部署)架构为主。不过随着云上数仓越发定制，发展迅速，存在2个较大缺陷, 1是存储与计算的耦合,2是扩展伸缩现有的困难性与破坏性。主要问题在于很多公司存储资源与计算资源存在错配, 例如数据存储较大,但不需要计算资源，或者需要大量机器计算的ETL任务, 但非固定的吞吐量弹性扩展。Redshift的share-nothing architecture事实上会共享部分资源。

**典型MPP数据库(Redshift)水平扩展的计算性能慢且是真正的管理员任务。这一定需要数据复制/数据重分布, 增长存储能力需要更多磁盘+更多的服务器, 这样意味着存储本是不再便宜**

Redshift最近以来新产品升级: Redshift Spectrum 2017上线/Redshift Elastic Resize 2018上线。Redshift RA3 Cluster新机型现在开始支持存算分离, 其整体费用逐步下降, 更加让客户可接受。

但是Snowflake依然有着很大的产品优势,在完全的存算分离,线性且秒级弹性伸缩,完全独立多租户数据处理等全新的技术。

- Scales Seamlessly within Seconds.
- Scales Linearly, Saves You Time
- Seamless Time-Travel
- Near-Realtime Pipeline (Snowpipe)
- Cluster isolation

**Snowflake vs Redshift详细对比内容**

1-惯例成本

Redshift最小消费$2.4/hour / Snowflake 消费$2.5/hour。产品费用接近。

2-Auto-Suspend and Auto-Resume能力: 

 Snowflake拥有最顺畅的自动挂起和自动恢复能力.如果设置*alter warehouse suspend*，当suspend, 将计算Cost恢复为0。如果你忘记suspend,  Snowflake会根据设置时间来自动挂起, 可以按照每个Cluster来独立设置。相比之下，Redshift RA3的暂停和恢复距离无缝连接的体验较大。例如1个空的xlplus 2-node cluster 需要花费1m30s开始且暂停需要5分钟。这是一个非常重要的可用性能力, 一个典型公司在夜晚释放资源，却无法自动恢复当用户要重新查询，因为需要更多的时间来挂起和恢复。这个能力上Snowflake完胜。

3-Scaling伸缩性

 对于MPP数据库来说, 另一个重要的Feature在于不间断的弹性伸缩。其用户案例非常明显:如果你在执行ETL,可能你需要一个巨大的集群,因为你在处理海量数据,但当这些数据使用完之后,只需要一个很小的集群来使用。Snowflake对于资源的释放是非常迅速且不间断的。你可能在当前查询的过程中, 当你scale up到一个更大的集群, 下一个查询SQL可以直接使用。当然你也可以在暂停的状态下重新调整你的集群规模,  以至于下一个查询可以按照新的集群规格来执行。另一个Scaling的模式是"多集群"的水平扩展, 将你的集群"自我复制"成多集群以适应更大的工作负载，这可以手工触发or自动触发。再次,Redshift RA3又是一个完全不同的故事。Scaling伸缩性离丝滑顺畅比较远,它需要使用Console or API访问才能实现, 其最接近的对比选项是弹性规格变更,只支持双倍扩展现有集群，而且还需要5 minutes。这个能力上Snowflake明显有优势。

4-工作负载隔离

AWS Redshift有个明显的缺陷在于工作负载隔离。分析师尝试有非常重的查询,则大多数时候这些查询都是针对特定策略下主动的即席ad-hoc查询。缺少优秀的工作负载资源管理(WLM)设置, 一次又一次, 我们看到这些分析查询SQL导致Redshift集群的halt挂起。WLM管理难度很大,无论你如何方式, 总会有遗漏。

Redshift RA3到现在为止还未解决这个问题, 分析与ETL工作负载仍然在同一计算资源池内共享资源。Snowflake拥有非常完备的工作资源隔离能力。用户随时可以衍生出很多新的集群，所有的集群都会被完全互相隔离开来。典型场景是,你可以分别单独创立 分析集群/ETL集群/Reporting集群 3个独立集群，而且可以讲计算资源独立设置，并跟踪其资源消耗情况。Snowflake再胜一城

5-自动化数据脱敏

数据安全对于每个公司来说都非常重要, 其中数据脱敏扮演重要的部分。你需要确定你使用高效访问控制方式来限制任何个人隐私数据。关于Redshift, 我总是用我自己的安全架构, 其配置通过一层的Views来驱动并实现数据脱敏。另外也可以通过付费插件方式来实现，例如 [DataSunrise](https://aws.amazon.com/blogs/big-data/protect-and-audit-pii-data-in-amazon-redshift-with-datasunrise-security/)。Snowflake的确做得更加简洁，用它的动态列脱敏 [dynamic data masking](https://docs.snowflake.com/en/user-guide/security-column-ddm-use.html)。

另外还有些比较暖心的设计，当然不能上升为技术评估决定的因素。例如**Timetravel**,Snowflake支持非常顺滑的时间旅行功能。

```
select from table at(timestamp => '2020-13-31 12:01');
```

Redshift支持表级别的数据恢复从之前的某个snapshot切片，不过这是个管理员级别的操作。而Snowflake以undrop table命令来恢复之前删除的表。自动化数据提取/外表加载 2个数据库都支持。

总结

  首先, 通过很长时间的磨练，Redshift终于向更优秀的架构来演进了。当我以为已经到达终点的时刻，它实际上还需继续向前进一步。Redshift RA3本身就是基于S3存储之上的云数仓服务，为什么暂停释放一个空集群需要5分钟？为什么在执行暂停操作前一定要创建一个snapshot? 虽然AWS Redshift已是一个很不错的产品，但是Snowflake可能是更好的分析数据仓库产品选择，能为DBA/开发人员提供更强大的能力。

#### 6.云上智能数仓发展

#### x.Ref

