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

# 图的顺序存储结构（邻接矩阵）

实现图的邻接矩阵存储，支持有向图、无向图、有向网、无向网四种类型的建图与打印。通过 `creategraph` 分发函数根据枚举类型选择具体建图逻辑。

<!-- more -->

邻接矩阵用二维数组 `arcs[i][j].adj` 表示顶点 i 到 j 的弧，无权图存 0/1，有权图存权值。`info` 指针预留扩展信息。

## 完整代码

```cpp
#include <stdio.h>

#define max_vertex_num 20
#define vrtype int
#define infotype char
#define vertextype int

typedef enum { dg, dn, udg, udn } graphkind;

typedef struct
{
    vrtype adj;
    infotype* info;
} arccell, adjmatrix[max_vertex_num][max_vertex_num];

typedef struct
{
    vertextype vexs[max_vertex_num];
    adjmatrix arcs;
    int vexnum, arcnum;
    graphkind kind;
} mgraph;

int locatevex(mgraph* g, vertextype v)
{
    int i = 0;
    for (; i < g->vexnum; i++)
    {
        if (g->vexs[i] == v)
            break;
    }
    if (i == g->vexnum)
    {
        printf("no such vertex.\n");
        return -1;
    }
    return i;
}

void createdg(mgraph* g)
{
    int i, j;
    scanf("%d,%d", &(g->vexnum), &(g->arcnum));
    for (i = 0; i < g->vexnum; i++)
        scanf("%d", &(g->vexs[i]));
    for (i = 0; i < g->vexnum; i++)
        for (j = 0; j < g->vexnum; j++)
        {
            g->arcs[i][j].adj = 0;
            g->arcs[i][j].info = NULL;
        }
    for (i = 0; i < g->arcnum; i++)
    {
        int v1, v2;
        scanf("%d,%d", &v1, &v2);
        int n = locatevex(g, v1);
        int m = locatevex(g, v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        g->arcs[n][m].adj = 1;
    }
}

void createdn(mgraph* g)
{
    int i, j;
    scanf("%d,%d", &(g->vexnum), &(g->arcnum));
    for (i = 0; i < g->vexnum; i++)
        scanf("%d", &(g->vexs[i]));
    for (i = 0; i < g->vexnum; i++)
        for (j = 0; j < g->vexnum; j++)
        {
            g->arcs[i][j].adj = 0;
            g->arcs[i][j].info = NULL;
        }
    for (i = 0; i < g->arcnum; i++)
    {
        int v1, v2;
        scanf("%d,%d", &v1, &v2);
        int n = locatevex(g, v1);
        int m = locatevex(g, v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        g->arcs[n][m].adj = 1;
        g->arcs[m][n].adj = 1;   // 无向图对称赋值
    }
}

void createudg(mgraph* g)
{
    int i, j;
    scanf("%d,%d", &(g->vexnum), &(g->arcnum));
    for (i = 0; i < g->vexnum; i++)
        scanf("%d", &(g->vexs[i]));
    for (i = 0; i < g->vexnum; i++)
        for (j = 0; j < g->vexnum; j++)
        {
            g->arcs[i][j].adj = 0;
            g->arcs[i][j].info = NULL;
        }
    for (i = 0; i < g->arcnum; i++)
    {
        int v1, v2, w;
        scanf("%d,%d,%d", &v1, &v2, &w);
        int n = locatevex(g, v1);
        int m = locatevex(g, v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        g->arcs[n][m].adj = w;
    }
}

void createudn(mgraph* g)
{
    int i, j;
    scanf("%d,%d", &(g->vexnum), &(g->arcnum));
    for (i = 0; i < g->vexnum; i++)
        scanf("%d", &(g->vexs[i]));
    for (i = 0; i < g->vexnum; i++)
        for (j = 0; j < g->vexnum; j++)
        {
            g->arcs[i][j].adj = 0;
            g->arcs[i][j].info = NULL;
        }
    for (i = 0; i < g->arcnum; i++)
    {
        int v1, v2, w;
        scanf("%d,%d,%d", &v1, &v2, &w);
        int m = locatevex(g, v1);
        int n = locatevex(g, v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        g->arcs[n][m].adj = w;
        g->arcs[m][n].adj = w;   // 无向网对称赋值
    }
}

void creategraph(mgraph* g)
{
    scanf("%d", &(g->kind));
    switch (g->kind)
    {
        case dg:  createdg(g);  break;
        case dn:  createdn(g);  break;
        case udg: createudg(g); break;
        case udn: createudn(g); break;
        default:  break;
    }
}

void printgraph(mgraph g)
{
    int i, j;
    for (i = 0; i < g.vexnum; i++)
    {
        for (j = 0; j < g.vexnum; j++)
            printf("%d ", g.arcs[i][j].adj);
        printf("\n");
    }
}

int main()
{
    mgraph g;
    creategraph(&g);
    printgraph(g);
    return 0;
}
```

`locatevex` 在顶点未找到时用 `i == vexnum` 判断，此处逻辑正确——循环终止时 `i` 不会超过 `vexnum`。

四种建图函数共享相同的初始化流程：读入顶点数和弧数、录入顶点数据、矩阵清零、逐弧赋值。不同之处在于：
- **有向图 DG**：仅 `arcs[n][m] = 1`
- **无向图 DN**：同时赋值 `arcs[m][n] = 1`
- **有向网 UDG / 无向网 UDN**：邻接值改为权值 `w`
