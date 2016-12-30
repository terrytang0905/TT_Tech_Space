---
layout: post
category : bigdata
tags : [nosql, tutorial]
title: MongoDB Practice Thoughts
---
{% include JB/setup %}

In the past one year, I have chance to take responsibility for design data storage using MongoDB in mobile internet application.It is very amazing adventure for NoSQL database study.
Some MongoDB features need to be recognized if you want to adopt it in new product.

### MongoDB advantage
From my perspective, the following MongoDB advantage could be utilized.

- Firstly, MongoDB is the schema-less database. The documents stored in the database can have varying sets of fields, with different types for each field. 
But the data structure of MongoDB just supports the nested document node in one child layer not multiple child layers. It’s not like the xDB NOSQL DB which could embed the nested element nodes in multiple child layers.

- Secondly, MongoDB could support Hash sharding feature besides range sharding since version 2.4. It could help the developer create the shard key more easily.
MongoDB provides autosharding, which means that, once you've configured sharding, MongoDB will automatically manage the storage of documents in the appropriate physical location. This includes rebalancing shards as the number of documents grows or the number of mongod instances changes.

- Thirdly, MongoDB added the embedded full text search engine to support full text query on MongoDB.
The new text search feature is not meant to match Lucene, but to provide basic capabilities such as more efficient Boolean queries ("dog and cat but not bird"), stemming (search for "reading" and you'll also get "read"), and the automatic culling of stop words (for example, "and", "the", "of") from the index.You have to adopt other powerful open source search solution such as ElasticSearch if you want to search more complex and flexible information.

- Fourthly, MongoDB, mapreduce serves as the means of general data processing, information aggregating, and analytics. It could execute more complex aggregate query like SQL group by semantics.You have to be careful with long-running mapreduce operations, because their execution involves lengthy locks.

- Fifthly, mongostat/mongotop is very useful command-line utilities.In addition, 10gen provides the free cloud-basedMongoDB Monitoring Service (MMS)which provides a monitoring dashboard for MongoDB installations

- Sixthly,the JavaScript engine has been replaced by Google's open source V8 engine. In the past, the JavaScript engine was single-threaded. V8 permits concurrent mapreduce jobs, as well as general speed improvements.


### MongoDB limitation
MongoDB limitation must be concerned due to different NoSQL design structure.

- Firstly, there exists the global write lock on MongoDB until 2.6. It impacts the concurrent write performance obviously because of thread block.Writes to MongoDB currently acquire a global write lock, although collection level locking is hopefully coming soon. By using more threads you're likely introducing more concurrency problems as the threads block each other while they wait for the lock to be released.The system implements shared-read, exclusive-write locking (many concurrent readers, but only one writer) with priority given to waiting writers over waiting readers.
This limitation also affects the data transfer operation. The insert operation must be executed one by one.

- Secondly, If you deploy MongoDB in the cluster environment such as replica set or master/slave. Secondaries node are updated asynchronously from the primary node so that they can take over in the event of a primary's crash. This, however, means that some read requests (sent to secondaries) may not be consistent with write requests (sent to primaries). This is an instance of MongoDB's "eventual consistency.” 

- Thirdly, MongoDB doesn't have an explicit memory caching layer. Instead, all MongoDB operations are performed through memory-mapped files. So it impacts the interactive performance. Oppositely, Couchbase has an explicit memory caching layer.

- Fourthly, you cannot perform pure ACID transactions on a MongoDB. Some workaround could help resolve this issue in some situation.MongoDB defines the $atomic isolation operator, which imposes what amounts to an exclusive-write lock on the document involved. However, $atomic is applied at the document level only. You cannot guard multiple updates across documents or collections.Two phase commit is one workaround and it supports the correct data commit properly even if it encountered the rollback exception.But this solution also couldn’t resolve $atomic isolation operator base on the business layer.

### Conclusion
MongoDB is very easy to use for developer. The grammar refer to mysql grammar in some aspect. It also supports distributed deployment, auto-failover and scale out. Due to the above advantage, MongoDB become the most popular NoSQL DB in the world. But it's not perfect. For example, MongoDB couldn't support complex data structure like XML structure (EMC xDB could do it.). MongoDB, Couchbase and EMC xDB are three different NoSQL database I study in the past few years. I will try to compare them in the next post.