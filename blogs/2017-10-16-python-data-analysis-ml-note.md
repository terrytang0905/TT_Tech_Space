---
layout: post
category : technology
tags : [datascience,datamining,development]
title: Python Data Analysis&Machine Learning Note
---

Python数据分析&机器学习研究


#### Python基础

- List
- Tuple
- Dictionary
- Set

#### Python数据探索

1.数据质量分析

	

##### 数据特征分析

1.基础分析
	- 分布分析
	- 定性数据的分布分析
	- 对比分析
3.统计量分析
4.周期性分析
5.贡献度分析-帕累托分析
6.相关性分析

##### Python数据探索函数

1.NumPy

2.SciPy

3.scikit-learn: Machine Learning in Python

4.Pandas: Python Data Analysis Library

5.统计作图函数 - Matplotlib/Pandas

6.iPython

#### Python数据挖掘


#### ML&Tensorflow

分类或预测是机器学习的基石

逻辑回归分类器

wx+b=y -> softmax(y) -> D(S,L)交叉熵
多项式逻辑回归分类法

最小化交叉熵

用梯度下降法(计算偏导数) 训练-线性逻辑回归

通过线性逻辑回归的训练集 泛化能力

Kaggle

过拟合导致泛化能力下降

交叉验证用于验证深度学习中的过拟合问题

Rule 30
> 30000 Examples
Changes > 0.1% in accuracy 


机器学习方式:

- 基于已标记范例的学习:有监督的学习
- 发现某些模式：非监督的学习
- 正确或错误的反馈：增强式学习

Deeplearning: 同时兼容有监督的学习、非监督的学习和增强式学习

DNN: 深度神经网络

Convolutions ->(块+Depth)-> Classifier

只有把图片映射到不同类的信息保留


我们如何更迅速的训练一个大规模的神经网络？

	-开拓更多的并行结构
	-并行结构的模型
	-并行的数据结构

