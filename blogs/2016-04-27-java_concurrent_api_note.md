---
layout: post
category : programming
tags : [develop,java]
title: Java Concurrent Utility API
---

Java 并发Concurrent Utility API
------------------------------------
The following new API is in java.util.concurrent of JDK5

#### 1.TimeUnit

尽管本质上 不是 Collections 类，但 java.util.concurrent.TimeUnit 枚举让代码更易读懂。使用 TimeUnit 将使用您的方法或 API 的开发人员从毫秒的 “暴政” 中解放出来。
TimeUnit 包括所有时间单位，从 MILLISECONDS 和 MICROSECONDS 到 DAYS 和 HOURS，这就意味着它能够处理一个开发人员所需的几乎所有的时间范围类型。同时，因为在列举上声明了转换方法，在时间加快时，将 HOURS 转换回 MILLISECONDS 甚至变得更容易。

#### 2.CopyOnWriteArrayList (New thread-safe List)

创建数组的全新副本是过于昂贵的操作，无论是从时间上，还是从内存开销上，因此在通常使用中很少考虑；开发人员往往求助于使用同步的 ArrayList。然而，这也是一个成本较高的选择，因为每当您跨集合内容进行迭代时，您就不得不同步所有操作，包括读和写，以此保证一致性。
这又让成本结构回到这样一个场景：需多读者都在读取 ArrayList，但是几乎没人会去修改它。
CopyOnWriteArrayList 是个巧妙的小宝贝，能解决这一问题。它的 Javadoc 将 CopyOnWriteArrayList 定义为一个 “ArrayList 的线程安全变体，在这个变体中所有易变操作（添加，设置等）可以通过复制全新的数组来实现”。
集合从内部将它的内容复制到一个没有修改的新数组，这样读者访问数组内容时就不会产生同步成本（因为他们从来不是在易变数据上操作）。
本质上讲，CopyOnWriteArrayList 很适合处理 ArrayList 经常让我们失败的这种场景：读取频繁，但很少有写操作的集合，例如 JavaBean 事件的 Listeners。

#### 3.BlockingQueue (Simpler List API) 阻塞队列

BlockingQueue 接口表示它是一个 Queue，意思是它的项以先入先出（FIFO）顺序存储。在特定顺序插入的项以相同的顺序检索 — 但是需要附加保证，从空队列检索一个项的任何尝试都会阻塞调用线程，直到这个项准备好被检索。同理，想要将一个项插入到满队列的尝试也会导致阻塞调用线程，直到队列的存储空间可用。
BlockingQueue 干净利落地解决了如何将一个线程收集的项“传递”给另一线程用于处理的问题，无需考虑同步问题。Java Tutorial 的 Guarded Blocks 试用版就是一个很好的例子。它构建一个单插槽绑定的缓存，当新的项可用，而且插槽也准备好接受新的项时，使用手动同步和 wait()/notifyAll() 在线程之间发信。（详见 Guarded Blocks 实现。）
尽管 Guarded Blocks 教程中的代码有效，但是它耗时久，混乱，而且也并非完全直观。退回到 Java 平台较早的时候，没错，Java 开发人员不得不纠缠于这种代码；但现在是 2010 年 — 情况难道没有改善？
清单 1 显示了 Guarded Blocks 代码的重写版，其中我使用了一个 ArrayBlockingQueue，而不是手写的 Drop。

清单 1. BlockingQueue
```java                           
import java.util.*;
import java.util.concurrent.*;

class Producer
    implements Runnable
{
    private BlockingQueue<String> drop;
    List<String> messages = Arrays.asList(
        "Mares eat oats",
        "Does eat oats",
        "Little lambs eat ivy",
        "Wouldn't you eat ivy too?");
        
    public Producer(BlockingQueue<String> d) { this.drop = d; }
    
    public void run()
    {
        try
        {
            for (String s : messages)
                drop.put(s);
            drop.put("DONE");
        }
        catch (InterruptedException intEx)
        {
            System.out.println("Interrupted! " + 
                "Last one out, turn out the lights!");
        }
    }    
}

class Consumer
    implements Runnable
{
    private BlockingQueue<String> drop;
    public Consumer(BlockingQueue<String> d) { this.drop = d; }
    
    public void run()
    {
        try
        {
            String msg = null;
            while (!((msg = drop.take()).equals("DONE")))
                System.out.println(msg);
        }
        catch (InterruptedException intEx)
        {
            System.out.println("Interrupted! " + 
                "Last one out, turn out the lights!");
        }
    }
}

public class ABQApp
{
    public static void main(String[] args)
    {
        BlockingQueue<String> drop = new ArrayBlockingQueue(1, true);
        (new Thread(new Producer(drop))).start();
        (new Thread(new Consumer(drop))).start();
    }
}
```

ArrayBlockingQueue 还体现了“公平” — 意思是它为读取器和编写器提供线程先入先出访问。这种替代方法是一个更有效，但又冒穷尽部分线程风险的政策。（即，允许一些读取器在其他读取器锁定时运行效率更高，但是您可能会有读取器线程的流持续不断的风险，导致编写器无法进行工作。）<br/>
_注意 Bug！_
>顺便说一句，如果您注意到 Guarded Blocks 包含一个重大 bug，那么您是对的 — 如果开发人员在 main() 中的Drop 实例上同步，会出现什么情况呢？
>BlockingQueue 还支持接收时间参数的方法，时间参数表明线程在返回信号故障以插入或者检索有关项之前需要阻塞的时间。这么做会避免非绑定的等待，这对一个生产系统是致命的，因为一个非绑定的等待会很容易导致需要重启的系统挂起。

##### 3.1.ArrayBlockingQueue

ArrayBlockingQueue是一个由数组支持的有界阻塞队列。<br/>
此队列按FIFO（先进先出）原则对元素进行排序。队列的头部是在队列中存在时间最长的元素。队列的尾部 是在队列中存在时间最短的元素。新元素插入到队列的尾部，队列获取操作则是从队列头部开始获得元素。

这是一个典型的“有界缓存区”，固定大小的数组在其中保持生产者插入的元素和使用者提取的元素。一旦创建了这样的缓存区，就不能再增加其容量。试图向已满队列中放入元素会导致操作受阻塞；试图从空队列中提取元素将导致类似阻塞。<br/>
此类支持对等待的生产者线程和消费者线程进行排序的可选公平策略。默认情况下，不保证是这种排序。然而，通过将公平性 (fairness) 设置为 true 而构造的队列允许按照FIFO顺序访问线程。公平性通常会降低吞吐量，但也减少了可变性和避免了“不平衡性”。 

##### 3.2.SynchronousQueues

根据 Javadoc，SynchronousQueue 是个有趣的东西：
这是一个阻塞队列，其中，每个插入操作必须等待另一个线程的对应移除操作，反之亦然。

*一个同步队列不具有任何内部容量，甚至不具有 1 的容量* <br/>
本质上讲，SynchronousQueue 是之前提过的BlockingQueue的又一实现。它给我们提供了在线程之间交换单一元素的极轻量级方法，使用 ArrayBlockingQueue 使用的阻塞语义。在清单 2 中，我重写了 清单 1 的代码，使用 SynchronousQueue替代ArrayBlockingQueue：

清单 2. SynchronousQueue

```java                     
import java.util.*;
import java.util.concurrent.*;

class Producer
    implements Runnable
{
    private BlockingQueue<String> drop;
    List<String> messages = Arrays.asList(
        "Mares eat oats",
        "Does eat oats",
        "Little lambs eat ivy",
        "Wouldn't you eat ivy too?");
        
    public Producer(BlockingQueue<String> d) { this.drop = d; }
    
    public void run()
    {
        try
        {
            for (String s : messages)
                drop.put(s);
            drop.put("DONE");
        }
        catch (InterruptedException intEx)
        {
            System.out.println("Interrupted! " + 
                "Last one out, turn out the lights!");
        }
    }    
}

class Consumer
    implements Runnable
{
    private BlockingQueue<String> drop;
    public Consumer(BlockingQueue<String> d) { this.drop = d; }
    
    public void run()
    {
        try
        {
            String msg = null;
            while (!((msg = drop.take()).equals("DONE")))
                System.out.println(msg);
        }
        catch (InterruptedException intEx)
        {
            System.out.println("Interrupted! " + 
                "Last one out, turn out the lights!");
        }
    }
}

public class SynQApp
{
    public static void main(String[] args)
    {
        BlockingQueue<String> drop = new SynchronousQueue<String>();
        (new Thread(new Producer(drop))).start();
        (new Thread(new Consumer(drop))).start();
    }
}
```

实现代码看起来几乎相同,但是应用程序有额外获益:SynchronousQueue 允许在队列进行一个插入，只要有一个线程等着使用它。
在实践中，SynchronousQueue 类似于 Ada 和 CSP 等语言中可用的 “会合通道”。这些通道有时在其他环境中也称为 “连接”，这样的环境包括 .NET （见 参考资料）。

#### 4.ConcurrentMap(New thread-safe Map)

Map 有一个微妙的并发 bug，这个 bug 将许多不知情的 Java 开发人员引入歧途。ConcurrentMap 是最容易的解决方案。
当一个 Map 被从多个线程访问时，通常使用 containsKey() 或者 get() 来查看给定键是否在存储键/值对之前出现。但是即使有一个同步的 Map，线程还是可以在这个过程中潜入，然后夺取对 Map 的控制权。问题是，在对 put() 的调用中，锁在 get() 开始时获取，然后在可以再次获取锁之前释放。它的结果是个竞争条件：这是两个线程之间的竞争，结果也会因谁先运行而不同。
如果两个线程几乎同时调用一个方法，两者都会进行测试，调用put，在处理中丢失第一线程的值。幸运的是，ConcurrentMap 接口支持许多附加方法，它们设计用于在一个锁下进行两个任务：putIfAbsent()，例如，首先进行测试，然后仅当键没有存储在 Map 中时进行 put。
For example, ConcurrentHashMap

##### 4.1.ConcurrentHashMap

_针对吞吐量进行优化_

ConcurrentHashMap 使用了几个技巧来获得高程度的并发以及避免锁定，包括为不同的32 hash buckets（桶）使用多个写锁和使用 JMM 的不确定性来最小化锁被保持的时间――或者根本避免获取锁。对于大多数一般用法来说它是经过优化的，这些用法往往会检索一个很可能在 map 中已经存在的值。事实上，多数成功的get()操作根本不需要任何锁定就能运行。
(警告：不要自己试图这样做！想比 JMM 聪明不像看上去的那么容易。Java.util.concurrent 类是由并发专家编写的，并且在 JMM 安全性方面经过了严格的同行评审。）

_多个写锁_

我们可以回想一下,Hashtable(或者替代方案Collections.synchronizedMap)的可伸缩性的主要障碍是它使用了一个 map 范围（map-wide）的锁，为了保证插入、删除或者检索操作的完整性必须保持这样一个锁，而且有时候甚至还要为了保证迭代遍历操作的完整性保持这样一个锁。这样一来，只要锁被保持，就从根本上阻止了其他线程访问 Map，即使处理器有空闲也不能访问，这样大大地限制了并发性。
ConcurrentHashMap摒弃了单一的map范围的锁，取而代之的是由32个锁组成的集合，其中每个锁负责保护 hash bucket 的一个子集。锁主要由变化性操作（put() 和 remove()）使用。具有 32 个独立的锁意味着最多可以有 32 个线程可以同时修改 map。这并不一定是说在并发地对 map 进行写操作的线程数少于 32 时，另外的写操作不会被阻塞――32 对于写线程来说是理论上的并发限制数目，但是实际上可能达不到这个值。但是，32 依然比 1 要好得多，而且对于运行于目前这一代的计算机系统上的大多数应用程序来说已经足够了。&#160
map 范围的操作
有 32 个独立的锁，其中每个锁保护 hash bucket 的一个子集，这样需要独占访问 map 的操作就必须获得所有32个锁。一些 map 范围的操作，比如说size() 和 isEmpty()，也许能够不用一次锁整个 map（通过适当地限定这些操作的语义），但是有些操作，比如 map 重排（扩大 hash bucket 的数量，随着 map 的增长重新分布元素），则必须保证独占访问。Java 语言不提供用于获取可变大小的锁集合的简便方法。必须这么做的情况很少见，一旦碰到这种情况，可以用递归方法来实现。

_JMM概述_

在进入put()、get()和remove()的实现之前，让我们先简单地看一下 JMM。JMM 掌管着一个线程对内存的动作(读和写)影响其他线程对内存的动作的方式。由于使用处理器寄存器和预处理 cache 来提高内存访问速度带来的性能提升，Java语言规范（JLS）允许一些内存操作并不对于所有其他线程立即可见。

有两种语言机制可用于保证跨线程内存操作的一致性―*synchronized(同步块与同步方法)和volatile*。<br/>
按照 JLS 的说法，“在没有显式同步的情况下，一个实现可以自由地更新主存，更新时所采取的顺序可能是出人意料的。”其意思是说，如果没有同步的话，在一个给定线程中某种顺序的写操作对于另外一个不同的线程来说可能呈现出不同的顺序,并且对内存变量的更新从一个线程传播到另外一个线程的时间是不可预测的。

虽然使用同步最常见的原因是保证对代码关键部分的原子访问，但实际上同步提供三个独立的功能――原子性、可见性和顺序性。原子性非常简单――同步实施一个可重入的（reentrant）互斥，防止多于一个的线程同时执行由一个给定的监视器保护的代码块。不幸的是，多数文章都只关注原子性方面，而忽略了其他方面。但是同步在 JMM 中也扮演着很重要的角色，会引起JVM在获得和释放监视器的时候执行内存壁垒（memory barrier).<br/>
一个线程在获得一个监视器之后，它执行一个读屏障（read barrier）――使得缓存在线程局部内存（比如说处理器缓存或者处理器寄存器）中的所有变量都失效，这样就会导致处理器重新从主存中读取同步代码块使用的变量。与此类似，在释放监视器时，线程会执行一个写屏障（write barrier）――将所有修改过的变量写回主存。互斥独占和内存壁垒结合使用意味着只要您在程序设计的时候遵循正确的同步法则（也就是说，每当写一个后面可能被其他线程访问的变量，或者读取一个可能最后被另一个线程修改的变量时，都要使用同步），每个线程都会得到它所使用的共享变量的正确的值。<br/>
如果在访问共享变量的时候没有同步的话，就会发生一些奇怪的事情。一些变化可能会通过线程立即反映出来，而其他的则需要一些时间（这由关联缓存的本质所致）。结果，如果没有同步您就不能保证内存内容必定一致（相关的变量相互间可能会不一致），或者不能得到当前的内存内容（一些值可能是过时的）。避免这种危险情况的常用方法（也是推荐使用的方法）当然是正确地使用同步。然而在有些情况下，比如说在像ConcurrentHashMap 之类的一些使用非常广泛的库类中，在开发过程当中还需要一些额外的专业技能和努力（可能比一般的开发要多出很多倍）来获得较高的性能。

_ConcurrentHashMap实现_

如前所述，ConcurrentHashMap使用的数据结构与Hashtable或HashMap的实现类似，是hash bucket 的一个可变数组，每个ConcurrentHashMap都由一个Map.Entry元素链构成，如清单1所示。与 Hashtable 和 HashMap 不同的是，ConcurrentHashMap 没有使用单一的集合锁（collection lock），而是使用了一个固定的锁池，这个锁池形成了bucket 集合的一个分区。

清单1. ConcurrentHashMap 使用的 Map.Entry 元素
```java
protected static class Entry implements Map.Entry {
    protected final Object key;
    protected volatile Object value;
    protected final int hash;
    protected final Entry next;
...}
```

不用锁定遍历数据结构与Hashtable或者典型的锁池Map实现不同，ConcurrentHashMap.get() 操作不一定需要获取与相关bucket 相关联的锁。如果不使用锁定，那么实现必须有能力处理它用到的所有变量的过时的或者不一致的值，比如说列表头指针和 Map.Entry元素的域(包括组成每个hash bucket条目的链表的链接指针)。<br/>
大多并发类使用同步来保证独占式访问一个数据结构(以及保持数据结构的一致性).ConcurrentHashMap没有采用独占性和一致性，它使用的链表是经过精心设计的，所以其实现可以检测到它的列表是否一致或者已经过时。如果它检测到它的列表出现不一致或者过时，或者干脆就找不到它要找的条目，它就会对适当的bucket锁进行同步并再次搜索整个链。这样做在一般的情况下可以优化查找，所谓的一般情况是指大多数检索操作是成功的并且检索的次数多于插入和删除的次数。<br/>

_使用不变性_

不一致性的一个重要来源是可以避免得，其方法是使 Entry 元素接近不变性――除了值字段（它们是易变的）之外，所有字段都是final的。这就意味着不能将元素添加到 hash 链的中间或末尾，或者从 hash 链的中间或末尾删除元素――而只能从hash链的开头添加元素，并且删除操作包括克隆整个链或链的一部分并更新列表的头指针。所以说只要有对某个 hash 链的一个引用，即使可能不知道有没有对列表头节点的引用，您也可以知道列表的其余部分的结构不会改变。而且，因为值字段是易变的，所以能够立即看到对值字段的更新，从而大大简化了编写能够处理内存潜在过时的 Map 的实现。<br/>
新的 JMM 为 final 型变量提供初始化安全，而老的 JMM 不提供，这意味着另一个线程看到的可能是 final 字段的默认值，而不是对象的构造方法提供的值。实现必须能够同时检测到这一点，这是通过保证 Entry中每个字段的默认值不是有效值来实现的。这样构造好列表之后，如果任何一个 Entry 字段有其默认值（零或空），搜索就会失败，提示同步 get() 并再次遍历链。<br/>

_检索操作_

检索操作首先为目标bucket查找头指针（是在不锁定的情况下完成的，所以说可能是过时的），然后在不获取bucket锁的情况下遍历bucket链。如果它不能发现要查找的值，就会同步并试图再次查找条目，如清单2所示：

清单2. ConcurrentHashMap.get() 实现
```java
public Object get(Object key) {
    int hash = hash(key); 
    // throws null pointer exception if key is null
    // Try first without locking...
    Entry[] tab = table;
    int index = hash & (tab.length - 1);
    Entry first = tab[index];
    Entry e;
    for (e = first; e != null; e = e.next) {  
        if (e.hash == hash && eq(key, e.key)) {
            Object value = e.value;
            // null values means that the element has been removed
            if (value != null)   
                return value;
                else  break;  
            }
        }// Recheck under synch if key apparently not there or interference
        Segment seg = segments[hash & SEGMENT_MASK];
        synchronized(seg) {   
            tab = table;  
            index = hash & (tab.length - 1);  
            Entry newFirst = tab[index];  
            if (e != null || first != newFirst) {
                for (e = newFirst; e != null; e = e.next) {  
                    if (e.hash == hash && eq(key, e.key)) 
                        return e.value;
                }  
            }  
            return null;
        }  
    }
```

_删除操作_

因为一个线程可能看到 hash 链中链接指针的过时的值，简单地从链中删除一个元素不足以保证其他线程在进行查找的时候不继续看到被删除的值。相反，从清单3我们可以看到，删除操作分两个过程――首先找到适当的 Entry 对象并把其值字段设为 null，然后对链中从头元素到要删除的元素的部分进行克隆，再连接到要删除的元素之后的部分。因为值字段是易变的，如果另外一个线程正在过时的链中查找那个被删除的元素，它会立即看到一个空值，并知道使用同步重新进行检索。最终，原始 hash 链中被删除的元素将会被垃圾收集。

清单3. ConcurrentHashMap.remove() 实现

```java
protected Object remove(Object key, Object value) {
    /*  Find the entry, then 
    1. Set value field to null, to force get() to retry
    2. Rebuild the list without this entry.   
    All entries following removed node can stay in list, but   all preceding ones need to be cloned.  Traversals rely   on this strategy to ensure that elements will not be  repeated during iteration.*/
    int hash = hash(key);
    Segment seg = segments[hash & SEGMENT_MASK];
    synchronized(seg) {  
        Entry[] tab = table;  
        int index = hash & (tab.length-1);  
        Entry first = tab[index];  
        Entry e = first;  
        for (;;) {
            if (e == null)  return null;
            if (e.hash == hash && eq(key, e.key))  
                 break;e = e.next;  
        }  
        Object oldValue = e.value;  
        if (value != null && !value.equals(oldValue)) return null;   
        e.value = null;  
        Entry head = e.next;  
        for (Entry p = first; p != e; p = p.next) 
            head = new Entry(p.hash, p.key, p.value, head);  
            tab[index] = head;  
            seg.count--;  
            return oldValue;
        }  
    }
```

图1为删除一个元素之前的 hash 链：

图1. Hash链
  
图2为删除元素3之后的链：

图2. 一个元素的删除过程
  
_插入和更新操作_

put() 的实现很简单。像 remove() 一样，put() 会在执行期间保持 bucket 锁，但是由于 put() 并不是都需要获取锁，所以这并不一定会阻塞其他读线程的执行（也不会阻塞其他写线程访问别的 bucket）。它首先会在适当的 hash 链中搜索需要的键值。如果能够找到，value字段（易变的）就直接被更新。如果没有找到，新会创建一个用于描述新 map 的新 Entry 对象，然后插入到 bucket 列表的头部。

_弱一致的迭代器_

由 ConcurrentHashMap 返回的迭代器的语义又不同于java.util 集合中的迭代器；而且它又是 弱一致的（weakly consistent） 而非 fail-fast 的（所谓 fail-fast 是指，当正在使用一个迭代器的时候，如何底层的集合被修改，就会抛出一个异常）。当一个用户调用keySet().iterator() 去迭代器中检索一组 hash 键的时候，实现就简单地使用同步来保证每个链的头指针是当前值。next()和hasNext() 操作以一种明显的方式定义，即遍历每个链然后转到下一个链直到所有的链都被遍历。弱一致迭代器可能会也可能不会反映迭代器迭代过程中的插入操作，但是一定会反映迭代器还没有到达的键的更新或删除操作，并且对任何值最多返回一次。ConcurrentHashMap 返回的迭代器不会抛出 ConcurrentModificationException 异常。

_动态调整大小_

随着 map 中元素数目的增长，hash 链将会变长，因此检索时间也会增加。从某种意义上说，增加 bucket 的数目和重排其中的值是非常重要的。在有些像 Hashtable 之类的类中，这很简单，因为保持一个应用到整个 map 的独占锁是可能的。在ConcurrentHashMap 中，每次一个条目插入的时候，如果链的长度超过了某个阈值，链就被标记为需要调整大小。当有足够多的链被标记为需要调整大小以后，ConcurrentHashMap 就使用递归获取每个 bucket 上的锁并重排每个 bucket 中的元素到一个新的、更大的 hash 表中。多数情况下，这是自动发生的，并且对调用者透明。

_不锁定？_

要说不用锁定就可以成功地完成 get() 操作似乎有点言过其实，因为 Entry 的 value 字段是易变的，这是用来检测更新和删除的。在机器级，易变的和同步的内容通常在最后会被翻译成相同的缓存一致原语，所以这里会有 一些 锁定，虽然只是细粒度的并且没有调度，或者没有获取和释放监视器的 JVM 开销。但是，除语义之外，在很多通用的情况下，检索的次数大于插入和删除的次数，所以说由 ConcurrentHashMap 取得的并发性是相当高的。

#### 5. CompletionService

Synchronizer classes

#### 6. Semaphore (信号量) (a classic Dijkstra counting semaphore)

在一些企业系统中，开发人员经常需要限制未处理的特定资源请求（线程/操作）数量，事实上，限制有时候能够提高系统的吞吐量，因为它们减少了对特定资源的争用。尽管完全可以手动编写限制代码，但使用 Semaphore类可以更轻松地完成此任务，它将帮您执行限制，如清单 1 所示：

清单 1. 使用 Semaphore 执行限制

```java                         
import java.util.*;import java.util.concurrent.*;

public class SemApp
{
    public static void main(String[] args)
    {
        Runnable limitedCall = new Runnable() {
            final Random rand = new Random();
            final Semaphore available = new Semaphore(3);
            int count = 0;
            public void run()
            {
                int time = rand.nextInt(15);
                int num = count++;
                
                try
                {
                    available.acquire();
                    
                    System.out.println("Executing " + 
                        "long-running action for " + 
                        time + " seconds... #" + num);
                
                    Thread.sleep(time * 1000);

                    System.out.println("Done with #" + 
                        num + "!");

                    available.release();
                }
                catch (InterruptedException intEx)
                {
                    intEx.printStackTrace();
                }
            }
        };
        
        for (int i=0; i<10; i++)
            new Thread(limitedCall).start();
    }
}
```

即使本例中的 10 个线程都在运行(您可以对运行 SemApp 的 Java 进程执行 jstack 来验证),但只有 3 个线程是活跃的。在一个信号计数器释放之前，其他 7 个线程都处于空闲状态。(实际上，Semaphore 类支持一次获取和释放多个 permit，但这不适用于本场景。)

#### 7.CyclicBarrier

The CyclicBarrier class is a synchronization aid that allows a set of threads to wait for the entire set of threads to reach a common barrier point.

#### 8.CountDownLatch

如果Semaphore是允许一次进入一个（这可能会勾起一些流行夜总会的保安的记忆）线程的并发性类，那么 CountDownLatch就像是赛马场的起跑门栅。此类持有所有空闲线程，直到满足特定条件，这时它将会一次释放所有这些线程。

清单 2. CountDownLatch：让我们去赛马吧！

```java                            
import java.util.*;
import java.util.concurrent.*;

class Race
{
    private Random rand = new Random();
    
    private int distance = rand.nextInt(250);
    private CountDownLatch start;
    private CountDownLatch finish;
    
    private List<String> horses = new ArrayList<String>();
    
    public Race(String... names)
    {
        this.horses.addAll(Arrays.asList(names));
    }
    
    public void run()
        throws InterruptedException
    {
        System.out.println("And the horses are stepping up to the gate...");
        final CountDownLatch start = new CountDownLatch(1);
        final CountDownLatch finish = new CountDownLatch(horses.size());
        final List<String> places = 
            Collections.synchronizedList(new ArrayList<String>());
        
        for (final String h : horses)
        {
            new Thread(new Runnable() {
                public void run() {
                    try
                    {
                        System.out.println(h + 
                            " stepping up to the gate...");
                        start.await();
                        
                        int traveled = 0;
                        while (traveled < distance)
                        {
                            // In a 0-2 second period of time....
                            Thread.sleep(rand.nextInt(3) * 1000);
                            
                            // ... a horse travels 0-14 lengths
                            traveled += rand.nextInt(15);
                            System.out.println(h + 
                                " advanced to " + traveled + "!");
                        }
                        finish.countDown();
                        System.out.println(h + 
                            " crossed the finish!");
                        places.add(h);
                    }
                    catch (InterruptedException intEx)
                    {
                        System.out.println("ABORTING RACE!!!");
                        intEx.printStackTrace();
                    }
                }
            }).start();
        }

        System.out.println("And... they're off!");
        start.countDown();        

        finish.await();
        System.out.println("And we have our winners!");
        System.out.println(places.get(0) + " took the gold...");
        System.out.println(places.get(1) + " got the silver...");
        System.out.println("and " + places.get(2) + " took home the bronze.");
    }
}

public class CDLApp
{
    public static void main(String[] args)
        throws InterruptedException, java.io.IOException
    {
        System.out.println("Prepping...");
        
        Race r = new Race(
            "Beverly Takes a Bath",
            "RockerHorse",
            "Phineas",
            "Ferb",
            "Tin Cup",
            "I'm Faster Than a Monkey",
            "Glue Factory Reject"
            );
        
        System.out.println("It's a race of " + r.getDistance() + " lengths");
        
        System.out.println("Press Enter to run the race....");
        System.in.read();
        
        r.run();
    }
}
```

注意，在 清单2 中，CountDownLatch有两个用途:首先，它同时释放所有线程，模拟马赛的起点，但随后会设置一个门闩模拟马赛的终点。这样，“主” 线程就可以输出结果。 为了让马赛有更多的输出注释，可以在赛场的 “转弯处” 和 “半程” 点，比如赛马跨过跑道的四分之一、二分之一和四分之三线时，添加 CountDownLatch。

#### 9.Timeout 方法

为阻塞操作设置一个具体的超时值（以避免死锁）的能力是java.util.concurrent 库相比起早期并发特性的一大进步，比如监控锁定。

这些方法几乎总是包含一个 int/TimeUnit 对，指示这些方法应该等待多长时间才释放控制权并将其返回给程序。它需要开发人员执行更多工作 — 如果没有获取锁，您将如何重新获取？ — 但结果几乎总是正确的：更少的死锁和更加适合生产的代码。

（关于编写生产就绪代码的更多信息，请参见 参考资料 中 Michael Nygard 编写的 Release It!。）
