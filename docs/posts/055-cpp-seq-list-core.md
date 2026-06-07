---
date: 2026-06-01
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - C
  - 数据结构
---

# 顺序表核心操作

实现顺序表的初始化、插入、删除与销毁四个核心操作。原代码存在两处缺陷：`destroylist` 未释放动态内存，`listdelete` 被删元素无法回传给调用方。以下给出修正后的完整代码。

<!-- more -->

## 完整代码

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

typedef int elemtype;
typedef int status;

typedef struct
{
    elemtype * elem;
    int length;
    int listsize;
} sqlist;

status initlist(sqlist &l)
{
    l.elem = (elemtype *)malloc(LIST_INIT_SIZE * sizeof(elemtype));
    if (!l.elem) exit(OVERFLOW);
    l.length = 0;
    l.listsize = LIST_INIT_SIZE;
    return OK;
}

status listinsert(sqlist &l, int i, elemtype e)
{
    if (i < 1 || i > l.length + 1) return ERROR;
    if (l.length >= l.listsize)
    {
        elemtype * newbase = (elemtype *)realloc(l.elem,
            (l.listsize + LISTINCREMENT) * sizeof(elemtype));
        if (!newbase) exit(OVERFLOW);
        l.elem = newbase;
        l.listsize += LISTINCREMENT;
    }
    elemtype * q = &(l.elem[i - 1]);
    for (elemtype * p = &(l.elem[l.length - 1]); p >= q; --p)
        *(p + 1) = *p;
    *q = e;
    ++l.length;
    return OK;
}

status listdelete(sqlist &l, int i, elemtype &e)         // 修正：参数改为引用，调用方可获取被删元素
{
    if (i < 1 || i > l.length) return ERROR;
    elemtype * p = &(l.elem[i - 1]);
    e = *p;
    elemtype * q = l.elem + l.length - 1;
    for (++p; p <= q; ++p) *(p - 1) = *p;
    --l.length;
    return OK;
}

status destroylist(sqlist &l)
{
    free(l.elem);                                        // 修正：先释放动态分配的内存，再置零结构体
    memset(&l, 0, sizeof(l));
    return OK;
}

int main()
{
    sqlist L;
    initlist(L);
    listinsert(L, 1, 1);
    listinsert(L, 2, 2);
    listinsert(L, 3, 3);
    listinsert(L, 4, 4);
    for (int i = 0; i < L.length; i++)
        printf("%d ", L.elem[i]);
    printf("\n");

    elemtype deleted;                                    // 新增：接收被删元素
    listdelete(L, 2, deleted);
    printf("删除: %d\n", deleted);
    for (int i = 0; i < L.length; i++)
        printf("%d ", L.elem[i]);

    destroylist(L);
    return 0;
}
```

`initlist` 分配初始容量为 `LIST_INIT_SIZE` 的存储空间。`listinsert` 在指定位置插入元素，若容量不足则通过 `realloc` 扩容。`listdelete` 将 `e` 改为引用传参，调用方可获取被删元素的值。`destroylist` 修正后先 `free` 再 `memset`，避免内存泄漏。
