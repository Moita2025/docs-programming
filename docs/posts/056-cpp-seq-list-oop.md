---
date: 2026-06-01
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数据结构
  - 面向对象
---

# 顺序表面向对象封装

将顺序表的核心操作用 C++ 类进行封装，构造函数处理初始化与数组批量导入，析构函数自动回收内存。

原代码的析构函数与 `destroy` 方法均直接用 `memset` 置零对象，忘记先释放 `elem` 指向的动态内存。

<!-- more -->

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASIBLE -1
#define OVERFLOW -2

#define LIST_INIT_SIZE 100
#define LISTINCREMENT 10

#define ARRLEN(a) (sizeof(a)/sizeof(a[0]))

typedef int elemtype;
typedef int status;

class sqlist
{
public:
    elemtype * elem;
    int length;
    int listsize;
    sqlist();
    sqlist(int arr[], int len);
    ~sqlist();                                           // 修正：析构函数声明移至类外实现
    status insert(int i, elemtype e);
    status excise(int i, elemtype e);
    status destroy();
    status sort();
    status append(elemtype e);
    status print();
};

sqlist::sqlist()
{
    elem = (elemtype *)malloc(LIST_INIT_SIZE * sizeof(elemtype));
    if (!elem) exit(OVERFLOW);
    length = 0;
    listsize = LIST_INIT_SIZE;
}

sqlist::sqlist(int arr[], int len)
{
    elem = (elemtype *)malloc(LIST_INIT_SIZE * sizeof(elemtype));
    if (!elem) exit(OVERFLOW);
    length = 0;
    listsize = LIST_INIT_SIZE;

    for (int i = 0; i < len; i++)                        // 修正：去掉 always-0 的 originallen
        append(arr[i]);
}

sqlist::~sqlist()
{
    free(elem);                                          // 修正：先释放动态内存再置零
    memset(this, 0, sizeof(*this));
}

status sqlist::insert(int i, elemtype e)
{
    if (i < 1 || i > length + 1) return ERROR;
    if (length >= listsize)
    {
        elemtype * newbase = (elemtype *)realloc(elem,
            (listsize + LISTINCREMENT) * sizeof(elemtype));
        if (!newbase) exit(OVERFLOW);
        elem = newbase;
        listsize += LISTINCREMENT;
    }
    elemtype * q = &(elem[i - 1]);
    for (elemtype * p = &(elem[length - 1]); p >= q; --p)
        *(p + 1) = *p;
    *q = e;
    ++length;
    return OK;
}

status sqlist::excise(int i, elemtype e)
{
    if (i < 1 || i > length) return ERROR;
    elemtype * p = &(elem[i - 1]);
    e = *p;
    elemtype * q = elem + length - 1;
    for (++p; p <= q; ++p) *(p - 1) = *p;
    --length;
    return OK;
}

status sqlist::destroy()
{
    free(elem);                                          // 修正：先释放动态内存
    memset(this, 0, sizeof(*this));
    return OK;
}

status sqlist::sort()
{
    for (int i = 1; i < length; i++)
        for (int j = length - 1; j >= i; j--)
            if (elem[j] < elem[j - 1])
            {
                int iTemp = elem[j - 1];
                elem[j - 1] = elem[j];
                elem[j] = iTemp;
            }
    return OK;
}

status sqlist::append(elemtype e)
{
    if (insert(length + 1, e) == OK)
        return OK;
    return ERROR;                                        // 修正：补充失败时的返回值
}

status sqlist::print()
{
    for (int i = 0; i < length; i++)
        printf("%d ", elem[i]);
    printf("\n");
    return OK;
}

int main()
{
    int a[] = {1, 2, 3, 4, 5};
    sqlist L = sqlist(a, ARRLEN(a));
    L.print();
    L.append(79);
    L.append(15);
    L.print();
    return 0;
}
```

相比 C 风格实现，OOP 版将 `initlist` 逻辑移入构造函数，支持数组批量构造；`destroy` 和析构函数均先 `free(elem)` 再 `memset` 置零。`append` 内部复用 `insert`，补充了 `ERROR` 返回值。
