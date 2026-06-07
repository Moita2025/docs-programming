---
date: 2026-06-01
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数据结构
  - 图论
  - 面向对象
---

# 邻接矩阵存储结构面向对象化

用类的继承体系重新组织邻接矩阵的四种建图逻辑：基类 `mgraph` 提供顶点定位和矩阵打印，派生类 `dg`、`dn`、`udg`、`udn` 在构造函数中完成输入与建图。

原代码混用 `<iostream>` 与 `scanf`，这里统一为 C 风格 IO。派生类的四个构造函数存在大量重复的初始化代码，体现继承体系中复用不足的问题。

<!-- more -->

## 修正后完整代码

```cpp
#include <stdio.h>

#define max_vertex_num 20

typedef int vrtype;
typedef int vertextype;

class arccell
{
public:
    vrtype adj;
    char* info;
};

class mgraph
{
public:
    vertextype vexs[max_vertex_num];
    arccell arcs[max_vertex_num][max_vertex_num];
    int vexnum, arcnum;
    const char* kind;

    int locatevex(vertextype v);
    void printgraph();
};

int mgraph::locatevex(vertextype v)
{
    int i = 0;
    for (; i < vexnum; i++)
        if (vexs[i] == v)
            break;
    if (i == vexnum)
    {
        printf("no such vertex.\n");
        return -1;
    }
    return i;
}

void mgraph::printgraph()
{
    int i, j;
    for (i = 0; i < vexnum; i++)
    {
        for (j = 0; j < vexnum; j++)
            printf("%d ", arcs[i][j].adj);
        printf("\n");
    }
}

// ===== 有向图 =====

class dg : public mgraph
{
public:
    dg();
};

dg::dg()
{
    kind = "dg";
    int i, j;
    printf("输入顶点和弧的个数（格式：顶点,弧）：\n");
    scanf("%d,%d", &vexnum, &arcnum);
    printf("输入顶点：\n");
    for (i = 0; i < vexnum; i++)
        scanf("%d", &vexs[i]);
    for (i = 0; i < vexnum; i++)
        for (j = 0; j < vexnum; j++)
        {
            arcs[i][j].adj = 0;
            arcs[i][j].info = NULL;
        }
    printf("输入弧始末端（格式：始点,终点）：\n");
    for (i = 0; i < arcnum; i++)
    {
        int v1, v2;
        scanf("%d,%d", &v1, &v2);
        int n = locatevex(v1);
        int m = locatevex(v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        arcs[n][m].adj = 1;
    }
}

// ===== 无向图 =====

class dn : public mgraph
{
public:
    dn();
};

dn::dn()
{
    kind = "dn";
    int i, j;
    printf("输入顶点和边个数（格式：顶点,边）：\n");
    scanf("%d,%d", &vexnum, &arcnum);
    printf("输入顶点：\n");
    for (i = 0; i < vexnum; i++)
        scanf("%d", &vexs[i]);
    for (i = 0; i < vexnum; i++)
        for (j = 0; j < vexnum; j++)
        {
            arcs[i][j].adj = 0;
            arcs[i][j].info = NULL;
        }
    printf("输入边端点（格式：顶点,顶点）：\n");
    for (i = 0; i < arcnum; i++)
    {
        int v1, v2;
        scanf("%d,%d", &v1, &v2);
        int n = locatevex(v1);
        int m = locatevex(v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        arcs[n][m].adj = 1;
        arcs[m][n].adj = 1;
    }
}

// ===== 有向网 =====

class udg : public mgraph
{
public:
    udg();
};

udg::udg()
{
    kind = "udg";
    int i, j;
    printf("输入顶点和弧的个数（格式：顶点,弧）：\n");
    scanf("%d,%d", &vexnum, &arcnum);
    printf("输入顶点：\n");
    for (i = 0; i < vexnum; i++)
        scanf("%d", &vexs[i]);
    for (i = 0; i < vexnum; i++)
        for (j = 0; j < vexnum; j++)
        {
            arcs[i][j].adj = 0;
            arcs[i][j].info = NULL;
        }
    printf("输入弧始末端及权值（格式：始点,终点,权值）：\n");
    for (i = 0; i < arcnum; i++)
    {
        int v1, v2, w;
        scanf("%d,%d,%d", &v1, &v2, &w);
        int n = locatevex(v1);
        int m = locatevex(v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        arcs[n][m].adj = w;
    }
}

// ===== 无向网 =====

class udn : public mgraph
{
public:
    udn();
};

udn::udn()
{
    kind = "udn";
    int i, j;
    printf("输入顶点和边个数（格式：顶点,边）：\n");
    scanf("%d,%d", &vexnum, &arcnum);
    printf("输入顶点：\n");
    for (i = 0; i < vexnum; i++)
        scanf("%d", &vexs[i]);
    for (i = 0; i < vexnum; i++)
        for (j = 0; j < vexnum; j++)
        {
            arcs[i][j].adj = 0;
            arcs[i][j].info = NULL;
        }
    printf("输入边端点及权值（格式：顶点,顶点,权值）：\n");
    for (i = 0; i < arcnum; i++)
    {
        int v1, v2, w;
        scanf("%d,%d,%d", &v1, &v2, &w);
        int m = locatevex(v1);
        int n = locatevex(v2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        arcs[n][m].adj = w;
        arcs[m][n].adj = w;
    }
}

// ===== 分发函数 =====

void creategraph()
{
    printf("输入要创建的图类型（dg/dn/udg/udn）：\n");
    char input[4];
    scanf("%s", input);
    if (input[0] == 'd' && input[1] == 'g' && input[2] == '\0')
    {
        dg G = dg();
        G.printgraph();
    }
    else if (input[0] == 'd' && input[1] == 'n' && input[2] == '\0')
    {
        dn G = dn();
        G.printgraph();
    }
    else if (input[0] == 'u' && input[1] == 'd' && input[2] == 'g' && input[3] == '\0')
    {
        udg G = udg();
        G.printgraph();
    }
    else if (input[0] == 'u' && input[1] == 'd' && input[2] == 'n' && input[3] == '\0')
    {
        udn G = udn();
        G.printgraph();
    }
    else
        printf("需要创建的类型不存在\n");
}

int main()
{
    creategraph();
    return 0;
}
```

基类 `mgraph` 封装了顶点数组、邻接矩阵和 `kind` 类型标识。四个派生类的构造函数结构高度相似：读入顶点数/弧数 → 录入顶点 → 矩阵清零 → 逐弧赋值。差异仅在于最后一步的赋值策略（单边/对称、无权/有权）。

原代码混用 `cin` 和 `scanf`，这里统一为 C 风格 IO。`kind` 从 `string` 改为 `const char*`，避免引入 `<string>` 头文件。
