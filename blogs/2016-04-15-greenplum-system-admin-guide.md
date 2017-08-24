---
layout: post
category : guide
tags : [bigdata,database]
title: Greenplum Database Command Guide
---

Greenplum 系统管理操作Notes
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

```SQL
SELECT * FROM pg_resqueue_status;

select * from pg_stat_activity where current_query not in ( '<IDLE>','<insufficient privilege>')
order by query_start, usename;
```

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

- 创建分区表

```SQL
create table nb_rfm_freq (
    dp_id varchar(255),
    buyer_nick varchar(255),
    dp_buyer varchar(255),
    frequency bigint,
    total_payment double precision,
    total_num bigint,
    max_payment double precision,
    last_interval varchar(255),
    last_created_date varchar(255),
    last_payment double precision,
    first_interval varchar(255),
    first_created_date varchar(255),
    first_payment double precision,
    avg_interval varchar(255),
    member_grade bigint,
    curr_date varchar(255),
    period integer
)DISTRIBUTED BY (period);
```

- 创建查询优化表

```SQL
CREATE TABLE "nb_analysis"."nb_rfm_freq" (
  "dp_id" varchar(255),
  "buyer_nick" varchar(255),
  "dp_buyer" varchar(255),
  "frequency" int8,
  "total_payment" float8,
  "total_num" int8,
  "max_payment" float8,
  "last_interval" varchar(255),
  "last_created_date" varchar(255),
  "last_payment" float8,
  "first_interval" varchar(255),
  "first_created_date" varchar(255),
  "first_payment" float8,
  "avg_interval" varchar(255),
  "member_grade" int8,
  "curr_date" varchar(255),
  "period" int4
)
WITH (appendonly=true,ORIENTATION=column,compresslevel=5)
distributed by (curr_date,period);
ALTER TABLE "nb_analysis"."nb_rfm_freq" OWNER TO "gpadmin";
```

greenplum 4.x 以后的appendonly表可以支持更新和删除操作，但是限制不能更新分布键所在的列

- 索引

CREATE INDEX idx1 on test (id); //B-tree Index 默认

CREATE INDEX idx_test ON test USING bitmap (ip); //Bitmap Index 位图索引

CREATE UNIQUE INDEX idx1 on test (id);

- 查询数据

select ip , count(*) from test group by ip order by count(*);

- 强制更新表字段类型

ALTER TABLE shop_order_detail ALTER COLUMN payment SET DEFAULT 0; <br/>
ALTER TABLE shop_order_detail ALTER COLUMN payment TYPE FLOAT USING payment::FLOAT

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

_容错导入_
```SQL
COPY shop_order_detail FROM '/data/hd_data/hd_order.csv' WITH DELIMITER E'\t' NULL as '' LOG ERRORS INTO err_order SEGMENT REJECT LIMIT 10000 ROWS; 
```
```SQL
COPY nb_base_trade FROM '/data/greenplum/sourcedata/nb_base_trade_exp/000003_0' WITH DELIMITER E'\001' NULL as '\\N' LOG ERRORS INTO err_order SEGMENT REJECT LIMIT 1000 ROWS; 
```

copy 命令如果出错 missing data for column columnname 则加上参数FILL MISSING FIELDS，默认的是用NULL值填充columnname所在列，但是真实的数据还是会进去的.

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

### 8. Greenplum系统优化

#### 8.1. Greenplum JDBC Driver

使用[Greenplum DataDirect JDBC Driver](https://network.pivotal.io/products/pivotal-gpdb#/releases) <br/>
(相比postgresql jdbc driver,性能差,原因未明)

#### 8.2. 数据压缩

当一个查询的结果过大溢出到硬盘时  采用gp_workfile_compress_algorithm指定的参数压缩，默认值none，可选值zlib，设置成zlib后，在密集型查询系统中可提升10%-20%的效率
设置方法:
```
gpconfig -c gp_workfile_compress_algorithm -v zlib
```
#### 8.3. 资源队列设置

自我创建资源队列，系统默认的资源队列pg_default，对内存参数没有做出限制，会有内存溢出的风险

资源队列相关参数

* ACTIVE_STATEMENTS:此参数限制队列中同是执行的query数量，当query数量超过此值是则处于等待状态。pg_default默认的值是20
* MEMORY_LIMIT:此参数限制起源队中所有活动query（参见ACTIVE_STATEMENTS参数）能使用的最大内存，不能超过物理内存，计算方法为 物理momery/机器的节点个数*0.9;


#### 8.4. 系统监控命令列表

gp_autostats_mode 参数控制统计信息发生的时机

  - none 不自动收集统计信息
  - on_change 当目标表变更的超过（gp_autostats_on_change_threshold）指定的行数之后开始收集
  - no_no_stats 当使用create tables as select 、insert、copy时，如果目标表没有收集过统计信息，数据库会用analyze收集统计信息


#### 8.5. 系统监控命令列表

--机器可以查看正在进行的会话数
ps -ef |grep -i postgres |grep -i con 在master

--表占的空间
```sql
select pg_size_pretty(pg_relation_size('schema.tablename'));
```
--查看数据库占用的空间
```sql
select pg_size_pretty(pg_database_size('databasename')); 
```
--查看一个schema占用的空间
```sql
select pg_size_pretty(pg_relation_size(tablename)) from pg_tables t inner join pg_namespace d on t.schemaname=d.nspname group by d.nspname;
```
--查看数据分布情况
```sql
select gp_segment_id,count(*) from tablename group by 1;
```
--查看锁的情况
```sql
SELECT locktype, database, c.relname, l.relation, l.transactionid, l.transaction, l.pid, l.mode, l.granted, a.current_query FROM pg_locks l, pg_class c, pg_stat_activity a WHERE l.relation=c.oid AND l.pid=a.procpid ORDER BY c.relname;
```
--查看当前用户的所有表信息
```sql
select * from pg_stat_user_tables;
```
--查看当前用户的index信息
```sql
select * from pg_stat_user_indexes;
```
--查看当前存活的查询
```sql
select procpid as pid, sess_id as session, usename as user, current_query as query, waiting, date_trunc('second', query_start) as start_time, client_addr as useraddr from pg_stat_activity where datname ='dbname' and current_query not like '%from pg_stat_activity%where datname =%'
order by start_time;
```
--查看正在运行的sql
```sql
select * from pg_stat_activity;
SELECT procpid, start, now() - start AS lap, current_query FROM (SELECT backendid, pg_stat_get_backend_pid(S.backendid) AS procpid,
pg_stat_get_backend_activity_start(S.backendid) AS start, pg_stat_get_backend_activity(S.backendid) AS current_query
FROM (SELECT pg_stat_get_backend_idset() AS backendid) AS S ) AS S WHERE current_query <> '<IDLE>' ORDER BY lap DESC;
```

--查看后端进行的SQL任务
```sql
select 'select pg_terminate_backend('||procpid||');',* from pg_stat_activity where datname = 'iadt';
```

--杀死正在执行的select语句
```sql
select pg_cancel_backend(pid int);
```
--杀死ddl语句
```sql
select pg_terminate_backend(pid int);
```
--修改分布键
```sql
alter table table_name set distributed by(column_1);
```
--查看操作记录(表创建 修改等)
```sql
SELECT schemaname as schema, objname as table, usename as role, actionname as action, subtype as type, statime as time
FROM pg_stat_operations WHERE objname = '';
```
--登录单个实例方法先登录数据库在执行以下是sql
```sql
dbname='-c gp_session_role=utility' psql  dbname  –p  xxxx
```
--查询节点状态
```sql
select * from gp_segment_configuration;
```
--获取分布键
```sql
select a.attrnums[i.i],b.attname.a.localoid::regclass from gp_distribution_policy a,(select generate_series(1,10))i(i),pg_attribute b where pg_attrnums[i.i] is not null and a.localoid=b.attrelid and attrnumsp[i.i]=attrnum and a.localoid='public.xxx'::regclass order by i.i;
```
--查看活跃的连接数,这个视图看一看到排队的sql排队的原因
```sql
select count(1) from pg_stat_activity;
```
--查看为gpadmin保留的连接数
```sql
show superuser_reserved_connections ;
```
--查看数据分布情况
```sql
get_ao_distribution(name)
```
--查看压缩率
```sql
get_ao_compression_ratio(name)
```
-- 查看表中是否含所有垃圾数据
```sql
gp_toolkit.__gp_aovisimap_compaction_info(select oid from pg_class where relname='tablename');最后一个字段percent_hidden，垃圾数据所占的百分比
```
--查询哪些表需要做统计收集的视图
```sql
gp_toolkit.gp_stats_missing
```
--查询哪些表需要做vaumm或者vacumm full视图
```sql
gp_toolkit.gp_bloat_diag
```
--查看down掉的节点视图
```sql
gp_toolkit.gp_pgdatabase_invalid
```
--查看资源队列的详细信息视图
```sql
select * gp_toolkit.gp_resq_activity where  and resqstatus = 'running'
```
--查看资源队列的简要信息
```sql
gp_toolkit.gp_resq_activity_by_queue
```
--查看资源队列正在处理的sql信息
```sql
gp_toolkit.gp_resq_priority_statement
```
--查看资源队列配置
```sql
gp_toolkit.gp_resqueue_status;
```

#### 8.5. 系统设置参数列表

gp_workfile_compress_algorithm  

   此参数配置成system级别，即用gpconfig -c -v的方式配置，可选值为none和zlib。此参数指定当一个查询数据量太大溢出到硬盘部分的数据的压缩格式，默认是none。配置成zlib在密集型查询系统中可提高10%-20%的查询效率。

gp_autostats_on_change_threshold

   此参数控制超过多少行数是收集统计信息，默认值 2147483647  

gp_resqueue_memory_policy

   此参数可选值为none和auto,当这设置为auto时内存受statement和资源队列的内存限制，同时work_mem、max_work_men、maintenance_work_men参数将失效。默认的值为none

gp_vmem_idle_resource_timeout

   设置数据库超时时间，超过此参数的的session将释放系统资源（内存，共享内存等），此参数越小集群并发度越高，默认值18s

gp_vmem_protect_limit

   这个值设置每个segment能使用的内存总数计算公式http://greenplum.org/calc/

log_min_duration_statement

   sql语句执行超过这个值是会记录日志默认值-1，也就是不记录日志（类似于mysql的慢查询统计功能）

max_appendonly_tables

   最大appendonly表的数目默认值10000

max_conncetions

   最大连接数默认值250，segment设置成master的5-10倍

max_statement_mem

   单个查询语句能使用的最大内存，默认值2000MB

shared_buffers

   此值的越大性能越好，但是设置过大会导致swap发生,默认值为125MB，建议将其设置为总内存的15%然后逐渐增大，观察最优值
   此值需要小于系统参数
     kernel.shmmax：master/standby取物理内存50%；segment取物理内存25%；
     shared_buffers：master/standby取物理内存10%;segment取物理内存10%/实例数；即可反之gp将不能启动

temp_buffers

   临时缓存区，数据库会按照此参数指定大小进行分片排序，将中间结果放在临时文件中，增加此参数会提高排序新更能但设置过大会导致swap发生，默认值1M

gp_log_format

   日志文件格式默认是csv 可选值csv、txt

gp_interconnect_setup_timeout

   在负载较大的参数中集群

statement_mem

   一次查询能使用内存大小，超出部分将溢出到磁盘,默认值125M

gp_workfile_limit_files_per_query

   如果为SQL查询分配的内存不足，Greenplum数据库会创建溢出文件（也叫工作文件）。在默认情况下，一个SQL查询最多可以创建 100000 个溢出文件，这足以满足大多数查询。该参数决定了一个查询最多可以创建多少个溢出文件。0意味着没有限制。限制溢出文件数据可以防止失控查询破坏整个系统。 如果分配内存不足或者出现数据倾斜，则一个SQL查询可能产生大量溢出文件。如果超过溢出文件上限，Greenplum数据库报错：

gp_appendonly_compaction_threshold

   默认值10，含义为一个百分比，当一个压缩表表的隐藏行数（删除或者更新的操作造成的垃圾数据）和总行数的比值，当Vacuum（without full）命令运行时，每个segment会判断自己持有的数据中隐藏行数和总行的比值和gp_appendonly_compaction_threshold进行比较，从而决定是否进行优化。如果比值低于endonly_compaction_threshold即使有垃圾数据也不会进行优化

resource_select_only

   默认值off，当为on是资源队列只对SELECT, SELECT INTO, CREATE TABLE AS SELECT,DECLARE CURSOR起作用，反之对所有操作起作用

stats_queue_level

   默认值off，决定视图pg_stat_resqueues是否被启用，此时图能看到资源队列的信息

gp_resqueue_priority_cpucores_per_segment

   指定cpu信息，计算方法为segment上的cpu核数除以segment个数，master 上面指定所有的cpu核数（机器上只有master进程）


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
