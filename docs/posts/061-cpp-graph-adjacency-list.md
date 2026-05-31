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

# 图的邻接表存储结构

实现有向图的邻接表存储，支持从控制台输入建图、查询指定顶点的出度与入度。原代码缺少销毁函数，arcnode 中未找到目标顶点时直接用 `'#'` 当哨兵值不够健壮。

<!-- more -->

邻接表为每个顶点维护一个单链表，链表结点存储该顶点指向的邻接顶点的下标。相比邻接矩阵，邻接表在稀疏图中显著节省空间。

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>
#define max_vertex_num 20

#define vertextype char

typedef struct arcnode
{
    int adjvex;                         // 邻接顶点在顶点数组中的下标
    struct arcnode* nextarc;            // 指向下一条弧
} arcnode;

typedef struct vnode
{
    vertextype data;                    // 顶点值
    arcnode* firstarc;                 // 指向第一条弧
} vnode, adjlist[max_vertex_num];

typedef struct
{
    adjlist vertices;                   // 顶点数组
    int vexnum, arcnum;                // 顶点数和弧数
} algraph;

void creategraph(algraph* graph)
{
    int i, j;
    char va, vb;
    arcnode* node = NULL;
    printf("输入顶点的数目：\n");
    scanf("%d", &(graph->vexnum));
    printf("输入弧的数目：\n");
    scanf("%d", &(graph->arcnum));
    scanf("%*[^\n]"); scanf("%*c");
    printf("输入各个顶点的值：\n");
    for (i = 0; i < graph->vexnum; i++)
    {
        scanf("%c", &(graph->vertices[i].data));
        getchar();
        graph->vertices[i].firstarc = NULL;
    }
    for (i = 0; i < graph->arcnum; i++)
    {
        printf("输入弧(a b 表示弧 a->b)：\n");
        scanf("%c %c", &va, &vb);
        getchar();
        node = (arcnode*)malloc(sizeof(arcnode));
        node->adjvex = -1;                               // 修正：用 -1 替代 '#' 作为哨兵
        node->nextarc = NULL;
        for (j = 0; j < graph->vexnum; j++)
        {
            if (vb == graph->vertices[j].data)
            {
                node->adjvex = j;
                break;
            }
        }
        if (node->adjvex == -1)
        {
            printf("弧信息有误！\n");
            free(node);                                  // 修正：错误时释放已分配的结点
            exit(0);
        }
        for (j = 0; j < graph->vexnum; j++)
        {
            if (va == graph->vertices[j].data)
            {
                node->nextarc = graph->vertices[j].firstarc;
                graph->vertices[j].firstarc = node;
                break;
            }
        }
        if (j == graph->vexnum)
        {
            printf("弧信息有误！\n");
            free(node);                                  // 修正：错误时释放已分配的结点
            exit(0);
        }
    }
}

int outdegree(algraph graph, char v)
{
    int j;
    int count = 0;
    for (j = 0; j < graph.vexnum; j++)
    {
        if (v == graph.vertices[j].data)
        {
            arcnode* p = graph.vertices[j].firstarc;
            while (p)
            {
                count++;
                p = p->nextarc;
            }
            break;
        }
    }
    if (j == graph.vexnum) return -1;
    return count;
}

int indegree(algraph graph, char v)
{
    int i, j, index = -1;
    int count = 0;
    for (j = 0; j < graph.vexnum; j++)
    {
        if (v == graph.vertices[j].data)
        {
            index = j;
            break;
        }
    }
    if (index == -1) return -1;
    for (j = 0; j < graph.vexnum; j++)
    {
        arcnode* p = graph.vertices[j].firstarc;
        while (p)
        {
            if (p->adjvex == index) count++;
            p = p->nextarc;
        }
    }
    return count;
}

void destroygraph(algraph* graph)                        // 新增：释放邻接表中所有弧结点
{
    for (int i = 0; i < graph->vexnum; i++)
    {
        arcnode* p = graph->vertices[i].firstarc;
        while (p)
        {
            arcnode* tmp = p;
            p = p->nextarc;
            free(tmp);
        }
        graph->vertices[i].firstarc = NULL;
    }
}

int main(void)
{
    algraph graph;
    creategraph(&graph);

    printf("%c 顶点的出度为 %d\n", 'A', outdegree(graph, 'A'));
    printf("%c 顶点的入度为 %d\n", 'A', indegree(graph, 'A'));

    destroygraph(&graph);                                // 新增：释放内存
    return 0;
}
```

## 测试数据

```
输入顶点的数目：
4
输入弧的数目：
4
输入各个顶点的值：
A B C D
输入弧(a b 表示弧 a->b)：
A B
输入弧(a b 表示弧 a->b)：
A C
输入弧(a b 表示弧 a->b)：
C D
输入弧(a b 表示弧 a->b)：
D A
A 顶点的出度为 2
A 顶点的入度为 1
```

### 结构说明

`creategraph` 为每条弧分配一个 `arcnode`，在其中存入目标顶点在 `vertices` 数组中的下标，然后用头插法链入源顶点的单链表。建图后的邻接表结构：

```text
vertices[0] A → [adjvex=1 | B] → [adjvex=2 | C] → NULL
vertices[1] B → NULL
vertices[2] C → [adjvex=3 | D] → NULL
vertices[3] D → [adjvex=0 | A] → NULL
```

**出度** 只需遍历该顶点链表的结点数。**入度** 需扫描所有顶点的链表，统计 `adjvex` 等于目标顶点下标的结点数。

### 修正点

- `adjvex` 哨兵值由 `'#'`（35）改为 `-1`，避免与合法顶点下标冲突。
- `creategraph` 在弧信息有误时先 `free(node)` 再退出，防止内存泄漏。
- 新增 `destroygraph` 遍历释放所有弧结点。
