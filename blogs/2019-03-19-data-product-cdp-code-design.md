---
layout: post
category : bigdata
tags : [bigdata,product,architect]
title: Data Product Note - DMP&CDP Code Design
---

## 大数据产品-DMP&CDP Code架构设计
-----------------------------------------------------------

### I.需求分析与设计

_1.核心Features设计_

	1.数据湖多数据源整合建模
	2.元数据模型抽象动态支持业务模型
	3.智能客户ID-Merge整合打通
	4.云端标签计算分析+标签库更新+数据下发
	5.OLAP联合查询与边缘计算
	6.离线与实时大数据处理与计算优化
	7.数据可视化Canvas生成

_2.架构通用要求_

	- 功能类型抽象
	- 分可配置与无配置
	- 可配置功能提供通用配置接口
	- 支持热部署方案
	- 不可配置如何转换成可配置


### II.架构设计

_1.数据接入 ngxdmp-data-load_

1.1. 客户行为监测 ngxdmp-monitor

	自动化埋点
	1.1.1，活动监测
	1.1.2，站点监测
	1.1.3，表单监测
	1.1.4. 移动端监测
	1.1.5. 广告监测

1.2.分布式数据采集接入模块

1.3. 数据采集接入管理

1.4. 数据监测收集+监测数据回流

	a. SDK数据监测
	b. 运营商数据接入
	c. 网络爬虫
	d. Kafka数据交换


_2.数据管理 ngxdmp-dm-web_

2.1.数据源管理

信息列表-陈列

按数据来源方式分类

数据源数据库信息收集

2.2.数据任务处理

数据基础处理流程状态

2.3.数据监控

基础数据样本统计报表

业务数据样本监控

**数据质量分析模型**

	数据质量管理

- 如何自动化验证数据的准确性
- 数据验证不能影响正常数据流处理
- 如何有效监控数据的状态
- 如何确保分布式环境下数据不丢失不重复(Kafka/Storm/DB)
- 如何正确补全缺损的数据
- 数据异常后的系统自动监控

2.4.数据资产管理

数据湖平台

数据资产信息列表(数据脱敏/数据清洗后)

定制基础数据库设计

数据权限管理

数据建模与业务数据模型


_3.受众分析 ngxdmp-profile_

3.1. 首页看板-客户运营分析

		(客户转化率，及分日、周、月客户UV数) 
	
3.2. 通用标签管理

		3.2.1，第一方标签(根据自己业务定义标签名称，并定义对应标签ID，其实就是标签字典表，及标签分组)
		3.2.2，第三方标签(同上，使用别人公司标签，定义标签字典表)
	    通用标签定义模型

3.3. 客户人群管理(功能丰富，为系统主要功能点!)+用户标签模型数据仓库

		3.3.1. ID-Merge客户数据资源整合(内外部数据整合)
		3.3.2，新建人群(通过标签圈筛选出人群，出报告)
		3.3.3，人群列表(可人群分发，可跳转到洞察，即报告)	
		通用人群管理与画像
	
云端标签计算分析+标签库更新+数据下发

3.4. 人群洞察=用户特征标签筛选+受众洞察

		3.4.1，标签画像
			3.4.1.1，人群洞察(可选样本、全局指标[人群占比、人群特征占比]、TGI)
						维度：车相关、购买次数、购买时间、购买周期、消费升级、新品体验、地域、购买用户、忠诚用户、购买渠道、竞品相关
		3.4.2，用户ID分析
			3.4.2.1，ID打通率统计(原始ID,归并用户数,打通用户数),(imei_md5,cookie_trk,android_id,openudid,mac,idfa,idfa_md5,idfa_sha1 等)
		3.4.3，活动效果分析


3.5. 全景洞察=实时人群洞察-ElasticSearch服务


_4.数据分析模型 ngxdmp-analytics_

4.1. 营销分析

	4.1.1，活动报告
	4.1.2，站点报告
	4.1.3，表单报告
	4.1.4，转化分析

4.2. 数据运营模型

	4.2.1，报告设置
	4.2.2，媒体管理
	4.2.3，客户管理

4.3. 报表分析

4.4. 实时数据计算分析

4.5. 数据模型效果评估

4.6.数据报告导出 ngxdmp-export

_5.用户权限管理 ngxdmp-account_

5.1.用户权限管理设置

#### 核心技术特点

1. SparkGraphX图计算与IDMerge


### III.ngxdmp代码详细设计

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


#### 1.ngxdmp-dm-web数据管理相关

##### 4.1.ngxdmp多数据源对接

##### 4.2.ngxdmp数据模型设计

_4.2.1.通用元数据定义_

- 主订单数据定义-trade
- 商品订单数据定义-order
- 商品信息数据定义-product_item
- 商品类目数据定义-category
- 客户分析数据定义-customer_rfm
- 店铺信息数据定义-shop(线上/线下)
- 平台数据定义-platform(淘宝/天猫/京东/线下/其他渠道)

按业务场景字段抽象零售相关数据结构

_4.2.2.数据源与元数据映射_

源数据->抽象模型->Cube数据主题

CMP元数据与数据分析元数据的差异

元数据模型设计

#### 2.ngxdmp-storage数据存储

冷热数据存储分离

#### 3.ngxdmp-profile受众管理

##### 6.1.ngxdmp ID-Merge

##### 6.2.通用标签引擎

终端标签计算-边缘计算

边缘计算编程模型

云端标签计算分析+标签库更新+数据下发

[用户标签模型设计](2018-06-06-user-label-profile-note.md)

#### 4.ngxdmp-monitor营销监测

多终端用户行为监测采集

#### 5.ngxdmp-analytics营销分析

##### 8.1.营销分析模型

[新零售分析模型](2017-04-16-new-retail-analytics-design-note.md)

##### 8.2.流量分析模型

DNS流量/TCP&IP流量

#### 6.ngxdmp olap查询引擎 - ngxdmp-olap/ngxdmp-olap-common

- [通用OLAP查询引擎设计](2017-02-01-bigdata-analytics-olap-query-engine-design-note.md)

- [分布式联合计算引擎Code设计](2019-03-18-bigdata-analytics-all-query-engine-code-design.md)

##### 6.1.ngxdmp 查询解析相关

##### 6.2.ngxdmp 查询优化相关

##### 6.3.ngxdmp 缓存设计相关

##### 6.4.数据检索查询

#### 7.ngxdmp分布式计算引擎

Spark/Flink/Beam

##### 7.1.数据处理计算

##### 7.2.实时数据计算


#### 8.数据可视化 ngxdmp-front


#### 9.核心问题有哪些?

*4.3.自动化数据质量监控*

[DataCleaner开源数据质量工具](https://github.com/datacleaner/DataCleaner)

*2.1.数据源数据指标评估确认?*

必须知晓数据源头数据精准信息,从而判断数据ETL后的数据变化。如何有效获取数据源信息?

*2.2.基础数据质量监控*

离线数据质量可以借助ETL监控完成。ETL应该可以获取数据源的精确信息

*2.3.实时数据质量监控*

实时数据质量只能保证所有输入端的数据,不丢失不重复。


### IV.核心技术解决方案

*4.1.SQL验证(参考ETL Kettle定时任务)*

- 比较数据源到本地NewBI数据仓库-同步数据量
- 业务逻辑数据匹配
- 趋势数据比较(保存最近30天数据),与当前数据进行趋势比较
- 数据变化的监控机制

*4.2.Backup数据版本(最近30天的增量数据)*



