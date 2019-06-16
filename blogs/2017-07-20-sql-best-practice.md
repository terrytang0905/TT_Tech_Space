---
layout: post
category : sql
tags : [database,datascience,sql]
title: Standard SQL Best Practice Note
---

## SQL Best Practice
------------------------------------------------------------

- SQL执行顺序
```sql
from... where... group by... having.... select ... order by...
```

**1.避免在 where 子句中对字段进行null值判断**

应尽量避免在 where 子句中对字段进行null值判断，否则将导致引擎放弃使用索引而进行全表扫描，如：

```sql
select id from t where num is null
可以在num上设置默认值0，确保表中num列没有null值，然后这样查询：
select id from t where num=0
```
**2.避免在 where 子句中使用!=或<>操作符**

应尽量避免在where子句中使用!=或<>操作符，否则将导致引擎放弃使用索引而进行全表扫描。优化器将无法通过索引来确定将要命中的行数,因此需要搜索该表的所有行。

**3.避免在 where 子句中使用or来连接条件**

应尽量避免在where子句中使用or来连接条件，否则将导致引擎放弃使用索引而进行全表扫描，如：
```sql
select id from t where num=10 or num=20
```
可以这样查询：
```sql
select id from t where num=10
union all
select id from t where num=20
```

**4.in和 not in也要慎用**

in和not in也要慎用，因为in会使系统无法使用索引,而只能直接搜索表中的数据。如：
```sql
select id from t where num in(1,2,3)
```

对于连续的数值，能用 between就不要用 in了：
```sql
select id from t where num between 1 and 3
```

**5.避免在索引的字符数据中使用非打头字母搜索**

尽量避免在索引过的字符数据中，使用非打头字母搜索。这也使得引擎无法利用索引。 见如下例子：

```sql
SELECT * FROM T1 WHERE NAME LIKE ‘%L%’(错误示范)
SELECT * FROM T1 WHERE SUBSTING(NAME,2,1)=’L’(错误示范)
SELECT * FROM T1 WHERE NAME LIKE ‘L%’(正确示范) 
```

即使NAME字段建有索引，前两个查询依然无法利用索引完成加快操作，引擎不得不对全表所有数据逐条操作来完成任务。而第三个查询能够使用索引来加快操作。

**6.必要时强制查询优化器使用某个索引**

必要时强制查询优化器使用某个索引，如在where子句中使用参数，也会导致全表扫描。因为SQL只有在运行时才会解析局部变量，但优化程序不能将访问计划的选择推迟到运行时;它必须在编译时进行选择。然而，如果在编译时建立访问计划，变量的值还是未知的，因而无法作为索引选择的输入项。如下面语句将进行全表扫描：
```sql
select id from t where
可以改为强制查询使用索引：
select id from t with(index(索引名)) where
```

**7.避免在 where 子句中对字段进行表达式操作**

应尽量避免在where子句中对字段进行表达式操作，这将导致引擎放弃使用索引而进行全表扫描。如：

```sql
SELECT* FROM T1 WHERE F1/2=100
应改为:
SELECT* FROM T1 WHERE F1=100*2
```
```sql
SELECT *FROM RECORD WHERE SUBSTRING(CARD_NO,1,4)=’5378’
应改为:
SELECT *FROM RECORD WHERE CARD_NO LIKE ‘5378%’
```
```sql
SELECT member_number,first_name,last_name FROM members
WHERE DATEDIFF(yy,datofbirth,GETDATE())> 21
应改为:
SELECT member_number,first_name,last_name FROM members
WHERE dateofbirth
```
即：任何对列的操作都将导致表扫描，它包括数据库函数、计算表达式等等，查询时要尽可能将操作移至等号右边。

**8.避免在where子句中对字段进行函数操作**

应尽量避免在where子句中对字段进行函数操作，这将导致引擎放弃使用索引而进行全表扫描。如：
```sql
select id from t where substring(name,1,3)=’abc’—name
以abc开头的id
select id from t where datediff(day,createdate,’2005-11-30′)=0–‘2005-11-30’
生成的id
操作符左侧禁止使用函数 
应改为:
select id from t where name like ‘abc%’
select id from t where createdate>=’2005-11-30’and createdate<‘2005-12-1′
```

**9.在使用索引字段作为条件时……**

在使用索引字段作为条件时，如果该索引是复合索引，那么必须使用到该索引中的第一个字段作为条件时才能保证系统使用该索引，否则该索引将不会被使用，并且应尽可能的让字段顺序与索引顺序相一致。

**10.很多时候用 exists是一个好的选择**

很多时候用 exists是一个好的选择：
```sql
selectnum from a where num in (select num from b)
```
用下面的语句替换：
```sql
selectnum from a where exists (select 1 from b where num=a.num)
```
```sql
SELECT SUM(T1.C1) FROM T1 WHERE(
(SELECT COUNT(\*) FROM T2 WHERE T2.C2=T1.C2>0)

SELECT SUM(T1.C1) FROM T1 WHERE EXISTS(SELECT * FROM T2 WHERE T2.C2=T1.C2)
```

两者产生相同的结果，但是后者的效率显然要高于前者。因为后者不会产生大量锁定的表扫描或是索引扫描。
如果你想校验表里是否存在某条纪录，不要用count(\*)那样效率很低，而且浪费服务器资源。可以用EXISTS代替。如：

```sql
IF (SELECT COUNT(*) FROM table_name WHERE column_name=‘xxx’)
可以写成：
IF EXISTS (SELECT * FROM table_name WHERE column_name =’xxx’)
```

经常需要写一个T_SQL语句比较一个父结果集和子结果集，从而找到是否存在在父结果集中有而在子结果集中没有的记录，如：

```sql
SELECT a.hdr_key FROM hdr_tbl a—-tbla表示tbl用别名a代替
WHERE NOT EXISTS (SELECT * FROM dtl_tbl b WHERE a.hdr_key =b.hdr_key)

SELECT a.hdr_key FROM hdr_tbla
LEFT JOIN dtl_tbl b ON a.hdr_key=b.hdr_key WHERE b.hdr_key IS NULL

SELEC Thdr_key FROM hdr_tbl
WHERE hdr_key NOT IN (SELECT hdr_key FROM dtl_tbl)

三种写法都可以得到同样正确的结果，但是效率依次降低。
```

**11.适当地使用临时表**

避免频繁创建和删除临时表，以减少系统表资源的消耗。 
临时表并不是不可使用，适当地使用它们可以使某些例程更有效，例如，当需要重复引用大型表或常用表中的某个数据集时。但是，对于一次性事件，最好使用导出表。

**12.可以使用 select into/insert into select 代替 create table**

	在新建临时表时，如果一次性插入数据量很大，那么可以使用 select into 代替 create table，避免造成大量 log ，以提高速度;
	如果数据量不大，为了缓和系统表的资源，应先create table，然后insert。

**13.在存储过程的最后务必将所有的临时表显式删除**

如果使用到了临时表，在存储过程的最后务必将所有的临时表显式删除，先truncate table ，然后 drop table，这样可以避免系统表的较长时间锁定。

**14.在存储过程和触发器的开始处设置 SET NOCOUNT ON**

在所有的存储过程和触发器的开始处设置 SET NOCOUNT ON，在结束时设置 SET NOCOUNT OFF。无需在执行存储过程和触发器的每个语句后向客户端发送DONE_IN_PROC消息。

**15.避免大事务操作**

尽量避免大事务操作，提高系统并发能力。

**16.避免向客户端返回大数据量**

尽量避免向客户端返回大数据量，若数据量过大，应该考虑相应需求是否合理，比如是否返回全对象，可不可以减少某些非必要字段。

默认要求RowLimit=1000

**17.避免使用不兼容的数据类型**

避免使用不兼容的数据类型,减少类型转换。例如float和int、char和varchar、binary和varbinary是不兼容的。数据类型的不兼容可能使优化器无法执行一些本来可以进行的优化操作。例如:

```sql
SELECT name FROM employee WHERE salary >60000
```
在这条语句中,如salary字段是money型的,则优化器很难对其进行优化,因为60000是个整型数。我们应当在编程时将整型转化成为货币型,而不要等到运行时转化。

**18.充分利用连接条件**

充分利用连接条件，在某种情况下，两个表之间可能不只一个的连接条件，这时在WHERE 子句中将连接条件完整的写上，有可能大大提高查询速度。例：

```sql
SELECT SUM(A.AMOUNT) FROM ACCOUNT A,CARD B WHERE A.CARD_NO =B.CARD_NO
SELECT SUM(A.AMOUNT) FROM ACCOUNT A,CARD B WHERE A.CARD_NO =B.CARD_NO AND A.ACCOUNT_NO=B.ACCOUNT_NO
第二句将比第一句执行快得多。
```

**19.使用视图加速查询**

	使用视图加速查询把表的一个子集进行排序并创建视图，有时能加速查询。它有助于避免多重排序操作，而且在其他方面还能简化优化器的工作。

**20.尽量用GROUP BY替代DISTINCT**

```sql
SELECT DISTINCT OrderID FROM Details WHERE UnitPrice >10
可改为：
SELECT OrderID FROM Details WHERE UnitPrice >10 GROUP BY OrderID
```

**21.COUNT(DISTINCT)是数据库查询的性能杀手**

	使用子查询可提升COUNT DISTINCT速度
	先聚合,然后Join.以减少处理数据量

**22.能用UNION ALL的时候就不用UNION**

	能用UNION ALL就不要用UNION,用UNION ALL加GROUP BY的方式替代UNION。
	UNION ALL不执行SELECT DISTINCT函数，这样就会减少很多不必要的资源  
