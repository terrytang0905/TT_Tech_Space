---
layout: post
category : programming
tags : [develop,java]
title: Java Concurrency Analysis Notes
---

## Core Java Concurrency Analysis Notes
-----------------------------------------------------

*The Reason of Thread Goodness*

- More responsive user interfaces
- Exploiting multiple processors.
- Simplicity of modeling. 
- Asynchronous or background processing.

*Thread Safety*

Must-be Thread Safety Application <br />
- GUI toolkits and background thread
- TimerTask
- Serlvet and JSP
- RMI

*The improvements for concurrency in JDK 5*

#### I.JVM-level changes:

compare-and-swap (CAS) 
CAS is a low-level, fine-grained technique for allowing multiple threads to update a single memory location while being able to detect and recover from interference from other threads.


#### II.Low-level utility classes -- locking and atomic variables

Using CAS as a concurrency primitive, the ReentrantLock class provides identical locking and memory semantics as the synchronized primitive

_Lock and ReentrantLock_

The Lock interface is a generalization of the locking behavior of built-in monitor locks, which allow for multiple lock implementations, while providing some features that are missing from built-in locks, such as timed waits, interruptible waits, lock polling, multiple condition-wait sets per lock, and non-block-structured locking.

When many threads are all contending for the same lock, the total throughput is generally going to be better with ReentrantLock than with synchronized. In other words, when many threads are attempting to access a shared resource protected by a ReentrantLock, the JVM will spend less time scheduling threads and more time executing them.

```java
Lock lock = new ReentrantLock();
...
lock.lock();
try {
// perform operations protected by lock
}
catch(Exception ex) {
// restore invariants
}
finally {
lock.unlock();
}

class ReentrantLockExample {
int a = 0;
ReentrantLock lock = new ReentrantLock();

public void writer() {
lock.lock();         //获取锁
try {
a++;
} finally {
lock.unlock();  //释放锁
}
}

public void reader () {
lock.lock();        //获取锁
try {
int i = a;
……
} finally {
lock.unlock();  //释放锁
}
}
}
```

一个可重入的互斥锁定 Lock，它具有与使用 synchronized方法和语句所访问的隐式监视器锁定相同的一些基本行为和语义，但功能更强大。ReentrantLock 将由最近成功获得锁定(对特定Object内部的锁定)，并且还没有释放该锁定的线程所拥有。当锁定没有被另一个线程所拥有时，调用lock的线程将成功获取该锁定并返回。如果当前线程已经拥有该锁定，此方法将立即返回。可以使用 isHeldByCurrentThread() 和 getHoldCount() 方法来检查此情况是否发生。

它提供了lock()方法：

- 如果该锁定没有被另一个线程保持，则获取该锁定并立即返回，将锁定的保持计数设置为 1。
- 如果当前线程已经保持该锁定，则将保持计数加 1，并且该方法立即返回。
- 如果该锁定被另一个线程保持，则出于线程调度的目的，禁用当前线程，并且在获得锁定之前，该线程将一直处于休眠状态，此时锁定保持计数被设置为 1。

_Conditions_

Just as the Lock interface is a generalization of synchronization, the Condition interface is a generalization of the wait() and notify() methods in Object. One of the methods in Lock is newCondition() – this asks the lock to return a new Condition object bound to this lock. The await(), signal(), and signalAll() methods are analogous(类似于) to wait(),notify(), and notifyAll(), with the added flexibility that you can create more than one condition variable per Lock. This simplifies the implementation of some concurrent algorithms.

_ReadWriteLock_

The locking discipline implemented by ReentrantLock is quite simple – one thread at a time holds the lock, and other threads must wait for it to be available. Sometimes, when data structures are more commonly read than
modified, it may be desirable to use a more complicated lock structure, called a read-write lock, which allows multiple concurrent readers but also allows for exclusive locking by a writer (多次读一次写). This approach offers greater concurrency in the common case (read only) while still offering the safety of exclusive access when necessary. The ReadWriteLock interface and the ReentrantReadWriteLock class provide this capability -- a multiple-reader,single-writer locking discipline that can be used to protect shared mutable resources.

多线程读取并修改一个资源时，我们过去通常使用synchronized同步锁，这个是有性能损失的，很多情况下：资源对象总是被大量并发读取，偶尔有一个线程进行修改，也就是说：以读为主，修改不是很频繁，那么我们在JDK5.0中用ReentrantReadWriteLock就获得比synchronized更高并发性能，高并发性能是我使用JDK5.0主要目的，而不是annotation和泛型等设计优点。

_ReentrantReadWriteLock_

被大量使用在缓存中，因为缓存中的对象总是被共享大量读操作，偶尔修改这个对象中的子对象，比如状态，那么只要通过ReentrantReadWriteLock来更新子对象就可以了，这就实现了Evans DDD中对不变性的要求，我们可以使用ReentrantReadWriteLock对根对象中生命周期短的子对象在内存中直接更新，不必依赖数据库锁，这又是一个摆脱数据库锁的进步。


#### III.java.util.concurrent.atomic 的隐藏精华

Most modern CPUs have primitives for atomic read-modify-write, such as compare-and-swap (CAS) or load-linked/store-conditional (LL/SC).
十五年前，多处理器系统是高度专用系统，要花费数十万美元（大多数具有两个到四个处理器）。现在，多处理器系统很便宜，而且数量很多，几乎每个主要微处理器都内置了多处理支持，其中许多系统支持数十个或数百个处理器。
要使用多处理器系统的功能，通常需要使用多线程构造应用程序。但是正如任何编写并发应用程序的人可以告诉你的那样，要获得好的硬件利用率，只是简单地在多个线程中分割工作是不够的，还必须确保线程确实大部分时间都在工作，而不是在等待更多的工作，或等待锁定共享数据结构。

_问题：线程之间的协调_

如果线程之间 不需要协调，那么几乎没有任务可以真正地并行。以线程池为例，其中执行的任务通常相互独立。如果线程池利用公共工作队列，则从工作队列中删除元素或向工作队列添加元素的过程必须是线程安全的，并且这意味着要协调对头、尾或节点间链接指针所进行的访问。正是这种协调导致了所有问题。

标准方法：锁定

在 Java 语言中，协调对共享字段的访问的传统方法是使用同步，确保完成对共享字段的所有访问，同时具有适当的锁定。通过同步，可以确定（假设类编写正确）具有保护一组给定变量的锁定的所有线程都将拥有对这些变量的独占访问权，并且以后其他线程获得该锁定时，将可以看到对这些变量进行的更改。弊端是如果锁定竞争太厉害（线程常常在其他线程具有锁定时要求获得该锁定），会损害吞吐量，因为竞争的同步非常昂贵。（Public Service Announcement：对于现代 JVM 而言，无竞争的同步现在非常便宜。
基于锁定的算法的另一个问题是：如果延迟具有锁定的线程（因为页面错误、计划延迟或其他意料之外的延迟），则 没有要求获得该锁定的线程可以继续运行。
还可以使用可变变量来以比同步更低的成本存储共享变量，但它们有局限性。虽然可以保证其他变量可以立即看到对可变变量的写入，但无法呈现原子操作的读-修改-写顺序，这意味着（比如说）可变变量无法用来可靠地实现互斥（互斥锁定）或计数器。

使用锁定实现计数器和互斥

假如开发线程安全的计数器类，那么这将暴露 get()、 increment() 和 decrement() 操作。清单 1 显示了如何使用锁定（同步）实现该类的例子。注意所有方法，甚至需要同步 get()，使类成为线程安全的类，从而确保没有任何更新信息丢失，所有线程都看到计数器的最新值。

清单 1. 同步的计数器类
```java     
public class SynchronizedCounter {
    private int value;
    public synchronized int getValue() { return value; }
    public synchronized int increment() { return ++value; }
    public synchronized int decrement() { return --value; }
}
```

increment() 和 decrement() 操作是原子的读-修改-写操作，为了安全实现计数器，必须使用当前值，并为其添加一个值，或写出新值，所有这些均视为一项操作，其他线程不能打断它。否则，如果两个线程试图同时执行增加，操作的不幸交叉将导致计数器只被实现了一次，而不是被实现两次。（注意，通过使值实例变量成为可变变量并不能可靠地完成这项操作。）
许多并发算法中都显示了原子的读-修改-写组合。清单 2 中的代码实现了简单的互斥， acquire() 方法也是原子的读-修改-写操作。要获得互斥，必须确保没有其他人具有该互斥（ curOwner = Thread.currentThread()），然后记录您拥有该互斥的事实（ curOwner = Thread.currentThread()），所有这些使其他线程不可能在中间出现以及修改 curOwner field。

清单 2. 同步的互斥类
```java      
public class SynchronizedMutex {
    private Thread curOwner = null;
    public synchronized void acquire() throws InterruptedException {
        if (Thread.interrupted()) throw new InterruptedException();
        while (curOwner != null) 
            wait();
        curOwner = Thread.currentThread();
    }
    public synchronized void release() {
        if (curOwner == Thread.currentThread()) {
            curOwner = null;
            notify();
        } else
            throw new IllegalStateException("not owner of mutex");
    }
}
```    

清单 1 中的计数器类可以可靠地工作，在竞争很小或没有竞争时都可以很好地执行。然而，在竞争激烈时，这将大大损害性能，因为 JVM 用了更多的时间来调度线程，管理竞争和等待线程队列，而实际工作（如增加计数器）的时间却很少。您可以回想 上月专栏中的图，该图显示了一旦多个线程使用同步竞争一个内置监视器，吞吐量将如何大幅度下降。虽然该专栏说明了新的 ReentrantLock 类如何可以更可伸缩地替代同步，但是对于一些问题，还有更好的解决方法。
锁定问题
使用锁定，如果一个线程试图获取其他线程已经具有的锁定，那么该线程将被阻塞，直到该锁定可用。此方法具有一些明显的缺点，其中包括当线程被阻塞来等待锁定时，它无法进行其他任何操作。如果阻塞的线程是高优先级的任务，那么该方案可能造成非常不好的结果（称为 优先级倒置的危险）。
使用锁定还有一些其他危险，如死锁（当以不一致的顺序获得多个锁定时会发生死锁）。甚至没有这种危险，锁定也仅是相对的粗粒度协调机制，同样非常适合管理简单操作，如增加计数器或更新互斥拥有者。如果有更细粒度的机制来可靠管理对单独变量的并发更新，则会更好一些；在大多数现代处理器都有这种机制。

_硬件同步原语_

如前所述，大多数现代处理器都包含对多处理的支持。当然这种支持包括多处理器可以共享外部设备和主内存，同时它通常还包括对指令系统的增加来支持多处理的特殊要求。特别是，几乎每个现代处理器都有通过可以检测或阻止其他处理器的并发访问的方式来更新共享变量的指令。

_CAS(compare-and-swap)_ 

支持并发的第一个处理器提供原子的测试并设置操作，通常在单位上运行这项操作。现在的处理器（包括 Intel 和 Sparc 处理器）使用的最通用的方法是实现名为 比较并转换或 CAS 的原语。（在 Intel 处理器中，比较并交换通过指令的 cmpxchg 系列实现。PowerPC 处理器有一对名为“加载并保留”和“条件存储”的指令，它们实现相同的目地；MIPS 与 PowerPC 处理器相似，除了第一个指令称为“加载链接”。）

CAS 操作包含三个操作数 —— 内存位置（V）、预期原值（A）和 新值(B)。如果内存位置的值与预期原值相匹配，那么处理器会自动将该位置值更新为新值。否则，处理器不做任何操作。无论哪种情况，它都会在 CAS 指令之前返回该位置的值。（在 CAS 的一些特殊情况下将仅返回 CAS 是否成功，而不提取当前值。）CAS 有效地说明了“我认为位置 V 应该包含值 A；如果包含该值，则将 B 放到这个位置；否则，不要更改该位置，只告诉我这个位置现在的值即可。”
通常将 CAS 用于同步的方式是从地址 V 读取值 A，执行多步计算来获得新值 B，然后使用 CAS 将 V 的值从 A 改为 B (snaphshot – Copy on Writer)。如果 V 处的值尚未同时更改，则 CAS 操作成功。

类似于CAS的指令允许算法执行读-修改-写操作，而无需害怕其他线程同时修改变量，因为如果其他线程修改变量，那么 CAS 会检测它（并失败），算法可以对该操作重新计算。清单 3 说明了 CAS 操作的行为（而不是性能特征），但是 CAS 的价值是它可以在硬件中实现，并且是极轻量级的（在大多数处理器中）：

清单 3. 说明比较并交换的行为（而不是性能）的代码
        
```java       
public class SimulatedCAS {
     private int value;

     public synchronized int getValue() { return value; }

  public synchronized int compareAndSwap(int expectedValue, int newValue) {
         int oldValue = value;
         if (value == expectedValue)
             value = newValue;
         return oldValue;
     }
}
```   

_使用 CAS 实现计数器_
基于 CAS 的并发算法称为 无锁定 算法，因为线程不必再等待锁定（有时称为互斥或关键部分，这取决于线程平台的术语）。无论 CAS 操作成功还是失败，在任何一种情况中，它都在可预知的时间内完成。如果 CAS 失败，调用者可以重试 CAS 操作或采取其他适合的操作。清单 4 显示了重新编写的计数器类来使用 CAS 替代锁定：

清单 4. 使用比较并交换实现计数器
```java
public class CasCounter {
    private SimulatedCAS value;
    public int getValue() {
        return value.getValue();
    }
    public int increment() {
        int oldValue = value.getValue();
        while (value.compareAndSwap(oldValue, oldValue + 1) != oldValue)
            oldValue = value.getValue();
        return oldValue + 1;
    }
}
```   

_无锁定且无等待算法_

如果每个线程在其他线程任意延迟（或甚至失败）时都将持续进行操作，就可以说该算法是 无等待的。与此形成对比的是， 无锁定算法要求仅 某个线程总是执行操作。（无等待的另一种定义是保证每个线程在其有限的步骤中正确计算自己的操作，而不管其他线程的操作、计时、交叉或速度。这一限制可以是系统中线程数的函数；例如，如果有 10 个线程，每个线程都执行一次CasCounter.increment() 操作，最坏的情况下，每个线程将必须重试最多九次，才能完成增加。）
再过去的 15 年里，人们已经对无等待且无锁定算法（也称为 无阻塞算法）进行了大量研究，许多人通用数据结构已经发现了无阻塞算法。无阻塞算法被广泛用于操作系统和 JVM 级别，进行诸如线程和进程调度等任务。虽然它们的实现比较复杂，但相对于基于锁定的备选算法，它们有许多优点：可以避免优先级倒置和死锁等危险，竞争比较便宜，协调发生在更细的粒度级别，允许更高程度的并行机制等等。

_原子变量类_

在 JDK 5.0 之前，如果不使用本机代码，就不能用 Java 语言编写无等待、无锁定的算法。在 java.util.concurrent.atomic 包中添加原子变量类之后，这种情况才发生了改变。所有原子变量类都公开比较并设置原语（与比较并交换类似），这些原语都是使用平台上可用的最快本机结构（比较并交换、加载链接/条件存储，最坏的情况下是旋转锁）来实现的。 java.util.concurrent.atomic 包中提供了原子变量的 9 种风格（ AtomicInteger； AtomicLong； AtomicReference； AtomicBoolean；原子整型；长型；引用；及原子标记引用和戳记引用类的数组形式，其原子地更新一对值）。
原子变量类可以认为是 volatile 变量的泛化，它扩展了可变变量的概念，来支持原子条件的比较并设置更新。读取和写入原子变量与读取和写入对可变变量的访问具有相同的存取语义。
虽然原子变量类表面看起来与清单 1 中的 SynchronizedCounter 例子一样，但相似仅是表面的。在表面之下，原子变量的操作会变为平台提供的用于并发访问的硬件原语，比如比较并交换。
更细粒度意味着更轻量级
调整具有竞争的并发应用程序的可伸缩性的通用技术是降低使用的锁定对象的粒度，希望更多的锁定请求从竞争变为不竞争。从锁定转换为原子变量可以获得相同的结果，通过切换为更细粒度的协调机制，竞争的操作就更少，从而提高了吞吐量。

_ABA 问题_

因为在更改 V 之前，CAS 主要询问“V 的值是否仍为 A”，所以在第一次读取 V 以及对 V 执行 CAS 操作之前，如果将值从 A 改为 B，然后再改回 A，会使基于 CAS 的算法混乱。在这种情况下，CAS 操作会成功，但是在一些情况下，结果可能不是您所预期的。（注意， 清单 1 和 清单 2 中的计数器和互斥例子不存在这个问题，但不是所有算法都这样。）这类问题称为 ABA 问题，通常通过将标记或版本编号与要进行 CAS 操作的每个值相关联，并原子地更新值和标记，来处理这类问题。 AtomicStampedReference 类支持这种方法。

_java.util.concurrent 中的原子变量_

无论是直接的还是间接的，几乎 java.util.concurrent 包中的所有类都使用原子变量，而不使用同步。类似 ConcurrentLinkedQueue 的类也使用原子变量直接实现无等待算法，而类似 ConcurrentHashMap 的类使用 ReentrantLock 在需要时进行锁定。然后， ReentrantLock 使用原子变量来维护等待锁定的线程队列。
如果没有 JDK 5.0 中的 JVM 改进，将无法构造这些类，这些改进暴露了（向类库，而不是用户类）接口来访问硬件级的同步原语。然后，java.util.concurrent 中的原子变量类和其他类向用户类公开这些功能。

Performance is a measure of "how fast can you execute this task." Scalability describes how an application's throughput behaves as its workload and available computing resources increase.

使用原子变量获得更高的吞吐量
之前介绍了 ReentrantLock 如何相对于同步提供可伸缩性优势，以及构造通过伪随机数生成器模拟旋转骰子的简单、高竞争示例基准。我向您显示了通过同步、 ReentrantLock 和公平 ReentrantLock 来进行协调的实现，并显示了结果。本月，我将向该基准添加其他实现，使用 AtomicLong 更新 PRNG 状态的实现。
清单 5 显示了使用同步的 PRNG 实现和使用 CAS 备选实现。注意，要在循环中执行 CAS，因为它可能会失败一次或多次才能获得成功，使用 CAS 的代码总是这样。

清单 5. 使用同步和原子变量实现线程安全 PRNG
```java       
public class PseudoRandomUsingSynch implements PseudoRandom {
    private int seed;
    public PseudoRandomUsingSynch(int s) { seed = s; }
    public synchronized int nextInt(int n) {
        int s = seed;
        seed = Util.calculateNext(seed);
        return s % n;
    }
}
public class PseudoRandomUsingAtomic implements PseudoRandom {
    private final AtomicInteger seed;
    public PseudoRandomUsingAtomic(int s) {
        seed = new AtomicInteger(s);
    }
    public int nextInt(int n) {
        for (;;) {
            int s = seed.get();
            int nexts = Util.calculateNext(s);
            if (seed.compareAndSet(s, nexts))
                return s % n;
        }
    }
}
```   

下面图 1 和图 2 中的图与上月那些图相似，只是为基于原子的方法多添加了一行。这些图显示了在 8-way Ultrasparc3 和单处理器 Pentium 4 上使用不同数量线程的随机发生的吞吐量（以每秒转数为单位）。测试中的线程数不是真实的；这些线程所表现的竞争比通常多得多，所以它们以比实际程序中低得多的线程数显示了 ReentrantLock 与原子变量之间的平衡。您将看到，虽然ReentrantLock 拥有比同步更多的优点，但相对于 ReentrantLock，原子变量提供了其他改进。（因为在每个工作单元中完成的工作很少，所以下图可能无法完全地说明与 ReentrantLock 相比，原子变量具有哪些可伸缩性优点。）

图 1. 8-way Ultrasparc3 中Synchronization、ReentrantLock、fair Lock 和 AtomicLong 的基准吞吐量
  

图 2. 单处理器 Pentium 4 中的Synchronization、ReentrantLock、fair Lock 和 AtomicLong 的基准吞吐量
  
大多数用户都不太可能使用原子变量自己开发无阻塞算法 — 他们更可能使用 java.util.concurrent 中提供的版本，如ConcurrentLinkedQueue。但是万一您想知道对比以前 JDK 中的相类似的功能，这些类的性能是如何改进的，可以使用通过原子变量类公开的细粒度、硬件级别的并发原语。
开发人员可以直接将原子变量用作共享计数器、序号生成器和其他独立共享变量的高性能替代，否则必须通过同步保护这些变量。


#### IV.Java No-blocking Algorithm

在不只一个线程访问一个互斥的变量时，所有线程都必须使用同步，否则就可能会发生一些非常糟糕的事情。Java 语言中主要的同步手段就是 synchronized 关键字（也称为内在锁），它强制实行互斥，确保执行 synchronized 块的线程的动作，能够被后来执行受相同锁保护的 synchronized 块的其他线程看到。在使用得当的时候，内在锁可以让程序做到线程安全，但是在使用锁定保护短的代码路径，而且线程频繁地争用锁的时候，锁定可能成为相当繁重的操作。
在 “流行的原子” 一文中，我们研究了原子变量，原子变量提供了原子性的读-写-修改操作，可以在不使用锁的情况下安全地更新共享变量。原子变量的内存语义与 volatile 变量类似，但是因为它们也可以被原子性地修改，所以可以把它们用作不使用锁的并发算法的基础。
非阻塞的计数器
清单 1 中的 Counter 是线程安全的，但是使用锁的需求带来的性能成本困扰了一些开发人员。但是锁是必需的，因为虽然增加看起来是单一操作，但实际是三个独立操作的简化：检索值，给值加 1，再写回值。（在 getValue 方法上也需要同步，以保证调用getValue 的线程看到的是最新的值。虽然许多开发人员勉强地使自己相信忽略锁定需求是可以接受的，但忽略锁定需求并不是好策略。）
在多个线程同时请求同一个锁时，会有一个线程获胜并得到锁，而其他线程被阻塞。JVM 实现阻塞的方式通常是挂起阻塞的线程，过一会儿再重新调度它。由此造成的上下文切换相对于锁保护的少数几条指令来说，会造成相当大的延迟。

清单 1. 使用同步的线程安全的计数器
```java
public final class Counter {
    private long value = 0;
    public synchronized long getValue() {
        return value;
    }
    public synchronized long increment() {
        return ++value;
    }
}
```

清单 2 中的 NonblockingCounter 显示了一种最简单的非阻塞算法：使用 AtomicInteger 的 compareAndSet() （CAS）方法的计数器。compareAndSet() 方法规定 “将这个变量更新为新值，但是如果从我上次看到这个变量之后其他线程修改了它的值，那么更新就失败”（请参阅 “流行的原子” 获得关于原子变量以及 “比较和设置” 的更多解释。）

清单 2. 使用 CAS 的非阻塞算法
```java
public class NonblockingCounter {
    private AtomicInteger value;
    public int getValue() {
        return value.get();
    }
    public int increment() {
        int v;
        do {
            v = value.get();
        while (!value.compareAndSet(v, v + 1));
        return v + 1;
    }
}
```

原子变量类之所以被称为原子的，是因为它们提供了对数字和对象引用的细粒度的原子更新，但是在作为非阻塞算法的基本构造块的意义上，它们也是原子的。非阻塞算法作为科研的主题，已经有 20 多年了，但是直到 Java 5.0 出现，在 Java 语言中才成为可能。
现代的处理器提供了特殊的指令，可以自动更新共享数据，而且能够检测到其他线程的干扰，而 compareAndSet() 就用这些代替了锁定。（如果要做的只是递增计数器，那么 AtomicInteger 提供了进行递增的方法，但是这些方法基于 compareAndSet()，例如NonblockingCounter.increment()）。
非阻塞版本相对于基于锁的版本有几个性能优势。首先，它用硬件的原生形态代替 JVM 的锁定代码路径，从而在更细的粒度层次上（独立的内存位置）进行同步，失败的线程也可以立即重试，而不会被挂起后重新调度。更细的粒度降低了争用的机会，不用重新调度就能重试的能力也降低了争用的成本。即使有少量失败的 CAS 操作，这种方法仍然会比由于锁争用造成的重新调度快得多。
NonblockingCounter 这个示例可能简单了些，但是它演示了所有非阻塞算法的一个基本特征 —— 有些算法步骤的执行是要冒险的，因为知道如果 CAS 不成功可能不得不重做。非阻塞算法通常叫作乐观算法，因为它们继续操作的假设是不会有干扰。如果发现干扰，就会回退并重试。在计数器的示例中，冒险的步骤是递增 —— 它检索旧值并在旧值上加一，希望在计算更新期间值不会变化。如果它的希望落空，就会再次检索值，并重做递增计算。

非阻塞堆栈
非阻塞算法稍微复杂一些的示例是清单 3 中的 ConcurrentStack。ConcurrentStack 中的 push() 和 pop() 操作在结构上与NonblockingCounter 上相似，只是做的工作有些冒险，希望在 “提交” 工作的时候，底层假设没有失效。push() 方法观察当前最顶的节点，构建一个新节点放在堆栈上，然后，如果最顶端的节点在初始观察之后没有变化，那么就安装新节点。如果 CAS 失败，意味着另一个线程已经修改了堆栈，那么过程就会重新开始。

清单 3. 使用 Treiber 算法的非阻塞堆栈
```java
public class ConcurrentStack<E> {
    AtomicReference<Node<E>> head = new AtomicReference<Node<E>>();
    public void push(E item) {
        Node<E> newHead = new Node<E>(item);
        Node<E> oldHead;
        do {
            oldHead = head.get();
            newHead.next = oldHead;
        } while (!head.compareAndSet(oldHead, newHead));
    }
    public E pop() {
        Node<E> oldHead;
        Node<E> newHead;
        do {
            oldHead = head.get();
            if (oldHead == null) 
                return null;
            newHead = oldHead.next;
        } while (!head.compareAndSet(oldHead,newHead));
        return oldHead.item;
    }
    static class Node<E> {
        final E item;
        Node<E> next;
        public Node(E item) { this.item = item; }
    }
}
```

_性能考虑_

在轻度到中度的争用情况下，非阻塞算法的性能会超越阻塞算法，因为 CAS 的多数时间都在第一次尝试时就成功，而发生争用时的开销也不涉及线程挂起和上下文切换，只多了几个循环迭代。没有争用的 CAS 要比没有争用的锁便宜得多（这句话肯定是真的，因为没有争用的锁涉及 CAS 加上额外的处理），而争用的 CAS 比争用的锁获取涉及更短的延迟。
在高度争用的情况下（即有多个线程不断争用一个内存位置的时候），基于锁的算法开始提供比非阻塞算法更好的吞吐率，因为当线程阻塞时，它就会停止争用，耐心地等候轮到自己，从而避免了进一步争用。但是，这么高的争用程度并不常见，因为多数时候，线程会把线程本地的计算与争用共享数据的操作分开，从而给其他线程使用共享数据的机会。（这么高的争用程度也表明需要重新检查算法，朝着更少共享数据的方向努力。）“流行的原子” 中的图在这方面就有点儿让人困惑，因为被测量的程序中发生的争用极其密集，看起来即使对数量很少的线程，锁定也是更好的解决方案。

_非阻塞的链表_

目前为止的示例（计数器和堆栈）都是非常简单的非阻塞算法，一旦掌握了在循环中使用 CAS，就可以容易地模仿它们。对于更复杂的数据结构，非阻塞算法要比这些简单示例复杂得多，因为修改链表、树或哈希表可能涉及对多个指针的更新。CAS 支持对单一指针的原子性条件更新，但是不支持两个以上的指针。所以，要构建一个非阻塞的链表、树或哈希表，需要找到一种方式，可以用 CAS 更新多个指针，同时不会让数据结构处于不一致的状态。
在链表的尾部插入元素，通常涉及对两个指针的更新：“尾” 指针总是指向列表中的最后一个元素，“下一个” 指针从过去的最后一个元素指向新插入的元素。因为需要更新两个指针，所以需要两个 CAS。在独立的 CAS 中更新两个指针带来了两个需要考虑的潜在问题：如果第一个 CAS 成功，而第二个 CAS 失败，会发生什么？如果其他线程在第一个和第二个 CAS 之间企图访问链表，会发生什么？
对于非复杂数据结构，构建非阻塞算法的 “技巧” 是确保数据结构总处于一致的状态（甚至包括在线程开始修改数据结构和它完成修改之间），还要确保其他线程不仅能够判断出第一个线程已经完成了更新还是处在更新的中途，还能够判断出如果第一个线程走向 AWOL，完成更新还需要什么操作。如果线程发现了处在更新中途的数据结构，它就可以 “帮助” 正在执行更新的线程完成更新，然后再进行自己的操作。当第一个线程回来试图完成自己的更新时，会发现不再需要了，返回即可，因为 CAS 会检测到帮助线程的干预（在这种情况下，是建设性的干预）。
这种 “帮助邻居” 的要求，对于让数据结构免受单个线程失败的影响，是必需的。如果线程发现数据结构正处在被其他线程更新的中途，然后就等候其他线程完成更新，那么如果其他线程在操作中途失败，这个线程就可能永远等候下去。即使不出现故障，这种方式也会提供糟糕的性能，因为新到达的线程必须放弃处理器，导致上下文切换，或者等到自己的时间片过期（而这更糟）。

清单 4 的 LinkedQueue 显示了 Michael-Scott 非阻塞队列算法的插入操作，它是由 ConcurrentLinkedQueue 实现的：

清单 4. Michael-Scott 非阻塞队列算法中的插入
```java
public class LinkedQueue <E> {
    private static class Node <E> {
        final E item;
        final AtomicReference<Node<E>> next;
        Node(E item, Node<E> next) {
            this.item = item;
            this.next = new AtomicReference<Node<E>>(next);
        }
    }
    private AtomicReference<Node<E>> head
        = new AtomicReference<Node<E>>(new Node<E>(null, null));
    private AtomicReference<Node<E>> tail = head;
    public boolean put(E item) {
        Node<E> newNode = new Node<E>(item, null);
        while (true) {
            Node<E> curTail = tail.get();
            Node<E> residue = curTail.next.get();
            if (curTail == tail.get()) {
                if (residue == null) /* A */ {
                    if (curTail.next.compareAndSet(null, newNode)) /* C */ {
                        tail.compareAndSet(curTail, newNode) /* D */ ;
                        return true;
                    }
                } else {
                    tail.compareAndSet(curTail, residue) /* B */;
                }
            }
        }
    }
}
```

像许多队列算法一样，空队列只包含一个假节点。头指针总是指向假节点；尾指针总指向最后一个节点或倒数第二个节点。图 1 演示了正常情况下有两个元素的队列：

图 1. 有两个元素，处在静止状态的队列
  
如 清单 4 所示，插入一个元素涉及两个指针更新，这两个更新都是通过 CAS 进行的：从队列当前的最后节点（C）链接到新节点，并把尾指针移动到新的最后一个节点（D）。如果第一步失败，那么队列的状态不变，插入线程会继续重试，直到成功。一旦操作成功，插入被当成生效，其他线程就可以看到修改。还需要把尾指针移动到新节点的位置上，但是这项工作可以看成是 “清理工作”，因为任何处在这种情况下的线程都可以判断出是否需要这种清理，也知道如何进行清理。
队列总是处于两种状态之一：正常状态（或称静止状态，图 1 和 图 3）或中间状态（图 2）。在插入操作之前和第二个 CAS（D）成功之后，队列处在静止状态；在第一个 CAS（C）成功之后，队列处在中间状态。在静止状态时，尾指针指向的链接节点的 next 字段总为 null，而在中间状态时，这个字段为非 null。任何线程通过比较 tail.next 是否为 null，就可以判断出队列的状态，这是让线程可以帮助其他线程 “完成” 操作的关键。

图 2. 处在插入中间状态的队列，在新元素插入之后，尾指针更新之前
  
插入操作在插入新元素（A）之前，先检查队列是否处在中间状态，如 清单 4 所示。如果是在中间状态，那么肯定有其他线程已经处在元素插入的中途，在步骤（C）和（D）之间。不必等候其他线程完成，当前线程就可以 “帮助” 它完成操作，把尾指针向前移动（B）。如果有必要，它还会继续检查尾指针并向前移动指针，直到队列处于静止状态，这时它就可以开始自己的插入了。
第一个 CAS（C）可能因为两个线程竞争访问队列当前的最后一个元素而失败；在这种情况下，没有发生修改，失去 CAS 的线程会重新装入尾指针并再次尝试。如果第二个 CAS（D）失败，插入线程不需要重试 —— 因为其他线程已经在步骤（B）中替它完成了这个操作！

图 3. 在尾指针更新后，队列重新处在静止状态
  
幕后的非阻塞算法
如果深入 JVM 和操作系统，会发现非阻塞算法无处不在。垃圾收集器使用非阻塞算法加快并发和平行的垃圾搜集；调度器使用非阻塞算法有效地调度线程和进程，实现内在锁。在 Mustang（Java 6.0）中，基于锁的 SynchronousQueue 算法被新的非阻塞版本代替。很少有开发人员会直接使用 SynchronousQueue，但是通过 Executors.newCachedThreadPool() 工厂构建的线程池用它作为工作队列。比较缓存线程池性能的对比测试显示，新的非阻塞同步队列实现提供了几乎是当前实现 3 倍的速度。在 Mustang 的后续版本（代码名称为 Dolphin）中，已经规划了进一步的改进。

#### V.High-level concurrent utility classes

The following new API is in java.util.concurrent of JDK5

##### 5.1.TimeUnit

尽管本质上 不是 Collections 类，但 java.util.concurrent.TimeUnit 枚举让代码更易读懂。使用 TimeUnit 将使用您的方法或 API 的开发人员从毫秒的 “暴政” 中解放出来。
TimeUnit 包括所有时间单位，从 MILLISECONDS 和 MICROSECONDS 到 DAYS 和 HOURS，这就意味着它能够处理一个开发人员所需的几乎所有的时间范围类型。同时，因为在列举上声明了转换方法，在时间加快时，将 HOURS 转换回 MILLISECONDS 甚至变得更容易。

##### 5.2.CopyOnWriteArrayList (New thread-safe List)

创建数组的全新副本是过于昂贵的操作，无论是从时间上，还是从内存开销上，因此在通常使用中很少考虑；开发人员往往求助于使用同步的 ArrayList。然而，这也是一个成本较高的选择，因为每当您跨集合内容进行迭代时，您就不得不同步所有操作，包括读和写，以此保证一致性。
这又让成本结构回到这样一个场景：需多读者都在读取 ArrayList，但是几乎没人会去修改它。
CopyOnWriteArrayList 是个巧妙的小宝贝，能解决这一问题。它的 Javadoc 将 CopyOnWriteArrayList 定义为一个 “ArrayList 的线程安全变体，在这个变体中所有易变操作（添加，设置等）可以通过复制全新的数组来实现”。
集合从内部将它的内容复制到一个没有修改的新数组，这样读者访问数组内容时就不会产生同步成本（因为他们从来不是在易变数据上操作）。
本质上讲，CopyOnWriteArrayList 很适合处理 ArrayList 经常让我们失败的这种场景：读取频繁，但很少有写操作的集合，例如 JavaBean 事件的 Listeners。

##### 5.3.BlockingQueue (Simpler List API) 阻塞队列

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

ArrayBlockingQueue 还体现了“公平” — 意思是它为读取器和编写器提供线程先入先出访问。这种替代方法是一个更有效，但又冒穷尽部分线程风险的政策。（即，允许一些读取器在其他读取器锁定时运行效率更高，但是您可能会有读取器线程的流持续不断的风险，导致编写器无法进行工作。）
注意 Bug！
顺便说一句，如果您注意到 Guarded Blocks 包含一个重大 bug，那么您是对的 — 如果开发人员在 main() 中的Drop 实例上同步，会出现什么情况呢？
BlockingQueue 还支持接收时间参数的方法，时间参数表明线程在返回信号故障以插入或者检索有关项之前需要阻塞的时间。这么做会避免非绑定的等待，这对一个生产系统是致命的，因为一个非绑定的等待会很容易导致需要重启的系统挂起。
LinkedBlockingQueue
PriorityBlockingQueue
ArrayBlockingQueue
SynchronousQueue

##### 5.4.SynchronousQueues

根据 Javadoc，SynchronousQueue 是个有趣的东西：
这是一个阻塞队列，其中，每个插入操作必须等待另一个线程的对应移除操作，反之亦然。*一个同步队列不具有任何内部容量，甚至不具有 1 的容量*。
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

实现代码看起来几乎相同，但是应用程序有额外获益：SynchronousQueue 允许在队列进行一个插入，只要有一个线程等着使用它。
在实践中，SynchronousQueue 类似于 Ada 和 CSP 等语言中可用的 “会合通道”。这些通道有时在其他环境中也称为 “连接”，这样的环境包括 .NET （见 参考资料）。

##### 5.5.ConcurrentMap (New thread-safe Map)

Map 有一个微妙的并发 bug，这个 bug 将许多不知情的 Java 开发人员引入歧途。ConcurrentMap 是最容易的解决方案。
当一个 Map 被从多个线程访问时，通常使用 containsKey() 或者 get() 来查看给定键是否在存储键/值对之前出现。但是即使有一个同步的 Map，线程还是可以在这个过程中潜入，然后夺取对 Map 的控制权。问题是，在对 put() 的调用中，锁在 get() 开始时获取，然后在可以再次获取锁之前释放。它的结果是个竞争条件：这是两个线程之间的竞争，结果也会因谁先运行而不同。
如果两个线程几乎同时调用一个方法，两者都会进行测试，调用put，在处理中丢失第一线程的值。幸运的是，ConcurrentMap 接口支持许多附加方法，它们设计用于在一个锁下进行两个任务：putIfAbsent()，例如，首先进行测试，然后仅当键没有存储在 Map 中时进行 put。
For example, ConcurrentHashMap

##### 5.6.ConcurrentHashMap

_针对吞吐量进行优化_

ConcurrentHashMap 使用了几个技巧来获得高程度的并发以及避免锁定，包括为不同的32 hash buckets（桶）使用多个写锁和使用 JMM 的不确定性来最小化锁被保持的时间――或者根本避免获取锁。对于大多数一般用法来说它是经过优化的，这些用法往往会检索一个很可能在 map 中已经存在的值。事实上，多数成功的get()操作根本不需要任何锁定就能运行。
(警告：不要自己试图这样做！想比 JMM 聪明不像看上去的那么容易。Java.util.concurrent 类是由并发专家编写的，并且在 JMM 安全性方面经过了严格的同行评审。）

_多个写锁_

我们可以回想一下,Hashtable(或者替代方案Collections.synchronizedMap)的可伸缩性的主要障碍是它使用了一个 map 范围（map-wide）的锁，为了保证插入、删除或者检索操作的完整性必须保持这样一个锁，而且有时候甚至还要为了保证迭代遍历操作的完整性保持这样一个锁。这样一来，只要锁被保持，就从根本上阻止了其他线程访问 Map，即使处理器有空闲也不能访问，这样大大地限制了并发性。
ConcurrentHashMap摒弃了单一的map范围的锁，取而代之的是由32个锁组成的集合，其中每个锁负责保护 hash bucket 的一个子集。锁主要由变化性操作（put() 和 remove()）使用。具有 32 个独立的锁意味着最多可以有 32 个线程可以同时修改 map。这并不一定是说在并发地对 map 进行写操作的线程数少于 32 时，另外的写操作不会被阻塞――32 对于写线程来说是理论上的并发限制数目，但是实际上可能达不到这个值。但是，32 依然比 1 要好得多，而且对于运行于目前这一代的计算机系统上的大多数应用程序来说已经足够了。&#160
map 范围的操作
有 32 个独立的锁，其中每个锁保护 hash bucket 的一个子集，这样需要独占访问 map 的操作就必须获得所有32个锁。一些 map 范围的操作，比如说size() 和 isEmpty()，也许能够不用一次锁整个 map（通过适当地限定这些操作的语义），但是有些操作，比如 map 重排（扩大 hash bucket 的数量，随着 map 的增长重新分布元素），则必须保证独占访问。Java 语言不提供用于获取可变大小的锁集合的简便方法。必须这么做的情况很少见，一旦碰到这种情况，可以用递归方法来实现。

_JMM概述_

在进入 put()、get() 和 remove() 的实现之前，让我们先简单地看一下 JMM。JMM 掌管着一个线程对内存的动作 （读和写）影响其他线程对内存的动作的方式。由于使用处理器寄存器和预处理 cache 来提高内存访问速度带来的性能提升，Java 语言规范（JLS）允许一些内存操作并不对于所有其他线程立即可见。有两种语言机制可用于保证跨线程内存操作的一致性
――*synchronized(同步块与同步方法)和volatile*。
按照 JLS 的说法，“在没有显式同步的情况下，一个实现可以自由地更新主存，更新时所采取的顺序可能是出人意料的。”其意思是说，如果没有同步的话，在一个给定线程中某种顺序的写操作对于另外一个不同的线程来说可能呈现出不同的顺序， 并且对内存变量的更新从一个线程传播到另外一个线程的时间是不可预测的。
虽然使用同步最常见的原因是保证对代码关键部分的原子访问，但实际上同步提供三个独立的功能――原子性、可见性和顺序性。原子性非常简单――同步实施一个可重入的（reentrant）互斥，防止多于一个的线程同时执行由一个给定的监视器保护的代码块。不幸的是，多数文章都只关注原子性方面，而忽略了其他方面。但是同步在 JMM 中也扮演着很重要的角色，会引起 JVM 在获得和释放监视器的时候执行内存壁垒（memory barrier）。
一个线程在获得一个监视器之后，它执行一个读屏障（read barrier）――使得缓存在线程局部内存（比如说处理器缓存或者处理器寄存器）中的所有变量都失效，这样就会导致处理器重新从主存中读取同步代码块使用的变量。与此类似，在释放监视器时，线程会执行一个写屏障（write barrier）――将所有修改过的变量写回主存。互斥独占和内存壁垒结合使用意味着只要您在程序设计的时候遵循正确的同步法则（也就是说，每当写一个后面可能被其他线程访问的变量，或者读取一个可能最后被另一个线程修改的变量时，都要使用同步），每个线程都会得到它所使用的共享变量的正确的值。
如果在访问共享变量的时候没有同步的话，就会发生一些奇怪的事情。一些变化可能会通过线程立即反映出来，而其他的则需要一些时间（这由关联缓存的本质所致）。结果，如果没有同步您就不能保证内存内容必定一致（相关的变量相互间可能会不一致），或者不能得到当前的内存内容（一些值可能是过时的）。避免这种危险情况的常用方法（也是推荐使用的方法）当然是正确地使用同步。然而在有些情况下，比如说在像 ConcurrentHashMap 之类的一些使用非常广泛的库类中，在开发过程当中还需要一些额外的专业技能和努力（可能比一般的开发要多出很多倍）来获得较高的性能。

_ConcurrentHashMap实现_
如前所述，ConcurrentHashMap 使用的数据结构与 Hashtable 或 HashMap 的实现类似，是 hash bucket 的一个可变数组，每个ConcurrentHashMap 都由一个 Map.Entry 元素链构成，如清单1所示。与 Hashtable 和 HashMap 不同的是，ConcurrentHashMap 没有使用单一的集合锁（collection lock），而是使用了一个固定的锁池，这个锁池形成了bucket 集合的一个分区。

清单1. ConcurrentHashMap 使用的 Map.Entry 元素
```java
protected static class Entry implements Map.Entry {
    protected final Object key;
    protected volatile Object value;
    protected final int hash;
    protected final Entry next;
...}
```

不用锁定遍历数据结构
与 Hashtable 或者典型的锁池 Map 实现不同，ConcurrentHashMap.get() 操作不一定需要获取与相关bucket 相关联的锁。如果不使用锁定，那么实现必须有能力处理它用到的所有变量的过时的或者不一致的值，比如说列表头指针和 Map.Entry 元素的域（包括组成每个 hash bucket 条目的链表的链接指针）。
大多并发类使用同步来保证独占式访问一个数据结构（以及保持数据结构的一致性）。ConcurrentHashMap 没有采用独占性和一致性，它使用的链表是经过精心设计的，所以其实现可以检测到它的列表是否一致或者已经过时。如果它检测到它的列表出现不一致或者过时，或者干脆就找不到它要找的条目，它就会对适当的 bucket 锁进行同步并再次搜索整个链。这样做在一般的情况下可以优化查找，所谓的一般情况是指大多数检索操作是成功的并且检索的次数多于插入和删除的次数。
使用不变性
不一致性的一个重要来源是可以避免得，其方法是使 Entry 元素接近不变性――除了值字段（它们是易变的）之外，所有字段都是 final 的。这就意味着不能将元素添加到 hash 链的中间或末尾，或者从 hash 链的中间或末尾删除元素――而只能从 hash 链的开头添加元素，并且删除操作包括克隆整个链或链的一部分并更新列表的头指针。所以说只要有对某个 hash 链的一个引用，即使可能不知道有没有对列表头节点的引用，您也可以知道列表的其余部分的结构不会改变。而且，因为值字段是易变的，所以能够立即看到对值字段的更新，从而大大简化了编写能够处理内存潜在过时的 Map 的实现。
新的 JMM 为 final 型变量提供初始化安全，而老的 JMM 不提供，这意味着另一个线程看到的可能是 final 字段的默认值，而不是对象的构造方法提供的值。实现必须能够同时检测到这一点，这是通过保证 Entry中每个字段的默认值不是有效值来实现的。这样构造好列表之后，如果任何一个 Entry 字段有其默认值（零或空），搜索就会失败，提示同步 get() 并再次遍历链。
检索操作
检索操作首先为目标 bucket 查找头指针（是在不锁定的情况下完成的，所以说可能是过时的），然后在不获取 bucket 锁的情况下遍历 bucket 链。如果它不能发现要查找的值，就会同步并试图再次查找条目，如清单2 所示：

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

删除操作
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
  
插入和更新操作
put() 的实现很简单。像 remove() 一样，put() 会在执行期间保持 bucket 锁，但是由于 put() 并不是都需要获取锁，所以这并不一定会阻塞其他读线程的执行（也不会阻塞其他写线程访问别的 bucket）。它首先会在适当的 hash 链中搜索需要的键值。如果能够找到，value字段（易变的）就直接被更新。如果没有找到，新会创建一个用于描述新 map 的新 Entry 对象，然后插入到 bucket 列表的头部。
弱一致的迭代器
由 ConcurrentHashMap 返回的迭代器的语义又不同于java.util 集合中的迭代器；而且它又是 弱一致的（weakly consistent） 而非 fail-fast 的（所谓 fail-fast 是指，当正在使用一个迭代器的时候，如何底层的集合被修改，就会抛出一个异常）。当一个用户调用keySet().iterator() 去迭代器中检索一组 hash 键的时候，实现就简单地使用同步来保证每个链的头指针是当前值。next()和hasNext() 操作以一种明显的方式定义，即遍历每个链然后转到下一个链直到所有的链都被遍历。弱一致迭代器可能会也可能不会反映迭代器迭代过程中的插入操作，但是一定会反映迭代器还没有到达的键的更新或删除操作，并且对任何值最多返回一次。ConcurrentHashMap 返回的迭代器不会抛出 ConcurrentModificationException 异常。
动态调整大小
随着 map 中元素数目的增长，hash 链将会变长，因此检索时间也会增加。从某种意义上说，增加 bucket 的数目和重排其中的值是非常重要的。在有些像 Hashtable 之类的类中，这很简单，因为保持一个应用到整个 map 的独占锁是可能的。在ConcurrentHashMap 中，每次一个条目插入的时候，如果链的长度超过了某个阈值，链就被标记为需要调整大小。当有足够多的链被标记为需要调整大小以后，ConcurrentHashMap 就使用递归获取每个 bucket 上的锁并重排每个 bucket 中的元素到一个新的、更大的 hash 表中。多数情况下，这是自动发生的，并且对调用者透明。
不锁定？
要说不用锁定就可以成功地完成 get() 操作似乎有点言过其实，因为 Entry 的 value 字段是易变的，这是用来检测更新和删除的。在机器级，易变的和同步的内容通常在最后会被翻译成相同的缓存一致原语，所以这里会有 一些 锁定，虽然只是细粒度的并且没有调度，或者没有获取和释放监视器的 JVM 开销。但是，除语义之外，在很多通用的情况下，检索的次数大于插入和删除的次数，所以说由 ConcurrentHashMap 取得的并发性是相当高的。


*Task Management*

By reusing threads for multiple tasks, the thread-creation overhead is spread over many tasks.

##### 5.7.Executor (Thread Pool)

清单 1 和 清单 2 中的示例都存在一个重要的缺陷，它们要求您直接创建 Thread 对象。这可以解决一些问题，因为在一些 JVM 中，创建 Thread 是一项重量型的操作，重用现有 Thread 比创建新线程要容易得多。而在另一些 JVM 中，情况正好相反：Thread 是轻量型的，可以在需要时很容易地新建一个线程。当然，如果 Murphy 拥有自己的解决办法（他通常都会拥有），那么您无论使用哪种方法对于您最终将部署的平台都是不对的。
JSR-166 专家组（参见 参考资料）在一定程度上预测到了这一情形。Java 开发人员无需直接创建 Thread，他们引入了 Executor 接口，这是对创建新线程的一种抽象。如清单 3 所示，Executor 使您不必亲自对 Thread 对象执行 new 就能够创建新线程：

清单 3. Executor

```java                           
Executor exec = getAnExecutorFromSomeplace();
exec.execute(new Runnable() { ... });
```

使用 Executor 的主要缺陷与我们在所有工厂中遇到的一样：工厂必须来自某个位置。不幸的是，与 CLR 不同，JVM 没有附带一个标准的 VM 级线程池。
Executor 类实际上 充当着一个提供 Executor 实现实例的共同位置，但它只有 new 方法（例如用于创建新线程池）；它没有预先创建实例。所以您可以自行决定是否希望在代码中创建和使用 Executor 实例。（或者在某些情况下，您将能够使用所选的容器/平台提供的实例。）
ExecutorService 随时可以使用
尽管不必担心 Thread 来自何处，但 Executor 接口缺乏 Java 开发人员可能期望的某种功能，比如结束一个用于生成结果的线程并以非阻塞方式等待结果可用。（这是桌面应用程序的一个常见需求，用户将执行需要访问数据库的 UI 操作，然后如果该操作花费了很长时间，可能希望在它完成之前取消它。）
对于此问题，JSR-166 专家创建了一个更加有用的抽象（ExecutorService 接口），它将线程启动工厂建模为一个可集中控制的服务。例如，无需每执行一项任务就调用一次 execute()，ExecutorService 可以接受一组任务并返回一个表示每项任务的未来结果的未来列表。

The Executors class contains static factory methods for constructing a number of different kinds of Executor
implementations:
Executors.newCachedThreadPool()
Executors.newFixedThreadPool(int n)
Executors.newSingleThreadExecutor()


##### 5.8.ScheduledExecutorServices (Scheduled Thread Pool)

尽管 ExecutorService 接口非常有用，但某些任务仍需要以计划方式执行，比如以确定的时间间隔或在特定时间执行给定的任务。这就是 ScheduledExecutorService 的应用范围，它扩展了 ExecutorService。
如果您的目标是创建一个每隔 5 秒跳一次的 “心跳” 命令，使用 ScheduledExecutorService 可以轻松实现，如清单 4 所示：

清单 4. ScheduledExecutorService 模拟心跳

```java                         
import java.util.concurrent.*;

public class Ping
{
    public static void main(String[] args)
    {
        ScheduledExecutorService ses =
            Executors.newScheduledThreadPool(1);
        Runnable pinger = new Runnable() {
            public void run() {
                System.out.println("PING!");
            }
        };
        ses.scheduleAtFixedRate(pinger, 5, 5, TimeUnit.SECONDS);
    }
}
```

这项功能怎么样？不用过于担心线程，不用过于担心用户希望取消心跳时会发生什么，也不用明确地将线程标记为前台或后台；只需将所有的计划细节留给 ScheduledExecutorService。
顺便说一下，如果用户希望取消心跳，scheduleAtFixedRate 调用将返回一个 ScheduledFuture 实例，它不仅封装了结果（如果有），还拥有一个 cancel 方法来关闭计划的操作。

##### 5.9. Future 

The Future interface allows you to represent a task that may have completed,may be in the process of being executed, or may not yet have started execution. Through the Future interface, you can attempt to cancel a task that has not yet completed, inquire whether the task has completed or cancelled, and fetch (or wait for) the task's result value.

The FutureTask class implements Future, and has constructors that allow you to wrap a Runnable or Callable (a result-bearing Runnable) with a Future interface. Because FutureTask also implements Runnable, you canthen simply submit FutureTask to an Executor. Some submission methods (like ExecutorService.submit()) will return a Future interface in addition to submitting the task.
The Future.get() method retrieves the result of the task computation (or throws ExecutionException if the task completed with an exception). If the task has not yet completed, Future.get() will block until the task completes; If it has already completed, the result will be returned immediately.

Building a cache with Future
This code example ties together several classes from java.util.concurrent, prominently showcasing the power of Future. It implements a cache, and uses Future to describe a cached value that may already be computed or that may be "under construction" in another thread.

It takes advantage of the atomic putIfAbsent() method in ConcurrentHashMap, ensuring that only one thread will try to compute the value for a given key. If another thread subsequently requests the value for that
same key, it simply waits (with the help of Future.get()) for the first thread to complete. As a result, two threads will not try to compute the same value.

```java
public class Cache<K, V> {
ConcurrentMap<K, FutureTask<V>> map = new ConcurrentHashMap();
Executor executor = Executors.newFixedThreadPool(8);
public V get(final K key) {
FutureTask<V> f = map.get(key);
if (f == null) {
Callable<V> c = new Callable<V>() {
public V call() {
// return value associated with key
}
};
f = new FutureTask<V>(c);
FutureTask old = map.putIfAbsent(key, f);
if (old == null)
executor.execute(f);
else
f = old;
}
return f.get();
}
}
``

##### 5.10. CompletionService

Synchronizer classes

##### 5.11. Semaphore (信号量) (a classic Dijkstra counting semaphore)

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

即使本例中的 10 个线程都在运行（您可以对运行 SemApp 的 Java 进程执行 jstack 来验证），但只有 3 个线程是活跃的。在一个信号计数器释放之前，其他 7 个线程都处于空闲状态。（实际上，Semaphore 类支持一次获取和释放多个 permit，但这不适用于本场景。）

##### 5.12. CyclicBarrier

The CyclicBarrier class is a synchronization aid that allows a set of threads to wait for the entire set of threads to reach a common barrier point.

##### 5.13. CountDownLatch

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

注意，在 清单 2 中，CountDownLatch 有两个用途：首先，它同时释放所有线程，模拟马赛的起点，但随后会设置一个门闩模拟马赛的终点。这样，“主” 线程就可以输出结果。 为了让马赛有更多的输出注释，可以在赛场的 “转弯处” 和 “半程” 点，比如赛马跨过跑道的四分之一、二分之一和四分之三线时，添加 CountDownLatch。

##### 5.14. Timeout 方法

为阻塞操作设置一个具体的超时值（以避免死锁）的能力是 java.util.concurrent 库相比起早期并发特性的一大进步，比如监控锁定。
这些方法几乎总是包含一个 int/TimeUnit 对，指示这些方法应该等待多长时间才释放控制权并将其返回给程序。它需要开发人员执行更多工作 — 如果没有获取锁，您将如何重新获取？ — 但结果几乎总是正确的：更少的死锁和更加适合生产的代码。（关于编写生产就绪代码的更多信息，请参见 参考资料 中 Michael Nygard 编写的 Release It!。）


#### VI.InterruptedException处理

这样的情景您也许并不陌生：您在编写一个测试程序，程序需要暂停一段时间，于是调用 Thread.sleep()。但是编译器或 IDE 报错说没有处理检查到的 InterruptedException。InterruptedException 是什么呢，为什么必须处理它？
对于 InterruptedException，一种常见的处理方式是 “生吞（swallow）” 它 —— 捕捉它，然后什么也不做（或者记录下它，不过这也好不到哪去）—— 就像后面的 清单 4 一样。不幸的是，这种方法忽略了这样一个事实：这期间可能发生中断，而中断可能导致应用程序丧失及时取消活动或关闭的能力。

_阻塞方法_

当一个方法抛出 InterruptedException 时，它不仅告诉您它可以抛出一个特定的检查异常，而且还告诉您其他一些事情。例如，它告诉您它是一个阻塞（blocking）方法，如果您响应得当的话，它将尝试消除阻塞并尽早返回。
阻塞方法不同于一般的要运行较长时间的方法。一般方法的完成只取决于它所要做的事情，以及是否有足够多可用的计算资源（CPU 周期和内存）。而阻塞方法的完成还取决于一些外部的事件，例如计时器到期，I/O 完成，或者另一个线程的动作（释放一个锁，设置一个标志，或者将一个任务放在一个工作队列中）。一般方法在它们的工作做完后即可结束，而阻塞方法较难于预测，因为它们取决于外部事件。阻塞方法可能影响响应能力，因为难于预测它们何时会结束。
阻塞方法可能因为等不到所等的事件而无法终止，因此令阻塞方法可取消 就非常有用（如果长时间运行的非阻塞方法是可取消的，那么通常也非常有用）。可取消操作是指能从外部使之在正常完成之前终止的操作。由 Thread 提供并受 Thread.sleep() 和Object.wait() 支持的中断机制就是一种取消机制；它允许一个线程请求另一个线程停止它正在做的事情。当一个方法抛出InterruptedException 时，它是在告诉您，如果执行该方法的线程被中断，它将尝试停止它正在做的事情而提前返回，并通过抛出 InterruptedException 表明它提前返回。 行为良好的阻塞库方法应该能对中断作出响应并抛出 InterruptedException，以便能够用于可取消活动中，而不至于影响响应。

_线程中断_

每个线程都有一个与之相关联的 Boolean 属性，用于表示线程的中断状态（interrupted status）。中断状态初始时为 false；当另一个线程通过调用 Thread.interrupt() 中断一个线程时，会出现以下两种情况之一。如果那个线程在执行一个低级可中断阻塞方法，例如 Thread.sleep()、 Thread.join() 或 Object.wait()，那么它将取消阻塞并抛出 InterruptedException。否则，interrupt() 只是设置线程的中断状态。 在被中断线程中运行的代码以后可以轮询中断状态，看看它是否被请求停止正在做的事情。中断状态可以通过 Thread.isInterrupted() 来读取，并且可以通过一个名为 Thread.interrupted() 的操作读取和清除。
中断是一种协作机制。当一个线程中断另一个线程时，被中断的线程不一定要立即停止正在做的事情。相反，中断是礼貌地请求另一个线程在它愿意并且方便的时候停止它正在做的事情。有些方法，例如 Thread.sleep()，很认真地对待这样的请求，但每个方法不是一定要对中断作出响应。对于中断请求，不阻塞但是仍然要花较长时间执行的方法可以轮询中断状态，并在被中断的时候提前返回。 您可以随意忽略中断请求，但是这样做的话会影响响应。
中断的协作特性所带来的一个好处是，它为安全地构造可取消活动提供更大的灵活性。我们很少希望一个活动立即停止；如果活动在正在进行更新的时候被取消，那么程序数据结构可能处于不一致状态。中断允许一个可取消活动来清理正在进行的工作，恢复不变量，通知其他活动它要被取消，然后才终止。

_处理 InterruptedException_

如果抛出 InterruptedException 意味着一个方法是阻塞方法，那么调用一个阻塞方法则意味着您的方法也是一个阻塞方法，而且您应该有某种策略来处理 InterruptedException。通常最容易的策略是自己抛出 InterruptedException，如清单 1 中putTask() 和 getTask() 方法中的代码所示。 这样做可以使方法对中断作出响应，并且只需将 InterruptedException 添加到 throws 子句。

清单 1. 不捕捉 InterruptedException，将它传
```java
public class TaskQueue {
    private static final int MAX_TASKS = 1000;

    private BlockingQueue<Task> queue 
        = new LinkedBlockingQueue<Task>(MAX_TASKS);

    public void putTask(Task r) throws InterruptedException { 
        queue.put(r);
    }

    public Task getTask() throws InterruptedException { 
        return queue.take();
    }
}
```

有时候需要在传播异常之前进行一些清理工作。在这种情况下，可以捕捉 InterruptedException，执行清理，然后抛出异常。清单 2 演示了这种技术，该代码是用于匹配在线游戏服务中的玩家的一种机制。 matchPlayers() 方法等待两个玩家到来，然后开始一个新游戏。如果在一个玩家已到来，但是另一个玩家仍未到来之际该方法被中断，那么它会将那个玩家放回队列中，然后重新抛出InterruptedException，这样那个玩家对游戏的请求就不至于丢失。

清单 2. 在重新抛出 InterruptedException 之前执行特定于任务的清理工作
```java
public class PlayerMatcher {
    private PlayerSource players;

    public PlayerMatcher(PlayerSource players) { 
        this.players = players; 
    }

    public void matchPlayers() throws InterruptedException { 
        try {
             Player playerOne, playerTwo;
             while (true) {
                 playerOne = playerTwo = null;
                 // Wait for two players to arrive and start a new game
                 playerOne = players.waitForPlayer(); // could throw IE
                 playerTwo = players.waitForPlayer(); // could throw IE
                 startNewGame(playerOne, playerTwo);
             }
         }
         catch (InterruptedException e) {  
             // If we got one player and were interrupted, put that player back
             if (playerOne != null)
                 players.addFirst(playerOne);
             // Then propagate the exception
             throw e;
         }
    }
}
```

_不要生吞中断_
有时候抛出 InterruptedException 并不合适，例如当由 Runnable 定义的任务调用一个可中断的方法时，就是如此。在这种情况下，不能重新抛出 InterruptedException，但是您也不想什么都不做。当一个阻塞方法检测到中断并抛出InterruptedException 时，它清除中断状态。如果捕捉到 InterruptedException 但是不能重新抛出它，那么应该保留中断发生的证据，以便调用栈中更高层的代码能知道中断，并对中断作出响应。该任务可以通过调用 interrupt() 以 “重新中断” 当前线程来完成，如清单 3 所示。至少，每当捕捉到 InterruptedException 并且不重新抛出它时，就在返回之前重新中断当前线程。

清单 3. 捕捉 InterruptedException 后恢复中断状态
```java
public class TaskRunner implements Runnable {
    private BlockingQueue<Task> queue;

    public TaskRunner(BlockingQueue<Task> queue) { 
        this.queue = queue; 
    }

    public void run() { 
        try {
             while (true) {
                 Task task = queue.take(10, TimeUnit.SECONDS);
                 task.execute();
             }
         }
         catch (InterruptedException e) { 
             // Restore the interrupted status
             Thread.currentThread().interrupt();
         }
    }
}
```

处理 InterruptedException 时采取的最糟糕的做法是生吞它 —— 捕捉它，然后既不重新抛出它，也不重新断言线程的中断状态。对于不知如何处理的异常，最标准的处理方法是捕捉它，然后记录下它，但是这种方法仍然无异于生吞中断，因为调用栈中更高层的代码还是无法获得关于该异常的信息。（仅仅记录 InterruptedException 也不是明智的做法，因为等到人来读取日志的时候，再来对它作出处理就为时已晚了。） 清单 4 展示了一种使用得很广泛的模式，这也是生吞中断的一种模式：

清单 4. 生吞中断 —— 不要这么做
```java
// Don't do this 
public class TaskRunner implements Runnable {
    private BlockingQueue<Task> queue;

    public TaskRunner(BlockingQueue<Task> queue) { 
        this.queue = queue; 
    }

    public void run() { 
        try {
             while (true) {
                 Task task = queue.take(10, TimeUnit.SECONDS);
                 task.execute();
             }
         }
         catch (InterruptedException swallowed) { 
             /* DON'T DO THIS - RESTORE THE INTERRUPTED STATUS INSTEAD */
         }
    }
}
```

如果不能重新抛出 InterruptedException，不管您是否计划处理中断请求，仍然需要重新中断当前线程，因为一个中断请求可能有多个 “接收者”。标准线程池 （ThreadPoolExecutor）worker 线程实现负责中断，因此中断一个运行在线程池中的任务可以起到双重效果，一是取消任务，二是通知执行线程线程池正要关闭。如果任务生吞中断请求，则 worker 线程将不知道有一个被请求的中断，从而耽误应用程序或服务的关闭。

_实现可取消任务_
语言规范中并没有为中断提供特定的语义，但是在较大的程序中，难于维护除取消外的任何中断语义。取决于是什么活动，用户可以通过一个 GUI 或通过网络机制，例如 JMX 或 Web 服务来请求取消。程序逻辑也可以请求取消。例如，一个 Web 爬行器（crawler）如果检测到磁盘已满，它会自动关闭自己，否则一个并行算法会启动多个线程来搜索解决方案空间的不同区域，一旦其中一个线程找到一个解决方案，就取消那些线程。
仅仅因为一个任务是可取消的，并不意味着需要立即 对中断请求作出响应。对于执行一个循环中的代码的任务，通常只需为每一个循环迭代检查一次中断。取决于循环执行的时间有多长，任何代码可能要花一些时间才能注意到线程已经被中断（或者是通过调用Thread.isInterrupted() 方法轮询中断状态，或者是调用一个阻塞方法）。 如果任务需要提高响应能力，那么它可以更频繁地轮询中断状态。阻塞方法通常在入口就立即轮询中断状态，并且，如果它被设置来改善响应能力，那么还会抛出InterruptedException。
惟一可以生吞中断的时候是您知道线程正要退出。只有当调用可中断方法的类是 Thread 的一部分，而不是 Runnable 或通用库代码的情况下，才会发生这样的场景，清单 5 演示了这种情况。清单 5 创建一个线程，该线程列举素数，直到被中断，这里还允许该线程在被中断时退出。用于搜索素数的循环在两个地方检查是否有中断：一处是在 while 循环的头部轮询 isInterrupted() 方法，另一处是调用阻塞方法 BlockingQueue.put()。

清单 5. 如果知道线程正要退出的话，则可以生吞中断
```java
public class PrimeProducer extends Thread {
    private final BlockingQueue<BigInteger> queue;

    PrimeProducer(BlockingQueue<BigInteger> queue) {
        this.queue = queue;
    }

    public void run() {
        try {
            BigInteger p = BigInteger.ONE;
            while (!Thread.currentThread().isInterrupted())
                queue.put(p = p.nextProbablePrime());
        } catch (InterruptedException consumed) {
            /* Allow thread to exit */
        }
    }

    public void cancel() { interrupt(); }
}
```

_不可中断的阻塞方法_
并非所有的阻塞方法都抛出 InterruptedException。输入和输出流类会阻塞等待 I/O 完成，但是它们不抛出InterruptedException，而且在被中断的情况下也不会提前返回。然而，对于套接字 I/O，如果一个线程关闭套接字，则那个套接字上的阻塞 I/O 操作将提前结束，并抛出一个 SocketException。java.nio 中的非阻塞 I/O 类也不支持可中断 I/O，但是同样可以通过关闭通道或者请求 Selector 上的唤醒来取消阻塞操作。类似地，尝试获取一个内部锁的操作（进入一个 synchronized 块）是不能被中断的，但是 ReentrantLock 支持可中断的获取模式。
不可取消的任务
有些任务拒绝被中断，这使得它们是不可取消的。但是，即使是不可取消的任务也应该尝试保留中断状态，以防在不可取消的任务结束之后，调用栈上更高层的代码需要对中断进行处理。清单 6 展示了一个方法，该方法等待一个阻塞队列，直到队列中出现一个可用项目，而不管它是否被中断。为了方便他人，它在结束后在一个 finally 块中恢复中断状态，以免剥夺中断请求的调用者的权利。（它不能在更早的时候恢复中断状态，因为那将导致无限循环 —— BlockingQueue.take() 将在入口处立即轮询中断状态，并且，如果发现中断状态集，就会抛出 InterruptedException。）

清单 6. 在返回前恢复中断状态的不可取消任务
```java
public Task getNextTask(BlockingQueue<Task> queue) {
    boolean interrupted = false;
    try {
        while (true) {
            try {
                return queue.take();
            } catch (InterruptedException e) {
                interrupted = true;
                // fall through and retry
            }
        }
    } finally {
        if (interrupted)
            Thread.currentThread().interrupt();
    }
}
```


#### VII.Concurrency Programming Bug Anaysis

编写多线程程序的第一准则是先保证正确性，再考虑优化性能。本文重点分析多线程编程中除死锁之外的两种常见Bug：违反原子性（Atomicity Violation）和违反执行顺序（Ordering Violation）。现在已经有很多检测多线程Bug的工具，但是这两种Bug还没有工具能完美地帮你检测出来，所以到目前为止最好的办法还是程序员自己有意识的避免这两种Bug。本文的目的就是帮助程序员了解这两种Bug的常见形式和常见解决办法。

_多线程程序执行模型_

在剖析Bug之前，我们先来简单回顾一下多线程程序是怎么执行的。从程序员的角度来看，一个多线程程序的执行可以看成是每个子线程的指令交错在一起共同执行的，即Sequential Consistency模型。它有两个属性：每个线程内部的指令是按照代码指定的顺序执行的（Program Order），但是线程之间的交错顺序是任意的、不确定的（Non deterministic）。
我原来举过一个形象的例子。伸出你的双手，掌心面向你，两个手分别代表两个线程，从食指到小拇指的四根手指头分别代表每个线程要依次执行的四条指令。
（1）对每个手来说，它的四条指令的执行顺序必须是从食指执行到小拇指
（2）你两个手的八条指令（八个手指头）可以在满足（1）的条件下任意交错执行（例如可以是左1，左2，右1，右2，右3，左3，左4，右4，也可以是左1，左2，左3，左4，右1，右2，右3，右4，也可以是右1，右2，右3，左1，左2，右4，左3，左4等等等等）
好了，现在让我们来看看程序员在写多线程程序时是怎么犯错的。

_违反原子性（Atomicity violation）_

何谓原子性？简单的说就是不可被其他线程分割的操作。大部分程序员在编写多线程程序员时仍然是按照串行思维来思考，他们习惯性的认为一些简单的代码肯定是原子的。
例如：

     Thread 1                                Thread 2
S1: if (thd->proc_info)
{               ...                     S3: thd->proc_info=NULL;
  S2: fputs(thd->proc_info,...)
}
这个Bug的根源就在于程序员认为线程1在执行S1时如果从
thd->proc&_info读到一个非NULL的值的话，在执行S2时thd->proc&_info的值肯定也是非NULL的。事实上，因为S1与S2并不是原子操作，所以它们之间可能被S3打断，即按S1->S2->S3的顺序执行，从而导致程序出错。
这个例子的对象是两条语句，所以很容易看出来它们不是原子的。事实上，有些看起来像是原子操作的代码实际上也不是原子的。最著名的莫过于多个线程执行类似“x++”这样的操作了。这条语句本身不是原子的，因为它在大部分硬件平台上其实是由三条语句实现的：

mov eax,dword ptr [x]
add eax,1
mov dword ptr [x],eax
同样，下面这个“r.Location = p”也不是原子的，因为事实上它是两个操作：“r.Location.X = p.X”和“r.Location.Y = p.Y”组成的。

struct RoomPoint {
   public int X;
   public int Y;
}

RoomPoint p = new RoomPoint(2,3);
r.Location = p;
从根源上来讲，如果你想让这段代码真正按照你的心意来执行，你就得在脑子里仔细考虑是否会出现违反你本意的执行顺序，特别是涉及的变量（例如thd->proc_info）在其他线程中有可能被修改的情况，也就是数据竞争（Data Race）。如果对同一个内存位置的同时进行的两个操作中至少有一个是写操作，数据竞争就发生了。
有时候数据竞争可是隐藏的很深的，例如下面的Parallel.For看似很正常：

Parallel.For(0, 10000,
    i => {a[i] = new Foo();})
实际上，如果我们去看看Foo的实现：

```java
class Foo {
        private static int counter;
        private int unique_id;
        public Foo()
       {
                unique_id = counter++;
       }
}
```

同志们，看出来哪里有数据竞争了么？是的，counter是静态变量，Foo()这个构造函数里面呃counter++产生数据竞争了！想避免Atomicity Violation，其实根本上就是要保证没有数据竞争（Data Race Free）。
解决方案
解决方案大致有三（可结合使用）：
（1）把变量隔离起来：只有一个线程可以访问它（isolation）
（2）把变量的属性定义为immutable的：这样它就是只读的了（immutability）
（3）同步对这个变量的读写：比如用锁把它锁起来（synchronization）
例如下面这个例子里面x是immutable的；a[]通过index i隔离起来了，不同线程处理a[]中不同的元素；

Parallel.For(1,1000,
i => {
    a[i] = x;
});
例如下面这个例子在构造函数中给x和y赋值（此时别的线程不能访问它们），保证了isolation；一旦构造完毕x和y就是只读的了，保证了immutability。

```java
public class Coordinate
{
   private double x, y;

   public Coordinate(double a,
                     double b)
   {
      x = a;
      y = b;
   }
   public void GetX() {
      return x;
   }
   public void GetY() {
      return y;
   }
}
```
而我最开始提到的关于thd->proc_info的Bug可以通过把S1和S2两条语句用pthread_mutex_lock/unlock包围起来解决。
还有另一个用锁来同步的例子，即通过使用锁（Java中的synchronized关键字）来保证没有数据竞争：
“Java 5 中提供了 ConcurrentLinkedQueue 来简化并发操作。但是有一个问题：使用了这个类之后是否意味着我们不需要自己进行任何同步或加锁操作了呢？
也就是说，如果直接使用它提供的函数，比如：queue.add(obj); 或者 queue.poll(obj);，这样我们自己不需要做任何同步。但如果是非原子操作，比如：”
```java
if(!queue.isEmpty()) {

   // 无法确定queue是否被其他线程修改，在执行poll之前
   queue.poll(obj);
}
```
事实情况就是在调用isEmpty()之后，poll()之前，这个queue没有被其他线程修改是不确定的，所以对于这种情况，我们还是需要自己同步：
```java
synchronized(queue) {
    if(!queue.isEmpty()) {
       queue.poll(obj);
    }
}
```
但是注意了，使用锁也会造成一堆Bug，死锁就先不说了，先看看初学者容易犯的一个错误（是的，我曾经就犯了这个错误），x在两个不同的临界区中被修改，加了锁跟没加一样，因为还是有数据竞争：

int x;
pthread_mutex_t lock1;
pthread_mutex_t lock2;

pthread_mutex_lock(&lock1);
x++;
pthread_mutex_unlock(&lock1);
...
...
pthread_mutex_lock(&lock2);
x++;
pthread_mutex_unlock(&lock2);

总结一下，语句之间的原子性也好，指令之间的原子性也好都需要大家格外小心，有经验之后很多Bug就可以被避免了。

_违反执行顺序（Ordering Violation）_

简单来说，多线程程序各个线程之间交错执行的顺序的不确定性（Non-deterministic）是造成违反执行顺序Bug的根源[注1]。正是因为这个原因，程序员在编写多线程程序时就不能假设程序会按照你设想的某个顺序去执行，而是应该充分考虑到各种可能的顺序组合，从而采取正确的同步措施。

1. 违反执行顺序（Ordering Violation）

举例来说，下面这个来自Mozilla的多线程Bug产生的原因就是程序员错误地假设S1一定会在S2之前执行完毕，即在S2访问mThread之前S1一定已经完成了对mThread的初始化（因为线程2是由线程1创建的）。事实上线程2完全有可能执行的很快，而且S1这个初始化操作又不是原子的（因为需要几个时钟周期才能结束），从而在线程1完成初始化（即S1）之前就已经运行到S2从而导致Bug。
01  例1：
02      Thread 1                                 Thread 2
03  void init(...)                           void mMain(...)
04  { ...                                    { ...
05   S1: mThread=                              ...
06        PR_CreateThread(mMain, ...);         S2: mState = mThread->State;
07    ...                                      ...
08  }                                        }
上面这个例子是一个线程读一个线程写的情况，除此之外还有违反写-写顺序以及违反一组读写顺序的情况。例如下面这个程序，程序员错误的以为S2（写操作）一定会在S4（也是写操作）之前执行。但是实际上这个程序完全有可能先执行S4后执行S2，从而导致线程1一直hang在S3处：
01  例2：
02      Thread 1                                 Thread 2
03  int ReadWriteProc(...)                   void DoneWaiting(...)
04  {                                        {
05    ...                                     /*callback func of PBReadAsync*/
06   S1: PBReadAsync(&p);
07   S2: io_pending = TRUE;                   ...
08    ...                                     S4: io_pending = FALSE;
09   S3: while (io_pending) {...}             ...
10    ...                                    }
11  }
下面这个是违反一组读写操作顺序的例子：程序员假设S2一定会在S1之前执行，但是事实上可能S1在S2之前执行，从而导致程序crash。
01  例3：
02      Thread 1                                 Thread 2
03  void js_DestroyContext(...){             void js_DestroyContext(...){
04    /* last one entering this func */      /* non-last one entering this func */
05    S1: js_UnpinPinnedAtom(&atoms);          S2: js_MarkAtom(&atoms,...);
06  }                                        }
调试违反执行顺序这种类型的Bug最困难的地方就在只有某几种执行顺序才会引发Bug，这大大降低了Bug重现的几率。最简单的调试手段自然是使用printf了，但是类似printf这样的函数会干扰程序的执行顺序，所以有可能违反执行顺序的Bug更难产生了。我所知道的目前最领先的商业多线程Debugger是Corensic的Jinx，他们的技术核心是用Hypervisor来控制线程的执行顺序以找出可能产生Bug的那些特定的执行顺序（学生、开源项目可以申请免费使用，Windows/Linux版均有）。八卦一下，这个公司是从U of Washington发展出来的，他们现在做的Deterministic Parallelism是最热门的方向之一。

2. Ordering Violation的解决方案

常见的解决方案主要有四种：
（1）加锁进行同步
加锁的目的就在于保证被锁住的操作的原子性，从而这些被锁住的操作就不会被别的线程的操作打断，在一定程度上保证了所需要的执行顺序。例如上面第二个例子可以给{S1,S2}一起加上锁，这样就不会出现S4打断S1,S2的情况了（即S1->S4->S2），因为S4是由S1引发的异步调用，S4肯定会在{S1,S2}这个原子操作执行完之后才能被运行。
（2）进行条件检查
进行条件检查是另一种常见的解决方案，关键就在于通过额外的条件语句来迫使该程序会按照你所想的方式执行。例如下面这个例子就会对n的值进行检查：
01  例4：
02  retry:
03    n = block->n;
04    ...
05    ...
06    if (n!=block->n)
07    {
08      goto retry;
09    }
10    ...
（3）调整代码执行顺序
这个也是很可行的方案，例如上面的例2不需要给{S1,S2}加锁，而是直接调换S2与S1的顺序，这样S2就一定会在S4之前执行了！
（4）重新设计算法/数据结构
还有一些执行顺序的问题可以通过重新设计算法/数据结构来解决。这个就得具体情况具体分析了。例如MySQL的bug #7209中，一个共享变量HASH::current_record的访问有顺序上的冲突，但是实际上这个变量不需要共享，所以最后的解决办法就是线程私有化这个变量。

3. 总结

多线程Bug确实是个非常让人头痛的问题。写多线程程序不难，难的在于写正确的多线程程序。多线程的debug现在仍然可以作为CS Top10学校的博士论文题目。在看过这两篇分析多线程常见Bug的文章之后，不知道各位同学有没有什么关于多线程Bug的经历与大家分享呢？欢迎大家留言:)
需要注意的是，违反执行顺序和违反原子性这两种Bug虽然是相互独立的，但是两者又有着潜在的联系。例如，上一篇文章中我所讲到的第一个违反原子性的例子其实是因为执行顺序的不确定性造成的，而本文的第二个例子就可以通过把{S1,S2}加锁保证原子性来保证想要的执行顺序。
参考
[1] Learning from Mistakes – A Comprehensive Study on Real World Concurrency Bug Characteristics
[2] Understanding, Detecting and Exposing Concurrency Bugs
[3] Practical Parallel and Concurrent Programming
注1：严格来讲，多线程交错执行顺序的不确定性只是违反执行顺序Bug的原因之一。另一个可能造成违反执行顺序Bug的原因是编译器/CPU对代码做出的违反多线程程序语义的乱序优化，这种“错误的优化”直接引出了编程语言的内存模型（memory model）这个关键概念。后面我会专门分析下C++与Java的内存模型，敬请期待。
              Concurrency Programming Bug I: J2EE patterns: Double Checked Locking

双重检查锁定失效问题,一直是JMM无法避免的缺陷之一.了解DCL失效问题, 可以帮助我们深入JMM运行原理
要展示DCL失效问题, 首先要理解一个重要概念-延迟加载(lazy loading).
非单例的单线程延迟加载示例:
class Foo 
{
private Resource res = null;
public Resource getResource() 
{
    // 普通的延迟加载
if (res == null) 
        res = new Resource(); 
return res;
}
}

非单例的多线程延迟加载示例:
Class Foo 
{
Private Resource res = null;
Public synchronized Resource getResource()
{
      // 获取实例操作使用同步方式, 性能不高
If (res == null) res = new Resource();
return res;
}
}

非单例的DCL多线程延迟加载示例:
Class Foo 
{
Private Resource res = null;
Public Resource getResource() 
{
If (res == null)
{
       //只有在第一次初始化时,才使用同步方式.
synchronized(this)
{
if(res == null)
{
res = new Resource();
}
}
}
return res;
}
}

Double-Checked Locking看起来是非常完美的。但是很遗憾，根据Java的语言规范，上面的代码是不可靠的。

出现上述问题, 最重要的2个原因如下:
1, 编译器优化了程序指令, 以加快cpu处理速度.
2, 多核cpu动态调整指令顺序, 以加快并行运算能力.

问题出现的顺序:
1, 线程A, 发现对象未实例化, 准备开始实例化
2, 由于编译器优化了程序指令, 允许对象在构造函数未调用完前, 将共享变量的引用指向部分构造的对象, 虽然对象未完全实例化, 但已经不为null了.
3, 线程B, 发现部分构造的对象已不是null, 则直接返回了该对象.

不过, 一些著名的开源框架, 包括jive,lenya等也都在使用DCL模式, 且未见一些极端异常.
说明, DCL失效问题的出现率还是比较低的.
接下来就是性能与稳定之间的选择了?

DCL的替代Initialize-On-Demand:

public class Foo {
    // 似有静态内部类, 只有当有引用时, 该类才会被装载
    private static class LazyFoo {
       public static Foo foo = new Foo();
    }

    public static Foo getInstance() {
       return LazyFoo.foo;
    }
}

维基百科的DCL解释: http://en.wikipedia.org/wiki/Double-checked_locking

J2EE patterns: Double Checked Locking Solution by XXX
Background.

http://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html

Introduction.

In a highly concurrent application much time can be spent in acquiring locks.

Examples.

In many cases objects which need to be created are only known at runtime.

Case 1: You might want to store objects by name in a local cache. In a multithread environment it can be inefficient to synchronize on a local table which might store objects by name.

Case 2: In some cases it might be necessary to initialize variables lazily at runtime. In a multithreaded environment this would need to be synchronized.

Synchronization in a highly concurrent system can have a high cost in time. Removing non required synchronization can improve performance dramatically.

The original idea, which is incorrect.

public Object getObject() {
    if (object == null)
        synchronized(this) {
            if (object == null)
                object = new String("my object");
            }
            return object;
        }
    }
}


Proposed Solutions and Patterns below

```java
import java.util.HashMap;
import java.util.regex.Pattern;

abstract class OncePer {
    public final Object getObject(String arg) throws Exception {
        System.out.println(Thread.currentThread() + " entering getObject(arg: " + arg + ")");
        Object obj = doGet(arg);
        if (obj == null) {
            obj = synchronizedGetObject(arg);
        }
        return obj;
    }
    
    protected final synchronized Object synchronizedGetObject(String arg) throws Exception {
        System.out.println(Thread.currentThread() + " entering synchronizedGetObject(arg: " + arg + ")");
        Object obj = doGet(arg);
        if (obj == null) {
            obj = doCreate(arg);
        }
        return obj;
    }
    
    protected abstract Object doGet(String arg) throws Exception;
    
    protected abstract Object doCreate(String arg) throws Exception;
}

abstract class Once1Get {
    private volatile boolean todo = true;
    
    private Object obj = null;
    
    public final Object getObject() throws Exception {
        System.out.println(Thread.currentThread() + " entering getObject");
        if (todo) {
            synchronized (this) {
                if (todo) {
                    obj = doGet();
                    todo = false;
                }
            }
        }
        return obj;
    }
    
    protected abstract Object doGet() throws Exception;
}

abstract class Once2Get extends Once2 {
    private Object obj = null;
    
    public final Object getObject() throws Exception {
        System.out.println(Thread.currentThread() + " entering getObject");
        boolean first = acquire();
        if (first) {
            try {
                obj = doGet();
                release();
            } catch (Exception e) {
                e.printStackTrace();
                release(false);
                throw e;
            }
        }
        return obj;
    }
    
    protected abstract Object doGet() throws Exception;
}

abstract class Once2Block extends Once2 {
    public final void runBlock() throws Exception {
        System.out.println(Thread.currentThread() + " entering runBlock");
        boolean first = acquire();
        if (first) {
            try {
                doRun();
                release();
            } catch (Exception e) {
                e.printStackTrace();
                release(false);
                throw e;
            }
        }
    }
    
    protected abstract void doRun() throws Exception;
}

class Once2 {
    private volatile boolean todo = true;
    private volatile boolean first = true;
    
    public final boolean acquire() throws InterruptedException {
        System.out.println(Thread.currentThread() + " entering acquire");
        if (todo) {
            synchronized (this) {
                if (todo) {
                    for (;;) {
                        if (first) {
                            first = false;
                            return true;
                        } else {
                            wait();
                            if (!todo) {
                                break;
                            }
                        }
                    }
                }
            };
        }
        return false;
    }
    
    public final void release() {
        System.out.println(Thread.currentThread() + " entering release");
        release(true);
    }
    
    public final void release(boolean success) {
        System.out.println(Thread.currentThread() + " entering release(success:" + success + ")");
        if (success) {
            synchronized (this) {
                todo = false;
                notifyAll();
            }
        } else {
            synchronized (this) {
                first = true;
                notify();
            }
        }
    }
}
```

// Example test. Others removed due to length restrictions.
```java
public class Main {
    private Object oncePerObj = null;
    
    public static void main(String[] args) {
        Main main = new Main();
        main.testOncePer();
    }
    
    public void testOncePer() {
        System.out.println(Thread.currentThread() + " entering testOncePer");

        final OncePer once = new OncePer() {
            private HashMap table = new HashMap(); // This could be a WeakHashMap
            
            protected Object doGet(String arg) throws Exception {
                System.out.println(Thread.currentThread() + " entering doGet(arg: " + arg + ")");
                return table.get(arg);
            }
            
            protected Object doCreate(String arg) throws Exception {
                System.out.println(Thread.currentThread() + " entering doCreate(arg: " + arg + ")");
                Pattern pattern = Pattern.compile(arg);
                table.put(arg, pattern);
                return pattern;
            }
        };
        
        Thread th1 = new Thread(new Runnable() {
            public void run() {
                System.out.println(Thread.currentThread() + " entering run");
                try {
                    oncePerObj = (Pattern) once.getObject("[a-zA-Z0-9]+");
                    //test for matches
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }, "th1");
        
        Thread th2 = new Thread(new Runnable() {
            public void run() {
                System.out.println(Thread.currentThread() + " entering run");
                try {
                    oncePerObj = (Pattern) once.getObject("[a-zA-Z0-9]+");
                    //test for matches
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }, "th2");
        
        try {
            th1.start();
            th2.start();
            th1.join();
            th2.join();
            System.out.println(Thread.currentThread() + " oncePerObj: " + oncePerObj);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

