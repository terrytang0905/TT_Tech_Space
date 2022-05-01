---
layout: post
category : bigdata
tags : [bigdata, architect, database]
title: Big Data Research Note - Distributed Database Architect
---

## 大数据研究-分布式数据架构
--------------------------------------------------------

导读:A one size fits all database doesn't fit anyone

![BigDataDBMap](_includes/BigData&CAP.jpg)

### I.分布式数据存储架构

![BigDataStorage1](_includes/Distribute_DataStorage1.png)
![BigDataStorage2](_includes/Distribute_DataStorage2.png)
![BigDataStorage2](_includes/Distribute_DataStorage3.png)

#### II.分布式算法

**一致性**

数据一致性通常指关联数据之间的逻辑关系是否正确和完整。而数据存储的一致性模型则可以认为是存储系统和数据使用者之间的一种约定。如果使用者遵循这种约定，则可以得到系统所承诺的访问结果常用的

一致性模型有：

	a、严格一致性（linearizability, strict/atomic Consistency）：读出的数据始终为最近写入的数据。这种一致性只有全局时钟存在时才有可能，在分布式网络环境不可能实现。
	b、顺序一致性（sequential consistency）：所有使用者以同样的顺序看到对同一数据的操作，但是该顺序不一定是实时的。
	c、因果一致性（causal consistency）：只有存在因果关系的写操作才要求所有使用者以相同的次序看到，对于无因果关系的写入则并行进行，无次序保证。因果一致性可以看做对顺序一致性性能的一种优化，但在实现时必须建立与维护因果依赖图，是相当困难的。
	d、管道一致性（PRAM/FIFO consistency）：在因果一致性模型上的进一步弱化，要求由某一个使用者完成的写操作可以被其他所有的使用者按照顺序的感知到，而从不同使用者中来的写操作则无需保证顺序，就像一个一个的管道一样。 相对来说比较容易实现。
	e、弱一致性（weak consistency）：只要求对共享数据结构的访问保证顺序一致性。对于同步变量的操作具有顺序一致性，是全局可见的，且只有当没有写操作等待处理时才可进行，以保证对于临界区域的访问顺序进行。在同步时点，所有使用者可以看到相同的数据。
	f、释放一致性（release consistency）：弱一致性无法区分使用者是要进入临界区还是要出临界区， 释放一致性使用两个不同的操作语句进行了区分。需要写入时使用者acquire该对象，写完后release，acquire-release之间形成了一个临界区，提供 释放一致性也就意味着当release操作发生后，所有使用者应该可以看到该操作。
	g、最终一致性（eventual consistency）：当没有新更新的情况下，更新最终会通过网络传播到所有副本点，所有副本点最终会一致，也就是说使用者在最终某个时间点前的中间过程中无法保证看到的是新写入的数据。可以采用最终一致性模型有一个关键要求：读出陈旧数据是可以接受的。
	h、delta consistency：系统会在delta时间内达到一致。这段时间内会存在一个不一致的窗口，该窗口可能是因为log shipping的过程导致。这是书上的原话。。我也搞不很清楚。。 数据库完整性（Database Integrity）是指数据库中数据的正确性和相容性。数据库完整性由各种各样的完整性约束来保证，因此可以说数据库完整性设计就是数据库完整性约束的设计。包括实体完整性。域完整性。参照完整性。用户定义完整性。可以主键。check约束。外键来一一实现。这个使用较多

- 一致性协议-2PC(Two-Phrase Commit)
- Vector Clock向量时钟:

	可用性>一致性 
	与每个对象的每个版本相关联。通过审查其向量时钟,我们可以判断一个对象的两个版本是平行分枝或有因果顺序

- 一致性协议-RWN协议:Write+Read>N
- 一致性协议-Paxos协议:一致性>可用性

	Paxos是一个解决共识问题consensus problem的算法
	[介绍](http://www.jdon.com/artichect/paxos.html)
	Paxos完成一次写操作需要两次来回，分别是prepare/promise, 和propose/accept
	基于Paxos的数据一致性同步Zookeeper

	Paxos算法是莱斯利·兰伯特（Leslie Lamport，就是LaTeX 中的”La”，此人现在在微软研究院）于1990年提出的一种基于消息传递的一致性算法。这个算法被认为是类似算法中最有效的。
	Paxos 算法解决的问题是一个分布式系统如何就某个值(决议)达成一致。一个典型的场景是，在一个分布式数据库系统中，如果各节点的初始状态一致，每个节点执行相同的操作序列，那么他们最后能得到一个一致的状态。为保证每个节点执行相同的命令序列，需要在每一条指令上执行一个“一致性算法”以保证每个节点看到的指令一致。

	一个通用的一致性算法可以应用在许多场景中，是分布式计算中的重要问题。因此从20世纪80年代起对于一致性算法的研究就没有停止过。
	节点通信存在两种模型:共享内存(Shared memory)和消息传递(Messages passing)。Paxos算法就是一种基于消息传递模型的一致性算法。

![paxos](_includes/paxos.png)

- 一致性协议-ZooKeeperAtomicBroadcast(Paxos变形)
- 一致性协议-Raft协议:一致性>可用性.

	Raft是由Stanford提出的一种更易理解的一致性算法，意在取代目前广为使用的Paxos算法。目前，在各种主流语言中都有了一些开源实现，比如本文中将使用的基于JGroups的Raft协议实现。

	用于日志复制/表数据的复制.[介绍](http://www.jdon.com/artichect/raft.html)

	在Raft中，每个结点会处于下面三种状态中的一种：
		follower：所有结点都以follower的状态开始。如果没收到leader消息则会变成candidate状态
		candidate：会向其他结点“拉选票”，如果得到大部分的票则成为leader。这个过程就叫做Leader选举(Leader Election)
		leader：所有对系统的修改都会先经过leader。每个修改都会写一条日志(log entry)。leader收到修改请求后的过程如下，这个过程叫做日志复制(Log Replication)：
		复制日志到所有follower结点(replicate entry)
		大部分结点响应时才提交日志
		通知所有follower结点日志已提交
		所有follower也提交日志
		现在整个系统处于一致的状态

**CAP定理&BASE模型**

	Consistency/Availability/Partition tolerance
	
	Partition tolerance:网络分区的情况下，被分隔的节点仍能正常对外服务
	
	BASE模型反ACID模型，完全不同ACID模型，牺牲高一致性，获得可用性或可靠性：
	Basically Available基本可用。支持分区失败(e.g. sharding碎片划分数据库)
	Soft state软状态 状态可以有一段时间不同步，异步。
	Eventually consistent最终一致，最终数据是一致的就可以了，而不是时时高一致。

**并行化隔离算法:MVCC(MultiVersion Concurrency Control)多版本并发控制**

    PostgreSQL实现基于MVCC的快照级别隔离(Snapshot isolation),支持读-提交级别隔离。
    快照级别隔离的口号"读写互不干扰"

**可串行化的快照隔离**

**串行化隔离算法:two-phase locking,2PL**

    2PL不仅在并发写操作之间互斥,读取也会和修改产生互斥。
    性能下降:其事务吞吐量和查询响应时间相比于其他弱隔离级别下降非常多

**分布式事务-共识算法:two-phase commit,2PC**

![two_phase_commit_explain](_includes/two_phase_commit_explain.png)

    原子提交:一种在多节点之间实现事务原子提交的算法,用来确保所有节点要么全部提交    

**Bitmap**

	- bitmap可以理解为通过一个bit数组来存储特定数据的一种数据结构，每一个bit位都能独立包含信息，bit是数据的最小存储单位
	- bitmap就是用每一位来存放某种状态，适用于大规模数据，但数据特征分类又不是很多的情况(10-100)。通常是用来判断某个数据存不存在的,例如异常IP等
	- 统计一个对象的基数值(1亿)需要12M，如果统计10000个对象，就需要将近120G了，同样不能广泛用于大数据场景。

**BloomFilter**

	带随机概率(哈希函数)的bitmap,用于判断有序结构里是否存在指定的数据
	Bloom Filter靠多个哈希函数将集合映射到位数组中,判断元素数据是否存在

**HyperLogLog:DISTINCT近似值算法**

	- 分桶平均
	- 偏差修正
	- [redis new data structure](http://antirez.com/news/75)

**GeoHash算法**

	- 根据经纬度计算GeoHash二进制编码

**SkipList-跳跃表**

**LSM树 & LSM映射**

	- Log-Structured Merge Tree
	- LSM树原理把一棵大树拆分成N棵小树，它首先写入内存中，随着小树越来越大，内存中的小树会flush到磁盘中，磁盘中的树定期可以做merge操作，合并成一棵大树，以优化读性能。

**Merkle哈希树**

	- 默克尔树（又叫哈希树）是一种Hash二叉树，由一个根节点、一组中间节点和一组叶节点组成。最下面的叶节点包含存储数据或其哈希值，每个中间节点是它的两个孩子节点内容的哈希值，根节点也是由它的两个子节点内容的哈希值组成。
	- 据称哈希树经常应用在一些分布式系统或者分布式存储中的反熵机制(Anti-entropy),也有称做去熵的.这些应用包括Amazon的Dynamo 还有Apache的Cassandra数据库, 通过去熵可以去做到各个不同节点的同步, 即保持各个节点的信息都是同步最新.
	- 区块链的核心存储就是基于Merkle哈希树

**一致性哈希(ConsistentHashing)**

**虚拟桶哈希(VirtualBucketsHashing)**

	采用固定物理节点数量，来避免取模的不灵活性。
	采用可配置映射节点，来避免一致性hash的部分影响。
	支持动态扩容后对数据查询存储无影响。
	Couchbase采用该算法实现分布式数据查询

**Cuckoo哈希**

	使用2个hash函数来处理碰撞,从而每个key都对应到2个位置

**Gossip协议**

	Gossip算法如其名，灵感来自办公室八卦，只要一个人八卦一下，在有限的时间内所有的人都会知道该八卦的信息，这种方式也与病毒传播类似，因此Gossip有众多的别名“闲话算法”、“疫情传播算法”、“病毒感染算法”、“谣言传播算法”。
	但Gossip并不是一个新东西，之前的泛洪查找、路由算法都归属于这个范畴，不同的是Gossip给这类算法提供了明确的语义、具体实施方法及收敛性证明。
	Gossip算法又被称为反熵(Anti-Entropy),熵是物理学上的一个概念，代表杂乱无章，而反熵就是在杂乱无章中寻求一致，这充分说明了Gossip的特点：在一个有界网络中，每个节点都随机地与其他节点通信，经过一番杂乱无章的通信，最终所有节点的状态都会达成一致。每个节点可能知道所有其他节点，也可能仅知道几个邻居节点，只要这些节可以通过网络连通，最终他们的状态都是一致的，当然这也是疫情传播的特点。
	要注意到的一点是，即使有的节点因宕机而重启，有新节点加入，但经过一段时间后，这些节点的状态也会与其他节点达成一致，也就是说，Gossip天然具有分布式容错的优点。

**消息机制**

	消息的编解码方式 
	消息传递机制(ZeroMQ/RabbitMQ/RocketMQ)

**数据文件格式**

	- SequenceFile
	- RCFile 
	- ApacheORC = OptimizeRC
	- AliORC
	- [Parquet文件格式](https://parquet.apache.org/documentation/latest/)
	- CarbonData(华为开源)

**数据压缩算法**

	- Snappy 
	- LZSS 
	- GZ 

**数据传输与序列化**

- [Avro序列化组件](https://avro.apache.org/docs/current/) 
- [Thrift](http://thrift.apache.org/) 
- [ProtocalBuffer](http://code.google.com/p/protobuf) 


### III.分布式数据架构

分布式数据架构的整个框架是非常稳定的,主流的数据架构都是由存储引擎,执行引擎,网络交互和查询优化器组成的

主要用于以下4种分析场景
- reporting/dashboard: 百千级别query,ms延时,插入更新upsert数据多,实时,filters,aggregation类似操作
- embedded statics/data service: 在线服务/simply query & high qps,百万级别/qps实时更新
- ad-hoc analysis: 复杂查询在trillion data下即席查询分析,snowflake云端数据仓库
- monitoring: 内存时序分析


#### A.Distributed OLTP-分布式关系型数据库

- 1.Spanner

Spanner是一个Google开发的支持分布式读写事务，只读事务的分布式存储系统，只读事务不加任何锁。和其他分布式存储系统一样，通过维护多副本来提高系统的可用性。

一份数据的多个副本组成一个paxos group，通过paxos协议维护副本之间的一致性。对于涉及到跨机的分布式事务，涉及到的每个paxos group中都会选出一个leader，来参与分布式事务的协调。这些个leader又会选出一个大leader，称为coordinator leader，作为两阶段提交的coordinator，记作coordinator leader。其他leader作为participant。

数据库事务系统的核心挑战之一是并发控制协议(通用实现MVCC)。Spanner的读写事务使用两阶段锁来处理。

- 2.OceanBase分布式数据库

OceanBase底层架构实现LSM/分布式ACID等特征

- 3.[TiDB分布式数据库](2019-07-08-tidb-oltp-olap-design.md)

基于Spanner的TrueTime机制来解决不同时区数据一致性问题

- 4.TiKV分布式存储


#### B.分析型数据库设计-MPP

- 1.数据分析性需求对IT能力的要求包括:

	- 复杂分析查询能力
	- 批量数据处理
	- 一定的并发访问能力
	- 大规模Sacle-Out数据扩展

- 2.OLAP场景下的分析型数据仓库

	- 一致性协调器(Paxos/Raft) - 类Zookeeper
	- LSM-Tree&LSM映射存储
	- 索引设计 - B+Tree/Bitmap/FullText Index
	- 查询管理器
	- meta管理与存储
	- SQL查询解析器(是否需要支持JOIN)/查询重写
	- 查询优化器(JOIN优化/数据重分布/broadcast)
	- 数据存储格式 - 倒排PostingList/Column存储(Dremel数据存储格式)
	- 数据压缩算法 - Snappy等
	- 统计优化
	- 支持事务管理(原子锁/跨行事务/跨表)
	- 物化视图设计(view/project)
	- In-Database FullText Engine - 参考ELK
	- Data mining support(UDF)

- 3.[Greenplum架构解析](2017-02-11-greenplum-arch-design-note.md)

	- 第一款成熟的开源分布式分析型数据库

- 4.[Vertica数据库结构]()

#### C.Hadoop离线批处理(MapRedure->Spark)

总的来说，其架构的着力点在于数据高吞吐处理能力，在事务方面相较MPP更简化，仅提供粗粒度的事务管理.

Hadoop具备MPP所缺失的批量任务调整能力，数据的多副本存储使其具有更多“本地化”数据加工的备选节点，而且数据加工处理与数据存储并不绑定，可以根据节点的运行效率动态调整任务分布，从而在大规模部署的情况下具有整体上更稳定的效率。相比之下，MPP在相对较小的数据量下具有更好的执行效率。


#### MPP并行计算 vs 批处理计算 

- 1.MPP设计

MPP最开始的设计目的是为了消除共享资源的使用，即每个executor有独立的cpu、内存和磁盘等资源，每个executor一般不能访问其他executor的资源。但是有一种情况例外，那就是当数据必须要通过网络进行交换的时候(即Redistribute/shuffle)。

- 2.MPP的核心问题

	- 遇到的最大问题就是“落后者”(straggler)。
	如果某个节点在执行任何任务时都比其他的节点慢，那么不管集群规模多大，整体的执行性能都会由这个“有问题”的节点决定了。
	- 等集群到了一定规模，MPP系统总是会有那么一个节点发生磁盘阵列故障，这就会导致集群整体性能下降。这就是为什么几乎所有的MPP系统的单集群大小不会超过50台服务器。

MPP和MapReduce批处理架构的另外一个显著不同则在于并发(concurrency)方面。并发是指可以有效的同时运行的查询数（译者注：MPP一般面向即系查询业务，所以响应时间一般在秒级。所谓有效，就是说这些查询可以在用户可以接受的查询时间内返回，如果并发查询数很高，但是每个查询都需要等几个小时，那就不叫有效查询了）。MPP是完全“对称的”，即**当查询开始执行时，每个节点都在并行的执行完全相同的任务,就是说MPP支持的并发数和集群的节点数没有关系**。例如，4个节点的集群和400个节点的集群支持的并发查询数是相同的，随着并发数增加，这二者几乎在相同的时间点出现性能骤降。

![mpp_system_throughput](_includes/mpp_system_throughput.png)

	Tips:10-18个并发sessions(大查询)时，系统总的吞吐量最大。
	如果并发数上升到20以上，总吞吐就会下降到最大吞吐的70%
	(这里吞吐量是这样定义的:相同类型(比如都是groupby,或者都是join查询)的查询在固定时间段内完成执行的个数） 
	- MPP对小查询的并发处理基本可用,原因在于查询时间短,对系统的负载要求较低.


- 3.批处理设计

这类系统的主要思想是:原本在两个同步点之间是单task执行，现在则被切分成多个独立的“task”，而task的总数则和executor的总数无关。

举例来说明，HDFS上运行的MapReduce任务，task数等于总的split数(split数和要处理的HDFS文件的Block总数相同)。

	在两个同步点之间，这些任务被随机的分配到空闲的executor上;
	Hadoop-/**计算与存储分离+共享存储**/)
	这就和MPP不同了,MPP的task是和存储这个task要处理的数据的节点绑定的
	MPP-/**计算与存储绑定**/)。

MapReduce的同步点包括的job的启动、shuffle以及job的停止；对spark而言则是job的启动、shuffle、数据缓存和job停止。

**共享存储和细粒度(task级别调度)**结合,使得批处理系统在扩展性方面优于MPP，批处理系统的集群规模往往可以扩展到几千的节点和几万的磁盘的级别。

共享存储在处理一块数据,不需要让数据一定要存储在某个特定的节点，需要这块数据时，可以从集群中其他节点那里获取到。当然了,_Remote远程操作涉及网络和磁盘IO，有一定代价，所以计算框架会尝试优先处理本地存储的数据_。但是在“degraded”场景下，推测执行可以有效缓解性能下降问题。

- 4.批处理的问题

	- 如果在一个单独的executor中串行的处理不相关的task,就必须把中间结果写到本地磁盘上,以便下一个执行步骤能开始消费本步骤的数据。
	- 而MPP中，不需要把中间结果写入磁盘，因为每个executor处理一个task，所以数据可以直接“流入”下一执行阶段进行处理，这就是所谓的pipeline执行,性能非常可观。


- 5.MPP&批处理的差异

	- MPP按照关系数据库行列表方式存储数据(有模式)，Hadoop按照文件切片方式分布式存储(无模式)

		Tips:MPP数据库的数据存储格式要求严于分布式文件存储格式

	- 两者采用的数据分布机制不同，MPP采用Hash分布，计算节点和存储紧密耦合，数据分布粒度在记录级的更小粒度(一般在1k以下)；Hadoop FS按照文件切块后随机分配，节点和数据无耦合，数据分布粒度在文件块级（缺省64MB）。
	- MPP采用SQL并行查询计划，Hadoop批处理多采用Mapreduce框架

- 6.MPP&批处理各自缺陷

_MPP缺陷总结_

	- 批处理下的Straggler(落伍者)
		无论集群规模多大，批处理的整体执行速度都由Straggler决定，其他节点上的任务执行完毕后则进入空闲状态等待Straggler，而无法分担其工作
	- 多并发的性能瓶颈(对OLTP支持不好)
		由于MPP的“完全对称性”，即当查询开始执行时，每个节点都在并行的执行完全相同的任务，这意味着MPP支持的并发数和集群的节点数完全无关。
	
	Tips:为了规避MPP并发访问上的缺陷以及批量任务对联机查询的影响,通常会将数据按照应用粒度拆分到不同的单体OLTP数据库(PostgreSQL)或小型MPP数据库中以支持联机并发查询。即多个OLTP(PostgerSQL)+1个OLAP(Greenplum)

_批处理缺陷总结_

	- 批量加工效率较低(需要不停阶段性写磁盘)
	- 不能无缝衔接EDW实施方法论(不容易增量更新)
	- 联机查询(SQL on Hadoop)并发能力不足(对OLTP场景支持不好)
	
	Tips:在大体相同的数据量和查询逻辑情况下,Impala并发效果会低于GPDB

#### B+C.MPP+Hadoop

- 1.[Apache HAWQ](http://hawq.incubator.apache.org/)

HAWQ is a Hadoop native SQL query engine that combines the key technological advantages of MPP database with the scalability and convenience of Hadoop. HAWQ reads data from and writes data to HDFS natively.

![hawq_arch](_includes/hawq_architecture_components.png)

    - OushuDB数据库是实现HAWQ架构的商业版

- 2.Huawei FusionInsight+GuassDB 200

    FusionInsight改名为Huawei MRS
    GuassDB 200可以理解为Greenplum的商业改良版

- 3.[Lakehouse on Cloud](2020-06-06-bigdata-research-lake-house-solution.md)

- Ref:[云端大数据产品分析](2019-03-12-bigdata-research-common-product-solution.md)

#### B&C.分析型OLAP on Cloud - Cloud DataWareHouse

- 1.Snowflake-Cloud DataWarehouse

- 2.AWS Redshift-Cloud DataWarehouse

    支持PB级别的OLAP数据库

    - 列式数据存储：Amazon Redshift 以列组织数据，并非以一系列的行来存储数据。与适用于事务处理的基于行的系统不同，基于列的系统适用于数据仓库存储及分析，在此系统下，查询经常涉及到对大型数据集进行聚合。由于仅对涉及查询的列进行处理，且列式数据顺序存储在存储介质上，故基于列的系统所需的 I/O 要少得多，从而显著提高了查询性能。
    - 高级压缩：与基于行的数据存储相比，列式数据存储可进行更大程度的压缩，因为类似的数据是按顺序存储在硬盘上。Amazon Redshift 拥有多种压缩技术，与传统的关系数据存储相比，经常可进行很大程度的压缩。此外，与传统的关系数据库系统相比，Amazon Redshift 不需要索引或具体化视图，因此使用的空间较少。将数据加载到空表中时，Amazon Redshift 自动对您的数据进行采样并选择最合适的压缩方案。
    - 大规模并行处理 (MPP)：Amazon Redshift 在所有节点之间自动分配数据及查询负载。Amazon Redshift 可轻松将节点添加至您的数据仓库，而且随着您的数据仓库规模的扩大，仍能维持快速的查询性能。


- 3.Google BigQuery(Dremel)-Cloud Analytics Services

- 4.AliCloud MaxCompute+Hologres-Cloud Serverless DataWarehouse

- 5.[下一代OLAP引擎思考](2021-05-05-bigdata-analytics-olap-next-generation-note.md)


#### D.BigTable-KV数据存储架构

**基础特征:**

    - 大多基于LSM-Tree的大规模稀疏表 
    - 适合海量数据的KV类似查询
    - 支持多并发查询分析

- 1.[BigTable&HBase分析笔记](2017-03-12-bigtable&hbase-analysis-note.md)

    - 大数据量存储,大数据量高并发操作 
    - 需要对**数据随机读写操作**
    - 读写访问均是非常简单的操作

    MegaStore

- 2.DynamoDB-KV数据库(Amazon)

- 3.Cassandra开源数据库(Facebook)

    DataStax维护


#### D+.InMemory-KV内存数据库

- 1.Redis

- 2.Couchbase

- 3.Ignite

- 4.Monarch


#### E.Document文档数据库

- 1.[MongoDB数据库](2015-10-11-mongodb3-major-release.md)

- 2.Azure DocumentDB数据库(Microsoft)

#### MongoDB&DocumentDB对比

DocumentDB的某些优势

- PaaS：DocumentDB是直接以PaaS提供的。这样带来的好处是配置、管理、维护都更为简单。MongoDB则需要自行部署到VM中，需要花费成本运维。由于PaaS有诸多好处，作者都建议即使要使用MongoDB都最好使用第三方搭建好的现成PaaS。
- 伸缩能力：由于DocumentDB是PaaS驱动的架构，所以其处理水平扩展的方式和MongoDB完全不同。DocumentDB分区后无需管理复制，MongoDB还需同时处理复制。这点也是得利于DocumentDB后台依赖于Azure的伸缩能力。
- 原生REST接口：虽然两者都为开发人员提供了多种语言的SDK，但是DocumentDB是原生提供REST接口的，其实SDK也是REST接口的包装。相反，MongoDB没有原生REST接口，不过其有Wire协议和元数据驱动（基于TCP），可以语言无关的访问到数据。不过在有些情况下基于HTTP的REST接口显然更加方便（比如物联网）。
- 数据交换格式：DocumentDB使用JSON更加标准（RFC 7159 和 ECMA-404）。
- 索引处理：两者虽然都是基于B-Tree来进行索引，不过DocumentDB提供了两类索引Hash和Range，Range暂时不支持时间字段的索引，DocumentDB也不支持地理位置信息的索引而是依靠Azure Search来解决这个问题。从产品的角度看，在这点上MongoDB具备优势，不过实际使用过程中不会有太大的问题。
- 异步处理：由于DocumentDB原生提供REST接口，而这些接口或者.NET SDK都提供了async/await的支持，以提供并发处理能力。
- 定价：虽然MongoDB是开源免费，不过运维的费用也不会少。DocumentDB是基于使用量付费，不过费用不高，且可以通过DreamSpark和BizSpark来获取Azure免费订阅。
- 一致性：MongoDB的一致性可以配置来是否启用一致性，DocumentDB可以配置4级一致性等级。
- 二进制大对象存储：MongoDB依赖GridFS来实现Blob的存储，DocumentDB依赖Azure Blob Storage。
监控：Azure为DocumentDB提供了丰富的监控指标，MongoDB通过Mongo Monitoring Service (MMS)来跟踪宿主主机的情况。
- 可编程性：两者都支持JavaScript，DocumentDB的.NET SDK对LINQ支持更好，不过对debug支持不好（主要没有本地模拟器）。
- 其他不同：DocumentDB对聚合操作暂时有一定限制，无服务端排序，工具还不够丰富。MongoDB情况要稍好些。


#### F.Search搜索数据存储

- [ElasticSearch研究](2017-01-06-elastic-search-engine-architect-note.md)
  
    - 适合海量数据秒级查询
    - 支持多并发查询分析
    - 不适用于复杂的JOIN查询等关联分析


#### 数据库应用选择

![database_type_all](_includes/database_all.png)

	Tip:
	These Database solution come from Amazon excluded Hadoop Batch Processing.

### IV.数据库架构基础

#### 通用数据库架构分析

- [How does a relational database work](http://coding-geek.com/how-databases-work/)


*1.合并排序算法*

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

整体成本是 N \* log(N) 次运算

*2.Array与二维表*

	用阵列的话，你需要一个连续内存空间。如果你加载一个大表，很难分配足够的连续内存空间。

*3.二叉树结构与索引*

- binary search tree查询的成本是log(N)
- B+Tree可支持range scan(范围查询)。查询成本为M+log(N)。 在B+树中,插入和删除操作是 O(log(N))复杂度。	

*4.哈希表与HashJoin*

Hash取模运算。好的Hash函数时间复杂度是 O(1)

	- 一个哈希表可以只装载一半到内存，剩下的哈希桶可以留在硬盘上。

*5.客户端管理器 Client Manager*

	* 管理器首先检查你的验证信息（用户名和密码），然后检查你是否有访问数据库的授权。这些权限由DBA分配。
	* 然后，管理器检查是否有空闲进程（或线程）来处理你对查询。
	* 管理器还会检查数据库是否负载很重。
	* 管理器可能会等待一会儿来获取需要的资源。如果等待时间达到超时时间，它会关闭连接并给出一个可读的错误信息。
	* 然后管理器会把你的查询送给查询管理器来处理。
	* 因为查询处理进程不是『不全则无』的，一旦它从查询管理器得到数据，它会把部分结果保存到一个缓冲区并且开始给你发送。
	* 如果遇到问题，管理器关闭连接，向你发送可读的解释信息，然后释放资源。	

*6.查询管理器 Query Manager*

	* 查询首先被解析并判断是否合法
	* 然后被重写，去除了无用的操作并且加入预优化部分
	* 接着被优化以便提升性能，并被转换为可执行代码和数据访问计划。
	* 然后计划被编译
	* 最后查询被执行

*7.语义解析器 Query Parser*

SQL优化器的前置组件

SQL的理论基础是关系代数,而关系代数的主要操作只有5种,分别是并,差,积,选择,投影。所有的SQL语句最后都能用这5种操作组合完成。

语义解析器要分析查询中的表和字段

- 表是否存在
- 表的字段是否存在
- 对某类型字段的 运算 是否 可能(比如，你不能将整数和字符串进行比较，你不能对一个整数使用substring()函数)

在解析过程中，SQL查询被转换为内部表示(通常是一个语义树来描述查询计划树)


![semantic_tree](_includes/semantic_tree.png)


_Ref:_

- 语义解析解决方案:[ANTLR4语义解析](https://github.com/antlr/antlr4/blob/master/doc/index.md)
- 开源SQL Parser:[Apache Calcite](http://calcite.apache.org/docs/)


*8.查询优化器 Query Optimizer - DB核心模块*

**数据库优化器计算的是它们的 CPU成本、磁盘I/O成本、和内存需求**。时间复杂度和 CPU成本的区别是，时间成本是个近似值。而 CPU成本，我这里包括了所有的运算，比如:加法、条件判断、乘法、迭代。<br/>
**多数时候瓶颈在于磁盘I/O(数据文件随机读写)而不是CPU使用**。

- 查询重写器
- 逻辑查询优化
- 物理查询优化

    所有的现代数据库都在用*基于成本的优化*(即Cost-Based Optimization)来优化查询。<br/>
	它是看语句的代价(Cost),这里的代价主要指Cpu和内存。优化器在判断是否用这种方式时,主要参照的是表及索引的统计信息。<br/>

- 查询计划执行


详细可查看:[SQL Query Optimizer Design文档](2018-06-01-query-optimizer-design-note.md)


*9.查询执行器 Query Executor*

SQL优化器的后置组件

*10.数据管理器 Data Manager*

	* 关系型数据库使用事务模型，所以，当其他人在同一时刻使用或修改数据时，你无法得到这部分数据。
	* 数据提取是数据库中速度最慢的操作，所以数据管理器需要足够聪明地获得数据并保存在内存缓冲区内。

*11.缓存管理器 Cache Manager*

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

*12.事务管理器*

	* ACID/ 并发控制/ 锁管理器/ 悲观锁/ 死锁
	* 事务日志WAL/ 日志缓冲区/ STEAL 和 FORCE 策略/ 关于恢复
	
	* WAL规则
	
		1)每个对数据库的修改都产生一条日志记录，在数据写入磁盘之前日志记录必须写入事务日志。
		2)日志记录必须按顺序写入；记录 A 发生在记录 B 之前，则 A 必须写在 B 之前。
		3)当一个事务提交时，在事务成功之前，提交顺序必须写入到事务日志。
	
	* ARIES数据库恢复原型算法(Algorithms for Recovery and Isolation Exploiting Semantics) 
	
		1) 写日志的同时保持良好性能
		2) 快速和可靠的数据恢复
	
	* 日志结构
	
		- LSN：一个唯一的日志序列号（Log Sequence Number）。LSN是按时间顺序分配的 * ，这意味着如果操作 A 先于操作 B，log A 的 LSN 要比 log B 的 LSN 小。
		- TransID：产生操作的事务ID。
		- PageID：被修改的数据在磁盘上的位置。磁盘数据的最小单位是页，所以数据的位置就是它所处页的位置。
		- PrevLSN：同一个事务产生的上一条日志记录的链接。
		- UNDO：取消本次操作的方法。
			比如，如果操作是一次更新，UNDO将或者保存元素更新前的值/状态（物理UNDO），或者回到原来状态的反向操作(逻辑UNDO)。
		- REDO：重复本次操作的方法。 同样的，有 2 种方法：或者保存操作后的元素值/状态，或者保存操作本身以便重复。
		- …:(供您参考，一个 ARIES 日志还有 2 个字段：UndoNxtLSN 和 Type）
	
	* ARIES从崩溃中恢复有三个阶段
	
		1) 分析阶段：恢复进程读取全部事务日志，来重建崩溃过程中所发生事情的时间线，决定哪个事务要回滚（所有未提交的事务都要回滚）、崩溃时哪些数据需要写盘。
		2) Redo阶段：这一关从分析中选中的一条日志记录开始，使用 REDO 来将数据库恢复到崩溃之前的状态。
		3) Undo阶段：这一阶段回滚所有崩溃时未完成的事务。回滚从每个事务的最后一条日志开始，并且按照时间倒序处理UNDO日志（使用日志记录的PrevLSN）。
	
	ARIES提出了一个概念:检查点check point,就是不时地把事务表和脏页表的内容,还有此时最后一条LSN写入磁盘 


### V.常用算法

*1.排序算法*

将杂乱无章的数据元素，通过一定的方法按关键字顺序排列的过程叫做排序。假定在待排序的记录序列中，存在多个具有相同的关键字的记录，若经过排序，这些记录的相对次序保持不变，即在原序列中，ri=rj，且ri在rj之前，而在排序后的序列中，ri仍在rj之前，则称这种排序算法是稳定的；否则称为不稳定的。

- 插入排序

有一个已经有序的数据序列，要求在这个已经排好的数据序列中插入一个数，但要求插入后此数据序列仍然有序，这个时候就要用到一种新的排序方法——插入排序法,插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据，算法适用于少量数据的排序，时间复杂度为O(n^2)。是稳定的排序方法。插入算法把要排序的数组分成两部分：第一部分包含了这个数组的所有元素，但将最后一个元素除外（让数组多一个空间才有插入的位置），而第二部分就只包含这一个元素（即待插入元素）。在第一部分排序完成后，再将这个最后元素插入到已排好序的第一部分中。
插入排序的基本思想是：每步将一个待排序的纪录，按其关键码值的大小插入前面已经排序的文件中适当位置上，直到全部插入完为止。

- 桶排序

桶排序 (Bucket sort)或所谓的箱排序，是一个排序算法，工作的原理是将数组分到有限数量的桶子里。每个桶子再个别排序（有可能再使用别的排序算法或是以递归方式继续使用桶排序进行排序）。桶排序是鸽巢排序的一种归纳结果。当要被排序的数组内的数值是均匀分配的时候，桶排序使用线性时间（Θ（n））。但桶排序并不是 比较排序，他不受到 O(n log n) 下限的影响。

- 堆排序

堆排序(Heapsort)是指利用堆积树（堆）这种数据结构所设计的一种排序算法，它是选择排序的一种。可以利用数组的特点快速定位指定索引的元素。堆分为大根堆和小根堆，是完全二叉树。大根堆的要求是每个节点的值都不大于其父节点的值，即A[PARENT[i]] >= A[i]。在数组的非降序排序中，需要使用的就是大根堆，因为根据大根堆的要求可知，最大的值一定在堆顶。

*2.快速排序*

快速排序（Quicksort）是对冒泡排序的一种改进。
快速排序由C. A. R. Hoare在1962年提出。它的基本思想是：通过一趟排序将要排序的数据分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据都要小，然后再按此方法对这两部分数据分别进行快速排序，整个排序过程可以递归进行，以此达到整个数据变成有序序列。

*3.最大子数组*

最大和子数组是数组中和最大的子数组，又名最大和子序列。子数组是数组中连续的n个元素，比如a2,a3,a4就是一个长度为3的子数组。顾名思义求最大和子数组就是要求取和最大的子数组。
n个元素的数组包含n个长度为1的子数组：{a0}，{a1}，…{an-1}；
n个元素的数组包含n-1个长度为2的子数组：{a0,a1}，{a1,a2}，{an-2,an-1}；
………………………………………………………………………………………………
n个元素的数组包含1个长度为n的子数组：{a0,a1,…,an-1}；
所以，一个长度为n的数组包含的子数组个数为n+(n-1)+…+1=n x (n-1)/2。

*4.最长公共子序列*

一个数列 ，如果分别是两个或多个已知数列的子序列，且是所有符合此条件序列中最长的，则 称为已知序列的最长公共子序列。
最长公共子序列，英文缩写为LCS（Longest Common Subsequence）。其定义是，一个序列 S ，如果分别是两个或多个已知序列的子序列，且是所有符合此条件序列中最长的，则 S 称为已知序列的最长公共子序列。而最长公共子串(要求连续)和最长公共子序列是不同的。
最长公共子序列是一个十分实用的问题，它可以描述两段文字之间的“相似度”，即它们的雷同程度，从而能够用来辨别抄袭。对一段文字进行修改之后，计算改动前后文字的最长公共子序列，将除此子序列外的部分提取出来，这种方法判断修改的部分，往往十分准确。简而言之，百度知道、百度百科都用得上。

*5.最小生成树*

一个有 n 个结点的连通图的生成树是原图的极小连通子图，且包含原图中的所有 n 个结点，并且有保持图连通的最少的边。最小生成树可以用kruskal（克鲁斯卡尔）算法或prim（普里姆）算法求出。
最短路径
用于计算一个节点到其他所有节点的最短路径。主要特点是以起始点为中心向外层层扩展，直到扩展到终点为止。Dijkstra算法能得出最短路径的最优解，但由于它遍历计算的节点很多，所以效率低。

*6.矩阵的存储和运算*

列矩阵(column major)和行矩阵(row major)是数学上的概念，和电脑无关，它只是一套约定(convention),按照矢量和矩阵的乘法运算时，矢量是列矢还是行矢命名，这里只说4×4矩阵。齐次矢量可以看成是一个1×4的矩阵，就是行矢；或者4×1的矩阵，就是列矢。


### x.Ref

- [BigTable](https://baike.baidu.com/item/BigTable/3707131?fr=aladdin)
- [从架构特点到功能缺陷，重新认识分析型分布式数据库](https://mp.weixin.qq.com/s/O9sWvcHhrgafCWHSMiOMlA)
- [对比MPP计算框架和批处理计算框架](https://blog.csdn.net/sinat_27545249/article/details/78943823)
- [Google Mesa - OLAP数据仓库](http://static.googleusercontent.com/media/research.google.com/en/us/pubs/archive/42851.pdf)
- [built-databases-in-aws](https://www.allthingsdistributed.com/2018/06/purpose-built-databases-in-aws.html)

