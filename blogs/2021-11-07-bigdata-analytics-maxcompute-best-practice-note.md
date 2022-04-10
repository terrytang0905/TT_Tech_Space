---
layout: post
category : bigdata
tags : [bigdata,analytics,guide]
title: AliCloud MaxCompute Best Practice Note
---

## 阿里云MaxCompute-SaaS级智能数仓最佳实践
-------------------------------------------------------

#### 1.MaxCompute架构概述

“新一代计算引擎”的底层技术主要有三个：MaxCompute(离线计算)、Hologres(交互式分析)、Flink(实时计算)、PAI(人工智能)。在它们之上，是用来统一调度各个技术模块的操作系统：DataWorks。

MaxCompute主要服务于批量结构化数据的存储和计算,可以提供海量数据仓库的离线计算解决方案以及针对大数据的分析建模服务。


#### 1.1.MaxCompute特点

    - 大规模计算存储(海量离线计算)
    MaxCompute 适用于 100GB 以上规模的存储及计算需求，最大可达 EB 级别。
    - 多种计算模型 - NewSQL
    MaxCompute 支持 SQL、MapReduce、Graph 等计算类型及 MPI 迭代类算法。
    - 强数据安全
    MaxCompute已稳定支撑阿里全部离线分析业务7年以上，提供多层沙箱防护及监控。
    - 低成本
    与企业自建私有云相比，MaxCompute的计算存储更高效，可以降低20%-30%的采购成本。
    - AliORC文件格式


_MaxComputer技术栈_

![MaxCompute技术栈](/Users/zhenjie.tzj/Documents/!BigDataResearch/TT_Tech_Space/blogs/_includes/maxcomputer_tech.png)

#### 3.2.MaxCompute查询计算

![MaxCompute_lightning逻辑架构](/Users/zhenjie.tzj/Documents/!BigDataResearch/TT_Tech_Space/blogs/_includes/maxcompute_lightning.png)


_MaxCompute联合计算引擎平台_

_MaxCompute SQL Parser & SQL Optimizer_

	- 基于Volcano火山模型的CBO
	- Vectorized Execution Engine in MaxCompute 2.0
	- 优化规则
	- RBO&CBO&HBO模型

在编译器方面,基于AST的编译器模型,Visitor模型（Antlrv4），IDE IntelliSense，Warning支持完整的存储过程，LOOP/IFELSE判断等；

在优化器方面，CBO基于代价的优化器，Volcano模型，展开各种可能等价的执行计划，然后依赖统计信息，计算这些等价执行计划的“代价”，最后最低的执行计划

CBO代价模型

• 由CPU、IO、Row Count、Memory、Network组成的五元 组
• 每个operator关注于自身的Cost，整个plan的Cost由 引擎累积等到
• Cost model力求能够反映客观的物理实现
• Cost model不需要得到和真实一模一样，只需要能够选出较优的plan

主要包括类型：RBO/CBO/HBO

RBO是基于规则的优化器，在早期的MaxCompute中使用，是一种过时的优化器框架，它只认规则，对数据不敏感。优化是局部贪婪，容易陷入局部优化但全局差的场景，容易受应用规则的顺序而生产迥异的执行计划，往往结果不是最优的。

CBO是基于代价的优化器，它实际上是Volcano模型，可以展开各种可能等价的执行计划，然后依赖数据的统计信息，计算这些等价执行计划的代价，最后从中选用Cost最低的执行计划。

分布式场景的优化有别于单机优化。上图是在两张表上进行Join操作的简单案例，假设表T1已经按照a，b进行了分区；表T2按照a进行了分区。如果在单机系统中，分区问题不会出现；在分布式系统中，因为分区的出现可能会产生两个不同的执行计划：第一个执行计划是将T1按照a进行重新分区，之后再和T2进行Join；另一种执行计划是假设T1很大，而T2相对没那么大，此时不对T1重新进行分区，而是将T2数据广播给T1的每个分区。两种执行计划在不同的环境各具优势。

HBO:在大流量、高并发场景中，每天都需要处理大量相似的查询，这就给优化器带来了巨大机会。HBO优化器是基于历史优化的优化器，对每天提交的查询进行聚类，把以前运行数据作为Hint来帮助未来的相似的查询上。

在运行时方面，利用LLVM技术，在运行时生成较优的机器码，采用列式执行框架，提高CPU流水线的执行效率，并提高缓存命中率，使用SIMD。


_MaxCompute on Pangu(内部存储) + MaxCompute on OSS(外部存储) => Data Lake Analytics_

基于Datalake的技术，把不同的数据源用类似的方式存储，用统一的方法计算。是同一SQL查询引擎.


#### 3.3.数据架构设计

![MaxCompute架构](/Users/zhenjie.tzj/Documents/!BigDataResearch/TT_Tech_Space/blogs/_includes/maxcompute_arch.png)

#### A.核心计算引擎

#### B.数据存储结构

#### C.MaxCompute数据存储

AliORC/支持嵌套树型数据结构

![MaxCompute数据格式支持](/Users/zhenjie.tzj/Documents/!BigDataResearch/TT_Tech_Space/blogs/_includes/maxcompute_datasource.png)

#### D.MaxCompute数据安全

#### Ref

-[MaxCompute2018]

	- 超大规模的大数据计算服务
	- 通过计算下推来实现的*联合计算*
		如何实现联动多个存储和计算系统?
		如何实现最终的数据统一计算?
		联合计算的计算性能提升到底有多少?
	- Auto Data Warehouse数据自动驾驶
	- 面向企业的完整服务,跨集群数据容灾与调度系统(金融行业)
	- 新查询语言叫做NewSQL，它是阿里巴巴定义的一套新的大数据语言，这套语言兼容传统SQL特性，同时又提供imperative与declarative优势。

-[MaxCompute Ref](https://yq.aliyun.com/articles/78108)
-[MaxCompute 2.0](https://yq.aliyun.com/articles/656158?spm=a2c4e.11153940.blogcont78108.63.4f88123cEqWDsN)

	Comments:
	1.多个数据仓库产品功能重叠(HybridDB / AnalyticDB / PolarDB / MaxCompute / OceanBase)
	2.缺少全球化的TechWriter,以支持非中国区客户
	3.MaxCompute从大数据技术工具整合阿里数据提供深度数据模型分析服务。数据+技术=数据价值商业呈现(数据变现思考)
	4.超大规模的大数据计算服务(多租户体系)的核心应用场景在哪里?除了阿里和城市大脑。独立的大数据计算平台是不是更适合企业?
	5.MaxCompute面对企业客户如何设置ROI(低成本是如何定义的),如何合理定价来确保MaxCompute成本与收益?
	6.2019年MaxCompute面对的最大问题与挑战是什么? 如何面向国际化?
	7.如何规划与实现MaxCompute的生态圈与合作伙伴?
	8.MaxCompute与Spanner的差距到底在哪里?
	9.华为FusionInsight方案为什么在外媒眼中更加受欢迎?

#### 2.Data Modeling & Design-数据模型与设计

#### 3.MaxCompute 最佳实践&实操 

#### 4.MaxCompute 生态与Functions

#### 5.云上智能数仓发展

MaxCompute技术趋势

_1.新硬件的发展_

计算层面越来越与新硬件的创新紧密结合，硬件会带来平台革命。例如芯片类的CPU(AVX、SIMD)、ARM众核架构、GPU，FPGA，ASIC，存储类的NVM、SSD、SRM，网络类的智能网卡和RDMA等新硬件的发展，新硬件与软件的配合是值得关注的发展方向。

	Comments:硬件提升大数据计算性能提升

_2.非关系型计算领域(图计算)有很多机会_

大数据现在还是在关系型的处理层面，包括流和批都是基于关系型数据的计算，事实上，现在非关系的计算越来越流行了，包括知识图谱、画像等越来越有价值，这些数据组织不是关系型表达，而是以点边的形式用图的方式表达，更符合物理抽象，比如人和货的关系，在风控层面，知识图谱层面，用来描述物理实体的关系更合适。

明年初将会推出MaxCompute的图计算系统MaxGraph，支持图存储、查询、模式匹配和GraphEmbedding等机器学习运算。

	Comments:基于MaxGraph的知识图谱+用户画像模型设计.这些能力应用在哪里?
			 GraphCompute依托于MaxGraph的图数据库

_3.非结构化数据将变成大数据的主流_

越来越多的短视频、图片、语音类数据，并随着IoT的发展，可能占据80%的数据量，由于这类数据的特性在于结构各不相同，且数据非常大但是单位价值不高（相比传统结构化数据），如何快速高效的解析和处理非结构化数据，是计算平台的关键挑战。

去年的时候MaxCompute发布了一个非结构化数据处理模块，能够用户自定义的方式处理包括视频音频在内的数据。

	Comments:对非结构化数据处理(视频/音频)的意义在哪里? 视频/音频等内容数据的监测分析,用户的视频镜头偏好
			 针对非结构化数据的向量解析

_4.AI for Everything(also for BigData)_

DBA或将被淘汰？

大数据的特点是大，不仅仅是包括数据的处理规模，还包括了整个的海量数据的管理和优化。传统数据库领域依靠DBA人力去管理的模式将不再适用。

用AI优化数据分布、数据管理、做计算优化和成本优化(例如自动SubQuery合并,智能索引建立等)。“让大数据无人驾驶”，这也是未来的趋势。

	Comments:AI对大数据的影响与互补如何具体落地? 大数据+AI协同工作



#### x.Ref

