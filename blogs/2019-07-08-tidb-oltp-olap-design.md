---
layout: post
category : cloud
tags : [bigdata, product, database]
title: Database Research Note - TiDB
---

## 数据库研究 - TiDB
--------------------------------------------------------

### HTAP数据库

Hybrid Transaction/Analytical Processing

### 分布式数据库TiDB是如何结合OLTP和OLAP的



**NewSQL 混合事务分析、MySQL 兼容、水平可扩展数据库的架构和用例。**

TiDB 是一款开源、云原生、MySQL 兼容的分布式数据库，可以处理混合事务和分析处理（HTAP）工作负载。它是“NEWSQL”关系数据库的一员，被设计为方便大规模部署。也许有人想知道，“Ti”代表了钛。

PingCAP 在三年半前才开始搭建 TiDB，但是这个产品已经拥有了 15000 次 GitHub 点赞，200 名贡献者，7200 次提交，2000 个分支以及 300 名生产用户。最近 TiDB 获得了 InfoWorld Bossie Award 2018 数据存储和分析领域最佳开源项目奖。

在这篇文章中，我将介绍 TiDB 设计的核心功能和架构，覆盖数据库的三个主要用例，并预览了 PingCAP 即将推出的多云 TiDB 即服务和 TiDB 学术版。

*TiDB 功能*

TiDB 的核心功能包括弹性的水平可扩展性，有 ACID 保证的分布式事务，高可用性以及实时交易数据额分析。让我们来看一下这些功能背后隐藏的平台架构。TiDB 平台有以下这些组件：

- TiDB：无状态 SQL 层，可以兼容 MySQL，用 Go 语言开发。
- TiKV：分布式事务键值存储，用 Rust 语言开发。（TiKV 最近成为了云原生计算基金会项目）
- TiSpark：Apache Spark 插件，连接到 TiKV 或者专门的柱状存储引擎（我们还在研究的部分，请持续关注）。
- Placement Driver（PD）：Etcd 提供的元数据集群，管理并调度 TiKV。

TiKV 是基础层。这是所有数据持久化的地方，自动分成小的块（我们称为“区域”），并通过执行 Raft 一致性协议自动复制并保持强一致。和 Placement Driver（PD）一起，TiKV 可以复制节点、数据中心和地理位置的数据。它还可以动态地去除形成的热点，并拆分或合并区域，以提升性能和存储使用率。我们在 TiKV 中实现了基于范围的切片，而不是基于哈希的切片，因为从一开始，我们的目标就是支持全功能的关系型数据库。因此 TiKV 也支持不同类型的扫描操作：表扫描、索引扫描等等。

TiDB 中的无状态 SQL 层用来负责所有的的在线交易处理（OLTP）工作和 80% 的常规在线分析处理（OLAP）。这样的设计提升了常规性能（参考我们最新的 TPC-H 基准测试 https://github.com/pingcap/docs/blob/master/benchmark/tpch-v2.md） ，这个无状态 SQL 层使用 TiKV 的分布式设计，通过协处理器层将部分查询下放到不同 TiKV 节点进行并行处理。

对于更复杂的 OLAP 工作，比如说训练机器学习模型的迭代分析或实时业务智能采集，是由第二个无状态 SQL 层 TiSpark 负责的，也是直接从 TiKV 获得数据。TiDB 兼容 MySQL，而 TiSpark 兼容 Spark SQL。

![](https://mmbiz.qpic.cn/mmbiz_jpg/ZBjVrHIdkOnrrfI9hxne4xsBEToRo28yvSnK7Yicfj8HMjH74sMfgibk34bvV98TZ1QG6CTEAM0K107D8pyzHMRw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

*TiDB 平台架构*

TiDB 架构

你可能已经注意到，整个 TiDB 平台是模块化的，所有的组件都有单独的代码库，并且是松耦合的。你可以将整个 TiDB 平台部署为一个完整的包（大多数用户都是这么做的）或是根据你的需要部署其中的一部分。这样的模块化的架构给用户提供了最大的灵活度，并符合云原生架构标准。根据 CNCF 的官方定义，云原生技术是“有弹性的、可管理的和可观察的松耦合系统”。

作为 TiDB 的用户，你可以扩展你的无状态 SQL 服务器或 TiSpark 层（也就是你的计算资源），或者是单独扩展 TiKV（也就是你的存储容量），允许你充分利用消耗的大部分资源，更好地满足你的工作负载。你几乎可以将 TiDB 无状态 SQL 服务认为是在 TiKV 之上的微服务，它是持久化数据的有状态应用程序。这个设计有利于隔离缺陷，更快地滚动升级和维护，而破坏性更小。

TiDB 这些优势的代价是额外的部署和监视复杂性，有更多需要追踪的部分。然而，随着 Kubernetes 的兴起以及 CoreOS 推动的 Operator 模式，部署和管理 TiDB 是简单、直接并且日益自动化的。开源的 TiDB Operator for Kubernetes（https://www.infoworld.com/article/3297700/kubernetes/introducing-the-kubernetes-operator-for-tidb.html） 可以帮助你在任何云环境下（公有、私有或混合）部署、扩展、升级和维护 TiDB。TiDB 默认安装 Prometheus 和 Grafana，所以可以立即进行监视。（查看我们的 TiDB Operator 教程 https://www.infoworld.com/article/3297700/kubernetes/introducing-the-kubernetes-operator-for-tidb.html）

灵活的技术资产扩展性是业务成功与否的最终关键。这就是你会成为下一个 Facebook 还是下一个 Friendster 的区别。TiDB 模块化和 Kubernetes 的加入可以给你的数据库服务带来灵活的扩展性。

*TiDB 主要用例*

最后，让我们来看一下 TiDB 的三个主要用例：MySQL 扩展性、HTAP 实时分析和统一数据存储。

![](https://mmbiz.qpic.cn/mmbiz_jpg/ZBjVrHIdkOnrrfI9hxne4xsBEToRo28ybBiaS2Rue4pN8xalpak1WNHaADsWPsSnZ3GXzM1cqib6FIqV0fLOmuuA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

示例 Grafana 仪表板监视 TiDB 部署

* TiDB 用例：MySQL 扩展性

由于 TiDB 兼容 MySQL，它同时兼容 MySQL 连接协议和 MySQL 生态系统工具，比如 MyDumper 和 MyLoader，对于 MySQL 用户来说，这是解决问题的自然选择。我们需要清楚，TiDB 并非要取代 MySQL，相反，它是 MySQL 的补充。MySQL 仍然是很好的单实例数据库选择，所以如果你的数据大小或工作负载不大，那请继续使用 MySQL。但如果你还在头疼这些问题：

- 考虑如何复制、迁移或扩展数据库得到更多容量
- 寻找优化现有存储容量的方法
- 查询性能慢
- 研究中间件扩展解决方案或实施手动分片策略

那么请开始考虑使用像 TiDB 这样的分布式 SQL 数据库吧，它可以帮你解决你关心的所有问题。MySQL 分片的缺陷让世界最大的单车共享平台之一 Mobike 选择使用 TiDB（阅读 Mobike 案例 https://www.pingcap.com/success-stories/tidb-in-mobike/） 。Mobike 在 200 个城市拥有 9 百万单车，服务于 2 亿名用户，因此不难想象团队使用 MySQL 时候会遇到的扩展瓶颈。Mobike 通过在 MySQL 之外部署 TiDB，以及 PingCAP 的企业级工具套件，包括可以自动将 MySQL 主机和 TiDB 集群同步的 Syncer，解决了弹性扩展需求。

TiDB 和其他 MySQL 兼容数据库之间最主要的区别在于 TiDB 的分布式架构。MySQL 技术已经存在了 23 年了，它从来没有打算涉足于分布式领域。比如说，不像 TiDB，MySQL 不能产生查询计划，将部分查询下放到多台机器中同时进行并行处理。TiDB 的 SQL 解析器、基于成本的优化器和协处理器层从头开始构建的，利用了分布式数据库的计算资源和并行性，因此 MySQL 用户可以从中获得更多功能。

* TiDB 用例：HTAP 实时分析

HTAP（混合事务和分析处理）是 Gartner 在 2014 年提出的一个术语，描述打破事务和分析数据工作之间隔阂的数据库架构。目标是给企业实时分析，这样就可以作出实时决策。其他行业分析公司有描述这个架构的专门术语：451 Research 的 HOAP（混合操作分析处理），Forrester 的 Translytical 以及 IDC 的 ATP（分析事务处理）。

正如我们讨论的，TiDB 通过解耦计算层和存储层，并使用不同的无状态 SQL 引擎（TiDB 和 TiSpark）来做不同的分析任务，打破了 OLTP 和 OLAP 之间的隔阂。这两个引擎都连接到同一个持久数据存储（TiKV），让系统自然拥有实时分析和决策的能力。复杂的 ETL 过程被简单化，”t+1”延迟不复存在，TiDB 中存储的数据可以更有创造力地进行使用。

服务于 5 百万用户的大型生鲜产品运送平台 Yiguo.com 在 TiDB 之上运行 Apache Spark（阅读 Yiguo.com 案例 https://www.datanami.com/2018/02/22/hybrid-database-capturing-perishable-insights-yiguo/） 来加速复杂的查询。通过从 SQL Server 升级其基础设施，并通过部署 TiDB 到其现有的 MySQL，Yiguo.com 可以高性能地在中国最大的在线购物节双 11 运行复杂的连接运算，进行实时决策。

* TiDB 用例：统一数据存储

分布式、模块化、HTAP 数据库 TiDB 被设计为可以水平地扩展计算和存储容量，灵活地适应不同的工作负载，同时还是“唯一可信来源”。通过在键值存储之上提供可扩展的 SQL 服务，TiDB 旨在动态地降低基础设施栈中维护数据管理层的人力和技术成本。

对于世界上最大的食物配送平台之一 Ele.me 来说，想要统一数据存储是采用 TiDB 和 TiKV 的关键原因之一（阅读 Ele.me 的案例 https://www.pingcap.com/success-stories/tidb-in-eleme/） 。之前，Ele.me 的数据分散在不同的数据库中，包括 MongoDB、MySQL、Cassandra 和 Redis。最终，这个临时堆栈不再可用，因为操作和维护成本不断增加。现在 Ele.me 2 亿 6 千万用户的 80% 操作在单个 TiKV 部署下服务。这个 TiKV 集群跨越了 4 个数据中心，每个都有 100 多个节点，存储了十几个 TB 的数据，这些数据总是存在，一直可用。

多云 TiDB 即服务和 TiDB Academy

自 PingCAP 开始搭建 TiDB 已经超过了 3 年，该数据库在各种情况下都进行了测试。现在，超过 300 家公司都在使用 TiDB 满足他们的 OLTP/OLAP、数据库扩展性、实时分析和统一存储的需求。然而，TiDB 的路线图上还有许多目标。

其中一个是全面管理的多云 TiDB 即服务，可以在各种云设置下使用，包括公有、私有和混合。PingCAP 正在开发企业级、全托管、基于 Kubernetes 的 TiDB，并将在今年年底发布第一个版本。如果你想要更早地使用，请在这里注册。

PingCAP 开发的另一个项目是 TiDB Academy，这是自己制定进度的实践课程，帮助数据库管理员、devops 以及系统架构师理解 TiDB 的架构、设计选择、长处和短板。第一个课程“给 MySQL DBA 的分布式数据库 TiDB”正在招生。你可以在这里注册（https://pingcap.com/tidb-cloud/）。





