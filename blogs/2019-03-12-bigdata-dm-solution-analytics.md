---
layout: post
category : bigdata
tags : [bigdata, database, analytics]
title: Database Research Note - Database Management for Analytics
---

## 大数据分析平台应用日志
--------------------------------------------------------

分析型数据平台研究主要是研究当前业内主流基于数据分析的大数据平台,整合MPP与Hadoop特性,来解决海量数据的分析查询性能问题。

#### Google BigQuery

基于Dremel的GoogleBigQuery

- Concept: distributed search engine design
- Dremel provides a high-level, SQL-like language to express ad hoc queries without translating them into MR job.
- Dremel uses a column-striped storage representation, which enables it to read less data from secondary storage and reduce CPU cost due to cheaper compression


1.A high-performance storage layer is critical for in situ data management.
2.Columnar storage proved successful for flat relational data but making it work for Google required adapting it to a nested data model.

Ref:

- [SQLonHadoop研究Note-Dremel](2017-04-04-olap-sqlonhadoop-research-note.md)
- [BigQuery](https://cloud.google.com/bigquery/)

#### Huawei FusionInsight

FusionInsight大数据平台通过统一的SQL引擎将Hadoop，流式计算和关系型MPP数据库融合到单一环境中。它可以部署在本地，华为公共云或合作伙伴的公共云环境中。 Hadoop开源内核的扩展已经在Apache CarbonData分布式存储引擎中进行，HiGraph用于图形处理，调度和编排以及Elk交互式查询语言。还提供了关系引擎和Hadoop之间的紧密集成。

提到大数据平台，就不得不提Hadoop。Hadoop有三大基因：第一，Hadoop需要share nothing的架构，所以它可以scale-out。第二，它是一个计算存储解耦的架构，好处是计算引擎可以多样化。举个例子，批处理有Hive，交互查询有Spark，机器学习还可以有后面的tensor flow这些深度学习的框架。第三，Hadoop是近数据计算的。因为大数据平台是一个数据密集的计算场景，在这种非场景下，IO会是个瓶颈，所以把计算移动到数据所在地会提升计算的性能。

网络技术的发展是推动大数据平台发展的一个关键因素。2012年以前是一个互联网的时代，这个时期互联网公司和电信运营商，掌握着海量的数据，所以他们开始利用Hadoop平台来进行大数据的处理。那时候程序员自己写程序跑在Hadoop平台上来解决应用问题。2012年以后移动互联网的迅猛发展，这使得服务行业率先数字化。例如在金融行业，手机App让用户可以随时随地查询、转账，此时银行开始面临海量数据和高并发的冲击，就需要一个大数据平台来解决这个问题。这也就是为什么华为在2013年面向行业市场推出大数据平台产品FusionInsight。接下来物联网的发展会让更多的实体行业数字化，数据的特征更多是半结构化和非结构化，AI等更多新的搜索技术将能够帮助我们轻松地使用大数据平台。

华为FusionInsight大数据平台是集 Hadoop 生态发行版、大规模并行处理数据库、大数据云服务于一体的融合数据处理与服务平台，拥有端到端全生命周期的解决方案能力。除了提供包括批处理、内存计算、流计算和MPPDB在内的全方位数据处理能力外，还提供数据分析挖掘平台、数据服务平台，帮助用户实现从数据到知识，从知识到智慧的转换，进而帮助用户从海量数据中挖掘数据价值。

此外华为FusionInsight大数据平台是根据行业客户需求进行优化的解决方案。为解决用户在具体场景下的问题，提供许多创新的技术能力，举几个例子：

第一个是统一SQL。大数据技术中有很多能够利用SQL语言进行数据处理的组件，比如Hive、SparkSQL、Elk、MPPDB等，当用户对于这些组件进行业务开发时，需要对不同组件分别进行，造成很大的不便。FusionInsight提供统一SQL，对外业务界面只出现一个SQL开发管理界面，通过统一SQL的业务分发层进行业务分发，这样就简化了业务开发。同时，华为还提供了SQL on Hadoop引擎Elk，这个引擎完全兼容SQL 2003标准，无需修改测试脚本就可以通过TPC-DS测试，性能超过开源产品3倍。通过使用统一SQL技术，某大型保险公司实现了用大数据平台替代传统数仓，在复杂计算业务场景下，其性能提升了10-100倍。

第二个是实时搜索。华为FusionInsight率先实现了对Hadoop平台与MPPDB数仓平台的统一全文检索，率先支持SQL on Solr接口，提升业务开发效率5倍以上，独创标签索引方案，提升搜索性能3-10倍。目前，实时搜索技术在平安城市和金融行业已经实现商用。在国内某省的平安城市项目中，百亿级规模数据集中查询，实时搜索响应时间<3秒。

第三个是实时决策。与日常生活息息相关的很多业务是需要实时决策的，比如使用银行卡交易过程中的风险控制。由于传统技术处理速度的原因，往往只能实现事后风控。也就是说用户在刷卡完成后，银行才能够检查出来，刚才的交易是否有风险。这样对于银行和客户而言，都会有很大的风险存在。而华为FusionInsight实时决策平台，可以实现毫秒级复杂规则的风险检查，提供百万TIPS的业务处理能力，从而让风险控制从事后变为事中，并确保端到端的交易可在500毫秒内完成，不影响交易用户的体验。

第四个是图分析技术。在生活中有很多时候是需要进行用户的关系分析来进行风险控制和业务处理的。如果我们的客户中有一个是VIP客户，那么他的朋友符合VIP客户条件的可能性就会很大。因此如果我们能够通过关系分析技术找到他的朋友圈，在针对他的朋友进行针对性营销，那么业务成功的可能性也就会大大增加。但是，传统的数据库技术在处理客户关系发现时很困难，某公司曾经做过一个测试，想在2000万客户中发现客户间的关系信息，但是一直无法算出来。但是用图分析技术就可以很好解决这一类问题。因为在图数据库中，用户就是点，用户关系就是边，发现用户关系就变成了发现点与点间需要几条边的问题。华为的分布式图数据库，能够实现万亿顶点百亿边的实时查询，从而很快发现用户关系。在某项目中，华为帮助客户实现了13.7亿条关系图谱数据，3层关系查询秒级响应，从而大大提高了业务响应的速度。

最后，华为大数据平台是有着丰富的市场实践的产品。华为FusionInsight大数据平台已在40+个国家，总计700+项目中实现了成功商用。客户包括中国石油、一汽集团、中国商飞、工商银行、招商银行、中国移动、西班牙电信等众多世界500强企业。同时华为公司在全球建成有13个开放实验室，在这里华为与各国200+合作伙伴进行大数据方案的联合创新，包括SAP、埃森哲、IBM、宇信科技、中软国际等，共同推动大数据技术在各行各业的应用。


华为 FusionInsight LibrA，让数据“慧”说话  
 
    根据大数据摩尔定理，全球数据总量大约每24个月会翻一番，在这个数据爆炸的时代，我们的生活和工作已经和大数据息息相关，如何处理海量数据，发挥大数据价值，让数据为企业服务？  
    
     FusionInsight LibrA是华为公司研发的OLAP（Online Analytical Processing）型数据库，旨在为您提供轻松、可靠的企业数仓、数据集市和大数据SQL结构化数据分析解决方案。
 
 
     FusionInsight LibrA采用MPP(Massive Parallel Processing)架构，支持行存储与列存储，提供PB(Petabyte，250字节)级别数据量的处理能力。在核心技术上较传统数据库有巨大优势，能够解决不同行业用户的数据分析性能问题，可以为超大规模数据分析提供高性价比的方案，并可用于支撑各类数据仓库系统、数据集市、BI(Business Intelligence)系统和决策支持系统。

     FusionInsight LibrA关键特性：
 
	专业的TD、Oracle迁移工具：支持平滑迁移，业务敏捷上线。

	数据入库快：支持并行数据导入，日入库达数百TB。

	查询响应快：全并行计算引擎，满足PB级业务所需。行列混和存储引擎，同时满足点查、复杂分析等混合业务场景。

	扩展性强：扩容不中断业务，且扩容后，容量/性能线性增长。

	企业级高可用：独创的主+备+Handoff三重数据保护，协调节点多活设计，提供企业级可靠性保障。

	安全：全方位安全保证机制，为数据安全保驾护航。

	全文检索：支持标准SQL对文本进行模糊搜索，提供文本数据类“Google”功能。

	SQL On Hadoop：无缝集成Hadoop，可通过标准SQL访问和处理Hadoop数据。

	

#### Alibaba Cloud - MaxComputer

MaxComputer SQL Parser & SQL Optimizer

#### Transwarp Data Hub

TDH主要提供6款核心产品:

	Transwarp Inceptor是大数据分析数据库
	Transwarp Slipstream是实时计算引擎
	Transwarp Discover专注于利用机器学习从数据提中取价值内容
	Transwarp Hyperbase用于处理非结构化数据
	Transwarp Search用于构建企业搜索引擎
	Transwarp Sophon则是支持图形化操作的深度学习平台


Transwarp Inceptor - OLAP SQL引擎

在Inceptor中，您可以使用常见的数据库对象,包括数据库(database),表(table),视图(view)和函数(function)。您可以使用Inceptor SQL、Inceptor PL/SQL以及Inceptor SQL PL来操作这些数据库对象。Inceptor中数据库对象的元数据保存在Inceptor Metastore中，而数据库对象内的数据可以存放在：
1．内存或者SSD中（Holodesk表） 
2．HDFS中（TEXT表/ORC表/CSV表）


Transwarp Holodesk 分布式列式存储组件




#### Gbase+Informix


#### 技术思考

1.数据清洗的优化算法

2.大数据查询优化器设计
Calcite
Spark Catalyst
Dremel查询引擎

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

Dremel NESTED COLUMNAR STORAGE

LSM数据结构

内存列式存储优化

distributed file system文件系统(HDFS/GFS)改造 





