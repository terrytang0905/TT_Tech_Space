---
layout: post
category : technology
tags : [datascience,datamining,development]
title: Python Image Recognition Note
---

Python图像识别研究


#### 研究方案

- 图像处理的相关库-openCV
- 基于PIL的相关库-pillow
- SIFT
- openCV+Keras+Tensorflow

#### 1.openCV+pillow

直方图计算法

平均哈希法(aHash)

感知哈希算法(pHash)

dHash算法

#### 2.openCV+SIFT

Scale Invariant Feature Transform:尺度不变特征变换


#### 3.openCV+Keras+Tensorflow

3.1.创立数据集

python3 extract_single_letters_from_captchas.py

3.2.训练神经网络识别

python3 train_model.py

3.3.利用模型识别CAPTCHAs

python3 solve_captchas_with_model.py



