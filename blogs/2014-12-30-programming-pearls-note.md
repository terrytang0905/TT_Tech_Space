---
layout: post
category : programming
tags : [develop, readnote]
title: Programming Pearls Study Note
---

## 编程珠玑 - 读书笔记
--------------------------------------------------

#### Thinking about 

位图数据结构 / dense set
Multiple-Pass算法
时间和空间之间的权衡 （减少程序空间同时也要求减少其运行时间）

运行时效率

#### Algorithm

二分查询 log2 n 
排序数组的二分查找

排序
二分查询
签名：用签名定义等价关系
mississippi i4mp2s4

顺序查找(n/2) VS 排序+二分查找

签名 -> 排序 -> 挤压
sign < dictionary | sort | squash > gramlist

#### Data Structure

编写生成器和模式
数组
构造数据

将重复性的代码改写到数组中
封装复杂的结构
使用高级数据结构工具 
让数据去构造程序

递归算法
tax(n)=tax(n-1)+(0.13+0.01*n)*(income-(2200+500n))

int binarysearch(DataType x[],int n)
{
	int l,u,m;
	l=0;
	u=n-1;
	while(l<=u){
		m=(l+u)/2;
		if(x[m]<t)
			l=m+1;
		else if(x[m]==t)
			return m;
		else 
			u=m-1;	
	}
	return -1;
}

调试与性能计时

二叉树
O(n logn)

设计性能优化汇总
- 算法和数据结构
- 算法优化
- 数据结构重组
- 系统独立性代码优化
- 系统依赖性代码优化
- 硬件

分解模块&降低耦合性以便于测试和确定性能

#### 封底计算/Fermi Approximations/快速计算

72法则 
time=y,interest=r% 
if(y*r=72) 
revener=revener * 2

数据库设计者 -> 读取和写入记录的时间

平均负载n,平均响应时间z+r,吞吐量x,利特尔法则n=x*(z+r)

阅读列表:

> * How To Lie With Stastics *
> * Innumeracy:Mathematical Illiteracy and Its Consequences *


#### 算法设计技术

二次算法

分治算法/二分算法
O(nlogn)

扫描算法/线性算法
maxsofar = 0
maxendinghere = 0
for i = [0,n)
	maxendinghere = max(maxendinghere + x[i],0)
	maxsofar = max(maxsofar,maxendinghere)
O(n)

保存状态/信息预处理到数据结构/分治算法/扫描算法/累积

阅读列表:

> * Introduction to Algorithm *
> * Code Complete *


#### 压缩空间


