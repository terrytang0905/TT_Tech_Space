---
layout: post
category : datascience
tags : [bigdata, database, architect]
title: Bigdata Database Architect Research Note
---

## Bigdata Database Architect Research Note
----------------------------------------------

### I.数据库架构

#### 通用数据库架构分析

-[How does a relational database work](http://coding-geek.com/how-databases-work/)

1._合并排序算法_

```java
array mergeSort(array a)

   if(length(a)==1)

      return a[0];

   end if

   //recursive calls

   [left_array right_array] := split_into_2_equally_sized_arrays(a);

   array new_left_array := mergeSort(left_array);

   array new_right_array := mergeSort(right_array);


   //merging the 2 small ordered arrays into a big one

   array result := merge(new_left_array,new_right_array);

   return result;
```

整体成本是 N*log(N) 次运算

2._Array与二维表_

	用阵列的话，你需要一个连续内存空间。如果你加载一个大表，很难分配足够的连续内存空间。

3._二叉树结构与索引_

- binary search tree查询的成本是log(N)
- B+Tree可支持range scan(范围查询)。查询成本为M+log(N)。 在B+树中,插入和删除操作是 O(log(N))复杂度。	

4._哈希表与HashJoin_

Hash取模运算。好的Hash函数时间复杂度是 O(1)

	* 一个哈希表可以只装载一半到内存，剩下的哈希桶可以留在硬盘上。

5._客户端管理器 Client Manager_

* 管理器首先检查你的验证信息（用户名和密码），然后检查你是否有访问数据库的授权。这些权限由DBA分配。
* 然后，管理器检查是否有空闲进程（或线程）来处理你对查询。
* 管理器还会检查数据库是否负载很重。
* 管理器可能会等待一会儿来获取需要的资源。如果等待时间达到超时时间，它会关闭连接并给出一个可读的错误信息。
* 然后管理器会把你的查询送给查询管理器来处理。
* 因为查询处理进程不是『不全则无』的，一旦它从查询管理器得到数据，它会把部分结果保存到一个缓冲区并且开始给你发送。
* 如果遇到问题，管理器关闭连接，向你发送可读的解释信息，然后释放资源。	

6._查询管理器 Query Manager_

* 查询首先被解析并判断是否合法
* 然后被重写，去除了无用的操作并且加入预优化部分
* 接着被优化以便提升性能，并被转换为可执行代码和数据访问计划。
* 然后计划被编译
* 最后查询被执行

7._查询解析器 Query Parser_

解析器要分析查询中的表和字段

- 表是否存在
- 表的字段是否存在
- 对某类型字段的 运算 是否 可能(比如，你不能将整数和字符串进行比较，你不能对一个整数使用substring()函数)

在解析过程中，SQL 查询被转换为内部表示（通常是一个树）

8._查询重写器 Query Rewriter_

* 预优化查询
* 避免不必要的运算
* 帮助优化器找到合理的最佳解决方案

查询重写部分规则:

	- 视图合并：如果你在查询中使用视图，视图就会转换为它的 SQL 代码。
	- 子查询扁平化：子查询是很难优化的，因此重写器会尝试移除子查询
	- 去除不必要的运算符：比如，如果你用了 DISTINCT，而其实你有 UNIQUE 约束（这本身就防止了数据出现重复），那么 DISTINCT 关键字就被去掉了。
	- 排除冗余的联接：如果相同的 JOIN 条件出现两次，比如隐藏在视图中的 JOIN 条件，或者由于传递性产生的无用 JOIN，都会被消除。
	- 常数计算赋值：如果你的查询需要计算，那么在重写过程中计算会执行一次。比如 WHERE AGE > 10+2 会转换为 WHERE AGE > 12 ， TODATE(“日期字符串”) 会转换为 datetime 格式的日期值。
	- (高级)分区裁剪(Partition Pruning):如果你用了分区表，重写器能够找到需要使用的分区。
	- (高级)物化视图重写(Materialized view rewrite):如果你有个物化视图匹配查询谓词的一个子集，重写器将检查视图是否最新并修改查询，令查询使用物化视图而不是原始表。
	- (高级)自定义规则：如果你有自定义规则来修改查询（就像 Oracle policy），重写器就会执行这些规则。
	- (高级)OLAP转换：分析/加窗 函数，星形联接，ROLLUP 函数……都会发生转换(但我不确定这是由重写器还是优化器来完成，因为两个进程联系很紧，必须看是什么数据库)

9._统计优化_

数据库统计用于预计数据库具体情况,可优化查询性能。

	* 表中行和页的数量
	* 表中每个列中的：
		唯一值
		数据长度（最小，最大，平均）
		数据范围（最小，最大，平均）
	* 表的索引信息

这些统计信息会帮助优化器估计查询所需的磁盘I/O、CPU、和内存使用。对每个列的统计非常重要,可判读列数据是否是唯一,还是重复数据	

高级统计叫直方图

	* 出现最频繁的值
	* 分位数 

统计信息必须及时更新,PostgerSQL统计

10._查询优化器 Query Optimizer - DB核心模块_

所有的现代数据库都在用*基于成本的优化*(即Cost-Based Optimization)来优化查询。<br/>
它是看语句的代价(Cost),这里的代价主要指Cpu和内存。优化器在判断是否用这种方式时,主要参照的是表及索引的统计信息。<br/>
**数据库优化器计算的是它们的 CPU 成本、磁盘 I/O 成本、和内存需求**。时间复杂度和 CPU 成本的区别是，时间成本是个近似值。而 CPU 成本，我这里包括了所有的运算，比如:加法、条件判断、乘法、迭代。<br/>
**多数时候瓶颈在于磁盘I/O(数据文件读写)而不是CPU使用**。

优化模式:

	- Rule：基于规则的方式。
	- Choose：默认的情况下Oracle用的便是这种方式。指的是当一个表或索引有统计信息，则走CBO的方式，如果表或索引没统计信息，表又不是特别的小，而且相应的列有索引时，那么就走索引，走RBO的方式。
	- FirstRows：它与Choose方式是类似的，所不同的是当一个表有统计信息时，它将是以最快的方式返回查询的最先的几行，从总体上减少了响应时间。
	- All Rows:也就是我们所说的Cost的方式，当一个表有统计信息时，它将以最快的方式返回表的所有的行，从总体上提高查询的吞吐量。没有统计信息则走RBO的方式。

* A.执行计划与扫描

	- 存取路径-获取数据的方式
	- 全扫描Full Scan(Sequential Scan) / Index Scan
	- 范围扫描 Range Scan /  索引范围扫描
	- 唯一扫描 Unique Scan
	- 根据ROW ID存取
	- 其他路径

由于所有存取路径的真正问题是磁盘I/O问题

* B.内关系与外关系(inner relation and outer relation)

	- 外关系是左侧数据集
	- 内关系是右侧数据集
	- 针对外关系的每一行
	- 查看内关系里的所有行来寻找匹配的行
	- 内关系必须是最小的，因为它有更大机会装入内存

* C.JOIN联接运算符

    - Nested Loop Join -算法需要 N + N*M 次访问(每次访问读取一行) – 大表JOIN小表

	* With Inner Sequential Scan(FullScan)
	* With Inner Index Scan

    - Hash Join -复杂度就是 O(M+N) – 类似大小的表join

	哈希联接的道理是：
	1) 读取内关系的所有元素
	2) 在内存里建一个哈希表
	3) 逐条读取外关系的所有元素
	4) (用哈希表的哈希函数)计算每个元素的哈希值，来查找内关系里相关的哈希桶内
	5) 是否与外关系的元素匹配
	6) 生成哈希表需要时间

    - Merge join -唯一产生排序的联接算法, O(N*Log(N) + M*Log(M))-需排序, O(N+M)-已排序,我们是只挑选相同的元素。道理如下：

	1) 在两个关系中，比较当前元素（当前=头一次出现的第一个）
	2) 如果相同，就把两个元素都放入结果，再比较两个关系里的下一个元素
	3) 如果不同，就去带有最小元素的关系里找下一个元素（因为下一个元素可能会匹配）
	4) 重复 1、2、3步骤直到其中一个关系的最后一个元素。

    - 联接运算算法选择:

	* 空闲内存：没有足够的内存的话就跟强大的哈希联接拜拜吧(至少是完全内存中哈希联接)。
	*  两个数据集的大小。比如，如果一个大表联接一个很小的表，那么嵌套循环联接就比哈希联接快，因为后者有创建哈希的高昂成本；如果两个表都非常大，那么嵌套循环联接CPU成本就很高昂。
	*  是否有索引：有两个B+树索引的话，聪明的选择似乎是合并联接。
	*  结果是否需要排序：即使你用到的是未排序的数据集，你也可能想用成本较高的合并联接（带排序的），因为最终得到排序的结果后，你可以把它和另一个合并联接串起来（或者也许因为查询用 ORDER BY/GROUP BY/DISTINCT 等操作符隐式或显式地要求一个排序结果）。
	*  关系是否已经排序：这时候合并联接是最好的候选项。
	*  联接的类型：是等值联接（比如 tableA.col1 = tableB.col2 ）？ 还是内联接？外联接？笛卡尔乘积？或者自联接？有些联接在特定环境下是无法工作的。
	*  数据的分布：如果联接条件的数据是倾斜的（比如根据姓氏来联接人，但是很多人同姓），用哈希联接将是个灾难，原因是哈希函数将产生分布极不均匀的哈希桶。
	*  如果你希望联接操作使用多线程或多进程。

* D.动态编程,启发式算法及贪婪算法

	- 完全动态编程 - O(3^N)
		它们都有相同的子树(A JOIN B),所以,不必在每个计划中计算这个子树的成本,计算一次,保存结果,当再遇到这个子树时重用。
	- 启发式算法 - 附加额外规则
	- 贪婪算法 -  算法的复杂度是 O(N*log(N))
		原理是按照一个规则(或启发)以渐进的方式制定查询计划。在这个规则下，贪婪算法逐步寻找最佳算法，先处理一条JOIN，接着每一步按照同样规则加一条新的JOIN。
	- 基因算法
	- [数据库JOIN查询算法](http://www.acad.bg/rismim/itc/sub/archiv/Paper6_1_2009.PDF)

	_SQLite优化器_

		使用Nested嵌套联接
		[N最近邻居](https://www.sqlite.org/queryplanner-ng.html) 贪婪算法

	_DB2优化器_

		使用所有可用的统计，包括线段树(frequent-value)和分位数统计(quantile statistics)。
		使用所有查询重写规则(含物化查询表路由，materialized query table routing),除了在极少情况下适用的计算密集型规则。
		使用动态编程模拟联接
			有限使用组合内关系（composite inner relation）
			对于涉及查找表的星型模式，有限使用笛卡尔乘积
		考虑宽泛的访问方式，含列表预取(list prefetch,注:我们将讨论什么是列表预取),index ANDing(注:一种对索引的特殊操作),和物化查询表路由。
		默认的，DB2 对联接排列使用受启发式限制的动态编程算法。

	默认的，DB2 对联接排列使用受启发式限制的动态编程算法。	

* E.查询计划缓存

10.1. _Pivotal Query Optimizer - first cost-based optimizer for Big Data_

[PQO_Doc](https://content.pivotal.io/blog/greenplum-database-adds-the-pivotal-query-optimizer)

![PQC-OrcaArch](_includes/Orca_arch.png)

10.2. _Legacy Query Optimizer - Greenplum_

Append-only Columnar Scan

10.3. _Genetic Query Optimizer - PostgerSQL_

[geqo_postgreSQL](https://www.postgresql.org/docs/9.6/static/geqo.html)



11._查询执行器 Query Executor_

12._数据管理器 Data Manager_

* 关系型数据库使用事务模型，所以，当其他人在同一时刻使用或修改数据时，你无法得到这部分数据。
* 数据提取是数据库中速度最慢的操作，所以数据管理器需要足够聪明地获得数据并保存在内存缓冲区内。

13._缓存管理器 Cache Manager_

* 数据库的主要瓶颈是磁盘 I/O。通过CacheManager提高性能,包括数据库IO写入性能/数据库查询性能<br/>
* 缓冲池是从内存读取数据显著地提升数据库性能。

* 预读

	- 当查询执行器处理它的第一批数据时
	- 会告诉缓存管理器预先装载第二批数据
	- 当开始处理第二批数据时
	- 告诉缓存管理器预先装载第三批数据，并且告诉缓存管理器第一批可以从缓存里清掉了

* 缓冲区置换策略-LRU算法

	- LRU-K页面置换算法
	- 2Q（类LRU-K算法）
	- CLOCK（类LRU-K算法）
	- MRU（最新使用的算法，用LRU同样的逻辑但不同的规则）
	- LRFU（Least Recently and Frequently Used，最近最少使用最近最不常用）

* 写缓冲区

	缓冲区保存的是页Page(最小的数据单位)而不是行 

14._事务管理器_

* ACID/ 并发控制/ 锁管理器/ 悲观锁/ 死锁
* 事务日志WAL/ 日志缓冲区/ STEAL 和 FORCE 策略/ 关于恢复

* WAL规则

	1)每个对数据库的修改都产生一条日志记录，在数据写入磁盘之前日志记录必须写入事务日志。
	2)日志记录必须按顺序写入；记录 A 发生在记录 B 之前，则 A 必须写在 B 之前。
	3)当一个事务提交时，在事务成功之前，提交顺序必须写入到事务日志。

* ARIES数据库恢复原型算法(Algorithms for Recovery and Isolation Exploiting Semantics) 

	1) 写日志的同时保持良好性能
	2) 快速和可靠的数据恢复

	日志结构

		- LSN：一个唯一的日志序列号（Log Sequence Number）。LSN是按时间顺序分配的 * ，这意味着如果操作 A 先于操作 B，log A 的 LSN 要比 log B 的 LSN 小。
		- TransID：产生操作的事务ID。
		- PageID：被修改的数据在磁盘上的位置。磁盘数据的最小单位是页，所以数据的位置就是它所处页的位置。
		- PrevLSN：同一个事务产生的上一条日志记录的链接。
		- UNDO：取消本次操作的方法。
			比如，如果操作是一次更新，UNDO将或者保存元素更新前的值/状态（物理UNDO），或者回到原来状态的反向操作（逻辑UNDO） **。
		- REDO：重复本次操作的方法。 同样的，有 2 种方法：或者保存操作后的元素值/状态，或者保存操作本身以便重复。
		- …:(供您参考，一个 ARIES 日志还有 2 个字段：UndoNxtLSN 和 Type）

	ARIES从崩溃中恢复有三个阶段

		1) 分析阶段：恢复进程读取全部事务日志，来重建崩溃过程中所发生事情的时间线，决定哪个事务要回滚（所有未提交的事务都要回滚）、崩溃时哪些数据需要写盘。
		2) Redo阶段：这一关从分析中选中的一条日志记录开始，使用 REDO 来将数据库恢复到崩溃之前的状态。
		3) Undo阶段：这一阶段回滚所有崩溃时未完成的事务。回滚从每个事务的最后一条日志开始，并且按照时间倒序处理UNDO日志（使用日志记录的PrevLSN）。

	ARIES提出了一个概念:检查点check point,就是不时地把事务表和脏页表的内容,还有此时最后一条LSN写入磁盘 


### II.分布式数据存储架构

#### 分布式算法

- CAP定理
- 一致性协议-2PC(Two-Phrase Commit)
- Vector Clock向量时钟:

	可用性>一致性 
	与每个对象的每个版本相关联。通过审查其向量时钟,我们可以判断一个对象的两个版本是平行分枝或有因果顺序

- 一致性协议-RWN协议:Write+Read>N
- 一致性协议-Paxos协议:一致性>可用性

	[介绍](http://www.jdon.com/artichect/paxos.html)
	Paxos是一个解决共识问题consensus problem的算法
	Paxos完成一次写操作需要两次来回，分别是prepare/promise, 和 propose/accept

- 一致性协议-Raft协议:一致性>可用性.

	用于日志复制/表数据的复制.[介绍](http://www.jdon.com/artichect/raft.html)

- MVCC多版本并行控制
- BloomFilter:带随机概率的bitmap,用于判断有序结构里是否存在指定的数据

	bitmap就是用每一位来存放某种状态，适用于大规模数据，但数据状态又不是很多的情况。通常是用来判断某个数据存不存在的

- SkipList:跳跃表
- LSM树 & LSM映射
- Merkle哈希树
- 一致性哈希(ConsistentHashing)
- 虚拟桶哈希(VirtualBucketsHashing)

	采用固定物理节点数量，来避免取模的不灵活性。<br/>
	采用可配置映射节点，来避免一致性hash的部分影响。<br/>
	支持动态扩容后对数据查询存储无影响。<br/>

- Cuckoo哈希:使用2个hash函数来处理碰撞,从而每个key都对应到2个位置
- Gossip协议
- 数据文件格式

	[Parquet文件格式](https://parquet.apache.org/documentation/latest/)

- 数据压缩算法

	Snappy
	LZSS
	GZ

- 数据传输与序列化

	[Avro序列化组件](https://avro.apache.org/docs/current/)
	[Thrift](http://thrift.apache.org/)

### III.分布式存储架构分析

#### 分析数据库设计

1.分析型数据库

	- 分布式架构设计-MPP
	- 一致性协调器(Paxos/Raft) - 类Zookeeper
	- LSM-Tree&LSM映射存储
	- 索引设计 - B+Tree/Bitmap
	- 查询管理器
	- meta管理与存储
	- SQL查询解析器(是否需要支持JOIN)/查询重写
	- 查询优化器(JOIN优化/数据重分布/broadcast)
	- 数据结构存储 - Column存储/倒排PostingList
	- 数据压缩算法 - Snappy等
	- 统计优化
	- 支持事务管理(原子锁/跨行事务/跨表)
	- 物化视图设计(view/project)
	- In-Database FullText/Data mining support(UDF)

2.OLAP设计

	- 大数据量数据Load接口
	- 多维数据分析 - ROLAP - Cube模型定义
	- MDX转换SQL/NoSQL解析器
	- 缓存管理器-聚合Cache设计
	- 内存计算/RealTime实时计算
	- 过滤器管理器
	- Batch历史数据查询
	- 数据排序处理
	- 格式化处理
	- 可视化数据展示 - E-chart/D3


1.[Greenplum架构解析](2017-02-11-greenplum-arch-design-note.md)

2.Impala与Greenplum性能差异成因

3.Google Dremel大数据分析数据库分析


### IV.BigTable&HBase架构

1.[BigTable&HBase分析笔记](2017-03-12-bigtable&hbase-analysis-note.md)

2.OceanBase数据库与分析数据库差别

### V.区块链

#### 区块链结构

### x.Ref

- [BigTable]()
- [Dremel]()

