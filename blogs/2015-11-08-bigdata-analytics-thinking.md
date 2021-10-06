---
layout: post
category : datascience
tags : [bigdata,datamining,algorithm]
title: Big Data Analytics Note - Data Deep Thinking
---

## 大数据分析-深度数据随想
-------------------------------------------------

数据价值思考的起点

- 数据=生产资料
- 技术=生产力
- 商业模式=生产关系


### Information,NLP,Mathematics

**数据挖掘应用**

1. 数据处理:自然语言处理技术(NLP)
2. 统计和计数:A/B test、top N排行榜、地域占比
3. 多维分析:RFM分析,同比,环比,趋势分析
4. 机器学习:分类,预测模型,聚类,关联规则分析,文本情感分析
5. 人工智能:深度学习,迁移学习,建模仿真

        Tips:其中机器学习领域与数据库领域是数据挖掘的两大支柱

### I.基本定义

#### 1.1.数据分析技术分类:

* 大数据的“4V”特征

 - Volume — 数据量大数据量巨大。 从数兆字节(TB)1 级别跃升到数十兆亿字节 (PB) 级别 。如一个CT图像含有大约 150MB的数据，而一个基因组序列文件大小约为 750MB，一个标准的病理接近 5 GB。考虑到人口数量和平均寿命等因素，仅一个社区医院就可以生成和累积达数个TB甚至数个PB级的数据。
 - Velocity — 速度快处理速度快，时效性强。 举例来说，检测医疗支付中的欺诈行为可以事后追溯，也可以实时检测；如果能够实现实时检测，即在支付发生前甚至在医疗服务发生前就识别出欺诈行为，则可有效避免重大经济损失。
 - Variety — 种类多数据类型繁多，来源广泛。 既包括数值型数据，也包括文字、图形、图像、音频、视频、网络日志、邮件、等非数值型或者非结构化数据，且预计这些非结构化信息将占未来十年数据产生量的 90%。
 - Value — 价值高价值的体现的是大数据分析应用的目的意义所在。 通过深入的大数据分析挖掘，可以为各方各面的经营决策提供有效支持，创造巨大的经济及社会价值。

#### 1.2.数据源提取与存储:

1. 结构化数据：海量数据的查询、统计、更新等操作效率低
2. 非结构化数据：图片、视频、word、PDF、PPT等文件存储、不利于检索，查询和存储
3. 半结构化数据：转换为结构化数据存储、按照非结构化存储
4. 多数据源归整方案 - Hadoop等分布式存储

#### 1.3.数据定义属性:

- 分类(定性属性) - 维度
- 数值(定量属性) - 度量
- MetaData - 数据描述数据
- MainData - 主数据
- RefData - 时间/空间维度数据

#### 1.4.批处理/实时数据分析:

- 基于传统数据仓库,批处理离线数据分析
- 基于实时大数据处理,敏捷商务智能BI
- 批量数据 - ETL - DataWarehouse
- 实时数据 - 信息交换 - OPDM 操作型数据集市

#### 1.5.解决方案思考:

1. 数据采集与同步-Kafka
    海量数据采集 
2. 大数据离线存储: HDFS,Kudu
3. 实时流式计算: Apache Storm,Apache SparkStreaming(内存占用过大)
4. 大数据计算平台: Spark, Flink, MapReduce批处理技术
5. 内存数据存储: HBase Cassandra等
6. 分析型数据库: MPP(Vertica/Greenplum)
7. OLAP查询计算：SparkSQL, Hive, GoogleDremel, Impala, Presto, Druid, Kylin
8. 数据可视化趋势: D3, E-Charts

### II.数据仓库/大数据架构设计

#### 2.1.BI数据仓库概念设计

A. _Bill Inmon的企业信息化工厂_ <br />
![imnon_model](_includes/datamodel_imnon.png)
> 采用第三范式的格式 <br />
> ETL -> 企业数据仓库 -> 数据集市(多维物理数据) -> 用户探索&挖掘 <br />

B. _Ralph Kilmball维度数据仓库(多维数据分析)_ <br />
![kimball_model](_includes/datamodel_kimball.png)
> 多维模型–星型模型 <br />
> ETL -> 维度数据仓库 -> 虚拟数据集市(逻辑主题区域Cube) -> 用户探索&挖掘 <br />
> 集合数据集市DataMarts在维度数据仓库中 跨主题区域的关键企业维度的一致性使用 <br />
> 维度格式 可直接访问 <br />

    Tip:维度建模分析成为当前主流。

C. _独立型数据集市_
> ETL -> 数据集市(关注维度/主题区域) -> 用户探索&挖掘 <br />
> 脱离企业环境,只关注主题区域

#### 2.2.大数据&数据仓库演进技术选型

A.[分布式基础架构](2017-07-27-bigdata-research-architect-build.md)

B._大数据分布式存储_:

> HDFS(GFS) / HBase(Google BigTable) / Kudu  <br />
> LevelDB / RocksDB <br />
> LSM / SSTable

C.[分布式数据架构分析](2017-07-27-bigdata-research-database-architect.md)

D._分布式大数据分析_:

> Hive 
> [PrestoDB](2017-04-03-olap-distributed-presto-practice-note.md)  <br />
> [ElasticSearch](2017-01-06-elastic-search-engine-architect-note.md)
> [MongoDB](2016-02-28-mongodb-internal.md) / Couchbase / Redis <br />
> [BigTable&HBase分析](2017-03-12-bigtable&hbase-analysis-note.md)
> Cassandra / Amazon Dynamo

E._分布式OLAP分析_:

> Dremel / Spanner / MesaStore
> [Impala&Kudu](2016-12-12-olap-distributed-impala-research-note.md)  <br />
> [Greenplum](2017-02-11-greenplum-arch-design-note.md) / Vertica 分析型数据仓库 <br />
> HTAP: TiDB / OceanBase / Oushu Database(Apache HAWQ) / HashData
> Doris / Clickhouse

### III.数据预处理

#### 3.1.数据预处理&探索

- 聚集:aggregation
- 抽样
- 维归约  <br />
- 特征子集选择 <br />
`用于降低维度,除去冗余和不相关的特征` <br />
`特征选择方法: embedded approach / filter approach / wrapper approach` <br />
`特征加权` <br />
- 特征创建 <br />
`特征提取` <br />
`映射数据到新的空间` <br />
- 离散化和二元化 <br />
`发现关联模式的算法要求数据是二元属性形式` <br />
- 变量变换 <br />

#### 3.2.数据清理DataCleaning

A. _数据抽样_ <br />
    建模样本: TrainingSet，ValidationSet，TestingSet <br />
    数据缺失值和异常值 <br />

B. _数据转换_ <br />
     数据标准化(Normalization) <br />

C. _数据筛选/特征筛选_ <br />
     R平方 <br />
     卡方检验(Chi-Square Statistics):适用于类别型变量的检验 <br />
     数据降维:主成分分析和变量聚类 <br />

D. _共线性问题_ <br />
     自变量间存在较强的，甚至完全的线性相关关系 <br />

E. _数据完整性验证_
     介于大多数数据来源的不稳定性, 数据完整性是极为重要的<br />

**设计独立数据质量监控组件**

#### 3.3.数据处理方案

* ETL Kettle开源工具
* 任务队列与任务规则
* 基于SQL/存储过程/UDF数据处理组件
* [Hive/Spark/Storm/Flink数据处理](2017-07-29-bigdata-research-dataprocess-development.md)
* 大数据MQ-[Kafka应用](2017-07-29-bigdata-research-dataprocess-kafka-note.md)

#### 3.4.异常检验与处理

对于数据异常的验证非常重要


### IV.数据挖掘-多维数据分析(数据库领域)

OLAP与数据挖掘-机器学习的差异

  - 主要差异在于OLAP则用于数据探索,Data Mining用在根据假设进行推测
  - Data Mining常能挖掘出超越归纳范围的关系,但OLAP仅能利用现有数据查询探索及可视化的报表

#### 数据建模与Cube

定义Meta元数据模型 <br />
建立数据模型为DataCleaning指定清洗规则 <br />
为源数据与目标提供ETL mapping支持 <br />
理清数据与数据之间的关系 <br />

#### 4.1.数据建模规则

- 星型模式与雪花模式

 a. 代理键SK与自然键NK <br />
 b. 代理键可以基于单一的列实现事实表和维度表之间的连接操作 <br />
 c. 自然键可能包含多个列,历史记录等多条信息通过代理键来唯一对应 <br />
 d. 代理键的替代方案: <br />

        1.客户维度表的主键可能包含'customer_id'和一个包含序列号的'version_number',允许表中存储一个客户的多个版本
        2.为自然键增加一个时间戳

 e. 缓慢变化维度（lowly changing dimension）<br />

- 通过维度环境使事实具有实际意义

 a. 用于过滤查询或报表 <br />
 b. 用于控制聚集事实的范围 <br />
 c. 用于确定信息的顺序与排序 <br />
 d. 与事实一起构成提供报表的环境 <br />
 f. 用于定义主从结构,分组,分类汇总,汇总等 <br />

- 雪花模式及支架表 

        需要采用雪花模式和支架表的情况是一种特例而不能当做规则来使用

- 分析型环境,预先计算和存储这些冗余数据元素具有三个优点:性能，可用性和一致性

- 事实表粒度设计/宽表设计


#### 4.2.Summary Statistics汇总统计

- 频率与众数 <br />
        `frequency(Vi)=属性值Vi的对象数/m` <br />
        `分类属性的众数(mode)是具有最高频率的值` <br />
- 均值(mean) & 中位数(median)
- 散步度量:极差与方差 <br />
          `极差-range(x)=max(x)-min(x)` <br />
          `方差-variance(x)` <br />
          `标准差-standard deviation` <br />
- 多元汇总统计 <br />
        `covariance matrix协方差矩阵` <br />
        `两个不同参数之间的方差就是协方差` <br />
        `correlation matrix相关矩阵` <br />
        `值集的倾斜度(skewness)` <br />


#### 4.3.多维数据分析定义

- 分析多维数据 <br />
    (产品ID-日期-地方-销售额)
- 数据立方体:计算聚集量
- 维归约: 在一个维上聚集将数据的维度从3维归约2维 <br />
    `维归约的线性代数` <br />
    `主成分分析Principal Components Analysis - PCA` <br />
        = PCA把原先的n个特征用数目更少的m个特征取代,新特征是旧特征的线性组合,这些线性组合最大化样本方差,尽量使新的m个特征互不相关. <br />
    `奇异值分解Singular Value Decomposition - SVD` <br />
    `特征值分解和奇异值分解` <br />
    `维归约与PCA的区别` <br />
- 转轴(Pivoting): 在除两个维以外的所有维上聚集
- 切片(Slicing)和切块(dicing) - 穿透/查看明细
- 上卷(roll up)和下钻(drill down): 与聚集相关(基于维度的钻取)

#### 4.4.分析应用-客户划分

- 客户RFM模型
    消费新鲜度 (Recency)
    消费频度 (Frequency)
    消费金额 (Monetary)
- [客户RFM设计实例](http://wiki.yunat.com/pages/viewpage.action?pageId=39207407)
- [双十一RFM分析设计](http://wiki.yunat.com/pages/viewpage.action?pageId=43854085)
- 零售新老客分析
- 客户洞察新老客分析
- 客户分层金字塔模型

#### 4.5.OLAP数据分析引擎

数据库领域主要关注OLAP相关技术演进

- [OLAP数据分析引擎](2021-05-05-bigdata-analytics-olap-next-generation-note.md)


### V.数据挖掘-机器学习开发

- 分类预测分析(监督学习)
- 回归分析
- 聚类分析(无监督学习)
- 关联规则与推荐
- 特征分析
- 时间序列分析(指数平滑)
- **机器学习**
- **深度学习&神经网络**

        Tips:主成分分析解决特征向量过多问题,选择主成分的特征向量


#### 6.1.挖掘建模-预测响应(分类)

分类是找出数据库中一组数据对象的共同特点并按照分类模式将其划分为不同的类，其目的是通过分类模型，将数据库中的数据项映射到某个给定的类别。它可以应用到客户的分类、客户的属性和特征分析、客户满意度分析、客户的购买趋势预测等

A. _决策树归纳_

- 构建分类模型
- 最佳决策树:NP完全问题 <br />
     多项式复杂程度的非确定性问题 <br />
- 决策树时间复杂度O(w)
- 大多数决策树采用自顶向下的递归划分方法

- 决策树算法

    1.CHAID:Chi-square Automatic Interaction Detector(卡方自动相互关系检测)<br />
         依据局部最优原则,利用*卡方检验*来选择对因变量(Category)最有影响的自变量
    2.CART: Classification and Regression Tree <br />
         分类与回归树,检验标准为Gini等不纯度指标
    3.ID3: Iterative Dichotomiser <br />你你你你你你
         迭代的二分器,其自变量的挑选标准是基于信息增益度量，即选择具有最高信息增益的属性作为结点的分裂属性
    4.C4.5: ID3的后继版 <br />
         其自变量的挑选标准是基于信息增益率(GainRatio)

        Tips:其核心的贪心算法指向局部最优选择，而非整体最优。
        不适用于连续型变量。需用线性回归算法解决

B. _模型过拟合OverFitting_ 

    - 训练误差与泛化误差
    - 模型拟合不足与模型过分拟合(model overfitting)
    - 训练误差低(训练场景)/泛化误差高(真实场景)
    - 一个假设在训练数据上能够获得比其他假设更好的拟合，但是在训练数据外的数据集 上却不能很好的拟合数据。此时我们就叫这个假设出现了overfit的现象。出现这种现象的主要原因是训练数据中存在噪音或者训练数据太少 <br />
    - 过分拟合场景
    - 解决决策树过分拟合(先剪枝/后剪枝)

C._规则分类器与最近邻分类器_

    - 规则分类与分组维度
    - 计算测试样例和所有训练样例的距离(或相似度),以确定最近邻列表Dz
    - 基于最近邻分类器的协同过滤推荐算法

E. _Logistic Regression逻辑回归(离散值分类)_

- 设计原理 <br />

        构造预测函数
        构造Cost函数
        找到J(θ)函数的最小值 - 梯度下降法

- 针对二元的目标变量,预测一组自变量数值相对应得因变量'是'的概率.确保二元目标变量的预测概率P是介于[0,1]之间的
- 变量筛选方法:向前引入法,向后剔除法,逐步回归法

F. _贝叶斯分类_

- 基于概率统计的分类算法
- 属性集与类变量的概率关系建模
- 朴素贝叶斯分类器(属性间条件独立)
- 检索算法Lucene - 权重定义

G. _神经网络 / DeepLearning_

- 感知器:多个输入结点/一个输出结点/隐藏层与隐藏结点
- 前向型网络 <br />
       从输入端传向输出端
- Backpropagation反馈型网络 <br />
       从输入端传向输出端 + 有回环或反馈存在
- 大多数神经网络模型的学习过程,都是通过不断地改变权重来使误差达到总误差的最小绝对值

H. _支持向量机算法(Support Vector Machine)_

- 最大边缘超平面
- 具有较大边缘的决策边界比那些具有较小边缘的决策边界具有更好的泛化误差
- 最优分类线
- 结构风险最小化SRM
- 线性SVM-最大化决策边界边缘的线性分类器
- 非线性SVM

I. _组合方法_

G. _细分建模_ 

- 针对细分群体分别建模是建模过程中常用的,有效模型优化

#### 6.2.挖掘建模-回归分析

回归分析方法反映的是事务数据库中属性值在时间上的特征，产生一个将数据项映射到一个实值预测变量的函数，发现变量或属性间的依赖关系，其主要研究问题包括数据序列的趋势特征、数据序列的预测以及数据间的相关关系等。可以应用到市场营销的各个方面

D. _Linear Regression线性回归_

- y=ax+b


#### 6.3.挖掘建模-关联规则分析

关联规则是描述数据库中数据项之间所存在的关系的规则，即根据一个事务中某些项的出现可导出另一些项在同一事务中也出现，即隐藏在数据间的关联或相互关系。

1. 找出所有 *频繁项集frequent itemset*
2. 由频繁项集产生强 *关联规则assoiation rule*
3. OLAP如何支持关联规则数据挖掘
4. Apriori算法-频繁项集 <br />
    基于支持度的剪枝技术
5. 多层关联规则 <br />
    支持度(有无意义)+置信度(相关可靠性): 衡量关联规则强度的重要指标 <br />
    一致支持度（设置困难）<br />
    多维关联规则 <br />


关联分析与决策树/规则分析的差异

    - 关联分析是多个项目的组合本身的情况(无分类相关),来分析项目间关联的紧密程度
    - 决策树/规则分析是行为路径进行数据分类,先指定规则分类,后进行分析


#### 6.4.挖掘建模-聚类分析

聚类分析是把一组数据按照相似性和差异性分为几个类别，其目的是使得属于同一类别的数据间的相似性尽可能大，不同类别中的数据间的相似性尽可能小。它可以应用到客户群体的分类、客户背景分析、客户购买趋势预测、市场的细分。

1. 针对目标群体进行多指标的群体划分,精细化运营,个性化运营 <br />
2. 不同产品的价值组合进行探测,发现孤立点和异常值 <br />

    - _划分方法(Partitioning Methods)_
    - _K-Means聚类算法-数据平均值_ <br />
      K个初始质心(中心点),K为所期望的cluster个数 <br />
      在K-means中，我们将中心点取为当前cluster中所有数据点的平均值 <br />
      二分K-Means <br />
    - _K-Medoids算法_ <br />
      从当前cluster中选取这样一个点——它到其他所有（当前cluster中的）点的距离之和最小——作为中心点 <br />
    - _层次方法(Hierarchical Methods)_ <br />
      凝聚层次聚类 <br />
      分裂层次聚类 <br />
    - _基于密度的方法(Density-Based Methods)_ <br />
       DBSCAN - 基于中心的密度进行点分类
    - _Cluster评估_
    - _基于网格的方法(Grid-Based Methods)_

3. 数据,Cluster和聚类算法的特性
4. 基于原型的聚类
5. 基于密度的聚类
6. 基于图的聚类
7. 可伸缩的聚类算法
x. 数据标准化是聚类分析中最重要的一个数据预处理步骤


#### 6.5.特征分析

特征分析是从数据库中的一组数据中提取出关于这些数据的特征式，这些特征式表达了该数据集的总体特征。

矩阵的重要特性——特征向量。


#### 6.6.分析应用-用户画像分析

- 用户行为<->行为分类与特征提取<->用户特征属性关联
- 用户特征与标签规则的关联概率(置信度)
- 用户与属性标签的可信度矩阵

#### 6.7.分析应用-文本分析算法

根据语义分析算法与NLP分词策略,针对文本进行标签分析

- 用户评价文本分析

- 评价模型

针对二元变量的分类模型的评价体系,例如用户评价分析

	1. 系列指标 

    -min- TP:True Positive
    -min- TN:True Negative
    -min- FP:False Positive
    -min- FN:False Negative

    -min- Accuracy
    -min- Error rate
    -min- Sensitivity
    -min- Specificity
    -min- Accuracy=Sensitivity+Specificity

	2. ROC曲线 
	   Receiver Operating Characteristic 曲线 

	3. KS值
	4. Lift值

- 商品类目内容分析

PLSA \ LDA \ HMM

- [相关文档](http://www.52nlp.cn/%E6%A6%82%E7%8E%87%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E5%8F%8A%E5%85%B6%E5%8F%98%E5%BD%A2%E7%B3%BB%E5%88%971-plsa%E5%8F%8Aem%E7%AE%97%E6%B3%95)


#### 6.8.数据挖掘算法技术实现

A. MATLAB

利用其简单的矩阵语言加工具箱函数来实现数据挖掘算法的示例。<br />
- Statistics Toolbox和Neural Networks Toolbox可以用来实现回归和分类；<br />
- Optimization Toolbox和Genetic Algorithm and Direct Search Toolbox可以帮助聚类算法进行最优化运算；<br />
- Fuzzy Logic Toolbox可以进行规则推理——这些都是显而易见的。<br />

上述工具箱是一些通用的工具，而下面这几个函数的"挖掘味儿"则似乎更浓一些。<br />
- kmeans() k-均值聚类 <br />
- treefit() 决策树回归或分类 <br />
- svmclassify() 支持向量机分类 <br />
- knnclassify() k-近邻分类 <br />
- crossvalind() 交叉验证试验 <br />

B.Python

C.R

D.Spark


### VI.大数据与机器学习

Spark MLlib


### VII.垂直业务数据建模

#### 7.1.电商零售分析模型

- 目标客户特征分析
- 预测（响应,分类）模型
- 主成分分析PCA

[新零售分析模型设计](2017-04-16-data-usage-new-retail-analytics-design-note.md)

#### 7.2.互联网用户行为分析模型

* GrowingIO
* 诸葛IO
* 神策数据


### VII.数据可视化

- selection: 删除或不突出某些对象和属性
- 少量属性的可视化 - 单维图表
- 扩展的二维/三维图 - 多维图表
- 可视化时间空间数据 - 时间维度+地理维度
- 可视化高维数据 <br />
     `数据矩阵` <br />
     `平行坐标系` <br />
     `星型坐标和Chernoff脸` <br />
- 词云图
- sunburst partition



### VIII.数据分析产品设计

#### 8.1.常规分析产品设计

1. 数据提取 

    - 网络Scrapy <br />
    - 云平台数据API <br />
    - 数据库数据 <br />
    - 大数据平台数据 <br />
    - 实时数据处理 <br />
    - Deep Web表单处理 <br />

2. 数据建模

    - 数据表关联信息定义
    - Cube数据建模    

3. 数据预处理 

    - ETL + Data Cleaning(数据质量监控)
    - SQL/存储过程/UDF
    - 数据同步
    - 定时任务

    - 分布式实时流式计算 
    - 分布式批处理计算 

> 当前数据分析产品将环节1,2,3打包进行敏捷可视化实现    

4. 大数据存储平台

    - 大数据平台Hadoop-HDFS&HBase等 / MPP(Greenplum&Vertica) / NoSQL数据库
    - 动态生成宽表
    - 数据库优化/Index创建/数据仓库设计

5. OLAP查询分析

    - OLAP Query Engine (支持SQL查询) <br />
    - 交互式MPP计算 <br />
    - 内存计算 - Spark <br />
    - 缓存查询AggregateCache

6. 数据可视化

    仪表盘设计 <br />
    可视化图表展示 <br />
    可视化时间空间数据 - 全局时间空间数据过滤 <br />
    多维图表可视化 <br />
    [D3](https://d3js.org/) <br />

7. 数据挖掘&建模预测

   - SQL / R / Python / Spark / Weka
   - 相关性分析等
   - 特征提取
   - 设计建模
   - 数据训练
   - 模型评估
   - 循环迭代

8. [OLAP架构优化设计](http://wiki.yunat.com/pages/viewpage.action?pageId=47520652)

9. [NewBI技术架构](_includes/NewBI-Platform.png)

x. [数据挖掘导图](_includes/DataMiningThinking.jpg)

#### 8.2.敏捷分析竞品分析

*敏捷BI-行业数据分析*

- [Tableau分析](http://www.tableau.com/products/cloud-bi)
- [Looker](http://www.looker.com/)
- [永洪BI](http://wiki.yunat.com/pages/viewpage.action?pageId=47515985)
- PowerBI
- [星环科技](http://wiki.yunat.com/pages/viewpage.action?pageId=45850523)
- [魔镜MagicWindow](http://wiki.yunat.com/pages/viewpage.action?pageId=46766678)
- [QuickBI](http://wiki.yunat.com/pages/viewpage.action?pageId=46766762)

*日志分析*

- [SENSORS Analytics](https://sensorsdata.cn/?ch=itjuzi)
- GrowingIO
- 诸葛IO
- Splunk


#### 8.3.数据发现数据

    1. 观察的存在和可用性
    2. 能够从观察中提取特征并对特征进行分类
    3. 能够有效地发现相关的历史背景 - 持久性上下文
    4. 能够对新的观察作出判断
    5. 当新的观察推翻先前的判断时，能够做出识别
    6. 能够积累和坚持主张
    7. 能够识别相关性/洞察力如何形成
    8. 能够通知相应实体的洞察力

### X.Reference

- 数据挖掘导论
- STAR SCHEMA:数据仓库维度设计权威指南
- The Data Warehouse ETL Toolkit (Kimball著)
- 数学之美(吴军)
- 大数据日知录
- 机器学习与数据挖掘-[加州理工学院公开课](http://open.163.com/special/opencourse/learningfromdata.html)
- [机器学习](http://open.163.com/special/opencourse/machinelearning.html)
