---
layout: post
category : programming
tags : [develop,java]
title: Java Lock-free Programming Note
---

Java多线程与并发 - Lock-free无锁编程
------------------------

无锁编程 / lock-free / 非阻塞同步

无锁编程，即不使用锁的情况下实现多线程之间的变量同步，也就是在没有线程被阻塞的情况下实现变量的同步，所以也叫非阻塞同步（Non-blocking Synchronization）。
实现非阻塞同步的方案称为“无锁编程算法”（ Non-blocking algorithm）。
lock-free是目前最常见的无锁编程的实现级别（一共三种级别）。

为什么要 Non-blocking sync ？

使用lock实现线程同步有很多缺点：
* 产生竞争时，线程被阻塞等待，无法做到线程实时响应。
* dead lock。
* live lock。
* 优先级翻转。
* 使用不当，造成性能下降。

如果在不使用 lock 的情况下，实现变量同步，那就会避免很多问题。虽然目前来看，无锁编程并不能替代 lock。

实现级别

非同步阻塞的实现可以分成三个级别：wait-free/lock-free/obstruction-free。

wait-free
是最理想的模式，整个操作保证每个线程在有限步骤下完成。
保证系统级吞吐（system-wide throughput）以及无线程饥饿。
截止2011年，没有多少具体的实现。即使实现了，也需要依赖于具体CPU。

lock-free
允许个别线程饥饿，但保证系统级吞吐。
确保至少有一个线程能够继续执行。
wait-free的算法必定也是lock-free的。

obstruction-free
在任何时间点，一个线程被隔离为一个事务进行执行（其他线程suspended），并且在有限步骤内完成。在执行过程中，一旦发现数据被修改（采用时间戳、版本号），则回滚。
也叫做乐观锁，即乐观并发控制(OOC)。事务的过程是：1读取，并写时间戳；2准备写入，版本校验；3校验通过则写入，校验不通过，则回滚。
lock-free必定是obstruction-free的。

CAS原语

LL/SC, atom read-modify-write
如果CPU提供了Load-Link/Store-Conditional（LL/SC）这对指令，则就可以轻松实现变量的CPU级别无锁同步。
LL [addr],dst：从内存[addr]处读取值到dst。
SC value,[addr]：对于当前线程，自从上次的LL动作后内存值没有改变，就更新成新值。
上述过程就是实现lock-free的 read-modify-write 的原子操作。

CAS （Compare-And-Swap）
LL/SC这对CPU指令没有实现，那么就需要寻找其他算法，比如CAS。
CAS是一组原语指令，用来实现多线程下的变量同步。
在 x86 下的指令CMPXCHG实现了CAS，前置LOCK既可以达到原子性操作。截止2013，大部分多核处理器均支持CAS。
CAS操作系统同步原语有三个参数，内存地址，期望值，新值。如果内存地址的值==期望值，表示该值未修改，此时可以修改成新值。否则表示修改失败，返回false，由用户决定后续操作。


Bool CAS(T* addr, T expected, T newValue)
{
      if( *addr == expected )
    {
          *addr =  newValue;
          return true;
    }
    else
          return false;
}





ABA 问题
thread1意图对val=1进行操作变成2，cas(*val,1,2)。
thread1先读取val=1；thread1被抢占（preempted），让thread2运行。
thread2 修改val=3，又修改回1。
thread1继续执行，发现期望值与“原值”（其实被修改过了）相同，完成CAS操作。

使用CAS会造成ABA问题，特别是在使用指针操作一些并发数据结构时。

解决方案
ABAʹ：添加额外的标记用来指示是否被修改。

语言实现

Java demo
AtomicInteger atom = new AtomicInteger(1);
boolean r = atom.compareAndSet(1, 2);

C# demo
int i=1;
Interlocked.Increment(ref i);

CAS原理

 CAS通过调用JNI的代码实现的。JNI:Java Native Interface为JAVA本地调用，允许java调用其他语言。

而compareAndSwapInt就是借助C来调用CPU底层指令实现的。

下面从分析比较常用的CPU（intel x86）来解释CAS的实现原理。

 下面是sun.misc.Unsafe类的compareAndSwapInt()方法的源代码：


public final native boolean compareAndSwapInt(Object o, long offset,
                                              int expected,
                                              int x);




可以看到这是个本地方法调用。这个本地方法在openjdk中依次调用的c++代码为：unsafe.cpp，atomic.cpp和atomicwindowsx86.inline.hpp。这个本地方法的最终实现在openjdk的如下位置：openjdk-7-fcs-src-b147-27jun2011\openjdk\hotspot\src\oscpu\windowsx86\vm\ atomicwindowsx86.inline.hpp（对应于windows操作系统，X86处理器）。下面是对应于intel x86处理器的源代码的片段：



// Adding a lock prefix to an instruction on MP machine
// VC++ doesn't like the lock prefix to be on a single line
// so we can't insert a label after the lock prefix.
// By emitting a lock prefix, we can define a label after it.
#define LOCK_IF_MP(mp) __asm cmp mp, 0  \
                      __asm je L0      \
                      __asm _emit 0xF0 \
                      __asm L0:

inline jint    Atomic::cmpxchg    (jint    exchange_value, volatile jint*    dest, jint    compare_value) {
  // alternative for InterlockedCompareExchange
  int mp = os::is_MP();
  __asm {
    mov edx, dest
    mov ecx, exchange_value
    mov eax, compare_value
    LOCK_IF_MP(mp)
    cmpxchg dword ptr [edx], ecx
  }
}





如上面源代码所示，程序会根据当前处理器的类型来决定是否为cmpxchg指令添加lock前缀。如果程序是在多处理器上运行，就为cmpxchg指令加上lock前缀（lock cmpxchg）。反之，如果程序是在单处理器上运行，就省略lock前缀（单处理器自身会维护单处理器内的顺序一致性，不需要lock前缀提供的内存屏障效果）。


 intel的手册对lock前缀的说明如下：

- 确保对内存的读-改-写操作原子执行。在Pentium及Pentium之前的处理器中，带有lock前缀的指令在执行期间会锁住总线，使得其他处理器暂时无法通过总线访问内存。很显然，这会带来昂贵的开销。从Pentium 4，Intel Xeon及P6处理器开始，intel在原有总线锁的基础上做了一个很有意义的优化：如果要访问的内存区域（area of memory）在lock前缀指令执行期间已经在处理器内部的缓存中被锁定（即包含该内存区域的缓存行当前处于独占或以修改状态），并且该内存区域被完全包含在单个缓存行（cache line）中，那么处理器将直接执行该指令。由于在指令执行期间该缓存行会一直被锁定，其它处理器无法读/写该指令要访问的内存区域，因此能保证指令执行的原子性。这个操作过程叫做缓存锁定（cache locking），缓存锁定将大大降低lock前缀指令的执行开销，但是当多处理器之间的竞争程度很高或者指令访问的内存地址未对齐时，仍然会锁住总线。
- 禁止该指令与之前和之后的读和写指令重排序。
- 把写缓冲区中的所有数据刷新到内存中。

备注知识：

关于CPU的锁有如下3种：

　　3.1 处理器自动保证基本内存操作的原子性

　　首先处理器会自动保证基本的内存操作的原子性。处理器保证从系统内存当中读取或者写入一个字节是原子的，意思是当一个处理器读取一个字节时，其他处理器不能访问这个字节的内存地址。奔腾6和最新的处理器能自动保证单处理器对同一个缓存行里进行16/32/64位的操作是原子的，但是复杂的内存操作处理器不能自动保证其原子性，比如跨总线宽度，跨多个缓存行，跨页表的访问。但是处理器提供总线锁定和缓存锁定两个机制来保证复杂内存操作的原子性。

　　3.2 使用总线锁保证原子性

　　第一个机制是通过总线锁保证原子性。如果多个处理器同时对共享变量进行读改写（i++就是经典的读改写操作）操作，那么共享变量就会被多个处理器同时进行操作，这样读改写操作就不是原子的，操作完之后共享变量的值会和期望的不一致，举个例子：如果i=1,我们进行两次i++操作，我们期望的结果是3，但是有可能结果是2。如下图



　　原因是有可能多个处理器同时从各自的缓存中读取变量i，分别进行加一操作，然后分别写入系统内存当中。那么想要保证读改写共享变量的操作是原子的，就必须保证CPU1读改写共享变量的时候，CPU2不能操作缓存了该共享变量内存地址的缓存。

　　处理器使用总线锁就是来解决这个问题的。所谓总线锁就是使用处理器提供的一个LOCK＃信号，当一个处理器在总线上输出此信号时，其他处理器的请求将被阻塞住,那么该处理器可以独占使用共享内存。

　　3.3 使用缓存锁保证原子性

　　第二个机制是通过缓存锁定保证原子性。在同一时刻我们只需保证对某个内存地址的操作是原子性即可，但总线锁定把CPU和内存之间通信锁住了，这使得锁定期间，其他处理器不能操作其他内存地址的数据，所以总线锁定的开销比较大，最近的处理器在某些场合下使用缓存锁定代替总线锁定来进行优化。

　　频繁使用的内存会缓存在处理器的L1，L2和L3高速缓存里，那么原子操作就可以直接在处理器内部缓存中进行，并不需要声明总线锁，在奔腾6和最近的处理器中可以使用“缓存锁定”的方式来实现复杂的原子性。所谓“缓存锁定”就是如果缓存在处理器缓存行中内存区域在LOCK操作期间被锁定，当它执行锁操作回写内存时，处理器不在总线上声言LOCK＃信号，而是修改内部的内存地址，并允许它的缓存一致性机制来保证操作的原子性，因为缓存一致性机制会阻止同时修改被两个以上处理器缓存的内存区域数据，当其他处理器回写已被锁定的缓存行的数据时会起缓存行无效，在例1中，当CPU1修改缓存行中的i时使用缓存锁定，那么CPU2就不能同时缓存了i的缓存行。

　　但是有两种情况下处理器不会使用缓存锁定。第一种情况是：当操作的数据不能被缓存在处理器内部，或操作的数据跨多个缓存行（cache line），则处理器会调用总线锁定。第二种情况是：有些处理器不支持缓存锁定。对于Inter486和奔腾处理器,就算锁定的内存区域在处理器的缓存行中也会调用总线锁定。

　　以上两个机制我们可以通过Inter处理器提供了很多LOCK前缀的指令来实现。比如位测试和修改指令BTS，BTR，BTC，交换指令XADD，CMPXCHG和其他一些操作数和逻辑指令，比如ADD（加），OR（或）等，被这些指令操作的内存区域就会加锁，导致其他处理器不能同时访问它。


CAS缺点

 CAS虽然很高效的解决原子操作，但是CAS仍然存在三大问题。ABA问题，循环时间长开销大和只能保证一个共享变量的原子操作

1.  ABA问题。因为CAS需要在操作值的时候检查下值有没有发生变化，如果没有发生变化则更新，但是如果一个值原来是A，变成了B，又变成了A，那么使用CAS进行检查时会发现它的值没有发生变化，但是实际上却变化了。ABA问题的解决思路就是使用版本号。在变量前面追加上版本号，每次变量更新的时候把版本号加一，那么A－B－A 就会变成1A-2B－3A。

从Java1.5开始JDK的atomic包里提供了一个类AtomicStampedReference来解决ABA问题。这个类的compareAndSet方法作用是首先检查当前引用是否等于预期引用，并且当前标志是否等于预期标志，如果全部相等，则以原子方式将该引用和该标志的值设置为给定的更新值。

关于ABA问题参考文档: http://blog.hesey.net/2011/09/resolve-aba-by-atomicstampedreference.html

2. 循环时间长开销大。自旋CAS如果长时间不成功，会给CPU带来非常大的执行开销。如果JVM能支持处理器提供的pause指令那么效率会有一定的提升，pause指令有两个作用，第一它可以延迟流水线执行指令（de-pipeline）,使CPU不会消耗过多的执行资源，延迟的时间取决于具体实现的版本，在一些处理器上延迟时间是零。第二它可以避免在退出循环的时候因内存顺序冲突（memory order violation）而引起CPU流水线被清空（CPU pipeline flush），从而提高CPU的执行效率。

3. 只能保证一个共享变量的原子操作。当对一个共享变量执行操作时，我们可以使用循环CAS的方式来保证原子操作，但是对多个共享变量操作时，循环CAS就无法保证操作的原子性，这个时候就可以用锁，或者有一个取巧的办法，就是把多个共享变量合并成一个共享变量来操作。比如有两个共享变量i＝2,j=a，合并一下ij=2a，然后用CAS来操作ij。从Java1.5开始JDK提供了AtomicReference类来保证引用对象之间的原子性，你可以把多个变量放在一个对象里来进行CAS操作。

Java 轻量级锁原理详解(Lightweight Locking)

大家知道，Java的多线程安全是基于Lock机制实现的，而Lock的性能往往不如人意。

原因是，monitorenter与monitorexit这两个控制多线程同步的bytecode原语，是JVM依赖操作系统互斥(mutex)来实现的。

互斥是一种会导致线程挂起，并在较短的时间内又需要重新调度回原线程的，较为消耗资源的操作。

为了优化Java的Lock机制，从Java6开始引入了轻量级锁的概念。

轻量级锁（Lightweight Locking）本意是为了减少多线程进入互斥的几率，并不是要替代互斥。

它利用了CPU原语Compare-And-Swap(CAS，汇编指令CMPXCHG)，尝试在进入互斥前，进行补救。

本文将详细介绍JVM如何利用CAS，实现轻量级锁。

原理详解Java Object Model中定义，Object Header是一个2字（1 word = 4 byte）长度的存储区域。

第一个字长度的区域用来标记同步，GC以及hash code等，官方称之为 mark word。第二个字长度的区域是指向到对象的Class。

在2个word中，mark word是轻量级锁实现的关键。它的结构见下表

从表中可以看到，state为lightweight locked的那行即为轻量级锁标记。bitfieds名为指向lock record的指针，这里的lock record，其实是一块分配在线程堆栈上的空间区域。

用于CAS前，拷贝object上的mark word(为什么要拷贝，请看下文)。

第三项是重量级锁标记。后面的状态单词很有趣，inflated，译为膨胀，在这里意思其实是锁已升级到OS-level。

在本文的范围内，我们只关注第二和第三项即可。

为了能直观的理解lock，unlock与mark word之间的联系，我画了一张流程图：

在图中，提到了拷贝object mark word，由于脱离了原始mark word，官方将它冠以displaced前缀，即displaced mark word(置换标记字)。

这个displaced mark word是整个轻量级锁实现的关键，在CAS中的compare就需要用它作为条件。

为什么要拷贝mark word？
其实很简单，原因是为了不想在lock与unlock这种底层操作上再加同步。

在拷贝完object mark word之后，JVM做了一步交换指针的操作，即流程中第一个橙色矩形框内容所述。

将object mark word里的轻量级锁指针指向lock record所在的stack指针，作用是让其他线程知道，该object monitor已被占用。

lock record里的owner指针指向object mark word的作用是为了在接下里的运行过程中，识别哪个对象被锁住了。

下图直观地描述了交换指针的操作。

最后一步unlock中，我们发现，JVM同样使用了CAS来验证object mark word在持有锁到释放锁之间，有无被其他线程访问。

如果其他线程在持有锁这段时间里，尝试获取过锁，则可能自身被挂起，而mark word的重量级锁指针也会被相应修改。

此时，unlock后就需要唤醒被挂起的线程。