---
layout: post
category : programming
tags : [develop,java]
title: Java Concurrency Tech Analysis Map
---

## Java多线程与并发 - 技术分析索引
----------------------------------------------------------

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
   - Optimistic Locking / Pessimistic Locking
   - 数据库ACID中的锁管理/死锁/乐观锁

![Java多线程](_includes/java_multithread.jpg)   

### 前言

线程安全问题，在做高并发的系统的时候，是程序员经常需要考虑的地方。怎么有效的防止线程安全问题，保证数据的准确性？怎么合理的最大化的利用系统资源等，这些问题都需要充分的理解并运行线程。当然关于多线程的问题在面试的时候也是出现频率比较高的。下面就来学习一下吧！

### 线程

先来看看什么是进程和线程？

进程是资源（CPU、内存等）分配的基本单位，它是程序执行时的一个实例。程序运行时系统就会创建一个进程，并为它分配资源，然后把该进程放入进程就绪队列，进程调度器选中它的时候就会为它分配CPU时间，程序开始真正运行。就比如说，我们开发的一个单体项目，运行它，就会产生一个进程。

线程是程序执行时的最小单位，它是进程的一个执行流，是CPU调度和分派的基本单位，一个进程可以由很多个线程组成，线程间共享进程的所有资源，每个线程有自己的堆栈和局部变量。线程由CPU独立调度执行，在多CPU环境下就允许多个线程同时运行。同样多线程也可以实现并发操作，每个请求分配一个线程来处理。在这里强调一点就是：计算机中的线程和应用程序中的线程不是同一个概念。

总之一句话描述就是：进程是资源分配的最小单位，线程是程序执行的最小单位。

### 什么是线程安全

什么是线程安全呢？什么样的情况会造成线程安全问题呢？怎么解决线程安全呢？这些问题都是在下文中所要讲述的。

**线程安全：**当多个线程访问一个对象时，如果不用考虑这些线程在运行时环境下的调度和交替执行，也不需要进行额外的同步，或者在调用方进行任何其他的协调操作，调用这个对象的行为都可以获得正确的结果，那这个对象就是线程安全的。

那什么时候会造成线程安全问题呢？当多个线程同时去访问一个对象时，就可能会出现线程安全问题。那么怎么解决呢？请往下看！

### 解决线程安全

在这里提供4种方法来解决线程安全问题，也是最常用的4种方法。前提是项目在一个服务器中，如果是分布式项目可能就会用到分布锁了，这个就放到后面文章来详谈了。

讲4种方法前，还是先来了解一下悲观锁和乐观锁吧！

悲观锁，顾名思义它是悲观的。讲得通俗点就是，认为自己在使用数据的时候，一定有别的线程来修改数据，因此在获取数据的时候先加锁，确保数据不会被线程修改。形象理解就是总觉得有刁民想害朕。

而乐观锁就比较乐观了，认为在使用数据时，不会有别的线程来修改数据，就不会加锁，只是在更新数据的时候去判断之前有没有别的线程来更新了数据。具体用法在下面讲解。

现在来看有那4种方法吧！

- 方法一：使用synchronized关键字，一个表现为原生语法层面的互斥锁，它是一种悲观锁，使用它的时候我们一般需要一个监听对象 并且监听对象必须是唯一的，通常就是当前类的字节码对象。它是JVM级别的，不会造成死锁的情况。使用synchronized可以拿来修饰类，静态方法，普通方法和代码块。比如：Hashtable类就是使用synchronized来修饰方法的。put方法部分源码：

  ```java
   public synchronized V put(K key, V value) {
          // Make sure the value is not null
          if (value == null) {
              throw new NullPointerException();
          } 
  
   
  ```

  而ConcurrentHashMap类中就是使用synchronized来锁代码块的。putVal方法部分源码：

  ```java
   else {
                  V oldVal = null;
                  synchronized (f) {
                      if (tabAt(tab, i) == f) {
                          if (fh >= 0) {
                              binCount = 1;
  ```

  synchronized关键字底层实现主要是通过monitorenter 与monitorexit计数 ，如果计数器不为0，说明资源被占用，其他线程就不能访问了，但是可重入的除外。说到这，就来讲讲什么是可重入的。这里其实就是指的可重入锁：指的是同一线程外层函数获得锁之后，内层递归函数仍然有获取该锁的代码，但不受影响，执行对象中所有同步方法不用再次获得锁。避免了频繁的持有释放操作，这样既提升了效率，又避免了死锁。

  其实在使用synchronized时，存在一个锁升级原理。它是指在锁对象的对象头里面有一个 threadid 字段，在第一次访问的时候 threadid 为空，jvm 让其持有偏向锁，并将 threadid 设置为其线程 id，再次进入的时候会先判断 threadid 是否与其线程 id 一致，如果一致则可以直接使用此对象，如果不一致，则升级偏向锁为轻量级锁，通过自旋循环一定次数来获取锁，执行一定次数之后，如果还没有正常获取到要使用的对象，此时就会把锁从轻量级升级为重量级锁，此过程就构成了 synchronized 锁的升级。锁升级的目的是为了减低了锁带来的性能消耗。在 Java 6 之后优化 synchronized 的实现方式，使用了偏向锁升级为轻量级锁再升级到重量级锁的方式，从而减低了锁带来的性能消耗。可能你又会问什么是偏向锁？什么是轻量级锁？什么是重量级锁？这里就简单描述一下吧，能够帮你更好的理解synchronized。

  偏向锁（无锁）：大多数情况下锁不仅不存在多线程竞争，而且总是由同一线程多次获得。偏向锁的目的是在某个线程获得锁之后（线程的id会记录在对象的Mark Word中），消除这个线程锁重入（CAS）的开销，看起来让这个线程得到了偏护。

  轻量级锁（CAS）：就是由偏向锁升级来的，偏向锁运行在一个线程进入同步块的情况下，当第二个线程加入锁争用的时候，偏向锁就会升级为轻量级锁；轻量级锁的意图是在没有多线程竞争的情况下，通过CAS操作尝试将MarkWord更新为指向LockRecord的指针，减少了使用重量级锁的系统互斥量产生的性能消耗。

  重量级锁：虚拟机使用CAS操作尝试将MarkWord更新为指向LockRecord的指针，如果更新成功表示线程就拥有该对象的锁；如果失败，会检查MarkWord是否指向当前线程的栈帧，如果是，表示当前线程已经拥有这个锁；如果不是，说明这个锁被其他线程抢占，此时膨胀为重量级锁。

- 方法二：使用Lock接口下的实现类。Lock是juc（java.util.concurrent）包下面的一个接口。常用的实现类就是ReentrantLock 类，它其实也是一种悲观锁。一种表现为 API 层面的互斥锁。通过lock() 和 unlock() 方法配合使用。因此也可以说是一种手动锁，使用比较灵活。但是使用这个锁时一定要注意要释放锁，不然就会造成死锁。一般配合try/finally 语句块来完成。比如：

  ```java
  public class TicketThreadSafe extends Thread{
        private static int num = 5000;
        ReentrantLock lock = new ReentrantLock();
        @Override
        public void run() {
          while(num>0){
               try {
                 lock.lock();
                 if(num>0){
                   System.out.println(Thread.currentThread().getName()+"你的票号是"+num--);
                 }
                } catch (Exception e) {
                   e.printStackTrace();
                }finally {
                   lock.unlock();
                }
              }
        }
  }
  
    
  ```

  相比 synchronized，ReentrantLock 增加了一些高级功能，主要有以下 3 项：等待可中断、可实现公平锁，以及锁可以绑定多个条件。

  等待可中断是指：当持有锁的线程长期不释放锁的时候，正在等待的线程可以选择放弃等待，改为处理其他事情，可中断特性对处理执行时间非常长的同步块很有帮助。

  公平锁是指：多个线程在等待同一个锁时，必须按照申请锁的时间顺序来依次获得锁；而非公平锁则不保证这一点，在锁被释放时，任何一个等待锁的线程都有机会获得锁。synchronized 中的锁是非公平的，ReentrantLock 默认情况下也是非公平的，但可以通过带布尔值的构造函数要求使用公平锁。

  ```java
  public ReentrantLock(boolean fair) {
          sync = fair ? new FairSync() : new NonfairSync();
      }
  ```

  锁绑定多个条件是指：一个 ReentrantLock 对象可以同时绑定多个 Condition 对象，而在 synchronized 中，锁对象的 wait() 和 notify() 或 notifyAll() 方法可以实现一个隐含的条件，如果要和多于一个的条件关联的时候，就不得不额外地添加一个锁，而 ReentrantLock 则无须这样做，只需要多次调用 newCondition() 方法即可。

  ```java
  final ConditionObject newCondition() { //ConditionObject是Condition的实现类
              return new ConditionObject();
      } 
  
    
  ```

- 方法三：使用线程本地存储ThreadLocal。当多个线程操作同一个变量且互不干扰的场景下，可以使用ThreadLocal来解决。它会在每个线程中对该变量创建一个副本，即每个线程内部都会有一个该变量，且在线程内部任何地方都可以使用，线程之间互不影响，这样一来就不存在线程安全问题，也不会严重影响程序执行性能。在很多情况下，ThreadLocal比直接使用synchronized同步机制解决线程安全问题更简单，更方便，且结果程序拥有更高的并发性。通过set(T value)方法给线程的局部变量设置值；get()获取线程局部变量中的值。当给线程绑定一个 Object 内容后，只要线程不变,就可以随时取出；改变线程,就无法取出内容.。这里提供一个用法示例：

  ```java
  public class ThreadLocalTest {
        private static int a = 500;
        public static void main(String[] args) {
              new Thread(()->{
                    ThreadLocal<Integer> local = new ThreadLocal<Integer>();
                    while(true){
                          local.set(++a);   //子线程对a的操作不会影响主线程中的a
                          try {
                                Thread.sleep(1000);
                          } catch (InterruptedException e) {
                                e.printStackTrace();
                          }
                          System.out.println("子线程："+local.get());
                    }
              }).start();
              a = 22;
              ThreadLocal<Integer> local = new ThreadLocal<Integer>();
              local.set(a);
              while(true){
                    try {
                          Thread.sleep(1000);
                    } catch (InterruptedException e) {
                          e.printStackTrace();
                    }
                    System.out.println("主线程："+local.get());
              }
        }
  } 
  
   
  ```

  ThreadLocal线程容器保存变量时，底层其实是通过ThreadLocalMap来实现的。它是以当前ThreadLocal变量为key ，要存的变量为value。获取的时候就是以当前ThreadLocal变量去找到对应的key，然后获取到对应的值。源码参考如下：

  ```java
   public void set(T value) {
          Thread t = Thread.currentThread();
          ThreadLocalMap map = getMap(t);
          if (map != null)
              map.set(this, value);
          else
              createMap(t, value);
      }
       ThreadLocalMap getMap(Thread t) {
          return t.threadLocals; //ThreadLocal.ThreadLocalMap threadLocals = null;Thread类中声明的
      }
      void createMap(Thread t, T firstValue) {
          t.threadLocals = new ThreadLocalMap(this, firstValue);
      }
  ```

  观察源码就会发现，其实每个线程Thread内部有一个ThreadLocal.ThreadLocalMap类型的成员变量threadLocals，这个threadLocals就是用来存储实际的变量副本的，键值为当前ThreadLocal变量，value为变量副本（即T类型的变量）。

  初始时，在Thread里面，threadLocals为空，当通过ThreadLocal变量调用get()方法或者set()方法，就会对Thread类中的threadLocals进行初始化，并且以当前ThreadLocal变量为键值，以ThreadLocal要保存的副本变量为value，存到threadLocals。

  然后在当前线程里面，如果要使用副本变量，就可以通过get方法在threadLocals里面查找即可。

- 方法四：使用乐观锁机制。前面已经讲述了什么是乐观锁。这里就来描述哈在java开发中怎么使用的。

  其实在表设计的时候，我们通常就需要往表里加一个version字段。每次查询时，查出带有version的数据记录，更新数据时，判断数据库里对应id的记录的version是否和查出的version相同。若相同，则更新数据并把版本号+1；若不同，则说明，该数据发生了并发，被别的线程使用了，进行递归操作，再次执行递归方法，直到成功更新数据为止。