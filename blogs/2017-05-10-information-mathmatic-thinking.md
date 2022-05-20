---
layout: post
category : datascience
tags : [bigdata,datamining,algorithm]
title: Information&NLP&Mathematics Thinking
---

## 信息处理与数学应用研究
-----------------------------------------------

### 1Information,NLP,Mathematics

**NLP**

	- 文本特征向量VSM
	- 矩阵运算与SVD/LSA
	- 期望最大化EM算法
	- 最优化理论和方法
	- 文字识别-Tesseract-OCR
	- word2vec-词向量

**图像识别**

	- 图像处理的相关库-openCV
	- 基于PIL的相关库-pillow
	- SIFT算法
	- openCV+Keras+Tensorflow

**图片关键字提取**

**视频信息自动识别**

	- 信息指纹与关键帧识别

**广告分类识别**

**Search & Recommend & Advertising**




### 2.NLP文本分类识别

- 文本基础分词
- 将文本按主题分类
- 将词汇表中的字词按意思分类

- NLP based on rule 
- NLP based on statistics
- 从规则到统计
- Ambiguation(词义的二义性)Solution:
- 中文分词

[NLPIR](https://github.com/NLPIR-team/NLPIR)

_Ref:_

- [NLTK -- Natural Language Toolkit](http://www.nltk.org/book/)
- [Pattern]()
- [TextBlob -- Simplified Text Processing](http://textblob.readthedocs.org/en/dev/)
- Jieba: 结巴中文分词

#### 2.1.文本特征向量

1. 计算文本TF-IDF特征向量

文本-特征词-TD-IDF
特征向量代表特定文本

2. 统计向量间的余弦距离

用于定义文本间的相似性程度

3. 计算所有文本之间的余弦相似性,相似性大于阀值的文本合并为小类

4. 交叉验证 

5. 小类中文本作为一个整体,计算小类的特征向量,再计算小类间的余弦相似性,以此类推。

#### 2.2.矩阵运算与SVD

文本与词汇的矩阵

A=X*B*Y

	M = 文本中词典数100W(分词后)
	N = 文章数50W
	
	X = 文本词典数M x 词类
	B = 词类 x 文章分类
	Y = 文章分类 x 文章数N

#### 2.3.文本主题挖掘

1. LSA模型:潜在语义分析(Latent Semantic Analysis)

2. PLSI模型:概率潜在语义索引(Probabilistic Latent Semantic Indexing,PLSI)方法

   通过对文档生成的过 程进行概率建模来进行主题分析
   可以较容易地实现分布式求解

3. γ泊松(GaP)模型

4. LDA模型:潜在狄利克雷分配(Latent Dirichlet Allocation,LDA)方法

   PLSI的贝叶斯版本

5. 有监督主题模型

结合广告定向的情景，可以关注两种有监督主题模型。
	

	(1)有监督的 LDA(supervised LDA，sLDA)，这是在某种标签监督下进行主题 挖掘的通用模型，适用于标签为各种分布的情形。当标签为离散值时，就对应于根据某种 分类进行主题挖掘。
	(2)层次化的有监督的 LDA(Hierarchically Supervised LDA，HSLDA)。在此模 型中，标注的类型是一个 Hierarchy 上的层次标签，这非常契合于广告中的需求。关于这 方面的具体技术可以参考上面提到的文献。


#### 2.4.期望最大化EM算法

EM算法就是为了解决有隐变量存在时的最大似然估计问题的。这是一种迭代的算法，每个迭 代又可以分为 E-step 和 M-step。在 E-step 阶段，将参数变量和观测变量都固定，得到隐 变量的后验分布;在 M-step 阶段，用得到的隐变量的后验分布和观测变量再去更新参数 变量。

文本自收敛分类

    - 定义最大化函数
    - 模型训练
    - 迭代收敛模型

#### 2.5.神经网络-word2vec

CBOW与Skip-Gram用于神经网络语言模型

基于Hierarchical Softmax的模型概述

基于Negative Sampling的模型概述

#### 2.6.Tesseract-OCR



### 3.图像&视频识别分类识别分

关键帧的提取和特征的提取

#### 3.1.openCV+pillow

**图片对比**

直方图计算法

感知哈希算法是一类算法的总称，包括aHash、pHash、dHash。顾名思义，感知哈希不是以严格的方式计算Hash值，而是以更加相对的方式计算哈希值，因为“相似”与否，就是一种相对的判定。

基本原理如下：

	1. 把图片转成一个可识别的字符串，这个字符串也叫哈希值
	2. 和其他图片匹配字符串


**aHash算法(平均哈希法)**

	速度比较快，但是常常不太精确。

**pHash算法(余弦变换感知哈希算法)**

	精确度比较高，但是速度方面较差一些。

**dHash算法(均值感知哈希算法)**

	Amazing！精确度较高，且速度也非常快。因此我就选择了dHash作为我图片判重的算法。

#### 3.2.openCV+SIFT

SIFT=Scale Invariant Feature Transform(尺度不变特征变换)

	SIFT特征对旋转、尺度缩放、亮度变化等保持不变性，是一种非常稳定的局部特征。

SIFT的4个主要步骤

	1. 尺度空间的极值检测 搜索所有尺度空间上的图像，通过高斯微分函数来识别潜在的对尺度和选择不变的兴趣点。
	2. 特征点定位 在每个候选的位置上，通过一个拟合精细模型来确定位置尺度，关键点的选取依据他们的稳定程度。
	3. 特征方向赋值 基于图像局部的梯度方向，分配给每个关键点位置一个或多个方向，后续的所有操作都是对于关键点的方向、尺度和位置进行变换，从而提供这些特征的不变性。
	4. 特征点描述 在每个特征点周围的邻域内，在选定的尺度上测量图像的局部梯度，这些梯度被变换成一种表示，这种表示允许比较大的局部形状的变形和光照变换。

核心关键:

	- DoG尺度空间的极值检测
	- 删除不稳定的极值点
	- 确定特征点的主方向
	- 生成特征点的描述点

#### 3.3.openCV+Keras+Tensorflow

验证码CAPTCHAs图片识别

a.创立数据集

python3 extract_single_letters_from_captchas.py

b.训练神经网络识别

python3 train_model.py

c.利用模型识别CAPTCHAs

python3 solve_captchas_with_model.py



### 4.Data Mining-

大数据量与维度诅咒

1.将数据模型限定在特定模型之下

线性模型/正态分布/隐型马氏过程

2.通过数据的特殊结构 - 降维处理

#### 


### IX.Reference

- 数学之美(吴军)
- [Python开发Dev笔记](2017-10-06-python-dev-everything-note.md)
- [FullTextSearch研究思考](2014-12-20-fulltext-search-design-thinking.md)
