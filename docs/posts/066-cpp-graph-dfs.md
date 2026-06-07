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

# 图的深度优先搜索（邻接矩阵）

在邻接矩阵存储的无向图上实现深度优先搜索。使用 `firstadjvex` 和 `nextadjvex` 获取邻接顶点，递归访问未标记结点。

- 使用依赖：[<code>mgraph 邻接矩阵</code>](https://moita2025.github.io/docs-programming/2026/06/01/065-cpp-graph-adjacency-matrix/#完整代码)

<!-- more -->

原 DFS 文件单独成篇时重复定义了简化版的 `mgraph` 和 `createdn`。通过跨页面依赖声明，本文复用前一篇的完整结构体与建图函数，仅补充 DFS 特有逻辑。`locatevex` 中 `i > vexnum` 判断永不为真，已修正。

## 完整代码

```cpp
#include <stdio.h>

#define max_vertex_num 20
#define vrtype int
#define vertextype int

bool visited[max_vertex_num];

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
        printf("no such vertex.\n");
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

// ===== 深度优先搜索 =====

void dfs(mgraph g, int v)
{
    int w;
    printf("%d ", g.vexs[v]);
    visited[v] = true;
    for (w = firstadjvex(g, v); w >= 0; w = nextadjvex(g, v, w))
        if (!visited[w])
            dfs(g, w);
}

void dfstraverse(mgraph g)
{
    int v;
    for (v = 0; v < g.vexnum; ++v)
        visited[v] = false;
    for (v = 0; v < g.vexnum; v++)
        if (!visited[v])
            dfs(g, v);
}

int main()
{
    mgraph g;
    createdn(&g);
    dfstraverse(g);
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

预期输出：`1 2 4 8 5 3 6 7`

`firstadjvex` 返回顶点 v 的第一个邻接顶点下标，`nextadjvex` 从 w+1 继续扫描。DFS 访问当前顶点后标记为 true，再对每个未访问的邻接顶点递归调用自身。

### 修正点

`locatevex` 中 `i > vexnum` 改为 `i >= vexnum`——循环终止时 `i` 最大为 `vexnum`，原条件永不成立。
