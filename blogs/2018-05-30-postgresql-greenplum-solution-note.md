---
layout: post
category : datascience
tags : [bigdata,database,guide]
title: PostgreSQL&Greenplum Solution Practice Note
---

1.PostgreSQL10

2.PgBouncer数据库连接池

pgbouncer -d /etc/pgbouncer/pgbouncer.ini

psql -h 10.110.64.101 -p 6432 -U ir_user -d irview_iadt

- [pgbouncer](http://pgbouncer.projects.postgresql.org/doc/config.html)

3.Greenplum5

4.SQL查询性能问题

5.PostgreSQL分布式

5.1.PostgreSQL-XL

[PostgreSQL-XL](https://www.postgres-xl.org/documentation/intro-whatis-postgres-xl.html) 

Postgres-XL is a horizontally scalable open source SQL database cluster, flexible enough to handle varying database workloads:

	- OLTP write-intensive workloads
	- Business Intelligence requiring MPP parallelism
	- Operational data store
	- Key-value store
	- GIS Geospatial
	- Mixed-workload environments
	- Multi-tenant provider hosted environments

5.2.CitusDB


