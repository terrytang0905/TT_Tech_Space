---
layout: post
category : programming
tags : [develop,java]
title: Java Concurrency Analysis Map
---

Java多线程与并发-分析索引
------------------------------------

1. Java中的并发
   
    - java.util.concurrent API
    - 阻塞队列/非阻塞队列/无锁队列/fork-join

2. 多线程开发API

   - Thread/Runnable/Callback/Executor/线程池ExecutorService
   - Double Check Locking问题

3. Lock-free无锁编程

   - CAS原理及数据结构
   
4. CAS非阻塞算法实现(unsafe) + 用例

5. Lock/ ReentrantLock / ReadWriteLock / FileLock API分析

6. Java Lock用例及LockSupport（park/unpark）

7. Lock-free 与 Lock 使用比较

   - Lock原理分析
   - 数据库ACID中的锁管理/死锁/乐观锁