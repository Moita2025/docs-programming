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

# 图的十字链表存储结构

实现有向图的十字链表存储，每个顶点通过 `firstin` 和 `firstout` 分别串起入弧和出弧。支持建图、查询入度/出度与销毁操作。

原代码的 `locatevex` 未找到判断与上一篇邻接多重表相同——`i > vexnum` 在循环上限恰为 `vexnum` 时永不为真。此外 `createdg` 缺少弧顶点有效性校验，`main` 中查询顶点与测试数据大小写不一致。

<!-- more -->

十字链表将邻接表与逆邻接表合二为一：每个弧结点同时链入弧尾顶点的出弧链表（通过 `tlink`）和弧头顶点的入弧链表（通过 `hlik`），求出入度均为 O(1) 定位 + O(d) 遍历。

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define max_vertex_num 20
#define vertextype char

typedef struct arcbox
{
    int tailvex, headvex;               // 弧尾、弧头顶点的下标
    struct arcbox* hlik, * tlink;       // hlik: 同弧头的下一条弧；tlink: 同弧尾的下一条弧
} arcbox;

typedef struct vexnode
{
    vertextype data;
    arcbox* firstin, * firstout;        // 入弧链表、出弧链表的首结点
} vexnode;

typedef struct
{
    vexnode xlist[max_vertex_num];
    int vexnum, arcnum;
} olgraph;

int locatevex(olgraph* g, vertextype v)
{
    int i;
    for (i = 0; i < g->vexnum; i++)
    {
        if (g->xlist[i].data == v)
            break;
    }
    if (i >= g->vexnum)                                  // 修正：>= 替代 >
    {
        printf("no such vertex.\n");
        return -1;
    }
    return i;
}

void createdg(olgraph* g)
{
    int i, j, k;
    vertextype v1, v2;
    arcbox* p = NULL;

    scanf("%d %d", &(g->vexnum), &(g->arcnum));
    getchar();
    for (i = 0; i < g->vexnum; i++)
    {
        scanf("%c", &(g->xlist[i].data));
        getchar();
        g->xlist[i].firstin = NULL;
        g->xlist[i].firstout = NULL;
    }
    for (k = 0; k < g->arcnum; k++)
    {
        scanf("%c %c", &v1, &v2);
        getchar();
        i = locatevex(g, v1);
        j = locatevex(g, v2);
        if (i < 0 || j < 0)                              // 修正：校验弧顶点有效性
        {
            printf("弧顶点不存在\n");
            exit(0);
        }
        p = (arcbox*)malloc(sizeof(arcbox));
        p->tailvex = i;
        p->headvex = j;
        // 头插法链入弧头顶点 j 的入弧链表
        p->hlik = g->xlist[j].firstin;
        // 头插法链入弧尾顶点 i 的出弧链表
        p->tlink = g->xlist[i].firstout;
        g->xlist[j].firstin = g->xlist[i].firstout = p;
    }
}

int indegree(olgraph* g, vertextype x)
{
    int i;
    int num = 0;
    for (i = 0; i < g->vexnum; i++)
    {
        if (x == g->xlist[i].data)
        {
            arcbox* p = g->xlist[i].firstin;
            while (p)
            {
                num++;
                p = p->hlik;
            }
            break;
        }
    }
    if (i == g->vexnum)
    {
        printf("图中没有指定顶点\n");
        return -1;
    }
    return num;
}

int outdegree(olgraph* g, vertextype x)
{
    int i;
    int num = 0;
    for (i = 0; i < g->vexnum; i++)
    {
        if (x == g->xlist[i].data)
        {
            arcbox* p = g->xlist[i].firstout;
            while (p)
            {
                num++;
                p = p->tlink;
            }
            break;
        }
    }
    if (i == g->vexnum)
    {
        printf("图中没有指定顶点\n");
        return -1;
    }
    return num;
}

void deletedg(olgraph* g)
{
    int i;
    arcbox* p = NULL, * del = NULL;
    for (i = 0; i < g->vexnum; i++)
    {
        p = g->xlist[i].firstout;
        while (p)
        {
            del = p;
            p = p->tlink;                                // 先推进再释放，避免悬空指针
            free(del);
        }
        g->xlist[i].firstout = NULL;
        g->xlist[i].firstin = NULL;
    }
}

int main()
{
    olgraph g;
    createdg(&g);
    printf("%c 顶点的入度为 %d\n", 'A', indegree(&g, 'A'));   // 修正：大写与测试数据一致
    printf("%c 顶点的出度为 %d\n", 'A', outdegree(&g, 'A'));
    deletedg(&g);
    return 0;
}
```

## 测试数据

```
4 5
A B C D
A B
A C
C D
D A
D B
```

预期输出：

```text
A 顶点的入度为 1
A 顶点的出度为 2
```

### 结构示意

以测试数据建图后，十字链表的逻辑结构（出弧链表用 `→`，入弧链表用 `←`）：

```text
        firstin  firstout
A:  ←[D→A]──┐   →[A→C]→[A→B]→NULL
B:  ←[A→B]←[D→B]→NULL
C:  ←[A→C]──┐   →[C→D]→NULL
D:  ←[C→D]──┘   →[D→B]→[D→A]→NULL
```

弧结点 `[A→B]` 同时出现在 A 的 `firstout` 链（通过 `tlink`）和 B 的 `firstin` 链（通过 `hlik`）。`deletedg` 只沿 `firstout` 遍历释放，保证每条弧处理一次。

### 修正点

| 位置 | 问题 | 修正 |
|------|------|------|
| `locatevex` | `i > vexnum` 永不为真 | 改为 `i >= vexnum` |
| `createdg` | `locatevex` 返回 -1 后仍继续建弧，导致越界访问 | 增加 `i < 0 \|\| j < 0` 校验 |
| `main` | 查询小写 `'a'` 与测试数据大写 `A` 不匹配 | 统一为大写 |
