---
layout: post
category : datascience
tags : [thinking,product,datascience]
title: DataProduct Architect Design Note
---

## 数据应用产品思考
-----------------------------------------------------------

### I.产品设计维度

#### 0. 数据源采集

- 数据源数据类型(dpi/sdk/app/爬虫/wifi)
- 数据源质量评估
- 数据源对接方式

#### 1. 数据清洗-识别数据规则&异常数据过滤s

- 数据清洗安全脱敏
- 基于已标记范例的学习:有监督的学习
- 借助神经网络的多重增强学习,实现海量数据有效过滤

	comment:基于海量数据的不确定性特征,高效的数据清洗与过滤算法非常有价值

#### 2. 数据处理-数据分类与数据传输

#### 3. 数据仓库-有效分类行为数据开发

- 交易数据(数据银行)
- 行为定向(behaviorial targeting)
- 上下文定向(contextual targeting)

#### 4. 数据分析

核心在于用户特定行为的深度分析。

- 数据指标开发

	* 网络行为数据指标
	* 电商交易数据指标
	* 服务内行为数据指标

- 流量数据分析
- 分类数据排名分析
- 历史数据趋势分析

#### 5. 数据挖掘&人工智能

- 内容数据标签开发
- 基于内容分类数据的行为预测分析

	* 识别数据规则
	* 数据分类与详细信息
	* 有效分类行为数据采集
	* 基于分类数据的行为预测分析

- [PostgreSQL用户行为分析](2017-05-30-postgresql-best-practice-note.md)
- [用户分层与用户画像分析](2018-06-06-user-behavior-profile-note.md)

	* 1.路由用户画像数据
	* 2.Looklike 全流量用户视频数据
	* 3.放大 全流量用户IMEI/MAC

- 点击率建模(click modeling)
- 分配规划(planning)


#### 6. [大数据分析思路](2015-11-08-bigdata-analysis-thinking.md)

### II.架构设计维度

#### 0. [大数据研究之架构组成](2017-07-27-bigdata-research-architect-build.md)

#### 1. 数据采集-爬虫&Scrapy

#### 2. 分布式数据存储-Hadoop&HDFS

- [大数据存储架构](2017-01-22-bigdata-database-architect-research-note.md)

#### 3. 大数据处理开发

- 基础数据分析技术 -Hive/Spark&SparkSQL/Impala/Presto
- [大数据研究-SQL设计](2017-07-28-bigdata-research-sql-design.md)
- 实时数据处理-SparkStreaming/Storm
- [大数据研究-数据处理计算](2017-07-28-bigdata-research-bigdata-development.md)
- [大数据研究-OLAP分析](2017-02-01-bigdata-research-olap-anlysis.md)
- [ElaticSearch搜索架构](2017-01-06-elasticsearch-search-engine-architect-note.md)
- ETL数据处理 -Kettle
- 数据同步 -Sqoop/DataX/gphdfs
- 数据质量分析

#### 4. 深度数据分析-Greenplum/Python/Tensorflow

- [Greenplum最佳实践](2017-05-28-greenplum-best-practice-note.md)
- [机器学习&Python数据挖掘](2017-10-16-ml-python-data-analysis-note.md)

#### 5. 应用数据存储-PostgreSQL

- [PostgreSQL最佳实践](2017-05-30-postgresql-best-practice-note.md)

#### 6. 产品应用架构-微服务(Java/PHP)

#### 7. 数据可视化&商业智能-Tableau/永洪BI/E-Charts/D3.js

#### 8. 数据产品性能优化

	数据结构/ETL/缓存/业务架构/数据更新

#### 9. 数据产品常规问题

	数据安全脱敏/数据验证/数据完整性/数据冲突/样本异常/性能问题


### III.产品价值维度

_0.产品增长黑客-数据驱动_

	- [产品用户行为分析](2017-09-30-user-behavior-analysis-note.md)

_1.大数据平台相关_


_2.大数据挖掘与情报分析_

	- 网络行为数据分析采集
	- 内容数据+NLP分类识别规则定义+内容榜单分析
	- 内容流量与趋势分析
	- 人群定向筛选+对应内容/行为分析+广告投放
	- 总体/定向用户行为分析+用户分层

_3.搜索-推荐-广告(计算广告)_

广告营销计算技术

	- [计算广告](2017-07-01-compute-adverting-bigdata-note.md)
	- 广告内容分析与检索
	- 广告排序和用户行为反馈模型

![web_adver](_includes/web_adver_map.png)

计算广告最具挑战的算法问题大多都集中在离线数据处理的部分。离线数据处理有两 个输出目标:

	一是统计日志得到报表、dashboard 等，供决策人进行决策时作为参考;
	二是利用数据挖掘、机器学习技术进行受众定向、点击率预估、分配策略规划等，为在线的 机器决策提供支持。

_4.大数据征信风控模型_

	- 用户特征信息库开发
	- 用户交易行为采集

_5.大数据金融交易模型(门槛有点高)_


### IV.人工智能-数据产品终局

	- 计算机视觉
	- 语音识别
	- 知识图谱
	- 语义识别(传递信息/沟通/同感)

