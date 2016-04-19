---
layout: post
category : guide
tags : [bigdata,database]
title: Greenplum Database Command Guide
---

Greenplum 命令操作手册
------------------------------------

### 1.Greenplum初始化

```Shell
root -> sudo /bin/bash greenplum.bin //安装greenplum
source greenplum_path.sh //生效greenplum_path.sh
gpssh-exkeys -f hostlist //创建greenplum ssh访问隧道
gpssh -f hostlist
```
-创建数据库—
```Shell
[root@mdw gp]# su - gpadmin
[gpadmin@mdw ~]$ psql -d postgres
[gpadmin@yunying-newbi-01 ~]$ createdb yunyingADB -E utf-8
```
### 2.Greenplum服务管理

```Shell
su - gpadmin
gpstart # 正常启动
gpstop # 正常关闭
gpstop -M fast # 快速关闭
gpstop –r # 重启
gpstop –u # 重新加载配置文件
```

### 3.psql登陆与退出

- 正常登陆

```Shell
psql gpdb
psql -d gpdb -h gphostm -p 5432 -U gpadmin
psql -d yunyingADB  -h 127.0.0.1 -p 2345 -U gpadmin
```

- 使用 utility 方式

```Shell
PGOPTIONS="-c gp_session_role=utility"
psql -h -d dbname hostname -p port
```
- 退出

在psql命令行执行\q

- 参数查询

```Shell
psql -c 'SHOW ALL;' -d gpdb
gpconfig --show max_connections
```

- 创建数据库

createdb -h localhost -p 5432 dhdw

### 4.GP文件系统管理

- 文件系统名

gpfsdw

- 子节点，视 segment 数创建目录

```Shell
mkdir -p /gpfsdw/seg1
mkdir -p /gpfsdw/seg2
chown -R gpadmin:gpadmin /gpfsdw
```

- 主节点

```Shell
mkdir -p /gpfsdw/master
chown -R gpadmin:gpadmin /gpfsdw
gpfilespace -o gpfilespace_config
gpfilespace -c gpfilespace_config
```

- 创建GP表空间

```Shell
psql gpdb
create tablespace TBS_DW_DATA filespace gpfsdw;
SET default_tablespace = TBS_DW_DATA;
```

- 删除GP数据库

gpdeletesystem -d /gpmaster/gpseg-1 -f

- 查看segment配置

select * from gp_segment_configuration;

- 文件系统

select * from pg_filespace_entry;

- 磁盘、数据库空间

```SQL
SELECT * FROM gp_toolkit.gp_disk_free ORDER BY dfsegment;
SELECT * FROM gp_toolkit.gp_size_of_database ORDER BY sodddatname;
```

- 日志

```SQL
SELECT * FROM gp_toolkit.__gp_log_master_ext;
SELECT * FROM gp_toolkit.__gp_log_segment_ext;
```

- 索引占用空间

```SQL
SELECT soisize/1024/1024 as size_MB, relname as indexname
FROM pg_class, gp_toolkit.gp_size_of_index
WHERE pg_class.oid = gp_size_of_index.soioid
AND pg_class.relkind='i';
```

- OBJECT 的操作统计

```SQL
SELECT schemaname as schema, objname as table, usename as role, actionname as action, subtype as type, statime as time
FROM pg_stat_operations
WHERE objname = '<name>';
```

- 锁

```SQL
SELECT locktype, database, c.relname, l.relation, l.transactionid, l.transaction, l.pid, l.mode, l.granted, a.current_query
FROM pg_locks l, pg_class c, pg_stat_activity a
WHERE l.relation=c.oid AND l.pid=a.procpid ORDER BY c.relname;
```

- 队列

SELECT * FROM pg_resqueue_status;

### 5.GP表管理

- 表描述

/d+ <tablename>

- 表分析

VACUUM ANALYZE tablename;

- 表数据分布

SELECT gp_segment_id, count(*) FROM <table_name> GROUP BY gp_segment_id;

- 表占用空间

```SQL
SELECT relname as name, sotdsize/1024/1024 as size_MB, sotdtoastsize as toast, sotdadditionalsize as other FROM gp_toolkit.gp_size_of_table_disk as sotd, pg_class WHERE sotd.sotdoid = pg_class.oid ORDER BY relname;
```

### 6.GP数据管理

#### 6.1.常规数据管理

- 创建普通表

create table test select * from TD_APP_LOG_BUYER;

- 索引

CREATE INDEX idx_test ON test USING bitmap (ip);

- 查询数据

select ip , count(*) from test group by ip order by count(*);

#### 6.2.外部表数据服务

- 启动gpfdist服务

```Shell
gpfdist &
gpfdist -d /share/txt -p 8081 –l /share/txt/gpfdist.log &
gpfdist -d /data/greenplum/sourcedata/nb_base_trade -p 9000 -l /data/greenplum/log/gpfdist.log &
```

- 创建外部表，分隔符为 ’/t’

```SQL
drop EXTERNAL TABLE TD_APP_LOG_BUYER;
CREATE EXTERNAL TABLE TD_APP_LOG_BUYER (
 IP         text,
 ACCESSTIME text,
 REQMETHOD  text,
 URL        text,
 STATUSCODE int,
 REF        text,
 name       text,
 VID        text)
LOCATION ('gpfdist://gphostm:8081/xxx.txt')
FORMAT 'TEXT' (DELIMITER E'/t'
FILL MISSING FIELDS) SEGMENT REJECT LIMIT 1 percent;
```

```SQL
CREATE WRITABLE EXTERNAL TABLE unload_expenses
( LIKE expenses )
LOCATION ('gpfdist://etlhost-1:8081/expenses1.out',
'gpfdist://etlhost-2:8081/expenses2.out')
FORMAT 'TEXT' (DELIMITER ',')
DISTRIBUTED BY (exp_id);
```

```SQL
create READABLE external table  nb_base_buyer (
dp_id varchar(255) ,
seller_nick varchar(255) ,
buyer_nick varchar(255) ,
first_pay_date varchar(255) ,last_pay_date varchar(255) ,buyer_R integer ,buyer_R_tier varchar(255) ,buyer_F integer ,buyer_F_tier varchar(255) ,buyer_M double precision ,buyer_M_tier varchar(255) ,buyer_AUS double precision ,buyer_AUS_tier varchar(255) ,buyer_sum_num integer ,buyer_IPT double precision ) Location ( 'gpfdist://localhost:8080/temp1/' ) Format 'TEXT' (delimiter as ',' null as '\\N' escape 'OFF')
```

```SQL
create external table  nb_base_trade_3 (
tid varchar(255),
dp_id varchar(255),
user_name varchar(255),
seller_nick varchar(255) ,
buyer_nick varchar(255) ,
status varchar(255),
trade_from varchar(255),
trade_from_type varchar(255),
type varchar(255),
payment double precision,
payment_type varchar(255),
discount_fee double precision,
total_fee double precision,
created_time timestamp,
modified_time timestamp,
pay_date date,
pay_hour integer,
receive_name varchar(255),
receive_mobile varchar(255),
receive_phone varchar(255),
receive_zip varchar(255),
receive_address varchar(255),
receive_city varchar(255),
receive_district varchar(255),
receive_state varchar(255),
receive_region varchar(255),
receive_type varchar(255),
lifetime_order_rank integer,
day_order_rank integer,
day_is_repeat varchar(255),
day_rank_tab varchar(255),
day_is_new varchar(255),
month_order_rank integer,
month_is_repeat varchar(255),
month_rank_tab varchar(255),
month_is_new varchar(255),
quarter_order_rank integer,
quarter_is_repeat varchar(255),
quarter_rank_tab varchar(255),
quarter_is_new varchar(255),
year_order_rank integer,
year_is_repeat varchar(255),
year_rank_tab varchar(255),
year_is_new varchar(255)
) Location ( 'gpfdist://localhost:9000/part_3/' ) Format 'TEXT' (delimiter as '\001' null as '\\N' escape 'OFF')
```

```SQL
CREATE EXTERNAL TABLE nb_base_trade_external
(
  tid character varying(255),
  dp_id character varying(255),
  user_name character varying(255),
  seller_nick character varying(255),
  buyer_nick character varying(255),
  status character varying(255),
  trade_from character varying(255),
  trade_from_type character varying(255),
  type character varying(255),
  payment double precision,
  payment_type character varying(255),
  discount_fee double precision,
  total_fee double precision,
  created_time timestamp,
  modified_time timestamp,
  pay_date date,
  pay_hour integer,
  receive_name character varying(255),
  receive_mobile character varying(255),
  receive_phone character varying(255),
  receive_zip character varying(255),
  receive_address character varying(255),
  receive_city character varying(255),
  receive_district character varying(255),
  receive_state character varying(255),
  receive_region character varying(255),
  receive_type character varying(255),
  lifetime_order_rank integer,
  day_order_rank integer,
  day_is_repeat character varying(255),
  day_rank_tab character varying(255),
  day_is_new character varying(255),
  month_order_rank integer,
  month_is_repeat character varying(255),
  month_rank_tab character varying(255),
  month_is_new character varying(255),
  quarter_order_rank integer,
  quarter_is_repeat character varying(255),
  quarter_rank_tab character varying(255),
  quarter_is_new character varying(255),
  year_order_rank integer,
  year_is_repeat character varying(255),
  year_rank_tab character varying(255),
  year_is_new character varying(255)
)
 LOCATION (
    'gpfdist://localhost:9000/total_1/'
)
 FORMAT 'text' (delimiter '\001' null '\\N' escape 'OFF')
ENCODING 'UTF8';
```
- 外部表授权
> ALTER TABLE nb_base_trade_external OWNER TO gpadmin;

- 写权限
> GRANT INSERT ON writable_ext_table TO <name>;

- 外部表写数据
> INSERT INTO writable_ext_table SELECT * FROM regular_table;

- 从Greenplum数据库卸载（UNLOAD） 数据

#### 6.3. gpload

- 创建控制文件

- 加载数据

> gpload -f my_load.yml

#### 6.4 Copy数据

##### 6.4.1. COPY文件数据导入

```SQL
COPY country FROM '/data/gpdb/country_data'
 WITH DELIMITER '|' LOG ERRORS INTO err_country
 SEGMENT REJECT LIMIT 10 ROWS;
```
```SQL
copy  nb_base_trade_new from '/data/greenplum/sourcedata/nb_base_trade/total_1'
delimiter as '\001' null as '\\N'；
```

##### 6.4.2. COPY数据库导出

```SQL
COPY (SELECT * FROM country WHERE country_name LIKE 'A%') TO '/home/gpadmin/a_list_countries.out';
psql gpdbname –f yoursqlfile.sql
```
或者psql登陆后执行

### 7. Schema

Schema是Database中逻辑组织object和data.

在同一Database中，不同schema的对象可以使用相同的名称。
例如：A schema 中表叫tab1， B schema中表也可以叫tab1.  但是在同一个schema中就会报错

> SELECT * FROM myschema.mytable;<br/>
> 注意：如果sql中指定了schema名字的话，就查询指定schema，否则查询search path中配置参数。

_管理命令_
- [创建schema] => CREATE SCHEMA myschema;
- [创建并设置owner] =>  CREATE SCHEMA myschema AUTHORIZATION username;
- [查看当前schema] => SELECT current_schema();
- [查看search path] => SHOW search_path;
- [修改search path] => ALTER DATABASE mydatabase SET search_path TO myschema, public, pg_catalog;<br/>
   集群数据库schema设置(需添加相关schema到search_path中,否则无法正常创建Connection连接)

- [删除schema<必须是空schema,未包含任何对象>] => DROP SCHEMA myschema;
- [删除schema及数据库中所有对象] => DROP SCHEMA myschema CASCADE;

### x.psql 参数命令

- \h：查看SQL命令的解释，比如\h select。
- \?：查看psql命令列表。
- \l：列出所有数据库。
- \c [database_name]：连接其他数据库。
- \d：列出当前数据库的所有表格。
- \d [table_name]：列出某一张表格的结构。
- \du：列出所有用户。
- \e：打开文本编辑器。
- \conninfo：列出当前数据库和连接的信息
- \i yoursqlfile.sql
- \q 退出