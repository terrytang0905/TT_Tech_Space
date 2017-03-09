---
layout: post
category : datascience
tags : [bigdata,database,architect]
title: Greenplum Architect Design Note
---

Greenplum Architect Design Note
--------------------------------------------------

#### I.Greenplum Architecture

Pivotal Greenplum Database is a massively parallel processing (MPP-shared nothing architecture) database server with an architecture specially designed to manage large-scale analytic data warehouses and business intelligence workloads.Greenplum uses this high-performance system architecture to distribute the load of multi-terabyte data warehouses, and can use all of a system's resources in parallel to process a query.

It is based on PostgreSQL 8.2.15

The system catalog, optimizer, query executor, and transaction manager components have been modified and enhanced to be able to execute queries simultaneously across all of the parallel PostgreSQL database instances.

Greenplum Database also includes features designed to optimize PostgreSQL for business intelligence (BI) workloads.

![High Architecture](_includes/highlevel_arch.jpg).

_About the Greenplum Master_

The Greenplum Database master is the entry to the Greenplum Database system, accepting client connections and SQL queries, and distributing work to the segment instances.The global system catalog(Master) is the set of system tables that contain metadata about the Greenplum Database system itself.

_About the Greenplum Segments_

Greenplum Database segment instances are independent PostgreSQL databases that each store a portion of the data and perform the majority of query processing.
A segment host typically executes from two to eight Greenplum segments, depending on the CPU cores, RAM, storage, network interfaces, and workloads.

_About the Greenplum Interconnect(Greenplum Core Value)_

The interconnect is the networking layer of the Greenplum Database architecture.<br/>
The interconnect refers to the inter-process communication between segments and the network infrastructure on which this communication relies.<br/>
The interconnect tasks include query plan,data scan,query execution,redistribute,broadcast and so on.

> interconnect承载了并行查询计划生产和Dispatch分发（QD）、协调节点上QE执行器的并行工作、负责数据分布、Pipeline计算、镜像复制、健康探测等等诸多任务。

The Greenplum interconnect uses a standard **10-Gigabit Ethernet switching fabric**.<br/>
By default, the interconnect uses User Datagram Protocol(UDP) with flow control for interconnect traffic to send messages over the network. The Greenplum software performs packet verification beyond what is provided by UDP. 

##### About Management and Monitoring Utilities

Greenplum provides utilities for the following administration tasks:

- Installing Greenplum Database on an array
- Initializing a Greenplum Database System
- Starting and stopping Greenplum Database
- Adding or removing a host
- Expanding the array and redistributing tables among new segments
- Managing recovery for failed segment instances
- Managing failover and recovery for a failed master instance
- Backing up and restoring a database (in parallel)
- Loading data in parallel
- Transferring data between Greenplum databases
- System state reporting

![Network Architecture](_includes/cc_arch_gpdb.png).

Segment data collection agents send their data to the Greenplum master at regular intervals (typically every 15 seconds).

##### About Concurrency Control in Greenplum Database

Greenplum Database uses the PostgreSQL Multiversion Concurrency Control(MVCC) model to manage concurrent transactions for heap tables.

Concurrency control in a database management system allows concurrent queries to complete with correct results while ensuring the integrity of the database. With MVCC, each query operates on a snapshot of the database when the query starts. Queries that read rows can never block waiting for transactions that write rows. Conversely, queries that write rows cannot be blocked by transactions that read rows. 

> Append-optimized tables are managed with a different concurrency control model than the MVCC model discussed in this topic. 

_Snapshots_

A snapshot is the set of rows that are visible at the beginning of a statement or transaction. The snapshot ensures the query has a consistent and valid view of the database for the duration of its execution.

Each transaction is assigned a unique transaction ID (XID), an incrementing 32-bit value.When a transaction inserts a row, the XID is saved with the row in the xmin system column. When a transaction deletes a row, the XID is saved in the xmax system column. Updating a row is treated as a delete and an insert, so the XID is saved to the xmax of the current row and the xmin of the newly inserted row.

Multi-statement transactions must also record which command within a transaction inserted a row (cmin) or deleted a row (cmax) so that the transaction can see changes made by previous commands in the transaction. The command sequence is only relevant during the transaction, so the sequence is reset to 0 at the beginning of a transaction. 

The master coordinates distributed transactions with the segments using a cluster-wide session ID number, called *gp_session_id*. The segments maintain a mapping of distributed transaction IDs with their local XIDs. The master coordinates distributed transactions across all of the segment with the two-phase commit protocol. 

_Transaction ID Wraparound_

Greenplum Database uses modulo 232 arithmetic with XIDs, which allows the transaction IDs to wrap around, much as a clock wraps at twelve o'clock. 

Vacuuming the database at least every two billion transactions prevents XID wraparound. Greenplum Database monitors the transaction ID and warns if a VACUUM operation is required.<br/>
See [Recovering from a Transaction ID Limit Error](http://gpdb.docs.pivotal.io/43110/admin_guide/managing/maintain.html#topic3__np160654) for the procedure to recover from this error.

_Transaction Isolation Modes_

The SQL standard describes three phenomena that can occur when database transactions run concurrently:

	- Dirty read – a transaction can read uncommitted data from another concurrent transaction.
	- Non-repeatable read – a row read twice in a transaction can change because another concurrent transaction committed changes after the transaction began.
	- Phantom read – a query executed twice in the same transaction can return two different sets of rows because another concurrent transaction added rows.

The Greenplum Database SQL commands allow you to request 

- READ UNCOMMITTED
- READ COMITTED
- REPEATABLE READ 
- SERIALIZABLE 

Greenplum Database treats READ UNCOMMITTED the same as READ COMMITTED. Requesting REPEATABLE READ produces an error; use SERIALIZABLE instead. The default isolation mode is READ COMMITTED.

The MVCC snapshot isolation model prevents dirty reads, non-repeatable reads, and phantom reads without expensive locking, but there are other interactions that can occur between some SERIALIZABLE transactions in Greenplum Database that prevent them from being truly serializable.

[mvcc_example](http://gpdb.docs.pivotal.io/43110/admin_guide/intro/mvcc_example.html)

##### About Parallel Data Loading

Greenplum supports fast, parallel data loading with its external tables feature.

By using external tables in conjunction with Greenplum Database's parallel file server(gpfdist), administrators can achieve maximum parallelism and load bandwidth from their Greenplum Database system.

Another Greenplum utility, gpload, runs a load task that you specify in a YAML-formatted control file. You describe the source data locations, format, transformations required, participating hosts, database destinations, and other particulars in the control file and gpload executes the load. The gpload is the package solution based on gpfdist.


##### About Redundancy and Failover in Greenplum Database

You can deploy Greenplum Database without a single point of failure by mirroring components. 

_About Segment Mirroring_

Mirror segments allow database queries to fail over to a backup segment if the primary segment becomes unavailable.
Mirroring is strongly recommended for production systems and required for Pivotal support.
The secondary (mirror) segment must always reside on a different host than its primary segment to protect against a single host failure.

Two standard mirroring configurations are available when you initialize or expand a Greenplum system.

	- Group mirroring places all the mirrors for a host's primary segments on one other host in the cluster. 
	- Spread mirroring(command-line option) spreads each host's mirrors over the remaining hosts and requires that there are more hosts in the cluster than primary segments per host. 

![spread_mirroring](_includes/spread-mirroring.png)

_Segment Failover and Recovery_

When mirroring is enabled in a Greenplum Database system, the system will automatically fail over to the mirror segment if a primary copy becomes unavailable. 
If the master cannot connect to a segment instance, it marks that segment instance as down in the Greenplum Database system catalog and brings up the mirror segment in its place. A failed segment instance will remain out of operation until an administrator takes steps to bring that segment back online. 

If you do not have mirroring enabled, the system will automatically shut down if a segment instance becomes invalid. You must recover all failed segments before operations can continue.

_About Master Mirroring_

You can also optionally deploy a backup or mirror of the master instance on a separate host from the master node. A backup master host serves as a warm standby in the event that the primary master host becomes unoperational. The standby master is kept up to date by a transaction log(WAL)replication process, which runs on the standby master host and synchronizes the data between the primary and standby master hosts.

_About Interconnect Redundancy_

##### About Database Statistics in Greenplum Database

_ANALYZE_

Statistics are metadata that describe the data stored in the database. The query optimizer needs up-to-date statistics to choose the best execution plan for a query.For example, if a query joins two tables and one of them must be broadcast to all segments, the optimizer can choose the smaller of the two tables to minimize network traffic.

The statistics used by the optimizer are calculated and saved in the system catalog by the ANALYZE command. There are three ways to initiate an analyze operation:
- You can run the ANALYZE command directly.
- You can run the analyzedb management utility outside of the database, at the command line.
- An automatic analyze operation can be triggered when DML operations are performed on tables that have no statistics or when a DML operation modifies a number of rows greater than a specified threshold.

In most cases, the default settings provide the information needed to generate correct execution plans for queries. If the statistics produced are not producing optimal query execution plans, the administrator can tune configuration parameters to produce more accurate stastistics by increasing the sample size or the granularity of statistics saved in the system catalog. 

_System Statistics_

Table Size

The query planner seeks to minimize the disk I/O and network traffic required to execute a query, using estimates of the number of rows that must be processed and the number of disk pages the query must access.  The data from which these estimates are derived are the pg_class system table columns reltuples and relpages, which contain the number of rows and pages at the time a VACUUM or ANALYZE command was last run.

_Analyzing Partitioned and Append-Optimized Tables_

When the ANALYZE command is run on a partitioned table, it analyzes each leaf-level subpartition, one at a time. You can run ANALYZE on just new or changed partition files to avoid analyzing partitions that have not changed.

The analyzedb command-line utility: Each time analyzedb runs, it saves state information for append-optimized tables and partitions in the db_analyze directory in the master data directory. The next time it runs, analyzedb compares the current state of each table with the saved state and skips analyzing a table or partition if it is unchanged. Heap tables are always analyzed.

If the Pivotal Query Optimizer is enabled, you also need to run ANALYZE ROOTPARTITION to refresh the root partition statistics. The Pivotal Query Optimizer requires statistics at the root level for partitioned tables. 

_Automatic Statistics Collection_

Automatic statistics collection has three modes:

- none disables automatic statistics collection.
- on_no_stats triggers an analyze operation for a table with no existing statistics when any of the commands CREATE TABLE AS SELECT, INSERT, or COPY are executed on the table.
- on_change triggers an analyze operation when any of the commands CREATE TABLE AS SELECT, UPDATE, DELETE, INSERT, or COPY are executed on the table and the number of rows affected exceeds the threshold defined by the gp_autostats_on_change_threshold configuration parameter.


##### Enabling High Availability Features

_Hardware Level RAID_

A best practice Greenplum Database deployment uses hardware level RAID to provide high performance redundancy for single disk failure without having to go into the database level fault tolerance. This provides a lower level of redundancy at the disk level.

_Segment Mirroring & Master Mirroring_

_Dual Clusters_

An additional level of redundancy can be provided by maintaining two Greenplum Database clusters, both storing the same data.

> Two methods for keeping data synchronized on dual clusters are "dual ETL" and "backup/restore".

_Backup and Restore_

Making regular backups of the databases is recommended except in cases where the database can be easily regenerated from the source data. 

Use the gpcrondump utility to backup Greenplum databases. gpcrondomp performs the backup in parallel across segments, so backup performance scales up as hardware is added to the cluster.

_Incremental Backups_

Greenplum Database allows incremental backup at the partition level for append-optimized and column-oriented tables. When you perform an incremental backup, only the partitions for append-optimized and column-oriented tables that have changed since the previous backup are backed up. (Heap tables are always backed up.) 

Incremental backup is beneficial only when the database contains large, partitioned tables where all but one or a few partitions remain unchanged between backups.

##### Backing Up and Restoring Databases

Greenplum Database supports parallel and non-parallel methods for backing up and restoring databases. Parallel operations scale regardless of the number of segments in your system, because segment hosts each write their data to local disk storage simultaneously. With non-parallel backup and restore operations, the data must be sent over the network from the segments to the master, which writes all of the data to its storage. 

_Parallel Backup and Restore_

The Greenplum Database parallel dump utility gpcrondump backs up the Greenplum master instance and each active segment instance at the same time.<br/>
By default, gpcrondump creates dump files in the db_dumps subdirectory of each segment instance. On the master, gpcrondump creates several dump files, containing database information such as DDL statements, the system catalog tables, and metadata files. On each segment, gpcrondump creates one dump file, which contains commands to recreate the data on that segment. Each file created for a backup begins with a 14-digit timestamp key that identifies the backup set the file belongs to.


#### II.Working with Databases

##### Defining Database Objects

Tablespaces allow database administrators to have multiple file systems per machine and decide how to best use physical storage to store database objects.


#### III.Working with Databases

##### About Greenplum Query Processing

_Understanding Query Planning and Dispatch_

The master receives, parses, and optimizes the query. The resulting query plan is either parallel or targeted. The master dispatches parallel query plans to all segments

![Dispatching the Parallel Query Plan](_includes/parallel_plan.jpg)

Each segment is responsible for executing local database operations on its own set of data.query plans.<br/>
Most database operations—such as table scans, joins, aggregations, and sorts—execute across all segments in parallel. Each operation is performed on a segment database independent of the data stored in the other segment databases.

Dispatching a Targeted Query Plan 

Certain queries may access only data on a single segment, such as single-row INSERT, UPDATE, DELETE, or SELECT operations or queries that filter on the table distribution key column(s). 

_Understanding Greenplum Query Plans_

A query plan is the set of operations Greenplum Database will perform to produce the answer to a query. Each node or step in the plan represents a database operation such as a table scan, join, aggregation, or sort. Plans are read and executed from bottom to top.<br/>
Greenplum Database has an additional operation type called *motion*. A motion operation involves moving tuples between the segments during query processing. <br/>
To achieve maximum parallelism during query execution, Greenplum divides the work of the query plan into *slices*. A slice is a portion of the plan that segments can work on independently. A query plan is sliced wherever a motion operation occurs in the plan, with one slice on each side of the motion.<br/>
The query plan for this example has a *redistribute motion* that moves tuples between the segments to complete the join.The redistribute motion is necessary because the customer table is distributed across the segments by cust_id, but the sales table is distributed across the segments by sale_id. To perform the join, the sales tuples must be redistributed by cust_id. The plan is sliced on either side of the redistribute motion, creating slice 1 and slice 2.<br/>
This query plan has another type of motion operation called a *gather motion*. A gather motion is when the segments send results back up to the master for presentation to the client. 

_Understanding Parallel Query Execution_

Greenplum creates a number of database processes to handle the work of a query. On the master, the query worker process is called the query dispatcher (QD). The QD is responsible for creating and dispatching the query plan.It also accumulates and presents the final results. On the segments, a query worker process is called a query executor (QE). A QE is responsible for completing its portion of work and communicating its intermediate results to the other worker processes.<br/>

Related processes that are working on the same slice of the query plan but on different segments are called *gangs*. As a portion of work is completed, tuples flow up the query plan from one gang of processes to the next. This inter-process communication between the segments is referred to as the interconnect component of Greenplum Database.

![gangs process](_includes/gangs_process.jpg)

#### IV. Greenplum Query Optimizer

The Pivotal Query Optimizer extends the planning and optimization capabilities of the Greenplum Database legacy optimizer. The Pivotal Query Optimizer is extensible and achieves better optimization in multi-core architecture environments.

The Pivotal Query Optimizer also enhances Greenplum Database query performance tuning in the following areas:

	* Queries against partitioned tables
	* Queries that contain a common table expression (CTE)
	* Queries that contain subqueries

The Pivotal Query Optimizer co-exists with the legacy query optimizer. By default, Greenplum Database uses the legacy query optimizer.

The Pivotal Query Optimizer includes enhancements for specific types of queries and operations:

	- Queries Against Partitioned Tables +
	- Queries that Contain Subqueries +
	- Queries that Contain Common Table Expressions +
	- DML Operation Enhancements with Pivotal Query Optimizer +
	- Improved join ordering
	- Join-Aggregate reordering
	- Sort order optimization
	- Data skew estimates included in query optimization

_Queries Against Partitioned Tables_

	* Partition elimination is improved.
	* Uniform multi-level partitioned tables are supported. For information about uniform multi-level partitioned tables, see About Uniform Multi-level Partitioned Tables.
	* Query plan can contain the Partition selector operator.
	* Partitions are not enumerated in EXPLAIN plans.

Pivotal Query Optimizer has introduced three new query operators that work together in a producer/consumer model to perform scans over partitioned tables: PartitionSelector, DynamicScan, and Sequence.

	* PartitionSelector computes all the child partition OIDs that satisfy the partition selection conditions given to it.
	* DynamicScan is responsible for passing tuples from the partitions identified by the PartitionSelector.
	* Sequence is an operator that executes its child operators and then returns the result of the last one.

_Queries that Contain Subqueries_

SubQuery Unnesting is probably the most significant enhancement in the Pivotal Query Optimizer, because of the heavy use of subqueries by the major BI/Reporting tools in the industry. A subquery is a query that is nested inside an outer query block, such as:

```sql
SELECT * FROM part
 WHERE price > (SELECT avg(price) FROM part)
 GROUP BY year;

```

	* Removing Unnecessary Nesting. 
	* Subquery Decorrelation.
	* Conversion of Subqueries into Joins.

_Queries that Contain Common Table Expressions_

CTEs are temporary tables that are used for just one query, and are typically heavily utilized in analytical workloads. <br/>
Pivotal Query Optimizer introduces a new producer-consumer model for WITH clause, much like the model introduced for Dynamic Partition Elimination. The model allows evaluating a complex expression once, and consuming its output by multiple operators. 

_DML Operation Enhancements with Pivotal Query Optimizer_


[Query Profiling](http://gpdb.docs.pivotal.io/43110/admin_guide/query/topics/query-profiling.html#topic39)

_Reading EXPLAIN Output_

A query plan is a tree of nodes. Each node in the plan represents a single operation, such as a table scan, join, aggregation, or sort.
The bottom nodes of a plan are usually table scan operations: sequential, index, or bitmap index scans.

The topmost plan nodes are usually Greenplum Database motion nodes: redistribute, explicit redistribute, broadcast, or gather motions. These operations move rows between segment instances during query processing.

_Examining Query Plans to Solve Problems_

Examine its query plan and ask the following questions:

- Do operations in the plan take an exceptionally long time? 
- Are the optimizer's estimates close to reality?
- Are selective predicates applied early in the plan?
- Does the optimizer choose the best join order?When you have a query that joins multiple tables, make sure that the optimizer chooses the most selective join order. Joins that eliminate the largest number of rows should be done earlier in the plan so fewer rows move up the plan tree.
- Does the optimizer selectively scan partitioned tables?
- Does the optimizer choose hash aggregate and hash join operations where applicable? Hash operations are typically much faster than other types of joins or aggregations. Row comparison and sorting is done in memory rather than reading/writing from disk.


#### V. Greenplum SQL Definition

_SQL Lexicon_

_SQL Value Expressions_


#### VI.Managing Performance

Pivotal Query Optimizer introduces a new producer-consumer model for WITH clause, much like the model introduced for Dynamic Partition Elimination. The model allows evaluating a complex expression once, and consuming its output by multiple operators. 

- Dynamic Partition Elimination
- Memory Optimizations

Greenplum measures database performance based on the rate at which the database management system (DBMS) supplies information to requesters.

_Understanding the Performance Factors_

Database performance relies heavily on disk I/O and memory usage.

_Workload_

The total workload is a combination of user queries, applications, batch jobs, transactions, and system commands directed through the DBMS at any given time.

_Throughput_

_Contention_

_Optimization_

_Maintaining Database Statistcs_

Greenplum Database uses a cost-based query optimizer that relies on database statistics. Accurate statistics allow the query optimizer to better estimate the number of rows retrieved by a query to choose the most efficient query plan. 

_Optimizing Data Distribution_

When you create a table in Greenplum Database, you must declare a distribution key that allows for even data distribution across all segments in the system. If the data is unbalanced, the segments that have more data will return their results slower and therefore slow down the entire system.

_Workload Management with Resource Queues_

