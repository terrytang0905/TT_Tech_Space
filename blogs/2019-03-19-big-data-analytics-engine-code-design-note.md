---
layout: post
category : bigdata
tags : [bigdata,olap,architect]
title: Big Data Analytics Note - BigData Analytics Code Design
---

## 大数据交互式分析服务-Code架构设计
-----------------------------------------------------------

#### 需求分析

- 业务模型->元数据模型
	业务数据对应元数据
	业务数据模型关联
- 可视化Canvas生成

_架构通用要求_

	- 功能类型抽象
	- 分可配置与无配置
	- 可配置功能提供通用配置接口
	- 支持热部署方案
	- 不可配置如何转换成可配置


#### 1.架构设计

*1.数据接入 ngxdmp-data-load*

分布式数据采集接入模块

1.1. 数据采集接入管理

1.2. 数据监测收集

监测数据回流

1.4. SDK数据监测

1.5. 运营商数据接入

1.6. 网络爬虫

1.7. Kafka数据交换

*2.数据管理 ngxdmp-dm-web*

2.1.基础数据源信息列表-陈列

按数据来源方式分类

数据源数据库信息收集

2.2.数据任务处理

数据基础处理流程状态

2.3.数据监控

基础数据样本统计报表

业务数据样本监控

2.4.数据建模

2.5.数据资产查询

数据资产信息列表(数据脱敏/数据清洗后)

视频基础数据库

2.6.数据权限管理

2.7.数据质量分析模型

*3.受众分析 ngxdmp-profile*

	iD-Merge
	用户标签数据仓库
	标签管理
	人群管理
	用户特征标签筛选
	受众洞察
	实时人群洞察-ElasticSearch服务

3.1. 首页看板(客户转化率，及分日、周、月客户UV数)
3.2. 标签管理
		2.2.1，第一方标签(根据自己业务定义标签名称，并定义对应标签ID，其实就是标签字典表，及标签分组)
		2.2.2，第三方标签(同上，使用别人公司标签，定义标签字典表)
3.3. 人群管理(功能丰富，为系统主要功能点！)
		2.3.1，新建人群(通过标签圈筛选出人群，出报告)
		2.3.3，人群列表(可人群分发，可跳转到洞察，即报告)
3.4. 人群洞察
		2.4.1，标签画像
			2.4.1.1，人群洞察(可选样本、全局指标[人群占比、人群特征占比]、TGI)
						维度：车相关、购买次数、购买时间、购买周期、消费升级、新品体验、地域、购买用户、忠诚用户、购买渠道、竞品相关
		2.4.2，用户ID分析
			2.4.2.1，ID打通率统计(原始ID,归并用户数,打通用户数),(imei_md5,cookie_trk,android_id,openudid,mac,idfa,idfa_md5,idfa_sha1 等)
		2.4.3，活动效果分析
3.5. 全景资料(没有数据，从列看也就是上传文件的统计描述信息)

*4.营销监测 ngxdmp-monitor*

	app监测
	小程序/H5监测
	网站监测
	表单监测

4.1. 监测管理

	4.1.1，活动监测
	4.1.2，站点监测
	4.1.3，表单监测
	4.1.4. 移动端监测
	4.1.5. 广告监测

*5.数据分析 ngxdmp-analytics*

5.1. 营销分析

	5.1.1，活动报告
	5.1.2，站点报告
	5.1.3，表单报告
	5.1.4，转化分析

5.2. 数据运营模型

	5.2.1，报告设置
	5.2.2，媒体管理
	5.2.3，客户管理

5.3. 报表分析

5.4. 实时数据计算分析


*6.数据同步&报告导出 ngxdmp-export*

6.1.数据同步服务

数据库间大数据同步方法

6.2.数据报告导出

*7.OLAP数据查询引擎 ngxdmp-olap/ngxdmp-olap-common*

跨数据源整合查询

*8.数据可视化 ngxdmp-front*

*9.用户管理 ngxdmp-account*

9.1.用户权限管理


#### 2.ngxdmp代码详解

	ngxdmp-olap
	ngxdmp-olap-common
	ngxdmp-cache
	ngxdmp-common
	ngxdmp-rpc
	ngxdmp-dm-web
	ngxdmp-data-load
	ngxdmp-export
	ngxdmp-profile
	ngxdmp-analytics
	ngxdmp-web
	ngxdmp-k8s-ext

	ngxdmp-query-parser
	ngxdmp-query-optimizer
	ngxdmp-query-executer
	ngxdmp-data-model
	ngxdmp-file-format

#### 3.PrestoDB代码详解

[Presto-OLAP引擎](2017-04-03-olap-distributed-presto-practice-note.md)

#### 4.ngxdmp-dm-web数据管理相关

##### 4.1.ngxdmp多数据源对接

##### 4.2.ngxdmp数据模型设计

##### 4.2.1.通用元数据定义

- 主订单数据定义-trade
- 商品订单数据定义-order
- 商品信息数据定义-product_item
- 商品类目数据定义-category
- 客户分析数据定义-customer_rfm
- 店铺信息数据定义-shop(线上/线下)
- 平台数据定义-platform(淘宝/天猫/京东/线下/其他渠道)

按业务场景字段抽象零售相关数据结构

##### 4.2.2.数据源与元数据映射

源数据->抽象模型->Cube数据主题

CMP元数据与数据分析元数据的差异

元数据模型设计

#### 5.ngxdmp-storage数据存储

冷热数据存储分离

#### 6.ngxdmp-profile受众管理

##### 6.1.ngxdmp ID-Merge

##### 6.2.通用标签引擎

终端标签计算-边缘计算

边缘计算编程模型

云端标签计算分析+标签库更新+数据下发

[用户标签模型设计](2018-06-06-user-label-profile-note.md)

#### 7.ngxdmp-monitor营销监测

#### 8.ngxdmp-analytics营销分析

##### 8.1.营销分析模型

[新零售分析模型](2017-04-16-new-retail-anlysis-design-note.md)

##### 8.2.流量分析模型

DNS流量/TCP&IP流量

#### 9.ngxdmp olap查询引擎

[通用OLAP查询引擎设计](2017-02-01-olap-query-engine-design-note.md)

##### 9.1.ngxdmp 查询解析相关

##### 9.2.ngxdmp 查询优化相关

##### 9.3.ngxdmp 缓存设计相关

##### 9.4.数据检索查询

#### 10.ngxdmp计算引擎

##### 10.1.数据处理计算

##### 10.2.实时数据计算


#### x.数据质量管理

##### 1.我们要解决什么业务需求?

- 如何自动化验证数据的准确性
- 数据验证不能影响正常数据流处理
- 如何有效监控数据的状态
- 如何确保分布式环境下数据不丢失不重复(Kafka/Storm/DB)
- 如何正确补全缺损的数据
- 数据异常后的系统自动监控

##### 2.核心技术问题有哪些?

*2.1.数据源数据指标确认?*

必须知晓数据源头数据精准信息,从而判断数据ETL后的数据变化。如何有效获取数据源信息?

*2.2.离线数据质量监控*

离线数据质量可以借助ETL监控完成。ETL应该可以获取数据源的精确信息

*2.3.实时数据质量监控*

实时数据质量只能保证所有输入端的数据,不丢失不重复。

##### 3.问题的优先级是什么?

##### 4.详细设计方案 - 解决方案

*4.1.SQL验证(参考ETL Kettle定时任务)*

- 比较数据源到本地NewBI数据仓库-同步数据量
- 业务逻辑数据匹配
- 趋势数据比较(保存最近30天数据),与当前数据进行趋势比较
- 数据变化的监控机制

*4.2.Backup数据版本(最近30天的增量数据)*

*4.3.自动化数据质量监控*

[DataCleaner开源数据质量工具](https://github.com/datacleaner/DataCleaner)

