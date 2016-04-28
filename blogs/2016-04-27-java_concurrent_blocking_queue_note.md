---
layout: post
category : programming
tags : [develop,java]
title: Java BlockingQueue API
---

Java BlockingQueue 数据结构API
------------------------------------

_Queue_ 
----------------- 
- 1.ArrayDeque（数组双端队列） 
- 2.PriorityQueue(优先级队列） 
- 3.ConcurrentLinkedQueue(基于链表的并发队列) 
- 4.DelayQueue(延期阻塞队列)
- 5.BlockingQueue接口(阻塞队列)
- 5.1.ArrayBlockingQueue(基于数组的并发阻塞队列） 
- 5.2.LinkedBlockingQueue(基于链表的FIFO阻塞队列)
- 5.3.LinkedBlockingDeque(基于链表的FIFO双端阻塞队列)
- 5.4.PriorityBlockingQueue(带优先级的无界阻塞队列) 
- 5.5.SynchronousQueue(并发同步阻塞队列)
------------------

#### 1.BlockingQueue定义

BlockingQueue作为线程容器，可以为线程同步提供有力的保障。

#### 2.BlockingQueue定义的常用方法:

|操作类型| 抛出异常  | 特殊值    | 阻塞    | 超时                  |
|:-----:|:--------:|:--------:|:------:|:--------------------:|
| 插入  | add(e)   | offer(e) | put(e) | offer(e, time, unit) |
| 移除  | remove() | poll()   | take() | poll(time, unit)     |
| 检查  | element()| peek()   | 不可用  | 不可用                |

- add(anObject:把anObject加到BlockingQueue里,即如果BlockingQueue可以容纳,则返回true,否则招聘异常
- offer(anObject):表示如果可能的话,将anObject加到BlockingQueue里,即如果BlockingQueue可以容纳,则返回true,否则返回false.
- put(anObject):把anObject加到BlockingQueue里,如果BlockQueue没有空间,则调用此方法的线程被阻断直到BlockingQueue里面有空间再继续.
- poll(time):取走BlockingQueue里排在首位的对象,若不能立即取出,则可以等time参数规定的时间,取不到时返回null
- take():取走BlockingQueue里排在首位的对象,若BlockingQueue为空,阻断进入等待状态直到Blocking有新的对象被加入为止

其中：BlockingQueue 不接受null 元素。试图add、put 或offer 一个null 元素时，某些实现会抛出NullPointerException。null 被用作指示poll 操作失败的警戒值。 

#### 3.BlockingQueue的几个注意点

##### 3.1.BlockingQueue可以是限定容量的。

它在任意给定时间都可以有一个remainingCapacity，超出此容量，便无法无阻塞地put 附加元素。没有任何内部容量约束的BlockingQueue 总是报告Integer.MAX_VALUE 的剩余容量。

##### 3.2.BlockingQueue实现主要用于生产者-使用者队列

另外还支持Collection 接口。因此，举例来说，使用remove(x)从队列中移除任意一个元素是有可能的。然而，这种操作通常不会有效执行，只能有计划地偶尔使用，比如在取消排队信息时。

##### 3.3.BlockingQueue实现是线程安全的。

所有排队方法都可以使用内部锁或其他形式的并发控制来自动达到它们的目的。然而，大量的 Collection 操作（addAll、containsAll、retainAll 和removeAll）没有 必要自动执行，除非在实现中特别说明。因此，举例来说，在只添加了c 中的一些元素后，addAll(c) 有可能失败（抛出一个异常）。

##### 3.4.BlockingQueue实质上不支持使用任何一种“close”或“shutdown”操作来指示不再添加任何项。

这种功能的需求和使用有依赖于实现的倾向。例如，一种常用的策略是：对于生产者，插入特殊的end-of-stream 或poison对象，并根据使用者获取这些对象的时间来对它们进行解释。

#### 4.概述BlockingQueue常用四个实现类

- ArrayBlockingQueue:规定大小的BlockingQueue,其构造函数必须带一个int参数来指明其大小.其所含的对象是以FIFO(先入先出)顺序排序的.
- LinkedBlockingQueue:大小不定的BlockingQueue,若其构造函数带一个规定大小的参数,生成的BlockingQueue有大小限制,若不带大小参数,所生成的BlockingQueue的大小由Integer.MAX_VALUE来决定.其所含的对象是以FIFO(先入先出)顺序排序的
- PriorityBlockingQueue:类似于LinkedBlockQueue,但其所含对象的排序不是FIFO,而是依据对象的自然排序顺序或者是构造函数的Comparator决定的顺序.
- SynchronousQueue:特殊的BlockingQueue,对其的操作必须是放和取交替完成的.

其中LinkedBlockingQueue和ArrayBlockingQueue比较起来,它们背后所用的数据结构不一样,导致LinkedBlockingQueue的数据吞吐量要大于ArrayBlockingQueue,但在线程数量很大时其性能的可预见性低于ArrayBlockingQueue.  

#### 5.BlockingQueue的具体实现类

有耐心的同学请看具体实现类细节：

##### 5.1.ArrayBlockingQueue

ArrayBlockingQueue是一个由数组支持的有界阻塞队列。此队列按FIFO（先进先出）原则对元素进行排序。队列的头部 是在队列中存在时间最长的元素。队列的尾部是在队列中存在时间最短的元素。新元素插入到队列的尾部，队列检索操作则是从队列头部开始获得元素。

这是一个典型的“有界缓存区”，固定大小的数组在其中保持生产者插入的元素和使用者提取的元素。一旦创建了这样的缓存区，就不能再增加其容量。试图向已满队列中放入元素会导致放入操作受阻塞；试图从空队列中检索元素将导致类似阻塞。

ArrayBlockingQueue创建的时候需要指定容量capacity(可以存储的最大的元素个数，因为它不会自动扩容)以及是否为公平锁(fair参数)。

在创建ArrayBlockingQueue的时候默认创建的是非公平锁，不过我们可以在它的构造函数里指定。这里调用ReentrantLock的构造函数创建锁的时候，调用了：

```java
public ReentrantLock(boolean fair) {

sync = (fair)? new FairSync() : new NonfairSync();

}
```

FairSync/NonfairSync是ReentrantLock的内部类：

线程按顺序请求获得公平锁，而一个非公平锁可以闯入，且当它尚未进入等待队列，就会和等待队列head结点的线程发生竞争，如果锁的状态可用，请求非公平锁的线程可在等待队列中向前跳跃，获得该锁。内部锁synchronized没有提供确定的公平性保证。

_分三点来讲这个类:_

a. 添加新元素的方法：add/put/offer <br/>
b. 该类的几个实例变量：takeIndex/putIndex/count <br/>
c. Condition实现 <br/>

*a.添加新元素的方法：add/put/offer*

首先，谈到添加元素的方法，首先得分析以下该类同步机制中用到的锁：

```java
lock = new ReentrantLock(fair);       
notEmpty = lock.newCondition();//Condition Variable 1       
notFull =  lock.newCondition();//Condition Variable 2    
```

这三个都是该类的实例变量，只有一个锁lock，然后lock实例化出两个Condition，notEmpty/noFull分别用来协调多线程的读写操作。

```java
public boolean offer(E e) {       
        if (e == null) throw new NullPointerException();       
        final ReentrantLock lock = this.lock;//每个对象对应一个显示的锁       
        lock.lock();//请求锁直到获得锁（不可以被interrupte）       
        try {       
            if (count == items.length)//如果队列已经满了       
                return false;       
            else {       
                insert(e);       
                return true;       
            }       
        } finally {       
            lock.unlock();//       
        }       
}
```
//看insert方法：
```java       
private void insert(E x) {       
        items[putIndex] = x;       
        //增加全局index的值。       
        /*     
        Inc方法体内部：     
        final int inc(int i) {     
        return (++i == items.length)? 0 : i;     
            }     
        这里可以看出ArrayBlockingQueue采用从前到后向内部数组插入的方式插入新元素的。如果插完了，putIndex可能重新变为0（在已经执行了移除操作的前提下，否则在之前的判断中队列为满）     
        */      
        putIndex = inc(putIndex);        
        ++count;       
        notEmpty.signal();//wake up one waiting thread       
}      
```
```java    
public void put(E e) throws InterruptedException {       
        if (e == null) throw new NullPointerException();       
        final E[] items = this.items;       
        final ReentrantLock lock = this.lock;       
        lock.lockInterruptibly();//请求锁直到得到锁或者变为interrupted       
        try {       
            try {       
                while (count == items.length)//如果满了，当前线程进入noFull对应的等waiting状态       
                    notFull.await();       
            } catch (InterruptedException ie) {       
                notFull.signal(); // propagate to non-interrupted thread       
                throw ie;       
            }       
            insert(e);       
        } finally {       
            lock.unlock();       
        }       
}      
```
```java
public boolean offer(E e, long timeout, TimeUnit unit)       
        throws InterruptedException {       
      
    if (e == null) throw new NullPointerException();       
    long nanos = unit.toNanos(timeout);       
        final ReentrantLock lock = this.lock;       
        lock.lockInterruptibly();       
        try {       
            for (;;) {       
                if (count != items.length) {       
                    insert(e);       
                    return true;       
                }       
                if (nanos <= 0)       
                    return false;       
                try {       
                //如果没有被 signal/interruptes,需要等待nanos时间才返回       
                    nanos = notFull.awaitNanos(nanos);       
                } catch (InterruptedException ie) {       
                    notFull.signal(); // propagate to non-interrupted thread       
                    throw ie;       
                }       
            }       
        } finally {       
            lock.unlock();       
        }       
    }      
```
```java
public boolean add(E e) {       
    return super.add(e);       
    }       
父类：       
public boolean add(E e) {       
        if (offer(e))       
            return true;       
        else      
            throw new IllegalStateException("Queue full");       
    }    
```

*b.该类的几个实例变量：takeIndex/putIndex/count*

```java 
用三个数字来维护这个队列中的数据变更：       
/** items index for next take, poll or remove */      
    private int takeIndex;       
    /** items index for next put, offer, or add. */      
    private int putIndex;       
    /** Number of items in the queue */      
    private int count;      
```

提取元素的三个方法take/poll/remove内部都调用了这个方法：

```java
private E extract() {       
        final E[] items = this.items;       
        E x = items[takeIndex];       
        items[takeIndex] = null;//移除已经被提取出的元素       
        takeIndex = inc(takeIndex);//策略和添加元素时相同       
        --count;       
        notFull.signal();//提醒其他在notFull这个Condition上waiting的线程可以尝试工作了       
        return x;       
    }   
``` 
从这个方法里可见，tabkeIndex维护一个可以提取/移除元素的索引位置，因为takeIndex是从0递增的，所以这个类是FIFO队列。

putIndex维护一个可以插入的元素的位置索引。

count显然是维护队列中已经存在的元素总数。


*c.Condition实现*

Condition现在的实现只有java.util.concurrent.locks.AbstractQueueSynchoronizer内部的ConditionObject，并且通过ReentranLock的newCondition()方法暴露出来，这是因为Condition的await()/singal()一般在lock.lock()与lock.unlock()之间执行，当执行condition.await()方法时，它会首先释放掉本线程持有的锁，然后自己进入等待队列。直到sinal()，唤醒后又会重新试图去拿到锁，拿到后执行await()下的代码，其中释放当前锁和得到当前锁都需要ReentranLock的tryAcquire(int arg)方法来判定，并且享受ReentranLock的重进入特性。

```java
public final void await() throws InterruptedException {       
            if (Thread.interrupted())       
                throw new InterruptedException();       
           //加一个新的condition等待节点       
 Node node = addConditionWaiter();       
//释放自己的锁       
            int savedState = fullyRelease(node);        
            int interruptMode = 0;       
            while (!isOnSyncQueue(node)) {       
            //如果当前线程 等待状态时CONDITION，park住当前线程，等待condition的signal来解除       
                LockSupport.park(this);       
                if ((interruptMode = checkInterruptWhileWaiting(node)) != 0)       
                    break;       
            }       
            if (acquireQueued(node, savedState) && interruptMode != THROW_IE)       
                interruptMode = REINTERRUPT;       
            if (node.nextWaiter != null)       
                unlinkCancelledWaiters();       
            if (interruptMode != 0)       
                reportInterruptAfterWait(interruptMode);       
        }     
```

##### 5.2.SynchronousQueue

一种阻塞队列，其中每个 put 必须等待一个 take，反之亦然。<br/>
同步队列没有任何内部容量，甚至连一个队列的容量都没有。不能在同步队列上进行 peek，因为仅在试图要取得元素时，该元素才存在；除非另一个线程试图移除某个元素，否则也不能（使用任何方法）添加元素；也不能迭代队列，因为其中没有元素可用于迭代。<br/>

队列的头 是尝试添加到队列中的首个已排队线程元素；如果没有已排队线程，则不添加元素并且头为 null。对于其他Collection 方法（例如 contains），SynchronousQueue 作为一个空集合。此队列不允许 null 元素。
同步队列类似于 CSP 和 Ada 中使用的rendezvous信道。它非常适合于传递性设计，在这种设计中，在一个线程中运行的对象要将某些信息、事件或任务传递给在另一个线程中运行的对象，它就必须与该对象同步。
对于正在等待的生产者和使用者线程而言，此类支持可选的公平排序策略。默认情况下不保证这种排序。但是，使用公平设置为 true 所构造的队列可保证线程以 FIFO 的顺序进行访问。公平通常会降低吞吐量，但是可以减小可变性并避免得不到服务。

##### 5.3.LinkedBlockingQueue

一个基于已链接节点的、范围任意的 blocking queue。<br/>
此队列按 FIFO（先进先出）排序元素。队列的头部 是在队列中时间最长的元素。队列的尾部 是在队列中时间最短的元素。新元素插入到队列的尾部，并且队列检索操作会获得位于队列头部的元素。链接队列的吞吐量通常要高于基于数组的队列，但是在大多数并发应用程序中，其可预知的性能要低。<br/>
单向链表结构的队列,如果不指定容量默认为Integer.MAX_VALUE。<br/>
通过putLock和takeLock两个锁进行同步，两个锁分别实例化notFull和notEmpty两个Condtion，用来协调多线程的存取动作。其中某些方法(如remove,toArray,toString,clear等)的同步需要同时获得这两个锁，并且总是先putLock.lock紧接着takeLock.lock(在同一方法fullyLock中)，这样的顺序是为了避免可能出现的死锁情况(我也想不明白为什么会是这样?)

##### 5.4.PriorityBlockingQueue

一个无界的阻塞队列,它使用与类PriorityQueue相同的顺序规则,并且提供了阻塞检索的操作。<br/>
虽然此队列逻辑上是无界的，但是由于资源被耗尽，所以试图执行添加操作可能会失败（导致 OutOfMemoryError）。此类不允许使用 null 元素。依赖自然顺序的优先级队列也不允许插入不可比较的对象（因为这样做会抛出ClassCastException）。

看它的三个属性，就基本能看懂这个类了：
```java
    private final PriorityQueue q;       
    private final ReentrantLock lock = new ReentrantLock(true);       
    private final Condition notEmpty = lock.newCondition();   
```

本类内部数据结构是PriorityQueue，至于PriorityQueue怎么排序看之前一篇[文章](http://jiadongkai-sina-com.iteye.com/blog/825683) <br/>
lock说明本类使用一个lock来同步读写等操作。<br/>
notEmpty协调队列是否有新元素提供，而队列满了以后会调用PriorityQueue的grow方法来扩容。

##### 5.5.DelayQueue

Delayed元素的一个无界阻塞队列,只有在延迟期满时才能从中提取元素。<br/>
该队列的头部是延迟期满后保存时间最长的Delayed元素。如果延迟都还没有期满，则队列没有头部，并且 poll 将返回 null。当一个元素的getDelay(TimeUnit.NANOSECONDS)方法返回一个小于或等于零的值时，则出现期满。此队列不允许使用 null 元素。
Delayed接口继承自Comparable,我们插入的E元素都要实现这个接口。

DelayQueue的设计目的间API文档：

> An unbounded blocking queue of Delayed elements, in which an element can only be taken when its delay has expired. The head of the queue is that Delayed element whose delay expired furthest in the past. 
> If no delay has  expired there is no head and poll will returnnull. Expiration occurs when an element's getDelay(TimeUnit.NANOSECONDS) method returns a value less than or equal to zero. 
> Even though unexpired elements cannot be removed using take or poll, they are otherwise treated as normal elements. 
> For example, the size method returns the count of both expired and unexpired elements. This queue does not permit null elements.

因为DelayQueue构造函数了里限定死不允许传入comparator(之前的PriorityBlockingQueue中没有限定死),即只能在compare方法里定义优先级的比较规则。再看上面这段英文，“The head of the queue is that Delayed element whose delay expired furthest in the past.”说明compare方法实现的时候要保证最先加入的元素最早结束延时。而 “Expiration occurs when an element's getDelay(TimeUnit.NANOSECONDS) method returns a value less than or equal to zero.”说明getDelay方法的实现必须保证延时到了返回的值变为<=0的int。

上面这段英文中，还说明了：在poll/take的时候，队列中元素会判定这个elment有没有达到超时时间，如果没有达到，poll返回null，而take进入等待状态。但是，除了这两个方法，队列中的元素会被当做正常的元素来对待。例如，size方法返回所有元素的数量，而不管它们有没有达到超时时间。而协调的Condition available只对take和poll是有意义的。

另外需要补充的是，在ScheduledThreadPoolExecutor中工作队列类型是它的内部类DelayedWorkQueue，而DelayedWorkQueue的Task容器是DelayQueue类型，而ScheduledFutureTask作为Delay的实现类作为Runnable的封装后的Task类。也就是说ScheduledThreadPoolExecutor是通过DelayQueue优先级判定规则来执行任务的。

##### 5.6.BlockingDeque+LinkedBlockingQueue

BlockingDeque为阻塞双端队列接口,实现类有LinkedBlockingDeque。<br/>
双端队列特别之处是它首尾都可以操作。LinkedBlockingDque不同于LinkedBlockingQueue，它只用一个lock来维护读写操作，并由这个lock实例化出两个Condition(notEmpty及notFull)，而LinkedBlockingQueue读和写分别维护一个lock。

_参考：_

[Java线程(十三):BlockingQueue-线程的阻塞队列](http://blog.csdn.net/zzp_403184692/article/details/8021615)
[多线程与并发库之java5阻塞队列(BlockingQueue)的应用----子线程循环10次，接着主线程循环100次，接着又回到子线程循环10次，接着再回到主线程循环100次，如此循环50次](http://blog.csdn.net/itm_hadf/article/details/7538083) 
[线程----BlockingQueue(转)](http://www.cnblogs.com/likwo/archive/2010/07/01/1769199.html)
[并发容器——BlockingQueue相关类](http://developer.51cto.com/art/201104/256805.htm)
[Java Concurrent包学习之BlockingQueue](http://blog.csdn.net/derekjiang/article/details/5330019)

使用PriorityBlockingQueue进行任务按优先级同步执行,摘自Think in Java

```java
package concurrency;  
  
import java.util.ArrayList;  
import java.util.List;  
import java.util.Queue;  
import java.util.Random;  
import java.util.concurrent.ExecutorService;  
import java.util.concurrent.Executors;  
import java.util.concurrent.PriorityBlockingQueue;  
import java.util.concurrent.TimeUnit;  
  
  
class PrioritizedTask implements Runnable, Comparable<PrioritizedTask>  
{  
    private Random rand = new Random(47);  
    private static int counter = 0;  
    private final int id = counter++;  
    private final int priority;  
      
    protected static List<PrioritizedTask> sequence = new ArrayList<PrioritizedTask>();  
      
    public PrioritizedTask(int priority)   
    {  
        this.priority = priority;  
        sequence.add(this);  
    }  
      
    @Override  
    public int compareTo(PrioritizedTask o) {  
        //复写此方法进行任务执行优先级排序  
//      return priority < o.priority ? 1 :  
//          (priority > o.priority ? -1 : 0);  
        if(priority < o.priority)  
        {  
            return -1;  
        }else  
        {  
            if(priority > o.priority)  
            {  
                return 1;  
            }else  
            {  
                return 0;  
            }  
        }  
    }  
  
    @Override  
    public void run() {  
        //执行任务代码..  
        try {  
            TimeUnit.MILLISECONDS.sleep(rand.nextInt(250));  
        } catch (InterruptedException e) {  
              
        }  
        System.out.println(this);  
    }  
      
    @Override  
    public String toString() {  
        return String.format("[%1$-3d]", priority) + " Task id : " + id;  
    }  
      
    public String summary()  
    {  
        return "( Task id : " + id + " _priority : " + priority + ")";  
    }  
      
    /** 
     * 结束所有任务 
     */  
    public static class EndSentinel extends PrioritizedTask  
    {  
        private ExecutorService exec;  
        public EndSentinel(ExecutorService e) {  
            super(Integer.MAX_VALUE);  
            exec = e;  
        }  
          
        public void run()  
        {  
            int count = 0;  
            for(PrioritizedTask pt : sequence)  
            {  
                System.out.print(pt.summary());  
                if(++count % 5 == 0)  
                {  
                    System.out.println();  
                }  
            }  
            System.out.println();  
            System.out.println(this + "Calling shutdownNow()");  
            exec.shutdownNow();  
        }  
    }  
}  
  
/** 
 * 制造一系列任务,分配任务优先级 
 */  
class PrioritizedTaskProducer implements Runnable  
{  
    private Random rand = new Random(47);  
    private Queue<Runnable> queue;  
    private ExecutorService exec;  
      
    public PrioritizedTaskProducer(Queue<Runnable> q, ExecutorService e)   
    {  
        queue = q;  
        exec = e;  
    }  
      
    @Override  
    public void run() {  
          
        for(int i = 0; i < 20; i++)  
        {  
            queue.add(new PrioritizedTask(rand.nextInt(10)));  
            Thread.yield();  
        }  
          
        try {  
            for (int i = 0; i < 10; i++) {  
                TimeUnit.MILLISECONDS.sleep(250);  
                queue.add(new PrioritizedTask(10));  
            }  
              
            for(int i = 0; i < 10; i++)  
            {  
                queue.add(new PrioritizedTask(i));  
            }  
              
            queue.add(new PrioritizedTask.EndSentinel(exec));  
              
        } catch (InterruptedException e) {  
              
        }  
          
        System.out.println("Finished PrioritizedTaskProducer");  
    }  
}  
  
  
/** 
 * 使用PriorityBlockingQueue进行任务按优先级同步执行 
 */  
class PrioritizedTaskConsumer implements Runnable  
{  
    private PriorityBlockingQueue<Runnable> q;  
    public PrioritizedTaskConsumer(PriorityBlockingQueue<Runnable> q)  
    {  
        this.q = q;  
    }  
  
    @Override  
    public void run() {  
        try   
        {  
            while (!Thread.interrupted())   
            {  
                q.take().run();  
            }  
        } catch (InterruptedException e)   
        {  
        }  
        System.out.println("Finished PrioritizedTaskConsumer");  
    }  
      
}  
public class PriorityBlockingQueueDemo {  
      
    public static void main(String args[])  
    {  
        ExecutorService exec = Executors.newCachedThreadPool();  
        PriorityBlockingQueue<Runnable> queue = new PriorityBlockingQueue<Runnable>();  
          
        exec.execute(new PrioritizedTaskProducer(queue, exec));  
        try {  
            TimeUnit.MILLISECONDS.sleep(250);  
        } catch (InterruptedException e) {  
        }  
        exec.execute(new PrioritizedTaskConsumer(queue));  
    }  
}  
```
