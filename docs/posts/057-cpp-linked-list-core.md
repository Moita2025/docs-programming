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

# 线性链表基础操作

从多项式运算场景中抽取出通用的线性链表操作层，包含初始化、结点分配、首结点插入/删除、清空、追加、销毁等基础功能。

<!-- more -->

链表采用头尾指针 + 长度计数的结构体管理，便于多项式等场景中快速定位表尾。

## 完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASIBLE -1
#define OVERFLOW -2

typedef struct
{
    float coef;
    int expn;
} term, elemtype;

typedef struct lnode
{
    elemtype data;
    struct lnode *next;
} lnode, *link, *position;

typedef struct
{
    link head, tail;
    int len;
} linklist;

typedef linklist polynomial;
typedef int status;

status InitList(linklist *L)
{
    link p;
    p = (link)malloc(sizeof(lnode));
    if (p)
    {
        p->next = NULL;
        (*L).head = (*L).tail = p;
        (*L).len = 0;
        return OK;
    }
    else
        return ERROR;
}

status MakeNode(link *p, elemtype e)
{
    (*p) = (link)malloc(sizeof(lnode));
    if (!(*p)) return ERROR;
    (*p)->data = e;
    return OK;
}

status InsFirst(linklist *L, link h, link s)
{
    s->next = h->next;
    h->next = s;
    if (h == (*L).tail)
        (*L).tail = h->next;
    (*L).len++;
    return OK;
}

status DelFirst(linklist *L, link h, link *q)
{
    if (*q)
    {
        h->next = (*q)->next;
        if (!h->next)
            (*L).tail = h;
        (*L).len--;
        return OK;
    }
    else
        return FALSE;
}

status ClearList(linklist *L)
{
    link p, q;

    if (L->head != L->tail)
    {
        p = q = L->head->next;
        L->head->next = NULL;

        while (p != L->tail)
        {
            p = q->next;
            free(q);
            q = p;
        }

        free(q);

        L->tail = L->head;
        L->len = 0;
    }
    return OK;
}

position GetHead(linklist *L)
{
    return L->head;
}

position NextPos(link p)
{
    return p->next;
}

position PriorPos(linklist L, link p)
{
    link q;
    q = L.head;

    while (q->next != p)
        q = q->next;
    return q;
}

void FreeNode(link *p)
{
    free((*p));
    (*p) = NULL;
}

status ListEmpty(linklist L)
{
    return L.len == 0;
}

elemtype GetCurElem(link p)
{
    return p->data;
}

status Append(linklist *L, link s)
{
    int i = 1;
    (*L).tail->next = s;
    while (s->next)
    {
        i++;
        s = s->next;
    }
    (*L).tail = s;
    (*L).len += i;
    return OK;
}

void DestroyPolyn(linklist *L)
{
    ClearList(L);
    FreeNode(&(*L).head);
    (*L).tail = NULL;
    (*L).len = 0;
}
```

`linklist` 结构体同时记录 `head`（头结点）、`tail`（尾结点）和 `len`（长度）。`InsFirst` 在指定结点之后插入，并自动维护 `tail`。`DelFirst` 删除指定结点之后的首个结点。`Append` 将一段链表整段拼接到尾部。`DestroyPolyn` 先清空数据结点再释放头结点。
