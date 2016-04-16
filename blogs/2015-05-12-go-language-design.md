---
layout: post
category : programming
tags : [develop,internet]
title: Go Language Design Note
---

Go语言编程笔记
------------------------

### Go使用规则

1. Compile go files to .a file according to package name
2. 协程与channel, goruntine
3. reflect 反射
4. 支持多个返回值
5. pointer /array/slice/map/chan/struct/interface
6. go run: cannot run non-main package
7. :=用于明确表达同时进行变量声明和初始化的工作 <br />

> var v1 int = 10
> v1 = 10
> Equals
> v1:=10

出现在:=左侧的变量不应该是已经被声明过的,否则会导致编译错误
```Go
(var i int 
i := 2
```
会导致类似如下的编译错误: <br/>
no new variables on left side of :=)

value:=&Person{} <br />

8. 多重赋值功能 <br />
i, j = j, i <br />
9. Go有两种创建数据结构的方法 <br />

> new和make <br />
> new返回指针 / make返回初始化后的(非零)值 <br />
> new返回一个指向初始化为全0值的 指针，而make返回一个复杂的结构。<br />
> 基础的区别在于，new(T)返回一个*T类型，一个可以被隐性反向引用的指针（如图中的黑色指 针），而make(T,args)

返回一个原始的T，它并不是一个指针。T中常有写隐性的指针（如图中的灰色指针）

10. 在Go中字符串是不可变的 <br />
可变字符串需赋值 s := "hello"

12. array、slice、map <br />
```Go
var myArray [10]int = [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10} 
var mySlice []int = myArray[:5]

mySlice1 := make([]int, 5)

for i, v := range mySlice { 
fmt.Println("mySlice[", i, "] =", v)
}
```

Slice支持Go语言内置的cap()/len()/append()/copy()
```Go
    var myMap map[string] PersonInfo
    myMap = make(map[string] PersonInfo)
    delete()
    find方式：
    value, ok := myMap["key"] 
    if ok {// 找到了
    // 处理找到的value 
    }
```

13. Go内置有一个error类型

```Go
    type error interface 
    { Error() string
    }
    err := errors.New("emit macho dwarf: elf header corrupted")
    if err != nil {
        fmt.Print(err)
    }
```

14. panic()和recover() <br />
15. Go类型都是基于值传递的。要想修改变量的值,只能传递指针。<br />

- slice:指向数组(array)的一个区间。
- map:极其常见的数据结构,提供键值查询能力。
- channel:执行体(goroutine)间的通信设施。
- interface:对一组满足某个契约的类型的抽象




