---
layout: post
category : datascience
tags : [bigdata,develop]
title: SNS Recommendation Design Note
---

## 社交推荐功能设计
-----------------------------------------------------------

### 1.	Recommender System Solution比较

 根据现有OpenSource框架，Mahout是相对比较成熟的Machine Learning框架，其中的Taste是支持多种预测算法的推荐模块。其算法有基于MapReduce和pure 
 Java的两种实现。数据存储可选择Memory，File, 
 DB和Hadoop。Hadoop的批处理数据处理特性导致Mahout无法很好地支持实时数据分析与处理。不过现行需求下对实时性的需求不高，现有Mahout与Lucene/Hadoop的集成度较高, 
 且已提供足够成功的机器学习案例。因此我们首选Mahout作为社交类产品推荐核心框架。
 同时密切关注PredictionIO Solution (创业公司)，其方案是基于Mahout的Machine 
 Learning改进方案,且支持Spark，HBase等大数据分析工具。之后如Mahout无法满足现有需求，可选择切换到PredictionIO。


| Recommender  |  Link	                                              | Status  | Language | Feature |
| -------------|:-----------------------------------------------------|:--------|:---------|:--------|
|Apache Mahout | http://mahout.apache.org/                            | Active  | Java	   | 基于Hadoop,扩展性好,有较多支持,有现成实例，缺乏实时性数据分析 |
|Easyrec	   | http://easyrec.org/                                  | Abandon	| Java	   | 易用性,但已无维护                                        |
|Lenskit	   | http://lenskit.org/                                  | Active	| Java	   | 学术圈内的影响力很大                                      |
|GraphLab	   | http://docs.graphlab.org/collaborative_filtering.html| Active	| C++      | 实现了ALS，CCD++，SGD，Bias-SGD，SVD++，Weighted-ALS，Sparse-ALS，<br> |
|			   |													  |		    |		   | Non-negative  Matrix Factorization，Restarted Lanczos Algorithm等算法 |
|Oryx	       | https://github.com/OryxProject/oryx                  | Active	| Java     | 基于Lambda架构，支持Spark，Kafka                         |
|Predictionio  | http://prediction.io/                                | Active  | Scale	   | 基于Mahout,支持Apache Spark,Hbase,Spray，擅长用户交互、数据可视化 |
|Seldon	       | http://www.seldon.io/open-source/                    | Active  | Java	   | 支持Apache Spark,提供RestAPI |


### 2.	SNS Recommendation需求分析
SNS需提供推荐符合用户个人口味偏好的明星内容(视频/图片等)，以便让用户容易得到感兴趣的内容，及参与到相关社区/主题吧的互动中。

> 以下是我们项目所需的三种推荐模式，组合使用。

* Content-based Recommendation(内容相似性): 基于用户个人历史偏好和内容匹配的相关性推荐 (用于冷启动/推全新内容) 
* User-based Collaborative Filtering Recommendation (UserCF多用户相似性): 基于K-邻居用户历史偏好特征的对当前用户的内容推荐
* Item-based Collaborative Filtering Recommendation (ItemCF多用户历史偏好内容相似性): 基于多用户历史偏好关联来推断内容(目标item)的推荐

> 推荐流程如下：

1.	冷启动阶段,通过用户选择关注的明星信息/Track用户访问内容log, 提供基于Content-based Recommendation算法的推荐机制。包括推荐当前热门信息
2.	用户增长阶段,该阶段有一定用户,还未形成社群。添加基于ItemCF算法机制,基于所有用户历史偏好的内容关联来推荐信息。
3.	用户活跃阶级,用户已活跃在相关主题吧中。添加基于UserCF算法机制,对于相关社区内的K-邻居用户历史偏好来推荐信息。并使用聚类算法将用户数据对象分组,确保同类簇中的数据具有更大的相似性, 以便于准确查询相关信息。

以上流程仅是初步计划，可因用户行为及数量的变化而改变。在现今很流行的社交网络产品中，UserCF 是一个更不错的选择，User CF 加上社会网络信息，可以增加用户对推荐解释的信服程度。 

> 如何获得用户偏好特征信息？

1.	保留用户访问内容的相关行为信息/打分/投票/转发/收藏/关注/评论/点击流/页面停留时间。
2.	通过Mahout框架，添加用户/内容标签,以找到相似的用户或物品

### 3.	Recommendation Algorithm选择

按照协同过滤方法的分类, taste（mahout-core-0.9.jar）里的recommender可以分别划到对应的分类下：

* Item-based:
>        GenericItemBasedRecommender
>        GenericBooleanPrefItemBasedRecommender
>        KnnItemBasedRecommender (Deprecated)
* User-based:
>         GenericUserBasedRecommender
>         GenericBooleanPerfUserBasedRecommender
* Model-based:
>         SlopeOneRecommender (Deprecated)
>         SVDRecommender
>         TreeClusteringRecommender (Deprecated)
>         ItemAverageRecommender
>         ItemUserAverageRecommender	

在SNS中将尝试采用以下算法：

* GenericItemBasedRecommender
* GenericUserBasedRecommender
* KnnItemBasedRecommender
* SlopeOneRecommender 适用于用户对item的打分是具体数值的情况
* SVDRecommender 基于SVD矩阵分解技术的推荐器

具体算法调整与优化需根据用户和内容数据分析后得出的召回率和准确率决定。
算法及适用场景：
算法评分的结果：
 

### 4.	SNS Recommendation Engine设计

Apache Mahout 中提供的一个协同过滤算法的高效实现，它是一个基于 Java 实现的可扩展的，高效的推荐引擎。以下给出了 Apache Mahout 中协同过滤推荐实现的组件图，下面我们逐步深入介绍各个部分。
 
Taste 由以下五个主要的组件组成： 

* DataModel：DataModel 是用户喜好信息的抽象接口，它的具体实现支持从任意类型的数据源抽取用户喜好信息。Taste 默认提供 JDBCDataModel 和 FileDataModel，分别支持从数据库和文件中读取用户的喜好信息。

* UserSimilarity 和 ItemSimilarity：UserSimilarity 用于定义两个用户间的相似度，它是基于协同过滤的推荐引擎的核心部分，可以用来计算用户的“邻居”，这里我们将与当前用户口味相似的用户称为他的邻居。ItemSimilarity 类似的，计算内容之间的相似度。

* UserNeighborhood：用于基于用户相似度的推荐方法中，推荐的内容是基于找到与当前用户喜好相似的“邻居用户”的方式产生的。UserNeighborhood 定义了确定邻居用户的方法，具体实现一般是基于 UserSimilarity 计算得到的。

* Recommender：Recommender 是推荐引擎的抽象接口，Taste 中的核心组件。程序中，为它提供一个 DataModel，它可以计算出对不同用户的推荐内容。实际应用中，主要使用它的实现类 GenericUserBasedRecommender 或者 GenericItemBasedRecommender，分别实现基于用户相似度的推荐引擎或者基于内容的推荐引擎。
SNS mahoutRec 基于MVC架构的Recommender 独立服务System,提供相关RestAPI。


### 5.	Recommender System Demo

测试用例：

| userid | itemid | weight |
|--------|:-------|:-------|
|1       | 101    | 5.0    |
|1 | 102 |3.0 |
|1 | 103 |2.5 | 
|2 | 101 | 2.0 |
|2 | 102 | 2.5 |
|2 |103 |5.0 |
|2 |104 |2.0 |
|3 |101 |2.5 |
|3 |104 |4.0 |
|3 |105 |4.5 |
|3 |107 |5.0|
|4 |101 |5.0|
|4 |103 |3.0|
|4 |104 |4.5|
|4 |106 |4.0|
|5 |101 |4.0|
|5 |102 |3.0|
|5 |103 |2.0|
|5 |104 |4.0|
|5 |105 |3.5|
|5 |106 |4.0|

Recommender SourceCode:

执行结果：

UserCF:
uid:1(104,4.274336)(106,4.000000)
uid:2(105,4.055916)
uid:3(103,3.360987)(102,2.773169)
uid:4(102,3.000000)
uid:5

ItemCF:
uid:1(104,5.000000)
uid:2
uid:3(103,3.276647)(102,3.271243)
uid:4(102,5.000000)
uid:5





