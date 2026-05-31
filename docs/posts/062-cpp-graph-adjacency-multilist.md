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
  - 图论
---

# 图的邻接多重表存储结构

实现无向图的邻接多重表，每条边用一个结点表达、同时链入两个顶点的边链表。支持建图、插入边、删除边、打印边集与销毁操作。

原代码存在三处缺陷：`locatevex` 的未找到判断永远不成立；`initmarks` 边遍历被 `mark==1` 条件截断；`deletedn` 逐边调用 `deleteedge` 可能重复释放。以下给出修正后代码。

<!-- more -->

邻接多重表的核心在于 `ebox` 结构体：`ivex` 和 `jvex` 存两端顶点下标，`ilink` 和 `jlink` 分别链入两端顶点的边链表。一条边只分配一次，共享于两个顶点的链表之间。

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define max_vertex_num 20
#define vertextype char
#define status int

typedef enum { unvisited, visited } visitif;

typedef struct ebox
{
    visitif mark;
    int ivex, jvex;                     // 边两端顶点在数组中的下标
    struct ebox* ilink, * jlink;        // 分别指向 ivex 和 jvex 的下一条边
} ebox;

typedef struct vexbox
{
    vertextype data;
    ebox* firstedge;
} vexbox;

typedef struct
{
    vexbox adjmulist[max_vertex_num];
    int vexnum, edgenum;
} amlgraph;

int locatevex(amlgraph* g, vertextype v)
{
    int i;
    for (i = 0; i < g->vexnum; i++)
    {
        if (g->adjmulist[i].data == v)
            break;
    }
    if (i >= g->vexnum)                              // 修正：>= 替代 >，顶点不存在时 i==vexnum
    {
        printf("no such vertex.\n");
        return -1;
    }
    return i;
}

status insertedge(amlgraph* g, vertextype v1, vertextype v2)
{
    int v1add = locatevex(g, v1);
    int v2add = locatevex(g, v2);
    ebox* node = NULL;
    if (v1add < 0 || v2add < 0)
    {
        printf("顶点信息有误\n");
        exit(-1);
    }
    node = (ebox*)malloc(sizeof(ebox));
    node->mark = unvisited;
    node->ivex = v1add;
    node->jvex = v2add;
    // 头插法链入 v1 的边链表
    node->ilink = g->adjmulist[v1add].firstedge;
    g->adjmulist[v1add].firstedge = node;
    // 头插法链入 v2 的边链表
    node->jlink = g->adjmulist[v2add].firstedge;
    g->adjmulist[v2add].firstedge = node;
    return 1;
}

status createdn(amlgraph* g)
{
    int i, k;
    vertextype v1, v2;
    scanf("%d %d", &(g->vexnum), &(g->edgenum));
    getchar();
    for (i = 0; i < g->vexnum; i++)
    {
        scanf("%c", &(g->adjmulist[i].data));
        getchar();
        g->adjmulist[i].firstedge = NULL;
    }
    for (k = 0; k < g->edgenum; k++)
    {
        scanf("%c %c", &v1, &v2);
        getchar();
        insertedge(g, v1, v2);
    }
    return 1;
}

status deleteedge(amlgraph* g, vertextype v1, vertextype v2)
{
    int v1add = locatevex(g, v1);
    int v2add = locatevex(g, v2);
    ebox* icurnode = NULL, * iprenode = NULL;
    ebox* jcurnode = NULL, * jprenode = NULL;

    // 在 v1 的边链表中定位目标边
    icurnode = g->adjmulist[v1add].firstedge;
    while (icurnode && !(((icurnode->ivex == v1add) && (icurnode->jvex == v2add))
                      || ((icurnode->ivex == v2add) && (icurnode->jvex == v1add))))
    {
        iprenode = icurnode;
        if (icurnode->ivex == v1add)
            icurnode = icurnode->ilink;
        else
            icurnode = icurnode->jlink;
    }
    if (!icurnode) { printf("边不存在\n"); return -1; }

    // 在 v2 的边链表中定位目标边
    jcurnode = g->adjmulist[v2add].firstedge;
    while (jcurnode && !(((jcurnode->ivex == v1add) && (jcurnode->jvex == v2add))
                      || ((jcurnode->ivex == v2add) && (jcurnode->jvex == v1add))))
    {
        jprenode = jcurnode;
        if (jcurnode->ivex == v2add)
            jcurnode = jcurnode->ilink;
        else
            jcurnode = jcurnode->jlink;
    }

    // 从 v1 的链表中摘除
    if (iprenode == NULL)
        g->adjmulist[v1add].firstedge =
            (icurnode->ivex == v1add) ? icurnode->ilink : icurnode->jlink;
    else if (iprenode->ivex == v1add)
        iprenode->ilink = (icurnode->ivex == v1add) ? icurnode->ilink : icurnode->jlink;
    else
        iprenode->jlink = (icurnode->ivex == v1add) ? icurnode->ilink : icurnode->jlink;

    // 从 v2 的链表中摘除
    if (jprenode == NULL)
        g->adjmulist[v2add].firstedge =
            (jcurnode->ivex == v2add) ? jcurnode->ilink : jcurnode->jlink;
    else if (jprenode->ivex == v2add)
        jprenode->ilink = (jcurnode->ivex == v2add) ? jcurnode->ilink : jcurnode->jlink;
    else
        jprenode->jlink = (jcurnode->ivex == v2add) ? jcurnode->ilink : jcurnode->jlink;

    free(icurnode);
    return 1;
}

void initmarks(amlgraph* g)
{
    int i;
    ebox* p = NULL;
    for (i = 0; i < g->vexnum; i++)
    {
        p = g->adjmulist[i].firstedge;
        while (p)                                        // 修正：去掉 p->mark==1 条件，遍历所有边
        {
            p->mark = unvisited;
            if (p->ivex == i)
                p = p->ilink;
            else
                p = p->jlink;
        }
    }
}

void printedges(amlgraph* g)
{
    int i;
    ebox* p = NULL;
    initmarks(g);
    for (i = 0; i < g->vexnum; i++)
    {
        p = g->adjmulist[i].firstedge;
        while (p && (p->mark == unvisited))              // 修正：匹配 initmarks 语义
        {
            printf("%c-%c ", g->adjmulist[p->ivex].data,
                             g->adjmulist[p->jvex].data);
            p->mark = visited;
            if (p->ivex == i)
                p = p->ilink;
            else
                p = p->jlink;
        }
    }
    printf("\n");
}

status deletedn(amlgraph* g)
{
    int i;
    for (i = 0; i < g->vexnum; i++)
    {
        ebox* p = g->adjmulist[i].firstedge;
        while (p)
        {
            ebox* next;
            if (p->ivex == i)
                next = p->ilink;
            else
                next = p->jlink;
            // 修正：仅当 ivex==i 时释放，保证每条边只释放一次
            if (p->ivex == i)
            {
                // 同时清空另一端顶点的首边指针（若恰好指向本边）
                int other = p->jvex;
                if (g->adjmulist[other].firstedge == p)
                {
                    if (p->ivex == other)
                        g->adjmulist[other].firstedge = p->ilink;
                    else
                        g->adjmulist[other].firstedge = p->jlink;
                }
                free(p);
            }
            p = next;
        }
        g->adjmulist[i].firstedge = NULL;
    }
    return 1;
}

int main()
{
    amlgraph g;
    createdn(&g);
    printedges(&g);
    printf("删除 A-B 边：\n");
    deleteedge(&g, 'A', 'B');
    printedges(&g);
    deletedn(&g);
    return 0;
}
```

## 测试数据

```
5 6
A B C D E
A B
A D
B C
C D
C E
B E
```

预期输出：

```text
A-D A-B B-E B-C C-E C-D
删除 A-B 边：
A-D B-E B-C C-E C-D
```

### 结构示意

以测试数据建图后，邻接多重表的逻辑结构：

```text
A → [A,D] → [A,B] → NULL
B → [B,E] → [B,C] → [A,B] → NULL
C → [C,E] → [C,D] → [B,C] → NULL
D → [C,D] → [A,D] → NULL
E → [B,E] → [C,E] → NULL
```

`[A,B]` 同一条边结点出现在 A 和 B 两个链表中，通过 `ilink` 和 `jlink` 分别维护各自链表的后继关系。`printedges` 利用 `mark` 标志避免重复打印同一条边。

### 修正点

| 位置 | 问题 | 修正 |
|------|------|------|
| `locatevex` | `i > vexnum` 条件永远不成立 | 改为 `i >= vexnum` |
| `initmarks` | `while (p && p->mark==1)` 在遇到未标记边时截断 | 去掉 `mark==1` 条件，遍历所有边 |
| `deletedn` | 逐边调用 `deleteedge`，同一边被多次查找和释放 | 改为单次遍历，用 `ivex == i` 保证每条边只释放一次 |
