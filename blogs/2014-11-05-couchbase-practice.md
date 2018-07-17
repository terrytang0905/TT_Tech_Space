---
layout: post
category : bigdata
tags : [nosql, tutorial]
title: Couchbase NoSQL Database Notes
---

## Couchbase Practice
------------------------------------------------------


### Summary

As we all know, Memcached is very successful open-source caching technology for a period of time in the past. But all of data in Memcached server just is stored in memory level and the memory data couldn’t keep persistence in disk. Now Couchbase NoSQL database becomes a near-perfect replacement for Memcached that provides high performance data store in memory/disk level. We choose Couchbase to take Cache service and store massive frequent queries data efficiently. The following contents are about some thought how to use Couchbase correctly according to our daily use experience.

### High-Level Architecture 

Couchbase Server has a true shared-nothing architecture. It is setup as a cluster of multiple servers behind an application server. At the highest level, each node in a Couchbase cluster is identical and has two main components: the data manager and the cluster manager. This architecture scales out linearly without any single point of failure. Other important architectural elements are a powerful map reduce engine to incrementally index and query documents, and cross datacenter replication technology to replicate documents across geographical data centers.

Data is consistently hashed by the client to shards, which are evenly spread across all server nodes. The cluster map keeps track of which nodes store what data, and knows when nodes are added or go down.

### Auto-Sharding (Hash key sharding) 

Couchbase Server in cluster environment is support to auto-sharding feature. The basic unit of data manipulation in Couchbase Server is a document (JSON or binary data). Each document is associated with a key. The key space in Couchbase Server is partitioned based on a dynamically computed hash function (CRC32) into logical storage units called vBuckets. VBuckets are mapped to nodes across a cluster and stored in a lookup structure called the cluster map. Once a vBucket identifier has been calculated, a current copy of the cluster map is consulted within the client library to lookup the Couchbase Server node currently storing the active document associated with the key. The cluster map is shared among all the nodes in the Couchbase cluster as well as the Couchbase clients.The number of vBuckets always remains constant (1024 by design) regardless of the server topology.

When the number of nodes in the cluster changes (scaling-out or due to failures), redistribution of vBuckets is required to ensure that data is evenly distributed throughout the cluster and that application access to the data is load-balanced evenly across all the cluster nodes. This is triggered through a rebalance operation.

### High-availability and Failover  

High availability in the Couchbase Server cluster is achieved through replication at the vBucket level. Replication of data and failover in a Couchbase Server cluster provides consistent performance eliminating cold cache and sudden load shifts to the RDBMS layer. Couchbase also supports scale-out flexibility. It means that the synchronous speed is much faster between multi-node servers as server node is increased in cluster environment.

Couchbase maintains multiple copies of data within the cluster by replicating the active vBuckets (represented by A) on one node to its replica vBuckets on other nodes (represented by R). If a machine in the cluster crashes or becomes unavailable, the current cluster orchestrator will notify all the other machines in the cluster and, the replica vBuckets corresponding to the vBuckets on the down server node are made active. The cluster map is then updated on all the cluster nodes and the clients. This process of activating the replicas is known as failover, and is completed immediately once initiated. Based on Couchbase architecture limitation, auto-failover could be triggered in three more server nodes. If server nodes are less than three nodes, failover has to be triggered manually when a node crashes.

### Cluster Management and Monitoring 

The cluster manager supervises server configuration and interaction between servers within a Couchbase cluster. It is a critical component that manages replication and rebalancing operations in Couchbase. Although the cluster manager executes locally on each cluster node, it elects a clusterwide orchestrator node to oversee cluster conditions and carry out appropriate cluster management functions. If the orchestrator node crashes, existing nodes will detect that it is no longer available and will elect a new orchestrator immediately so that the cluster continues to operate without disruption. The cluster manager is built on Erlang/OTP, a proven environment for building and operating fault- tolerant distributed systems.

At a high level, there are three primary cluster manager components on each Couchbase node:

- The heartbeat watchdog periodically communicates with the cluster orchestrator using the heartbeat protocol. It provides regular health updates of the server. If the orchestrator crashes, existing cluster server nodes will detect the failed orchestrator and elect a new orchestrator.  

- The process monitor monitors what the local data manager does, restarts failed processes as required, and contributes status information to the heartbeat process.  

- The configuration manager receives, processes, and monitors a node’s local configuration. It controls the cluster map and active replication streams. When the cluster starts, the configuration manager pulls configuration of other cluster nodes and updates its local copy.

The Couchbase Server administration web console provides a unified view of the cluster health as well as the ability to perform granular drill-down analysis of operational statistics and information. Additionally, programmatic monitoring is possible using the REST API and a suite of command-line tools supporting integration capabilities with external monitoring systems. This simplifies your system management, monitoring and operations, enabling you to focus on the differentiating parts of your application.

### Data Management 

Every server in a Couchbase cluster includes a built-in multi-threaded object-managed cache, which provides consistent low-latency for read and write operations. Your application can access it using memcached compatible APIs such as get, set, delete, append, and prepend.

Hashtables represent partitions in Couchbase. Each document in a partition will have a corresponding entry in the hashtable, which stores the document’s ID, the metadata of the document, and potentially, the document’s content. In other words, the hashtable contains metadata for all the documents and may also serve as a cache for the document content. Since the hashtable is in memory and look-ups are fast, it offers a quick way of detecting whether the document exists in memory or not. Read and write operations first go to the in-memory object-managed cache: if a document being read is not in the cache, it is fetched from disk. The server also tracks read and write operations in the last 24-hours in an access log file. If you need to restart a server, the access log file is used for server warmup.

Each hashtable has multiple worker threads that process read/write requests. By default, there are three worker threads per data bucket, with two reader workers and one writer worker for the bucket. But this number can be increased to a max total of 8 worker threads. Before a worker thread accesses the hashtable, it needs to get a lock. Couchbase uses fine-grained locking to boost request throughput; each hashtable has multiple locks, and each lock controls access to certain sections of that hashtable. In a sense, Couchbase lock points to document level. As you add more documents to your cluster, the hashtable grows dynamically at runtime.

To keep track of document changes, Couchbase Server uses data structures called checkpoints. These are linked lists that keep track of outstanding changes that still need to be persisted by the storage engine and replicated to other replica partitions.

Disk writes in Couchbase Server are asynchronous. This means that as soon as the document is placed into the hashtable, and the mutation is added to the corresponding checkpoint, a success response is sent back to the client. If a mutation already exists for the same document, de-duplication takes place, and only the latest updated document is persisted to disk. Since Couchbase 2.1, there are multiple worker threads so that multiple processes can simultaneously read and write data from disk to maximize disk I/O throughput. These threads are assigned exclusively to certain groups of partitions. This ensures that only those assigned worker threads can serve the partition at a given time.

Disk fetch requests in Couchbase Server are batched. Documents are read from the underlying storage engine, and corresponding entries in the hashtable are filled. If there is no more space in memory, Couchbase needs to free up space from the object-managed cache. This process is called ejection. Couchbase tracks documents that are not recently accessed using the not-recently-used (NRU) metadata bit. Documents with the NRU bit set are ejected out of cache to the disk. Finally, after the disk fetch is complete, pending client connections are notified of the asynchronous I/O completion so that they can complete the read operation.

The user can store JSON documents or binary data in Couchbase Server. Documents are uniformly distributed across the cluster and stored in data containers called buckets. Buckets provide a logical grouping of physical resources within a cluster. For example, when you create a bucket in Couchbase, you can allocate a certain amount of RAM for caching data and configure the number of replicas. Since Couchbase 2.5, bucket memory quota (RAM) could be updated online after create operation.

To keep memory usage per bucket under control, Couchbase Server periodically runs a background task called the item pager. The high and low watermark limits for the item pager is determined by the bucket memory quota. The default high watermark value is 75 percent of the bucket memory quota, and the low watermark is 60 percent of the bucket memory quota. These watermarks are also configurable at runtime. If the high watermark is reached, the item pager scans the hashtable, ejecting items that are not recently used.

### Storage Engine 

In order to provide the above Couchbase features, Couchbase Server requires about 150 bytes of meta-data per item stored (memcached requires about 80). Additionally, the optional addition of replica copies of the data means RAM being taken up to store them as well.

With Couchbase’s append-only storage engine design, document mutations go only to the end of the file. If you append a document in Couchbase, it gets recorded at the end of the file. Files are open always in append mode, and there are no in-place file updates and the files are never in an inconsistent state. This improves disk write performance as updates are written sequentially. But writing to an ever-expanding file will eventually eat up all your diskspace. Therefore, Couchbase server has a process called compaction. Compaction cleans up the disk space by removing stale data and index values periodically so that the data and index files don’t unnecessarily eat up your disk space. It calculates the ratio of the actual file size to the current file. If this ratio goes below a certain threshold (configurable through the admin UI). Compaction scans through the current data file and copies non-stale data into a new data file. Since it is an online operation, Couchbase can still service requests. When the compaction process is completed, Couchbase copies over the data modified since the start of the compaction process to the new data file. The old data file is then deleted and the new data file is used until the next compaction cycle.

Couchbase Server uses multiple files for storage. It has a data file per partition, which we call data file, and multiple index files, which are either active or replicated indexes. The third type of file is a master file, which has metadata related to Couchbase views, and will be discussed later in the section on views.

As shown in the above picture, Couchbase Server organizes data files as b-trees. The root nodes shown in red contain pointers to intermediate nodes. These intermediate nodes contain pointers to the leaf nodes shown in blue. The root and intermediate nodes also track the sizes of documents under their sub-tree. The leaf nodes store the document ID, document metadata and pointers to document content. For index files the root and intermediate nodes track index items under their sub-tree.

### Query and Views 

With Couchbase Server, you can easily index and query JSON documents. Secondary indexes are defined using design documents and views.Each design document can have multiple views, and each Couchbase bucket can have multiple design documents. Design documents allow you to group views together. Views within a design document are processed sequentially and different design documents can be processed in parallel at different times.  

Views in Couchbase are defined in JavaScript using a map function, which pulls out data from your documents and an optional reduce function that aggregates the data emitted by the map function. The map function defines what attributes to build the index on.  Indexes in Couchbase are distributed; each server indexes the data it contains. Indexes are created on active documents and optionally on replica documents. During initial view building, on every server, Couchbase reads the partition data files and applies the map function across every document. Before writing the index file, the reduce function is applied to the b-tree nodes - if the node is a non-root node, the output of the reduce function is a partial reduce value of its sub-tree. If the node is a root node, the reduce value is a full reduce value over the entire b-tree.

Views in Couchbase are built asynchronously and hence eventually indexed. By default, queries on these views are eventually consistent with respect to the document updates. Indexes are created by Couchbase Server based on the view definition, but updating of these indexes can be controlled at the point of data querying, rather than each time data is inserted. 

Query contains some useful parameters to execute dynamic view on demand.
- IncludeDocs: set if the full documents should be included in the result.

- stale_state: allow the results from a stale view to be used. (If **stale=ok** is set, Couchbase will not refresh the view even if it is stale. The benefit of this is improved query latency. If **stale=update_after** is set, Couchbase will update the view **after** the stale result is returned. The default stale setting is update_after. If **stale=false** is set, Couchbase will refresh the view and return you most updated results. )

- limit & skip: is used to paginate the query result.

- group: group the results using the reduce function to a group or single row.

- group_level: group the result according to key fragment. The group degree depends on group level. (The sample group level is 1,2,3)

- range: returns records in the given key range.

- full_set: is used to scan full cluster dataset when querying documents.(The parameter is excluded in the current client SDK so far.Perhaps Couchbase developer is worry about the query performance if scanning full dataset.)

Please see the sample Couchbase Client Query SDK from this link: https://github.com/terrytang0905/JavaDev/tree/master/cache-cluster

New generation Couchbase query language, known as N1QL or ‘Nickel’. N1QL is similar to the standard SQL language for relational databases, but it is also includes some additional features which are suited for document-oriented databases. N1QL will be published in Couchbase version 3.0. It optimizes the usability of query document effectively.

### Cross Datacenter Replication 

Cross datacenter replication provides an easy way to replicate active data to multiple, geographically diverse datacenters either for disaster recovery or to bring data closer to its users. XDCR and intra-cluster replication occurs simultaneously. Intra-cluster replication is taking place within the clusters at both Datacenter 1 and Datacenter 2, while at the same time XDCR is replicating documents across datacenters. On each node, after a document is persisted to disk, XDCR pushes the replica documents to other clusters. On the destination cluster, replica documents received will be stored in the Couchbase object managed cache so that replica data on the destination cluster can undergo low latency read/ write operations.

### Best Practice

1.  The key-value document in the different content type couldn’t optimize the query/index performance through creating multiple different buckets like other RDBMS or NoSQL. So the single bucket could gain the optimal read/write performance.

2.  Because Couchbase single server or cluster server need the massive memory space, the memory resource in Couchbase is exclusive so that the physics server resource couldn’t be optimized the full use. So deploying Couchbase on virtual machine could resolve this problem perfectly.

3.  The bucket memory quota RAM could be online updated accordingly since Couchbase 2.5.

4.  For linux server, the frequency of virtual memory swap space partition will affect the memory/disk access performance. Through swappiness setting update, it could reduce disk cache access frequency and keep most of cache data in physics memory not disk. The advantage is that Couchbase read/write performance is high and the disadvantage is that the operation will cause the large numbers of memory occupancy. 

    Here is the linux shell command to update swappiness parameter. 
    (Range: 0~100. Swappiness=0 means to use the max volume physics memory and swappiness=100 means to use swap partition actively.)
    $ cat /proc/sys/vm/swappiness 
    $ sudo sysctl vm.swappiness=10 or vm.swappiness=0

### Limitation

In order to keep high performance, Couchbase always occupy high volume memory size and disk size exclusively. In this circumstance, Couchbase requires the competent hardware configuration and the low hardware configuration will cause Couchbase down or OOM exception.

Currently the Couchbase query function is very hard to use for developer or DBA even if Couchbase view could help query document and support map/reduce function. Because Couchbase query usage is very different from the common SQL query language. Besides that, view query impacts performance very deeply whatever is development view or product view. The product view isn’t support to update. If trying to execute dynamic view query, the customer must design the development view on demand firstly and publish it to product view mode.

### Conclusion 

At a word, the design philosophy of Couchbase substitutes memory and disk space for speed time and performance. Due to this philosophy, Couchbase architecture is unique compare with other NoSQL such as mongoDB. Couchbase simple query performance is much better than mongoDB but the query usage is much more elusive than mongoDB. In the conclusion, Couchbase is a special NoSQL database that has the outstanding advantage and the distinct disadvantage. It’s the wise choice to adopt Couchbase in the specific not most situation.

### Reference

[http://docs.couchbase.com/](http://docs.couchbase.com/admin/admin/Couchbase-intro.html)

[http://www.couchbase.com/couchbase-server/architecture](http://www.couchbase.com/nosql-databases/about-couchbase-server#GeneralPurpose)

**Thank you** for reading this far.

## Next Steps

Please take a look at [{{ site.categories.api.first.title }}]({{ BASE_PATH }}{{ site.categories.api.first.url }})
or jump right into [Usage]({{ BASE_PATH }}{{ site.categories.usage.first.url }}) if you'd like.