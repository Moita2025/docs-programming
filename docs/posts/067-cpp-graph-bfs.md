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

# 图的广度优先搜索（邻接矩阵）

在邻接矩阵存储的无向图上实现广度优先搜索。借助链式队列管理待访问顶点，从起点出发逐层扩散访问。

- 使用依赖：[<code>mgraph 邻接矩阵</code>](https://moita2025.github.io/docs-programming/2026/06/01/065-cpp-graph-adjacency-matrix/#完整代码)

<!-- more -->

BFS 的核心在于队列：访问起点后入队，然后循环出队、将其所有未访问邻接顶点访问并入队，直至队列为空。

## 完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define max_vertex_num 20
#define vrtype int
#define vertextype int

bool visited[max_vertex_num];

// ===== 链式队列 =====

typedef struct queue
{
    vertextype data;
    struct queue* next;
} queue;

void initqueue(queue** q)
{
    (*q) = (queue*)malloc(sizeof(queue));
    (*q)->next = NULL;
}

void enqueue(queue** q, vertextype v)
{
    queue* temp = (*q);
    queue* element = (queue*)malloc(sizeof(queue));
    element->data = v;
    element->next = NULL;
    while (temp->next != NULL)
        temp = temp->next;
    temp->next = element;
}

void dequeue(queue** q, int* u)
{
    if ((*q)->next == NULL) return;                      // 修正：增加队空判断
    queue* del = (*q)->next;
    (*u) = (*q)->next->data;
    (*q)->next = (*q)->next->next;
    free(del);
}

bool queueempty(queue* q)
{
    return q->next == NULL;
}

void delqueue(queue* q)
{
    queue* del = NULL;
    while (q->next)
    {
        del = q->next;
        q->next = q->next->next;
        free(del);
    }
    free(q);
}

// ===== 邻接矩阵结构（来自 图的顺序存储结构） =====

typedef struct
{
    vrtype adj;
} arccell, adjmatrix[max_vertex_num][max_vertex_num];

typedef struct
{
    vertextype vexs[max_vertex_num];
    adjmatrix arcs;
    int vexnum, arcnum;
} mgraph;

int locatevex(mgraph* g, vertextype v)
{
    int i;
    for (i = 0; i < g->vexnum; i++)
        if (g->vexs[i] == v) break;
    if (i >= g->vexnum)                                  // 修正：>= 替代 >
    {
        printf("no this vertex\n");
        return -1;
    }
    return i;
}

void createdn(mgraph* g)
{
    int i, j, n, m;
    int v1, v2;
    scanf("%d,%d", &(g->vexnum), &(g->arcnum));
    for (i = 0; i < g->vexnum; i++)
        scanf("%d", &(g->vexs[i]));
    for (i = 0; i < g->vexnum; i++)
        for (j = 0; j < g->vexnum; j++)
            g->arcs[i][j].adj = 0;
    for (i = 0; i < g->arcnum; i++)
    {
        scanf("%d,%d", &v1, &v2);
        n = locatevex(g, v1);
        m = locatevex(g, v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        g->arcs[n][m].adj = 1;
        g->arcs[m][n].adj = 1;
    }
}

// ===== 邻接顶点查找 =====

int firstadjvex(mgraph g, int v)
{
    int i;
    for (i = 0; i < g.vexnum; i++)
        if (g.arcs[v][i].adj)
            return i;
    return -1;
}

int nextadjvex(mgraph g, int v, int w)
{
    int i;
    for (i = w + 1; i < g.vexnum; i++)
        if (g.arcs[v][i].adj)
            return i;
    return -1;
}

// ===== 广度优先搜索 =====

void bfstraverse(mgraph g)
{
    int v, u, w;
    queue* q = NULL;
    initqueue(&q);
    for (v = 0; v < g.vexnum; ++v)
        visited[v] = false;
    for (v = 0; v < g.vexnum; v++)
    {
        if (!visited[v])
        {
            printf("%d ", g.vexs[v]);
            visited[v] = true;
            enqueue(&q, g.vexs[v]);
            while (!queueempty(q))
            {
                dequeue(&q, &u);
                u = locatevex(&g, u);
                for (w = firstadjvex(g, u); w >= 0; w = nextadjvex(g, u, w))
                {
                    if (!visited[w])
                    {
                        printf("%d ", g.vexs[w]);
                        visited[w] = true;
                        enqueue(&q, g.vexs[w]);
                    }
                }
            }
        }
    }
    delqueue(q);
}

int main()
{
    mgraph g;
    createdn(&g);
    bfstraverse(g);
    return 0;
}
```

## 测试数据

```
8,9
1
2
3
4
5
6
7
8
1,2
2,4
2,5
4,8
5,8
1,3
3,6
6,7
7,3
```

预期输出：`1 2 3 4 5 6 7 8`

BFS 从顶点 1 出发，先访问其邻接点 2、3；再依次处理 2 的邻接点 4、5，以此类推。队列保证了"先被发现的顶点先被处理"的逐层顺序。

### 修正点

- `locatevex` 中 `i > vexnum` 改为 `>=`
- `dequeue` 增加队空判断，防止空队列时解引用空指针
