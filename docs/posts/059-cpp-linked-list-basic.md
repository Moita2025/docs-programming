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

# 简单线性链表

一个轻量级的整数线性链表实现，提供头插法建表、指定位置插入与删除、数组批量导入等功能。

原代码存在三处缺陷：`listinsert` 分配结点后未链入链表；`listdelete` 分配了无用结点造成内存泄漏，且被删元素无法回传；两函数的位置越界判断有误。以下给出修正后代码。

<!-- more -->

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASIBLE -1
#define OVERFLOW -2

#define INTARRLEN(a) (sizeof(a)/sizeof(int))

typedef int elemtype;
typedef int status;

typedef struct lnode
{
    elemtype data;
    struct lnode * next;
} lnode, * linklist;

status listcreate(linklist &l, int n)
{
    l = (linklist)malloc(sizeof(lnode));
    l->next = NULL;
    for (int i = 0; i < n; i++)
    {
        linklist p = (linklist)malloc(sizeof(lnode));
        scanf("%d", &p->data);
        p->next = l->next;
        l->next = p;
    }
    return OK;
}

status listinsert(linklist &l, int i, elemtype e)
{
    linklist p = l;
    int j = 0;
    while (p && j < i - 1) { p = p->next; ++j; }
    if (!p || j > i - 1) return ERROR;                   // 修正：越界条件改为 j > i-1
    linklist s = (linklist)malloc(sizeof(lnode));
    s->data = e;
    s->next = p->next;
    p->next = s;                                         // 修正：将新结点链入链表
    return OK;
}

status listdelete(linklist &l, int i, elemtype &e)       // 修正：参数改为引用
{
    linklist p = l;
    int j = 0;
    while (p->next && j < i - 1) { p = p->next; ++j; }
    if (!(p->next) || j > i - 1) return ERROR;
    lnode * q = p->next;                                 // 修正：去掉无用 malloc
    p->next = q->next;
    e = q->data;
    free(q);
    return OK;
}

status printlist(linklist &l)
{
    lnode * templ = l;
    templ = templ->next;
    while (templ)
    {
        printf("%d ", templ->data);
        templ = templ->next;
    }
    printf("\n");                                        // 新增：输出换行
    return OK;                                           // 新增：补充返回值
}

status arraylist(linklist &l, elemtype arr[], int n)
{
    l = (linklist)malloc(sizeof(lnode));
    l->next = NULL;
    for (int i = 0; i < n; i++)
    {
        linklist p = (linklist)malloc(sizeof(lnode));
        p->data = arr[i];
        p->next = l->next;
        l->next = p;
    }
    return OK;
}

int main()
{
    linklist L;
    int a[] = {1, 2, 5, 6245, 232, 514, 124, 2, 22};
    arraylist(L, a, INTARRLEN(a));
    printlist(L);

    elemtype deleted;                                    // 新增：接收被删元素
    listdelete(L, 3, deleted);
    printf("删除第 3 个元素: %d\n", deleted);
    printlist(L);

    listinsert(L, 2, 999);
    printf("在第 2 位插入 999:\n");
    printlist(L);

    return 0;
}
```

`listcreate` 和 `arraylist` 均使用头插法，每次新结点插在头结点之后，因此数组元素的存储顺序与输入顺序相反。`listinsert` 修正后将 `s` 正确链入；`listdelete` 改为引用传参并去除了多余的 `malloc` 调用。位置越界判断统一使用 `j > i - 1` 逻辑。
