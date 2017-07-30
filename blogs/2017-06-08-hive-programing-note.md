---
layout: post
category : architect
tags : [bigdata,database,hadoop]
title: Hive Programing Design Note
---

## Hive Programing Design Note
------------------------------------------------------------

### 1.About Hive

Hive is a data warehouse infrastructure built on top of Hadoop. It provides tools to enable easy data ETL, a mechanism to put structures on the data, and the capability to querying and analysis of large data sets stored in hadoop files. Hive defines a simple SQL-like query language, called QL, that enables users familiar with SQL to query the data. At the same time, this language also allows programmers who are familiar with the MapReduce fromwork to be able to plug in their custom mappers and reducers to perform more sophisticated analysis that may not be supported by the built-in capabilities of the language.

### 2.Hive Architect

![Hive Architect](_includes/hive_architecture.png)

Figure 1 shows the major components of Hive and its interactions with Hadoop. As shown in that figure, the main components of Hive are:

	- UI – The user interface for users to submit queries and other operations to the system. As of 2011 the system had a command line interface and a web based GUI was being developed.
	- Driver – The component which receives the queries. This component implements the notion of session handles and provides execute and fetch APIs modeled on JDBC/ODBC interfaces.
	- Compiler – The component that parses the query, does semantic analysis on the different query blocks and query expressions and eventually generates an execution plan with the help of the table and partition metadata looked up from the metastore.
	- Metastore – The component that stores all the structure information of the various tables and partitions in the warehouse including column and column type information, the serializers and deserializers necessary to read and write data and the corresponding HDFS files where the data is stored.
	- Execution Engine – The component which executes the execution plan created by the compiler. The plan is a DAG of stages. The execution engine manages the dependencies between these different stages of the plan and executes these stages on the appropriate system components.


#### Hive SQL Executor

![Hive SQL Executor](_includes/hive_sql_execute.jpg)


### 3.Hive Programing using HiveQL

#### 3.1.HiveQL: Data Definition

#### 3.2.HiveQL: Data Manipulation

#### 3.3.HiveQL: Queries

#### 3.4.HiveQL: Views

#### 3.5.HiveQL: Indexes

#### 3.6.HiveQL: Schema Design


### 4.Hive Best Practice

Hive是将符合SQL语法的字符串解析生成可以在Hadoop上执行的MapReduce的工具。使用Hive尽量按照分布式计算的一些特点来设计sql，和传统关系型数据库有区别，所以需要去掉原有关系型数据库下开发的一些固有思维。

#### 4.1.Hive Tuning



#### 4.2.基本原则

1.尽量尽早地过滤数据,减少每个阶段的数据量,对于分区表要加分区,同时只选择需要使用到的字段

```sql
select ... from A join B
	on A.key = B.key
	where A.userid>10 and B.userid<10
        and A.dt='20120417'
        and B.dt='20120417';
```

应该改写为：

```sql
select .... from (select .... from A
    where dt='201200417' and userid>10) a
	join ( select .... from B
       where dt='201200417' and userid < 10   
     ) b
on a.key = b.key;
```

2.对历史库的计算经验(这项是说根据不同的使用目的优化使用方法)

	历史库计算和使用,分区


3.尽量原子化操作，尽量避免一个SQL包含复杂逻辑

	可以使用中间表来完成复杂的逻辑   

4.join操作   

	- 若其中有一个表很小使用map join，否则使用普通的reduce join，注意hive会将join前面的表数据装载内存,所以较小的一个表在较大的表之前,减少内存资源的消耗
	- 小表要注意放在join的左边（目前TCL里面很多都小表放在join的右边).否则会引起磁盘和内存的大量消耗


5.如果union all的部分个数大于2,或者每个union部分数据量大,应该拆成多个insert into语句,实际测试过程中,执行时间能提升50%

```sql
insert overwite table tablename partition (dt= ....)
select ..... from (
       select ... from A
       union all
       select ... from B
       union all
       select ... from C
                   ) R
where ...;
```

可以改写为：

```sql
insert into table tablename partition (dt= ....)
select .... from A
WHERE ...;

insert into table tablename partition (dt= ....)
select .... from B
WHERE ...;

insert into table tablename partition (dt= ....)
select .... from C
WHERE ...; 

``` 

6.HiveQL查询优化，如果有join,group操作的话，要注意是否会有数据倾斜

如果出现数据倾斜，应当做如下处理：

	- set hive.exec.reducers.max=200;
	- set mapred.reduce.tasks= 200;---增大Reduce个数
	- set hive.groupby.mapaggr.checkinterval=100000;--这个是group的键对应的记录条数超过这个值则会进行分拆,值根据具体数据量设置
	- set hive.groupby.skewindata=true; --如果是group by过程出现倾斜 应该设置为true
	- set hive.skewjoin.key=100000; --这个是join的键对应的记录条数超过这个值则会进行分拆,值根据具体数据量设置
	- set hive.optimize.skewjoin=true;--如果是join 过程出现倾斜 应该设置为true

(1)  启动一次job尽可能的多做事情，一个job能完成的事情,不要两个job来做

 通常来说前面的任务启动可以稍带一起做的事情就一起做了,以便后续的多个任务重用,与此紧密相连的是模型设计,好的模型特别重要.

(2) 合理设置reduce个数

reduce个数过少没有真正发挥hadoop并行计算的威力，但reduce个数过多，会造成大量小文件问题，数据量、资源情况只有自己最清楚，找到个折衷点,

(3) 使用hive.exec.parallel参数控制在同一个sql中的不同的job是否可以同时运行，提高作业的并发


(4)注意小文件的问题

在hive里有两种比较常见的处理办法

第一是使用Combinefileinputformat，将多个小文件打包作为一个整体的inputsplit，减少map任务数

	- set mapred.max.split.size=256000000;
	- set mapred.min.split.size.per.node=256000000
	- set Mapred.min.split.size.per.rack=256000000
	- set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat

第二是设置hive参数，将额外启动一个MR Job打包小文件

hive.merge.mapredfiles = false 是否合并 Reduce 输出文件，默认为 False 

hive.merge.size.per.task = 256*1000*1000 合并文件的大小 


(3)注意数据倾斜

在hive里比较常用的处理办法

第一通过hive.groupby.skewindata=true控制生成两个MR Job,第一个MR Job Map的输出结果随机分配到reduce做次预汇总,减少某些key值条数过多某些key条数过小造成的数据倾斜问题

第二通过hive.map.aggr = true(默认为true)在Map端做combiner,假如map各条数据基本上不一样, 聚合没什么意义，做combiner反而画蛇添足,hive里也考虑的比较周到通过参数hive.groupby.mapaggr.checkinterval = 100000 (默认)hive.map.aggr.hash.min.reduction=0.5(默认),预先取100000条数据聚合,如果聚合后的条数/100000>0.5，则不再聚合

 

(4)善用multi insert,union all

multi insert适合基于同一个源表按照不同逻辑不同粒度处理插入不同表的场景，做到只需要扫描源表一次，job个数不变，减少源表扫描次数

union all用好，可减少表的扫描次数，减少job的个数,通常预先按不同逻辑不同条件生成的查询union all后，再统一group by计算,不同表的union all相当于multiple inputs,同一个表的union all,相当map一次输出多条

(5) 参数设置的调优

集群参数种类繁多,举个例子比如

可针对特定job设置特定参数,比如jvm重用,reduce copy线程数量设置(适合map较快，输出量较大)

如果任务数多且小，比如在一分钟之内完成，减少task数量以减少任务初始化的消耗。可以通过配置JVM重用选项减少task的消耗


#### 4.3.Functions



### 5.From Hive on MapReduce to Hive on Spark




### X.Ref


