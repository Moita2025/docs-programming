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

# 线性链表 一元多项式相加与相乘

基于线性链表基础操作，实现一元多项式的创建、输出、加法、减法与乘法。

- 使用依赖：[<code>linklist 链表基础操作</code>](https://moita2025.github.io/docs-programming/2026/06/01/058-cpp-linked-list-core/#完整代码)

<!-- more -->

多项式以链表存储，每个结点包含系数 `coef` 和指数 `expn`，按指数升序排列。`LocateElem` 利用升序特性快速定位插入位置；`OrderInsert` 在插入时自动合并同类项。

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

// ===== 链表基础操作 =====

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

// ===== 多项式操作 =====

int cmp(term e1, term e2)
{
    if (e1.expn == e2.expn) return 0;
    if (e1.expn < e2.expn) return -1;
    return 1;
}

status LocateElem(linklist L, elemtype e, position *q,
                  int (*compare)(elemtype, elemtype))
{
    link p, pp;
    p = L.head;
    do
    {
        pp = p;
        p = p->next;
    } while (p && compare(p->data, e) < 0);

    if (!p || compare(p->data, e) > 0)
    {
        (*q) = pp;
        return FALSE;
    }
    else
    {
        (*q) = p;
        return TRUE;
    }
}

status OrderInsert(linklist *L, elemtype e,
                   int (*compare)(elemtype, elemtype))
{
    position q, s;
    if (LocateElem(*L, e, &q, compare))
    {
        q->data.coef += e.coef;

        if (!q->data.coef)
        {
            s = PriorPos(*L, q);
            if (!s)
                s = L->head;
            DelFirst(L, s, &q);
            FreeNode(&q);
        }
        return OK;
    }
    else
    {
        if (MakeNode(&s, e))
        {
            InsFirst(L, q, s);
            return OK;
        }
        return ERROR;
    }
}

void CreatePolyn(polynomial *P, int m)
{
    position q, s;
    int i;
    term e;

    InitList(P);

    printf("输入%d个系数和指数：\n", m);
    for (i = 1; i <= m; i++)
    {
        scanf("%f %d", &e.coef, &e.expn);
        if (!LocateElem(*P, e, &q, cmp))
        {
            if (MakeNode(&s, e))
                InsFirst(P, q, s);
        }
    }
}

void PrintPoly(link L)
{
    if (L->data.expn == 0)
    {
        printf("%.0f", L->data.coef);
    }
    else if (L->data.expn == 1)
    {
        if (L->data.coef == 1)
            printf("x");
        else if (L->data.coef == -1)
            printf("-x");
        else
            printf("%.0fx", L->data.coef);
    }
    else if (L->data.coef == 1)
    {
        printf("x^%d", L->data.expn);
    }
    else if (L->data.coef == -1)
    {
        printf("-x^%d", L->data.expn);
    }
    else
    {
        printf("%.0f*x^%d", L->data.coef, L->data.expn);
    }
}

void PrintPolyn(polynomial P)
{
    int n;
    link l;
    l = P.head->next;
    n = 0;
    while (l)
    {
        n++;
        if (n == 1)
        {
            PrintPoly(l);
        }
        else if (l->data.coef > 0)
        {
            printf("+");
            PrintPoly(l);
        }
        else
        {
            PrintPoly(l);
        }
        l = l->next;
    }
    printf("\n");
}

int PolynLength(polynomial P)
{
    link q;
    int i;

    q = P.head;
    i = 0;

    while (q != P.tail)
    {
        q = q->next;
        i++;
    }
    return i;
}

// ===== 多项式加法 =====

void AddPolyn(polynomial *Pa, polynomial *Pb)
{
    position ha, hb, qa, qb;
    term a, b;

    ha = GetHead(Pa);
    hb = GetHead(Pb);
    qa = NextPos(ha);
    qb = NextPos(hb);
    while (!ListEmpty(*Pa) && !ListEmpty(*Pb) && qa)
    {
        a = GetCurElem(qa);
        b = GetCurElem(qb);
        switch (cmp(a, b))
        {
        case -1:
            ha = qa;
            qa = NextPos(qa);
            break;
        case 0:
            qa->data.coef += qb->data.coef;
            if (qa->data.coef)
                ha = qa;
            else
            {
                DelFirst(Pa, ha, &qa);
                FreeNode(&qa);
            }
            DelFirst(Pb, hb, &qb);
            FreeNode(&qb);
            qa = NextPos(ha);
            qb = NextPos(hb);
            break;
        case 1:
            DelFirst(Pb, hb, &qb);
            InsFirst(Pa, ha, qb);
            qb = NextPos(hb);
            ha = NextPos(ha);
        }
    }
    if (!ListEmpty(*Pb))
    {
        Pb->tail = hb;
        Append(Pa, qb);
    }
    DestroyPolyn(Pb);
}

// ===== 多项式减法 =====

void Oppsite(polynomial *Pa)
{
    position p;
    p = Pa->head->next;
    while (p)
    {
        p->data.coef *= -1;
        p = p->next;
    }
}

void SubtractPolyn_N(polynomial *Pa, polynomial *Pb)
{
    Oppsite(Pb);
    AddPolyn(Pa, Pb);
}

// ===== 多项式乘法 =====

void MultipyPolyn(polynomial *Pa, polynomial *Pb)
{
    polynomial Pc;
    position qa, qb;
    term a, b, c;
    InitList(&Pc);
    qa = GetHead(Pa);
    qa = qa->next;
    while (qa)
    {
        a = GetCurElem(qa);
        qb = GetHead(Pb);
        qb = qb->next;
        while (qb)
        {
            b = GetCurElem(qb);
            c.coef = a.coef * b.coef;
            c.expn = a.expn + b.expn;
            OrderInsert(&Pc, c, cmp);
            qb = qb->next;
        }
        qa = qa->next;
    }

    DestroyPolyn(Pb);
    ClearList(Pa);
    Pa->head = Pc.head;
    Pa->tail = Pc.tail;
    Pa->len = Pc.len;
}

// ===== 使用示例 =====

int main()
{
    polynomial p, q;
    int m;
    printf("输入第一个一元多项式的非零项个数：");
    scanf("%d", &m);
    CreatePolyn(&p, m);
    PrintPolyn(p);

    printf("输入第二个一元多项式的非零项个数：");
    scanf("%d", &m);
    CreatePolyn(&q, m);
    PrintPolyn(q);

    // AddPolyn(&p, &q);
    // SubtractPolyn_N(&p, &q);
    MultipyPolyn(&p, &q);
    PrintPolyn(p);
    DestroyPolyn(&p);

    return 0;
}
```

## 核心算法

**`LocateElem`** 利用链表按指数升序排列的特性，从头遍历找到第一个指数不小于目标值的位置，返回该位置及其前驱。`OrderInsert` 据此决定是合并同类项（系数相加后若为零则删除结点）还是在对应位置插入新结点。

**`AddPolyn`** 双指针同时遍历两个多项式，比较当前项指数：Pa 指数较小则指针后移；相等则系数相加（结果为零时删除）；Pb 指数较小则将 Pb 当前结点摘下插入 Pa。遍历结束后将 Pb 剩余项整体追加到 Pa 尾部。

**`MultipyPolyn`** 对 Pa 和 Pb 的每一项做系数相乘、指数相加，通过 `OrderInsert` 插入临时多项式 Pc，最后将 Pa 替换为 Pc 的链表。
