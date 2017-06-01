---
layout: post
category : datascience
tags : [bigdata,database,guide]
title: Greenplum 4 Best Practice Note
---

#### 1.最佳实践概述


GPDB是一个基于大规模并行处理(MPP)和sharing-nothing架构的分析型数据库。这种数据库的数据模式与高度规范化的事务性SMP的数据库显著不同,支持具有大事实表和小维度表的Star或者雪花模式。


*数据模型*

* 跨表关联(JOIN)时字段使用相同的数据类型。
* 堆存储和追加优化存储(Append-Optimized,下称 AO)
* 若表和分区表需要进行迭代式的批处理或者频繁执行单个UPDATE、DELETE或INSERT操作,
* 若表和分区表需要并发执行 UPDATE、DELETE 或 INSERT 操作,使用堆存储。
* 若表和分区表在数据初始加载后更新不频繁,且仅以批处理方式插入数据,则使用 AO 存储。
* 不要对 AO 表执行单个 INSERT、UPDATE 或 DELETE 操作。
* 不要对 AO 表执行并发批量 UPDATE 或 DELETE 操作,但可以并发执行批量 INSERT 操作。

*行列存储*

* 若数据需要经常更新或者插入,则使用行存储。
* 若需要同时访问一个表的很多字段,则使用行存储。
* 对于通用或者混合型业务,建议使用行存储。
* 若查询访问的字段数目较少,或者仅在少量字段上进行聚合操作,则使用列存储。 
* 若仅常常修改表的某一字段而不修改其他字段,则使用列存储。

*数据压缩*

* 对于大 AO 表和分区表使用压缩,以提高系统 I/O。
* 在字段级别配置压缩。
* 考虑压缩比和压缩性能之间的平衡。

*数据分布Distribute*

为所有表定义分布策略:要么定义分布键,要么使用随机分布。不要使用缺省分布方式。

* 优先选择可均匀分布数据的单个字段做分布键。
* 不要选择经常用于 WHERE 子句的字段做分布键。
* 不要使用日期或时间字段做分布键
* 分布键Distribute和分区键Partition不要使用同一字段。
* 对经常执行 JOIN 操作的大表,优先考虑使用关联字段做分布键,尽量做到本地关联,以提高性能。
* 数据初始加载后或者每次增量加载后,检查数据分布是否均匀。
* 尽可能避免数据倾斜。

*内存管理*

* 设置 vm.overcommit_memory 为 2
* 不要为操作系统的页设置过大的值
* 使用 gp_vmem_protect_limit 设置单个节点数据库(Segment Database)可以为所有查询分 配的最大内存量。
	
	- 不要设置过高的 gp_vmem_protect_limit 值,也不要大于系统的物理内存。
	- gp_vmem_protect_limit 的建议值计算公式为: (SWAP + (RAM * vm.overcommit_ratio)) * 0.9 / number_Segments_per_server

* 使用 statement_mem 控制节点数据库为单个查询分配的内存量。
* 使用资源队列设置队列允许的当前最大查询数(ACTIVE_STATEMENTS)和允许使用的内存大小(MEMORY_LIMIT)。

	- 不要使用默认的资源队列,为所有用户都分配资源队列。 根据负载和时间段,设置和队列实际需求相匹配的优先级(PRIORITY)。 保证资源队列的内存配额不超过 gp_vmem_protect_limit。
	- 动态更新资源队列配置以适应日常工作需要。

*数据分区*

* 只为大表设置分区,不要为小表设置分区。
* 仅在根据查询条件可以实现分区裁剪时使用分区表。
* 建议优先使用范围(Range)分区,否则使用列表(List)分区。
* 根据查询特点合理设置分区。
* 不要使用相同的字段即做分区键又做分布键。
* 不要使用默认分区。
* 避免使用多级分区;尽量创建少量的分区,每个分区的数据更多些。
* 通过查询计划的 EXPLAIN 结果来验证查询对分区表执行的是选择性扫描 (分区裁剪)。
* 对于列存储的表,不要创建过多的分区,否则会造成物理文件过多:Physical files = Segments * Columns * Partitions。

*索引*

一般来说 GPDB 中索引不是必需的。

* 对于高基数(HIGH Cardinality-唯一值多)的列存储表,如果需要遍历且查询选择性较高,则创建单列索引。  频繁更新的列不要建立索引。
* 在加载大量数据之前删除索引,加载结束后再重新创建索引。
* 优先使用 B 树索引。
* 不要为需要频繁更新的字段创建位图索引。
* 不要为唯一性字段,基数非常高或者非常低的字段创建位图索引。
* 不要为事务性负载创建位图索引。
* 一般来说不要索引分区表。如果需要建立索引,则选择与分区键不同的字段。

*资源队列*

* 使用资源队列管理集群的负载。
* 为所有角色定义适当的资源队列。
* 使用 ACTIVE_STATEMENTS 参数限制队列成员可以并发运行的查询总数。 
* 使用 MEMORY_LIMIT 参数限制队列中查询可以使用的内存总量。
* 不要设置所有队列为 MEDIUM,这样起不到管理负载的作用。
* 根据负载和时间段动态调整资源队列。

*JDBC Driver*

使用Greenplum DataDirect JDBC Driver(相比postgresql jdbc driver,性能差。。。需研究)


#### 2.详细步骤

*2.1.自建资源队列*

建议通过greenplum command center的Administration->Manage resource queues选项操作。
自己创建资源队列,系统默认的资源队列pg_default,对内存参数没有做出限制，会有内存溢出的风险
Comment:必须设置资源队列,否则大数据量查询很容易产生内存溢出异常

资源队列具体参数设置:
ACTIVE_STATEMENTS:此参数限制队列中同是执行的query数量,当query数量超过此值是则处于等待状态。pg_default默认值是20。
MEMORY_LIMIT:此参数限制起源队中所有活动query(参见ACTIVE_STATEMENTS参数)能使用的最大内存，不能超过物理内存，计算方法为 物理momery/机器的节点个数*0.9;

* 创建资源队列

	CREATE RESOURCE QUEUE ir_rq WITH(
	ACTIVE_STATEMENTS=20,
	MEMORY_LIMIT=1800M)
* 创建用户

	CREATE ROLE username with login ENCRYPTED PASSWORD RESOURCE QUEUE ir_rq;


*2.2.统计优化Vacuum*

greenplum4后版本支持压缩表的插入删除和更新操作
GP删除数据是标识删除,磁盘上的数据并没有真正删除,因此该空间不可重用
官方建议Vacuum的执行周期是每晚.该策略需测试

* vacuum只是简单的回收空间且令其可以再次使用，没有请求排它锁，仍旧可以对表读写
* vacuum full执行更广泛的处理，包括跨块移动行，以便把表压缩至使用最少的磁盘块数目存储。相对vacuum要慢，而且会请求排它锁。
* 定期执行：在日常维护中，需要对数据字典定期执行vacuum，可以每天在数据库空闲的时候进行。然后每隔一段较长时间（两三个月）对系统表执行一次vacuum full，这个操作需要停机，比较耗时，大表可能耗时几个小时。
* reindex:执行vacuum之后,最好对表上的索引进行重建

*2.2.1.Heap表*

Vacuum命令会让标记删除数据占有空间变得可以被使用。参数具体如下
* FULL:回收空间并且对磁盘上的数据进行整理,类似磁盘碎片整理,耗时较长,并且锁表。因此不建议执行该命令
* ANALYZE:更新统计信息,查询分析器生成更新的EXPLAIN Plan.
* table:默认的是当前数据库下的所有表
* column:默认的当前表的所有列

*2.2.2.Append-Optimised追加优化*

greenplum 4.x 以后的appendonly表可以支持更新和删除操作，但是限制不能更新分布键distributeKey所在的列
Vacuum首先整理优化索引,接下来顺序的在每个segment节点上执行优化,最后整理优化辅助表并更新统计信息。在每个segment节点上操作如下:
	1. 复制当前segment所有可见的数据行到一个新的segment,之后删除当前segment上的数据并且让新segment上的数据变得可用
	2. Vacuum不带full参数,增删改查可以正常操作
	3. Vacuum full命令,锁表
	4. gp_appendonly_compaction_threshold,控制Vacuum(without full)运行时是否进行表优化

压缩系统设置

当一个查询的结果过大溢出到硬盘时  采用gp_workfile_compress_algorithm 指定的参数压缩，默认值none，可选值zlib，设置成zlib后，在密集型查询系统中可提升10%-20%的效率

	设置方法gpconfig -c gp_workfile_compress_algorithm -v zlib

*2.3.ANALYZE*

* 命令：analyze [talbe [(column,..)]]
* 收集表内容的统计信息，以优化执行计划。如创建索引后，执行此命令，对于随即查询将会利用索引。
* 自动统计信息收集
* 在postgresql.conf中有控制自动收集的参数gp_autostats_mode设置，gp_autostats_mode三个值：none、no_change、on_no_stats（默认） 
* none：禁止收集统计信息
* on change：当一条DML执行后影响的行数超过gp_autostats_on_change_threshold参数指定的值时，会执行完这条DML后再自动执行一个analyze 的操作来收集表的统计信息。
* no_no_stats：当使用create talbe as select 、insert 、copy时，如果在目标表中没有收集过统计信息，那么会自动执行analyze 来收集这张表的信息。gp默认使用on_no_stats，对数据库的消耗比较小，但是对于不断变更的表，数据库在第一次收集统计信息之后就不会再收集了。需要人为定时执行analyze.
* 如果有大量的运行时间在1分钟以下的SQL，你会发现大量的时间消耗在收集统计信息上。为了降低这一部分的消耗，可以指定对某些列不收集统计信息，如下所示：

	1. create table test(id int, name text,note text);
	上面是已知道表列note不需出现在join列上，也不会出现在where语句的过滤条件下，因为可以把这个列设置为不收集统计信息：
	2. alter table test alter note SET STATISTICS 0;

*2.4.两种聚合方式*

* HashAggregate 根据group by字段后面的值算出hash值，并根据前面使用的聚合函数在内存中维护对应的列表，几个聚合函数就有几个数组。相同数据量的情况下，聚合字段的重复度越小，使用的内存越大。
* GroupAggregate 先将表中的数据按照group by的字段排序，在对排好序的数据进行全扫描，并进行聚合函数计算。消耗内存基本是恒定的。
* 选择在SQL中有大量的聚合函数，group by的字段重复值比较少的时候，应该用groupaggregate

*2.5.JOIN关联方式*

分为三类：hash join、nestloop join、merge join，在保证sql执行正确的前提下，规划器优先采用hash join。
* hash join: 先对其中一张关联的表计算hash值，在内存中用一个散列表保存，然后对另外一张表进行全表扫描，之后将每一行与这个散列表进行关联。
* nestedloop:关联的两张表中的数据量比较小的表进行广播，如笛卡尔积：select * fromtest1，test2
* merge join:将两张表按照关联键进行排序，然后按照归并排序的方式将数据进行关联，效率比hash join差。full outer join只能采用merge join来实现。
* 关联的广播与重分布解析P133，一般规划器会自动选择最优执行计划。
* 有时会导致重分布和广播，比较耗时的操作

*2.6.Redistribute重分布*

一些sql查询中，需要数据在各节点重新分布，受制于网络传输、磁盘I/O，重分布的速度比较慢。
* 关联键强制类型转换 
一般，表按照指定的分布键作hash分部。如果两个表按照id:intege、id:numericr分布，关联时，需要有一个表id作强制类型转化，因为不同类型的hash值不一样，因而导致数据重分布。
* 关联键与分部键不一致
* group by、开窗函数、grouping sets会引发重分布


*2.7.数据Load策略*

gpfdist+gpload

- 使用 gpfdist 进行数据的加载和导出。
- 随着段数据库个数的增加,并行性增加。
- 尽量将数据均匀地分布到多个 ETL 节点上。 将非常大的数据文件切分成相同大小的块,并放在尽量多的文件系统上。
- 一个文件系统运行两个 gpfdist 实例。
- 在尽可能多的网络接口上运行 gpfdsit。
- 使用 gp_external_max_segs 控制访问每个 gpfdist 服务器的段数据库的个数.建议gp_external_max_segs的值和gpfdist进程个数为偶数。
- 数据加载前删除索引;加载完后重建索引。
- 数据加载完成后运行 ANALYZE 操作。
- 数据加载过程中,设置 gp_autostats_mode 为 NONE,取消统计信息的自动收集。 若数据加载失败,使用 VACUUM 回收空间。



2.8.Index

http://gpdb.docs.pivotal.io/4320/ref_guide/sql_commands/CREATE_INDEX.html

GP不建议使用索引
GP主要做快速有序地扫描（基于分区）
如果建立全局索引，数据分布机制和分区机制，会完全打乱索引。如果基于单个分区去建立索引，这个有点像阿里的xxx，应该有一定效果吧。

GP中索引的起作用的场景：

	返回1条或者很小的集合时
	当可以使用index来替代全表扫描的查询(append-optimized tables)
	GP只支持在用户创建的表上建立索引，不支持GP依据分区创建的叶表上创建索引。创建的索引会被复制到各个叶表上。

	用明确的JOIN控制规划器
	关闭自动提交
	使用COPY命令前,删除Index和外键约束,事后运行VACUUM ANALYZE


#### Ref

https://wenku.baidu.com/view/2f36c23d30126edb6f1aff00bed5b9f3f90f721c.html
https://www.linkedin.com/pulse/tuning-greenplum-database-sandeep-katta-
http://download.csdn.net/download/darkcatc/8474339