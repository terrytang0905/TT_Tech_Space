---
layout: post
category : technology
tags : [datascience,datamining,architect]
title: Hive Analysis & Utility Note
---

## Compute Adverting Note
------------------------------------------------------------


OneMedia产品架构设计

DMP:Data Management Platform，即数据管理平台。是把分散的第一和第三方数据整合到统一的技术平台里，再通过机器学习算法对这些数据进行标准化和细分管理，并把这些细分结果实时地应用于现有的互动营销环境里，帮助营销取得最大化效果。
http://www.cctime.com/html/2016-8-8/1204143.htm
DSP（Demand Side Platform）
http://baike.baidu.com/link?url=gAJ4qVU5r8JoY6onyYJkwUX5JdN6Tu8IaiXTcxBg3PFKVXzL83LI6VFOV9xsgb6G4QLACMjI313jnL0vB8NJ8q


PMP(PrivateMarketPlace, 私有交易市场)
PDB(ProgrammaticDirectBuy，私有程序化购买）

基于竞价机制和精准人群定向这两个核心功能,在线广告分化出了广告网络(ad Network,ADN)这种新的市场形态。它批量地运营媒体的广告位资源,按照人群或上下 文标签售卖给需求方,并用竞价的方式决定流量分配。

信息流广告分拣
OTT广告监控方案

流量预测(traffic forecasting)

1)售前指导
2)在线流量分配
3)出价指导

搜索广告的效率eCPM远远超过一般的展示广告
搜索广告的受众定向标签,即是上下文的搜索查询
搜索广告的展示形式与自然结果的展示方式非常接近
搜索广告发展出来的竞价交易模式已经发展成为互联网广告最主流的交易模式

在搜索广告中排序依据是eCPM
Google 将策略改变为在投放过程中 预估每条广告的点击率,然后按点击率和出价的乘积对广告排序,这也就形成了现在竞价 广告普遍采用的根据 eCPM 决策的逻辑。

我们重点需要研究的是市场处于稳定状态下的收益和其他特性。而所谓稳定,指的是 整个竞价系统处于纳什均衡(Nash equilibrium)状态,也即每个广告主都通过出价得到了 最符合自己利益的位置。

定价策略。
1.广义第二高价(GSP)




可以主动地影响流量,以利于合约的达成。这一产品策略问题称为流量塑形(traffic shaping)


