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

# 顺序表集合运算与扩展操作

在顺序表核心操作的基础上，追加排序、查找、归并以及集合交并差等扩展功能。

- 使用依赖：[<code>sqlist 核心操作</code>](https://moita2025.github.io/docs-programming/2026/06/01/054-cpp-seq-list-core/#完整代码)

<!-- more -->

原代码单独成篇时，核心操作（`initlist`、`listinsert`、`listdelete`、`destroylist`）与前一篇重复。通过跨页面依赖声明，本文只保留一份完整可运行的代码，避免两篇博文各自维护相同片段。

修正点：`destroylist` 补充内存释放；`listdelete` 参数改为引用；`appendlistbyarray` 修复了多余的偏移量计算；`listappend` 补充了失败时的返回值。

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

#define INTARRLEN(a) (sizeof(a)/sizeof(int))

typedef int elemtype;
typedef int status;

typedef struct
{
    elemtype * elem;
    int length;
    int listsize;
} sqlist;

// ===== 核心操作 =====

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

status listdelete(sqlist &l, int i, elemtype &e)         // 修正：参数改为引用
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
    free(l.elem);                                        // 修正：先释放内存再置零
    memset(&l, 0, sizeof(l));
    return OK;
}

// ===== 归并 =====

status listmerge(sqlist la, sqlist lb, sqlist &lc)
{
    elemtype * pa = la.elem;
    elemtype * pb = lb.elem;
    lc.listsize = lc.length = la.length + lb.length;
    elemtype * pc = lc.elem = (elemtype *)malloc(lc.listsize * sizeof(elemtype));
    if (!lc.elem) exit(OVERFLOW);
    elemtype * pa_last = la.elem + la.length - 1;
    elemtype * pb_last = lb.elem + lb.length - 1;
    while (pa <= pa_last && pb <= pb_last)
    {
        if (*pa <= *pb) *pc++ = *pa++;
        else *pc++ = *pb++;
    }
    while (pa <= pa_last) *pc++ = *pa++;
    while (pb <= pb_last) *pc++ = *pb++;
    return OK;
}

// ===== 排序与清空 =====

status listsort(sqlist &l)
{
    for (int i = 1; i < l.length; i++)
        for (int j = l.length - 1; j >= i; j--)
            if (l.elem[j] < l.elem[j - 1])
            {
                int iTemp = l.elem[j - 1];
                l.elem[j - 1] = l.elem[j];
                l.elem[j] = iTemp;
            }
    return OK;
}

status listclear(sqlist &l)
{
    if (!l.elem) exit(OVERFLOW);
    l.length = 0;
    return OK;
}

// ===== 追加与输出 =====

status listappend(sqlist &l, elemtype e)
{
    if (listinsert(l, l.length + 1, e) == OK)
        return OK;
    return ERROR;                                        // 修正：补充失败时的返回值
}

status printlist(sqlist &l)
{
    for (int i = 0; i < l.length; i++)
        printf("%d ", l.elem[i]);
    printf("\n");
    return OK;
}

status appendlistbyarray(sqlist &l, elemtype arr[], int len)
{
    for (int i = 0; i < len; i++)
        listappend(l, arr[i]);                           // 修正：去掉多余的 originlen 偏移
    return OK;
}

// ===== 查找 =====

int listcount(sqlist &l, elemtype e)
{
    int times = 0;
    for (int i = 0; i < l.length; i++)
        if (e == l.elem[i])
            times++;
    return times;
}

int listindex(sqlist &l, elemtype e)
{
    for (int i = 0; i < l.length; i++)
        if (e == l.elem[i])
            return i;
    return -1;
}

status locateelem(sqlist &l, elemtype e)
{
    for (int i = 0; i < l.length; i++)
        if (e == l.elem[i])
            return 1;
    return 0;
}

// ===== 集合运算 =====

status listintersect(sqlist &l1, sqlist &l2, sqlist &l3)
{
    for (int i = 0; i < l1.length; i++)
        for (int j = 0; j < l2.length; j++)
            if (l1.elem[i] == l2.elem[j])
                listappend(l3, l1.elem[i]);
    return OK;
}

status listunion(sqlist &l1, sqlist &l2, sqlist &l3)
{
    for (int i = 0; i < l1.length; i++)
        listappend(l3, l1.elem[i]);
    for (int i = 0; i < l2.length; i++)
        if (!locateelem(l1, l2.elem[i]))
            listappend(l3, l2.elem[i]);
    return OK;
}

status listdiffer(sqlist &l1, sqlist &l2, sqlist &l3)
{
    for (int i = 0; i < l1.length; i++)
        if (!locateelem(l2, l1.elem[i]))
            listappend(l3, l1.elem[i]);
    return OK;
}

// ===== 使用示例 =====

int main()
{
    sqlist l1, l2, l3;
    initlist(l1);
    initlist(l2);
    initlist(l3);

    int a1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int a2[] = {6, 7, 8, 9, 10, 11, 12, 13};
    appendlistbyarray(l1, a1, INTARRLEN(a1));
    appendlistbyarray(l2, a2, INTARRLEN(a2));

    printf("l1: "); printlist(l1);
    printf("l2: "); printlist(l2);

    printf("归并: ");
    listmerge(l1, l2, l3);
    printlist(l3);
    listclear(l3);

    printf("交集: ");
    listintersect(l1, l2, l3);
    printlist(l3);
    listclear(l3);

    printf("并集: ");
    listunion(l1, l2, l3);
    printlist(l3);
    listclear(l3);

    printf("差集 l1-l2: ");
    listdiffer(l1, l2, l3);
    printlist(l3);

    destroylist(l1);
    destroylist(l2);
    destroylist(l3);
    return 0;
}
```

## 操作说明

**归并** `listmerge` 将两个已排序顺序表合并为一个有序表，前提是输入已有序。

**排序** `listsort` 使用冒泡排序，每次内循环将较小值交换到数组前端。

**集合运算** 三函数均将结果追加至目标表 `l3`，调用前需先初始化 `l3`。并集和差集依赖 `locateelem` 判断元素是否已在另一表中。
