---
layout: post
category : bigdata
tags : [bigdata,olap,architect]
title: Big Data OLAP Note - Impala Practice
---

## OLAP查询-Impala实时OLAP实践
------------------------------------------------------------

### Impala架构分析

#### 1.Impala组件列表:

- Impala demon: Impala核心组件-守护进程
- Statestore: 协调器(meta数据分发)
- Catalog: metadata管理与执行组件
- HiveMetastore: meta存储器
- DataStorage: HDFS / HBase / Kudu

#### 2.Impala特点描述:

- Impala是目前为止性能最佳的SQL-on-Hadoop OLAP引擎,特别是针对多用户下负载情况下

		Tips:Impala至今还是未成为最佳的SQL-on-Hadoop OLAP解决方案

- Impala不支持UPDATE或DELETE,与Hive一致。Impala支持ALTER TABLE DROP PARTITION分区设置
- Impala查询设计的核心是在数百台节点下的集群metadata信息的协作与同步。例如,及时获取最新版本的系统catalog
- Impala通过statestore组件实现简单的publish-subscribe服务,用于传播metadata信息更新到所有subscriber。这样极大减少网络连接(TCP/PRC)的开销
- Impala的catalog组件维护catalog metadata信息,并通过statestore组件进行传播,代替impala demon组件执行DDL操作(SQL).catalog组件通过第三方metadata仓库拉取数据相关信息并聚合其信息成impala可支持的catalog结构。当前默认metadata store为Hive Metastore,之后可替换为MySQL
- Impala支持内联视图view,非相关的和相关的子查询,支持outer join,semi-join 和 anti-join,包括分析窗口函数
- Impala查询选择的策略是建立基于网络的最小范围的数据交换,优先使用已有的join输入的分区数据。这个设计类似于Greenplum。
- LLVM(运行时代码生成)技术可提高查询性能。LLVM作为编译依赖库用于在运行中just-in-time编译
- Impala使用HDFS的short-circuit local reads特性,绕过DataNode协议访问本地磁盘,以接近硬件速度进行数据扫描
- Impala支持常规数据文件格式,包括Avro,RCFile,Sequence,TextFile and Parquet。建议使用Parquet文件格式,基于其高压缩与高扫描特性。

#### 3.Impala查询性能:

- 默认单请求Impala比Greenplum慢2-3倍(千万级数据级)
- 集群环境下Impala比Greenplum慢0.5-3倍(亿级数据级)
- Impala在多用户访问情况下性能更佳
- Impala支持大数据量(TB/PB数据)下OLAP查询且系统稳定。Greenplum在大数据量情况下容易影响系统异常,需具体调优
- Impala查询默认推荐使用PARQUET文件格式(HDFS环境下查询性能最佳)
- Kudu数据结构要求主键唯一限制,在部分NewBI数据(无唯一主键数据表)无法使用Kudu
- Impala默认支持OUTER JOIN / CROSS JOIN / GROUP BY关联查询与聚合查询
- 通过Impala PartitionTable方式提高Impala并行查询性能 (20%-100%)
- Impala查询中,建议使用大表join小表模式查询,可减少多节点间数据交换
- Impala查询中缓存效果非常明显,已缓存的SQL平均查询速度提高2-5倍
- OLAP场景下,IO写入与查询性能并重的前提下,可优先选择Kudu数据存储

#### 4.Impala限制：

##### 4.1.尽量少使用 invalidate metadata，尽量用REFRESH TABLE_NAME

##### 4.2.Unable to execute the Impala Query with More than one Distinct Values in an Query

	Exception:AnalysisException: all DISTINCT aggregate functions need to have the same set of parameters as count(DISTINCT color_key); deviating function: count(DISTINCT id)
	
	Impala当前版本(2.7.0)不支持超过一个Distinct关键字查询

##### 4.3.set APPX_COUNT_DISTINCT=true 与 ndv()函数是一样的,都只是估值

	Impala SQL不支持的一个查询中的多个聚合函数使用DISTINCT
	如:select count(distinct id),count(distinct uid) from table;执行会报错
	impala 提供了 ndv 函数 及 set APPX_COUNT_DISTINCT=true 参数。但这两个都不是精确值

##### 4.4.impala 保存含中文结果到文件

	impala-shell -i hadoop07 -B -q 'select "我" from dual' -o result.txt
	这个太坑了
	修改  /data/cloudera/parcels/CDH-5.6.0-1.cdh5.6.0.p0.45/bin/../lib/impala-shell/impala_shell.py
	添加
	# coding=utf-8
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	然后修改：
	query = self.imp_client.create_beeswax_query("select %s" % args,self.set_query_options)
	为
	query = self.imp_client.create_beeswax_query("select %s" % (args.encode('utf-8')),self.set_query_options)

##### 4.5.impala内存限制问题,超出内存查询任务就被Kill

	这个猜测有两种可能：
	1.就是的确集群的内存不足就该加内存了
	2.就是集群中内存足够,只是impala在生成查询计划时,计算的内存使用量比实际需要量小,这个对依赖的表都加上compute stat语句,这样impala在生成查询计划时就能更准确的计算资源使用量.
	(Memory Limit Exceeded Query(f14d4983f27e4bc9:aef735d6523a7eb7) Limit: Consumption=7.51 GB)

##### 4.6. impala not in 为 0,结果不准确

	就是在使用 not in 语句时得到的结果为0，但实际上并不是
	原因是表中 in 的字段有 null 值

##### 4.7.cdh impala 添加 Llama服务存在问题

	添加此服务是Llama会修改/yarn/nm/usercache/目录的权限,导致hive及mr都执行不了,因为yarn需要此目录的读写权限,不过后来改了权限还是老有问题,干脆就撤掉此服务

##### 4.8.Impala compute stats(用于数据状态的统计,预先执行可提高查询性能)

	总是遇到问题,猜测是因为元数据刷新延迟的问题,暂时在compute status前添加sleep 5s

#### 5.NewBI与Impala查询整合

##### 5.1.newbi-olap-common组件Impala支持

由于Impala查询引擎支持常规SQL99语法(支持大多数SQL语法),因此针对NewBI-olap代码调整较少。

	a.扩展NewBI数据源支持ImpalaJDBC驱动
	b.执行针对HDFS特定文件格式的日期维表 - olap_date_impala.sql
	c.默认扩展NewBI衍生日期维度支持impala日期函数

##### 5.2.Impala DISTINCT查询限制(关键)

	- 按度量数量分解查询SQL,转换为多个独立度量子查询,处理单个DISTINCT查询
	- 多个DISTINCT描述单个度量,借助衍生度量方式进行内存计算,例如COUNT(DISTINCT fee)/COUNT(DISTINST totalfee)
	- hyoerloglog-DISTINCT近似值算法(NDV函数)
	- COUNT() OVER (PARTITION BY id) 指向分组后的维度计数 无法替换COUNT(DISTINCT)
	- DISTINCT num = select num from t1 group by num
	- COUNT(DISTINCT num) = SELECT COUNT(1) FROM (select num from t1 group by num) t

##### 5.3.查询结果预加载

根据ETL数据处理完成,自动启动Impala查询预加载,生成系统缓存。提升查询性能

##### 5.4.数据导入Kudu-ETL扩展

数据流接入依赖于Kudu部署与KuduClient实现

##### 5.5.执行compute stat以提升查询性能


### 数据存储(HDFS/HBase/Kudu)

#### 1.数据导入方式

* 方法1:

	1) 创建hadoop数据文件(hdfs或hbase)
	hdfs dfs -put /data/impala/newbi/nb_trade2.txt /tmp/newbi/
	2) 在Hive中创建表
	hive > load data inpath '/user/cloudera/thousand_strings.txt' into table table_name;
	3) 由于impala共享Hive metaStore,执行impala同步元数据
	impala-shell > invalidate metadata tablename
	4) Kudu存储需在impala-shell中CREATE Kudu Table
	5) impala-shell > REFRESH table_name 

* 方法2:

Sqoop import

* 方法3:

[KuduClient](http://kudu.apache.org/docs/developing.html#build_java_client):API访问

#### 2.Kudu存储特性

- 1) Kudu主键必须唯一,支持联合主键
- 2) 创建Kudu表必须指向Kudu master节点
- 3) 部分Impala函数在Kudu表结构下,部分情况下无法正常使用,例如to_date(2012-08-18 11:41:58.0)
- 4) 查询性能略低于Parquet文件格式
- 5) Kudu支持实时数据插入,Parquet 只支持定时批量数据导入。从功能上说,kudu的列存除了提供跟parquet接近的scan速度，还支持随机读写。支持随机写，数据可以实时插入/更新存储中，达到实时查询的效果;

	但是parquet文件只能批量写，所以一般只能定期生成，所以增大了延迟/数据更新差。Kudu的存储类似Hbase的LSM存储。
    HBase还是用来做OLTP类存储跟Mysql类似,数据插入与更新快,快速查询慢,不支持JOIN. Kudu则用来升级我们现有的数据分析数据流，主要还是OLAP的workload

- 6) Kudu的技术特点可以来配合impala搭建实时ad-hoc实时分析(即席查询)应用
- 7) CREATE Kudu Table Sample

```sql
CREATE TABLE `my_first_table` (
`id` BIGINT,
`name` STRING
)
TBLPROPERTIES(
  'storage_handler' = 'com.cloudera.kudu.hive.KuduStorageHandler',
  'kudu.table_name' = 'my_first_table',
  'kudu.master_addresses' = 'kudu-master.example.com:7051',
  'kudu.key_columns' = 'id'
);
```

#### 3.Kudu架构分析

- Kudu是一种新型存储系统,其设计与实现源于解决高吞吐量顺序访问存储例如HDFS与低延迟随机访问例如HBase之间的巨大差异。
- Kudu提供简单的API,基于行级别的inserts,updates和deletes,同时提供类似Parquet的针对吞吐量的表扫描。对于静态数据,常用列式文件格式。
- 每一列有一个名称,可为空值。主键存在唯一性限制,其作用是可作为唯一Index用作基于行的高效更新或删除。
- Kudu当前不支持二级索引或除主键以外的其他唯一性限制。
- Kudu不提供任何多行操作的事务API。
- Kudu只提供Scan操作用于从表中获取数据,包括在一列与常量的数据比较,和组合主键的范围查询
- Kudu为调用者提供APIs定义特定服务器下的数据区域的映射,用于协助分布式执行框架,例如Spark,MapReduce,Impala。
- Kudu提供两种一致性模式的选择。默认的一致性模式是snapshot一致性。
- Kudu内部使用timestamps实现并行控制(MVCC),但不允许用户对写操作手工设置timestamp
- 类似于BigTable/GFS/HDFS设计,Kudu依赖于单个Master server,负责metadata和任意一个Tablet Server的数据存储。
- Kudu Master server可以复制用于容错,支持在宕机情况下迅速实现故障转移。
- Kudu的表是水平分区的,类似于BigTable
- 由于大表的吞吐量非常重要,建议每台机器创建10-100个表,每个表数十GB左右
- Kudu支持可变的分区schemes的队列(hash-partitioning/range-partitioning)
- Kudu通过多机器复制所有表数据。但Kudu不复制tablet的磁盘存储数据,而只复制其操作日志。Tablet的每个复制的物理存储都是完全解耦的。
- Kudu实现Raft协议的配置更新。

#### 4.Kudu数据存储应用测试

	a.Kudu水平扩展应用
	b.数据清理与空间释放(hdfs dfs -expunge)


### Impala查询优化

- 根据当前测试结果,我们可以基本获取以下数据库的查询性能比较结果:Vertica > Greenplum > HDFS Parquet(Impala) >= Kudu(Impala)
- 数据库的IO写入性能比较(预计):Kudu > Vertica > Greenplum > HDFS Parquet
- 除大数据分析(TB)级别外,常规数据分析可选用Vertica或Greenplum即可
- Impala&Kudu架构是大数据实时OLAP查询的可行选择。支持随机写，数据可以实时插入/更新存储中，达到实时查询的效果。

**a.Impala partitioning**

partition option:

- CREATE TABLE PARTITION
- ALTER TABLE (必须已是分区表)
- INSERT PARTITION
```sql
insert into t1 partition(x, y='b') select c1, c2 from some_other_table;
```
- Impala partition分区查询优化,平均查询提速20%-100%

[参考资料](http://www.cloudera.com/documentation/enterprise/5-8-x/topics/impala_partitioning.html)

**b.Performance Considerations for Join Queries**

- 统计优化- COMPUTE STATS statement, and then let Impala automatically optimize the query based on the size of each table, number of distinct values of each column, and so on
- 使用STRAIGHT_JOIN-override the automatic join order optimization by specifying the STRAIGHT_JOIN keyword immediately after the SELECT keyword

	推荐的join查询顺序为 the logical join order to try would be BIG, TINY, SMALL, MEDIUM Tables.这样的顺序可以最大限度的缩小查询结果.
	The STRAIGHT_JOIN keyword turns off the reordering of join clauses that Impala does internally, and produces a plan that relies on the join clauses being ordered optimally in the query text. 

```sql
select straight_join x from medium join small join (select * from big where c1 < 10) as big
  where medium.id = small.id and small.id = big.id;
```

- The Impala query planner chooses between different techniques for performing join queries, depending on the absolute and relative sizes of the tables.
- **Broadcast joins** are the default, where the right-hand table is considered to be smaller than the left-hand table, and its contents are sent to all the other nodes involved in the query. 
- **Partitioned join** (not related to a partitioned table) is more suitable for large tables of roughly equal size(相似表容量使用partitioned join查询).This join technique is that portions of each table are sent to appropriate other nodes where those subsets of rows can be processed in parallel.
Join order have a large impact for query optimization.

[参考资料](http://www.cloudera.com/documentation/enterprise/5-8-x/topics/impala_perf_joins.html#perf_joins)

**c.Impala Performance Tuning**

	Understanding Impala Query Performance
	Using the SUMMARY Report for Performance Tuning
	Using the Query Profile for Performance Tuning
	
	参考:http://www.cloudera.com/documentation/enterprise/5-8-x/topics/impala_performance.html

**d.Impala查询能力分析**

1.2000W/1亿下的并发查询性能

2.原生函数支持

	条件函数(case when)
	分析函数(over/window)
	聚合函数
	UDF函数

3.Impala数据查询SQL比较

4.更多复杂查询语句测试(with rollup/with cube/grouping set)

| GroupAggregate | Greenplum                      | Hive                                       | Impala | 
|----------------|--------------------------------|--------------------------------------------|--------|
| CUBE	         |GROUP BY CUBE(a,b,c)=GROUP BY GROUPING SETS((a,b,c),(a,b),(a),(b,c),(a,c),(b),(c),())|GROUP BY a,b,c WITH CUBE                    |noSupport| 
| ROLLUP	     |GROUP BY ROLLUP(a,b,c)=GROUP BY GROUPING SETS((a,b,c),(a,b),(a),())                  |GROUP BY a,b,c WITH ROLLUP                  |noSupport|
| GROUPING SETS  |GROUP BY GROUPING SETS((a,b,c), (a,b), (a), ())                                      |GROUP BY GROUPING SETS((a,b,c),(a,b),(a),())|noSupport|	 

### x.Reference

- [Impala&Kudu research note](2016-12-12-olap-distributed-impala-research-note.md)
