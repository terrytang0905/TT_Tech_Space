---
layout: post
category : datascience
tags : [bigdata,analysis,olap]
title: New Retail Analysis Design Note
---

## 新零售分析模型设计Note
------------------------------------------------------------

借助OLAP现有技术框架,针对新零售业态(电商与零售,线上与线下)数据融合分析做深度定制。实现新零售行业通用数据挖掘需求满足。
针对非阿里业务数据ETL接入必须进行深度优化,简化ETL数据接入流程。零售行业数据分析的定制化需求非常大,如何解决通用化设计?

#### 1.零售建模设计

**A.CRM与客户分析**

##### a.1.CRM客户洞察

##### a.2.雅诗兰黛数据分析月报(ELM)

复购率计算
```sql
select t.*,t1.ttl_cus,t.repeat_cus/t1.ttl_cus as'repeat_rate'
from(
select a.yearmoth,count(distinct customerno) as'repeat_cus' from(
select DATE_FORMAT('2017-01-01','%Y-%m') as'yearmoth',
customerno,if(count(distinct pay_time)=1,'1  time purchaser','Repeat purchaser') as'cus_type'
from base_trade_cl
where pay_time between '2017-01-01' and '2017-01-31'
group by customerno) a 
where a.cus_type='Repeat purchaser'
)t
left join 
(select DATE_FORMAT('2017-01-01','%Y-%m') as'yearmoth',count(distinct customerno)as'ttl_cus'
from base_trade_cl
where pay_time between '2017-01-01' and '2017-01-31')t1 on t.yearmoth=t1.yearmoth
```

##### a.3.CRM分析数据结构

**B.零售营销/库存/订单**
 
**C.电商数据建模设计**

##### c.1.RFM查询模型(重点)

应用场景设计:RFM客户划分
RFM数据建模分析
双十一数据建模分析设计


#### 2.数据挖掘应用


##### 2.1.表查询模型(重点)

通过查询表方式定义单元格(聚合),再在该单元格中进行计算
应用场景设计:RFM客户响应率或客单价
复购率统计指标

* 2.1.1.任意时间新老客定义

	a.创建客户粒度第一次购买时间聚合表
	b.订单表按时间进行数据筛选
	c.订单筛选表与客户聚合表JOIN连接,定义新老客
	d.自动生成新老客标签维度

* 2.1.2.定义自定义函数Fixed/Included/Excluded



##### 2.2.客户画像-朴素贝叶斯模型(概率统计)

应用场景设计:
概率
几率
似然
TF-IDF算法:关键字相关性统计
在无监督情况下,可用朴素贝叶斯模型进行相关性概率分析实现电商客户画像分析

朴素贝叶斯与相关性分析
TF-IDF算法


##### 2.3.线性回归(预测结果)

普通最小二乘回归分析:线性回归中找出最佳拟合曲线的常见方法
对于一个给定的数据集,总是可能找到一条最佳拟合曲线
应用场景设计:
	y=W.x+b
	构建模型（蓝色部分）
	基于模型构建成本函数（红色部分）
	使用梯度下降（绿色部分）
	最小化成本函数

##### 2.4.多特征线性回归

复杂的 n 特征公式可以用矩阵简化
y=W.x+W2.x2+b


##### 2.5.客户流失分析-逻辑回归(分类结果)

线性回归与逻辑回归的区别与相似
协调逻辑回归与线性回归
为了使逻辑回归利用 y = W.b + x，我们需要做出一些改变以协调上述差异。

1.特征变换，x
2.预测结果转换，y
3.成本函数的变换

客户流失率分析

##### 2.6.客户划分和分层效应

客户金字塔模型

基于用户分层后的营销投放

客户分层趋势分析

客户地域分布

##### 2.7.决策树

一个分层的规则集,可用于分类,评估与预测问题


##### 2.8.商品关联分析

购物篮分析

关联规则的目的就是在一个数据集中找出项与项之间的关系，也被称为购物篮分析(Market Basket analysis)。

Apriori algorithm具体应用


##### 2.9.评价舆情分析(文本解析)



#### 3.时间序列分析

适用于周期波动特征显著的数据分析预测。这个分析模型在当前电商及销售领域非常流行


#### 4.Cube数据建模设计

* 4.1.1.针对预处理后的数据结构进行Cube建模

* 4.1.2.参考客户洞察Cube模型




#### 5.用户营销模型




#### 6.产品效果如何检验?







