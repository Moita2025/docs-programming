---
date: 2026-05-31
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数据结构
---

# C++ 三元组数据结构

三元组（triplet）是一种只包含三个元素的基础数据结构。下面这份 C++ 代码用动态内存分配实现三元组，并提供了初始化、销毁、取值、赋值、判断升降序、取最值等操作。

<!-- more -->

## 完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define OK 1
#define ERROR 0

typedef int type;
typedef int status;
typedef type * triplet;

status inittriplet(triplet &t, type v1, type v2, type v3);
status destroytriplet(triplet &t);
status get(triplet t, int i, type &e);
status put(triplet &t, int i, type e);
status isascending(triplet t);
status isdescending(triplet t);
status max(triplet t, type &e);
status min(triplet t, type &e);

status inittriplet(triplet &t, type v1, type v2, type v3)
{
    t = (type *)malloc(3 * sizeof(type));
    if (!t) exit(0);
    t[0] = v1, t[1] = v2, t[2] = v3;
    return OK;
}

status destroytriplet(triplet &t)
{
    free(t);
    t = NULL;
    return OK;
}

status get(triplet t, int i, type &e)
{
    if (i < 1 || i > 3) return ERROR;
    e = t[i - 1];
    return OK;
}

status put(triplet &t, int i, type e)
{
    if (i < 1 || i > 3) return ERROR;
    t[i - 1] = e;
    return OK;
}

status isascending(triplet t)
{
    return (t[0] <= t[1]) && (t[1] <= t[2]);
}

status isdescending(triplet t)
{
    return (t[0] >= t[1]) && (t[1] >= t[2]);
}

status max(triplet t, type &e)
{
    e = (t[0] >= t[1])
        ? ((t[0] >= t[2]) ? t[0] : t[2])
        : ((t[1] >= t[2]) ? t[1] : t[2]);
    return OK;
}

status min(triplet t, type &e)
{
    e = (t[0] <= t[1])
        ? ((t[0] <= t[2]) ? t[0] : t[2])
        : ((t[1] <= t[2]) ? t[1] : t[2]);
    return OK;
}

int main()
{
    triplet tt;
    int a;

    inittriplet(tt, 100, 2122, 32);
    printf("三元组初始设定为：%d %d %d\n", tt[0], tt[1], tt[2]);

    get(tt, 3, a);
    printf("三元组的第三个元素为：%d\n", a);

    put(tt, 3, 54);
    get(tt, 3, a);
    printf("修改三元组的第三个元素为：%d\n", a);

    max(tt, a);
    printf("三元组中最大元素为：%d\n", a);

    min(tt, a);
    printf("三元组中最小元素为：%d\n", a);

    char ch;
    ch = (isascending(tt) == 1) ? ('1') : ('0');
    printf("三元组是否升序%c\n", ch);

    ch = (isdescending(tt) == 1) ? ('1') : ('0');
    printf("三元组是否降序%c\n", ch);

    destroytriplet(tt);
    return 0;
}
```

## 代码分析

### 类型定义

```cpp
typedef int type;      // 元素类型
typedef int status;    // 函数返回状态
typedef type * triplet;  // 三元组指针
```

`triplet` 本质是 `int*`，指向堆上的 3 个 `int`。状态返回值用 `OK`(1) 和 `ERROR`(0) 宏区分成功与失败。

### 核心操作

**初始化**：`malloc` 分配 3 个 `int` 的空间，逐个赋值。失败时直接 `exit(0)` 终止程序：

```cpp
t = (type *)malloc(3 * sizeof(type));
if (!t) exit(0);
t[0] = v1, t[1] = v2, t[2] = v3;
```

**销毁**：`free` 后立即将指针置为 NULL，防止调用方持有悬空指针：

```cpp
free(t);
t = NULL;
```

注意参数 `triplet &t` 是引用传参，所以 `t = NULL` 会同步修改调用方的指针变量。

**存取元素**：`get` 和 `put` 都用 1-based 索引，访问时转为 0-based。边界检查 `i < 1 || i > 3` 防止越界：

```cpp
if (i < 1 || i > 3) return ERROR;
e = t[i - 1];
```

**判断升降序**：`isascending` 返回 `(t[0] <= t[1]) && (t[1] <= t[2])`。注意使用的是 `<=` 而非 `<`，所以相等序列也被视为合法升序。降序同理。

**取最值**：用嵌套三元运算符逐对比大小，三元素只需两轮比较：

```cpp
e = (t[0] >= t[1])
    ? ((t[0] >= t[2]) ? t[0] : t[2])
    : ((t[1] >= t[2]) ? t[1] : t[2]);
```

### 主函数调用流程

```text
init(100, 2122, 32)  →  {100, 2122, 32}
get(3)               →  32
put(3, 54)           →  {100, 2122, 54}
max                  →  2122
min                  →  54
isascending          →  0 (否)
isdescending         →  0 (否)
destroy              →  释放内存
```

## 值得注意的问题

### NULL 指针未做防护

`get`、`isascending`、`isdescending`、`max`、`min` 都直接解引用 `t`，没有检查 `t == NULL`。如果在 `destroytriplet` 之后调用这些函数会直接崩溃。

建议在访问前增加空指针检查：

```cpp
status get(triplet t, int i, type &e)
{
    if (!t) return ERROR;  // 新增
    if (i < 1 || i > 3) return ERROR;
    e = t[i - 1];
    return OK;
}
```

### 重复初始化的内存泄漏

如果对同一个 `triplet` 变量两次调用 `inittriplet` 而中间没有 `destroytriplet`，第一次分配的堆内存就会泄漏。可以在 `inittriplet` 开头加上防御：

```cpp
if (t) free(t);  // 先释放旧内存
```

### C 风格内存管理混用 C++ 引用

`malloc` / `free` 是 C 的内存管理方式，而 `&` 引用是 C++ 语法。这种混用在教学代码中可以接受，但在实际项目中建议统一风格：纯 C 用指针和二级指针，纯 C++ 用 `new` / `delete` 或直接使用 `std::array<int, 3>`。

将 `typedef type * triplet` 改为 `std::array<type, 3>` 可以彻底避免上述所有内存管理问题，但作为练习理解指针操作仍有其价值。
