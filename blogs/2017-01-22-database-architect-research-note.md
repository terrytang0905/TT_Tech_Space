---
layout: post
category : datascience
tags : [bigdata, database, architect]
title: Database Architect Research Note
---

Database Architect Research Note
----------------------------------------------

### 数据库架构分析

#### 通用数据库架构

-[How does a relational database work](http://coding-geek.com/how-databases-work/)

### 分布式数据存储架构

#### 分布式算法

- CAP定理
- 一致性协议-2PC(Two-Phrase Commit)
- Vector Clock向量时钟:
	可用性>一致性 
	与每个对象的每个版本相关联。通过审查其向量时钟,我们可以判断一个对象的两个版本是平行分枝或有因果顺序
- 一致性协议-RWN协议:Write+Read>N
- 一致性协议-Paxos协议:
	一致性>可用性.[介绍](http://www.jdon.com/artichect/paxos.html)
- 一致性协议-Raft协议:
	用于日志复制/表数据的复制.[介绍](http://www.jdon.com/artichect/raft.html)
- MVCC多版本并行控制
- BloomFilter:带随机概率的bitmap,用于判断有序结构里是否存在指定的数据
	bitmap就是用每一位来存放某种状态，适用于大规模数据，但数据状态又不是很多的情况。通常是用来判断某个数据存不存在的。
- SkipList:跳跃表
- LSM树
- Merkle哈希树
- Snappy&LZSS数据压缩算法
- 一致性哈希(ConsistentHashing)
- 虚拟桶哈希(VirtualBucketsHashing)
	采用固定物理节点数量，来避免取模的不灵活性。
	采用可配置映射节点，来避免一致性hash的部分影响。
	支持动态扩容后对数据查询存储无影响。
- Cuckoo哈希:使用2个hash函数来处理碰撞,从而每个key都对应到2个位置
- Gossip协议

#### 分布式存储产品分析