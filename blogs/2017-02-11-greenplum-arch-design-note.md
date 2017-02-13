---
layout: post
category : datascience
tags : [bigdata,database,architect]
title: Greenplum Architect Design Note
---

Greenplum架构设计 Note
--------------------------------------------------

#### I.Greenplum Architecture

Pivotal Greenplum Database is a massively parallel processing (MPP-shared nothing architecture) database server with an architecture specially designed to manage large-scale analytic data warehouses and business intelligence workloads.Greenplum uses this high-performance system architecture to distribute the load of multi-terabyte data warehouses, and can use all of a system's resources in parallel to process a query.

It is based on PostgreSQL 8.2.15

The system catalog, optimizer, query executor, and transaction manager components have been modified and enhanced to be able to execute queries simultaneously across all of the parallel PostgreSQL database instances.

Greenplum Database also includes features designed to optimize PostgreSQL for business intelligence (BI) workloads.

![High Architecture](_includes/highlevel_arch.png).

_About the Greenplum Master_

The Greenplum Database master is the entry to the Greenplum Database system, accepting client connections and SQL queries, and distributing work to the segment instances.The global system catalog(Master) is the set of system tables that contain metadata about the Greenplum Database system itself.

_About the Greenplum Segments_

Greenplum Database segment instances are independent PostgreSQL databases that each store a portion of the data and perform the majority of query processing.
A segment host typically executes from two to eight Greenplum segments, depending on the CPU cores, RAM, storage, network interfaces, and workloads.

_About the Greenplum Interconnect_

The interconnect is the networking layer of the Greenplum Database architecture.<br/>
The interconnect refers to the inter-process communication between segments and the network infrastructure on which this communication relies. The Greenplum interconnect uses a standard 10-Gigabit Ethernet switching fabric.

By default, the interconnect uses User Datagram Protocol (UDP) with flow control for interconnect traffic to send messages over the network. The Greenplum software performs packet verification beyond what is provided by UDP. 

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




##### About Parallel Data Loading

##### About Redundancy and Failover in Greenplum Database

##### About Database Statistics in Greenplum Database


#### II.Working with Databases

#### III.Managing Performance



