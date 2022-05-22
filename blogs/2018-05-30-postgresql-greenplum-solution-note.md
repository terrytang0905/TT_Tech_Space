---
layout: post
category : database
tags : [product, database, solution]
title: PostgreSQL&Greenplum Solution Practice Note
---


## PostgreSQL&Greenplum解决方案实践
------------------------------------------------------------

### I.PostgreSQL

#### 1.PostgreSQL10(OLTP Solution)

- [PostgreSQL最佳实践](2017-05-30-postgresql-best-practice-note.md)
- [PostgreSQL&Greenplum Index研究](2017-12-16-postgresql-greenplum-index-note.md)

#### 2.PgBouncer数据库连接池

```linux
pgbouncer -d /etc/pgbouncer/pgbouncer.ini

psql -h 10.110.64.101 -p 6432 -U ir_user -d irview_iadt
```

- [pgbouncer](http://pgbouncer.projects.postgresql.org/doc/config.html)

#### 3.PostgreSQL新特性

- [Parallel Query In PostgreSQL](https://github.com/digoal/blog/blob/master/201707/20170714_01_pdf_001.pdf?spm=a2c4e.11153940.blogcont128016.25.3b0920adpIVVAw&file=20170714_01_pdf_001.pdf)
- 多核并行,单条SQL可以利用多个CPU并行计算。处理大查询非常高效
- 向量计算,使用CPU的向量计算指令,减少函数回调,大幅提升大量数据处理的性能
- JIT,动态编译,在处理大量的条件过滤或表达式时,性能提升非常的明显
- 列存储,更容易和JIT,向量计算结合,同时在处理按列统计时,效果非常好。

	需安装插件(imcs, cstore)

- 算子复用,一些聚合操作,中间步骤复用算子,减少运算量。效果提升也比较明
- GPU,利用GPU的计算能力,例如在十多个大表的JOIN时,效果提升20倍以上

	需安装插件(pg_strom)

- FPGA,利用FPGA的计算能力,效果与GPU类似。

	需安装插件

- MPP插件,例如Citus插件，,可以把PG数据库变成分布式数据库。

	需安装插件(citus)

- 流式计算,将计算分摊到每分每秒,解决集中式计算的运力需求。就好像春运一样,需要大量运力,而流计算不需要大量运力,因为把春运抹平了。
	
	需安装插件(pipelinedb)

- 时序插件,对应时序处理很有效。
	
	需安装插件(timescale)

- R、Python组件,用户可以编写R或Python的计算逻辑,在数据库中直接运行用户编写的代码,将数据和计算整合在一起,提升效率。
	
	安装语言插件(plpython, plr)

- MADLib,机器学习库。通过函数接口进行调用,也是进军OLAP的信号。

	需安装插件(madlib)

#### 4.PostgreSQL-XL

- [PostgreSQL-XL](https://www.postgres-xl.org/documentation/intro-whatis-postgres-xl.html) 

Postgres-XL is a horizontally scalable open source SQL database cluster, flexible enough to handle varying database workloads:

	- OLTP write-intensive workloads
	- Business Intelligence requiring MPP parallelism
	- Operational data store
	- Key-value store
	- GIS Geospatial
	- Mixed-workload environments
	- Multi-tenant provider hosted environments

#### 5.CitusDB分布式

#### PostgreSQL vs Greenplums

- [PostgreSQL 10 vs Deepgreen(Greenplum)](https://yq.aliyun.com/articles/128016)


### II.Greenplum(OLAP Solution)

#### Greenplum5

- [Greenplum系统管理指南](2016-04-15-greenplum-system-admin-guide.md)
- [Greenplum分析函数解析](2016-07-30-greenplum-analysis-function.md)
- [Greenplum架构设计研究](2017-02-11-greenplum-arch-design-note.md)
- [Greenplum最佳实践](2017-05-28-greenplum-best-practice-note.md)
- [Greenplum5最佳实践](2017-12-03-greenplum5-best-practice-note.md)

