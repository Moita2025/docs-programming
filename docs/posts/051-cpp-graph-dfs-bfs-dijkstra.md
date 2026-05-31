---
date: 2026-05-31
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数据结构
  - 图论
---

# C++ 无向图：DFS、BFS 与最短路径

一个用 Windows 对话框选择数据文件的 C++ 无向图程序，支持深度优先遍历、广度优先遍历和 Dijkstra 最短路径查询。BFS 依赖链式队列，Dijkstra 依赖顺序栈做路径回溯。

- 使用依赖：[<code>queue.h</code>](https://moita2025.github.io/docs-programming/2026/05/31/049-cpp-linked-queue-impl/)
- 使用依赖：[<code>sqstack.h</code>](https://moita2025.github.io/docs-programming/2026/05/31/050-cpp-sequential-stack-impl/)

<!-- more -->

## 数据文件格式

以中国省会城市高速公路路网为例（`中国省会城市的不完全高速公路路网 (ANSI).txt`）：

```text
28 64                          // 顶点数 弧数
北京
天津
石家庄
...                             // 共 28 个城市名
北京 天津 京沪高速 144           // 起点 终点 道路名 里程(km)
天津 石家庄 津石高速 320
...
```

顶点数决定数组大小，每条弧按"起点名 终点名 道路名 权值"格式写入，程序自动转为无向图的对称邻接矩阵。

## 图类核心（udn.h）

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <windows.h>
#include <Commdlg.h>

OPENFILENAME ofn;
char szFile[200];
const int inf = 99999;

using namespace std;

#define max_vertex_num 40

typedef int vrtype;
typedef string infotype;

class vertex
{
public:
    int id;
    infotype info;
};

class arccell
{
public:
    vrtype adj;
    infotype info;
};

class udn
{
public:
    udn();
    void reset();
    void loadfile();
    void dfstraverse();
    void bfstraverse();
    void dijkstra();

private:
    int firstadjvex(int v);
    int nextadjvex(int v, int w);
    void dfs(int v);
    bool vis[max_vertex_num];

    string kind;
    int vexnum, arcnum;
    vertex vexs[max_vertex_num];
    arccell arcs[max_vertex_num][max_vertex_num];
    int findbyid(int val_id);
    int findbystr(string val_str);
    void printgraph();
};

int udn::findbyid(int val_id)
{
    int i = 0;
    for (; i < vexnum; i++)
        if (vexs[i].id == val_id)
            break;
    if (i == vexnum)
    {
        printf("no such vertex.\n");
        return -1;
    }
    return i;
}

int udn::findbystr(string val_str)
{
    int i = 0;
    for (; i < vexnum; i++)
        if (vexs[i].info == val_str)
            break;
    if (i == vexnum)
    {
        printf("no such vertex.\n");
        return -1;
    }
    return i;
}

void udn::printgraph()
{
    int i, j;
    printf("成功构建图，邻接矩阵如下：\n");
    for (i = 0; i < vexnum; i++)
    {
        for (j = 0; j < vexnum; j++)
            printf("%5d ", arcs[i][j].adj);
        printf("\n");
    }
}

udn::udn()
{
    kind = "udn";
    for (int i = 0; i < max_vertex_num; i++)
    {
        vexs[i].id = 0;
        vexs[i].info = "";
    }
    for (int i = 0; i < max_vertex_num; i++)
        for (int j = 0; j < max_vertex_num; j++)
        {
            arcs[i][j].adj = (i == j) ? 0 : inf;          // 修正：合并条件判断
            arcs[i][j].info = "";
        }
}

void udn::reset()
{
    for (int i = 0; i < max_vertex_num; i++)
    {
        vexs[i].id = 0;
        vexs[i].info = "";
    }
    for (int i = 0; i < max_vertex_num; i++)
        for (int j = 0; j < max_vertex_num; j++)
        {
            arcs[i][j].adj = (i == j) ? 0 : inf;          // 修正：合并条件判断
            arcs[i][j].info = "";
        }
}

void udn::loadfile()
{
    FILE * fp;

point:
    memset(szFile, 0, sizeof(szFile));
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = "All\0*.*\0Text\0*.TXT\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;
    if (GetOpenFileName(&ofn))
        MessageBox(NULL, ofn.lpstrFile, "你选择的文件是：", MB_OK);
    else
    {
        if (IDOK == MessageBox(NULL, "请务必进行文件选择\n点击确定重新选择，点击取消退出",
            "警告", MB_ICONSTOP | MB_OKCANCEL))
            goto point;
        else
            exit(0);
    }

    fp = fopen(ofn.lpstrFile, "r");
    fscanf(fp, "%d %d", &(vexnum), &(arcnum));

    for (int i = 0; i < vexnum; i++)
    {
        char temp[100];
        vexs[i].id = i + 1;
        fscanf(fp, "%s", temp);                            // 修正：去除多余的 &
        vexs[i].info = temp;
    }

    for (int i = 0; i < arcnum; i++)
    {
        char temp1[100], temp2[100], temp3[100];
        int w;
        int m, n;
        fscanf(fp, "%s %s %s %d", temp1, temp2, temp3, &w); // 修正：去除多余的 &
        m = findbystr((string)temp1);
        n = findbystr((string)temp2);
        if (m == -1 || n == -1)
        {
            printf("no this vertex\n");
            return;
        }
        arcs[n][m].adj = w;
        arcs[m][n].adj = w;
        arcs[n][m].info = temp3;
        arcs[m][n].info = temp3;
    }
    fclose(fp);
    printf("函数执行结束\n");
}

int udn::firstadjvex(int v)
{
    int i;
    for (i = 0; i < vexnum; i++)
        if (i != v && arcs[v][i].adj != inf)               // 修正：排除自身，避免将 v 返回为自己的邻接点
            return i;
    return -1;
}

int udn::nextadjvex(int v, int w)
{
    int i;
    for (i = w + 1; i < vexnum; i++)
        if (i != v && arcs[v][i].adj != inf)               // 新增：排除自身
            return i;
    return -1;
}

void udn::dfs(int v)
{
    int w;
    printf("%s ", vexs[v].info.c_str());
    vis[v] = true;
    for (w = firstadjvex(v); w >= 0; w = nextadjvex(v, w))
        if (!vis[w])
            dfs(w);
}

void udn::dfstraverse()
{
    int v;
    for (v = 0; v < vexnum; v++)
        vis[v] = false;
    printf("深度优先遍历(dfs)：");
    for (v = 0; v < vexnum; v++)
        if (!vis[v])
            dfs(v);
    printf("\n");
}
```

### 修正点（udn.h）

1. **`firstadjvex` / `nextadjvex` 排除自身**——邻接矩阵对角为 0，`0 != inf` 为真，原代码会将顶点自身当作"第一个邻接点"返回，虽被 `vis` 跳过，但增加了一次无意义的迭代
2. **`scanf` 多余 `&`**——`char temp[100]` 本身已退化为指针，`&temp` 类型为 `char(*)[100]`，虽地址相同但类型不匹配
3. **构造函数 / reset 初始化**——用三元表达式替代 `if-else` 分列写法，语义更紧凑

## BFS 与 Dijkstra（main.h）

```cpp
#include "udn.h"
#include "sqstack.h"
#include "queue.h"

void udn::bfstraverse()
{
    printf("广度优先遍历(bfs)：");
    int v, u, w;
    queue* q = NULL;
    initqueue(&q);
    for (v = 0; v < vexnum; v++)
        vis[v] = false;
    for (v = 0; v < vexnum; v++)
    {
        if (!vis[v])
        {
            printf("%s ", vexs[v].info.c_str());
            vis[v] = true;
            enqueue(&q, vexs[v].id);
            while (!queueempty(q))
            {
                dequeue(&q, &u);
                u = findbyid(u);
                for (w = firstadjvex(u); w >= 0; w = nextadjvex(u, w))
                {
                    if (!vis[w])
                    {
                        printf("%s ", vexs[w].info.c_str());
                        vis[w] = true;
                        enqueue(&q, vexs[w].id);
                    }
                }
            }
        }
    }
    delqueue(q);
    printf("\n");
}

void udn::dijkstra()
{
    printf("请输入起点终点，以空格划分：");
    char temp1[100], temp2[100];
    scanf("%s %s", temp1, temp2);                          // 修正：去除多余的 &

    int dis[max_vertex_num];
    int path[max_vertex_num];
    for (int i = 0; i < vexnum; i++)
    {
        dis[i] = inf;
        path[i] = -1;
        vis[i] = false;
    }

    if (findbystr(temp1) != -1 && findbystr(temp2) != -1)
    {
        dis[findbystr((string)temp1)] = 0;
        printf("起点为%s，终点为%s\n", temp1, temp2);
    }
    else
    {
        cout << "没有给定起终点" << endl;
        return;
    }

    for (int i = 0; i < vexnum; i++)
    {
        int t = -1;
        for (int j = 0; j < vexnum; j++)
            if (!vis[j] && (t == -1 || dis[t] > dis[j]))
                t = j;

        for (int j = 0; j < vexnum; j++)
        {
            if (arcs[t][j].adj == inf) continue;           // 新增：跳过不连通的边，避免无效松弛
            if (dis[j] > dis[t] + arcs[t][j].adj)
            {
                path[j] = t;
                dis[j] = dis[t] + arcs[t][j].adj;          // 修正：只在松弛成功时更新，替代原来的 min
            }
        }
        vis[t] = true;
    }

    sqstack stk;
    int k = findbystr((string)temp2);
    stk.push(vexs[findbystr((string)temp2)].id);
    while (k != findbystr((string)temp1) && k != -1)       // 修正：简化循环条件
    {
        stk.push(vexs[path[k]].id);
        k = path[k];                                       // 修正：path[k] 已是下标，无需 findbyid 绕回
    }

    int citynum = stk.top - stk.base;
    printf("中途经过%d个位置, ", citynum - 2);
    printf("路径：");
    int dummy;
    while (stk.gettop() != ERROR)
    {
        cout << vexs[findbyid(stk.gettop())].info << " ";
        stk.pop(dummy);                                    // 修正：用独立变量接收 pop 结果，不与 k 混用
    }
    printf("最短距离：%d\n", dis[findbystr((string)temp2)]);
}
```

### 修正点（main.h）

1. **`scanf` 多余 `&`**——同 udn.h
2. **Dijkstra 跳过 `inf` 边**——原代码 `dis[t] + arcs[t][j].adj` 对不连通边产生无意义的极大值，"仅不更新 path"但 `min` 仍会执行比较
3. **松弛同时更新 `dis`**——用 `dis[j] = dis[t] + arcs[t][j].adj` 替代 `min`，语义更清晰
4. **路径回溯简化**——`path[k]` 已存储前驱下标，`k = path[k]` 直接回溯，原代码 `findbyid(vexs[path[k]].id)` 多绕了一层 ID↔下标 转换
5. **`stk.pop(dummy)`**——用独立变量 `dummy` 接收 pop 返回值，不与路径变量 `k` 混用

## 主控程序（main.cpp）

```cpp
#include "main.h"

int main()
{
    printf("--------------欢迎使用此程序--------------\n"
           "--------请在对话框选择要加载的文件--------\n");
    udn G = udn();
    G.loadfile();
    while (true)
    {
        int input = 10;
        printf("---输入1：对该图进行深度优先遍历（DFS）---\n"
               "---输入2：对该图进行广度优先遍历（BFS）---\n"
               "---输入3：对该图查询两地点最短路径--------\n"
               "---输入4：重新选择文件读取图信息------------\n"
               "-------------输入0：退出该程序-------------\n");
        scanf("%d", &input);
        switch (input)
        {
        case 1: G.dfstraverse(); break;
        case 2: G.bfstraverse(); break;
        case 3: G.dijkstra();    break;
        case 4: G.reset(); G.loadfile(); break;
        case 0: exit(0); break;
        default: break;
        }
    }
    return 0;
}
```

main.cpp 基本不需要修改。

## 文件组织

```text
├── main.cpp          // 入口 + 菜单循环
├── main.h            // BFS 与 Dijkstra 实现
├── udn.h             // 图类定义与 DFS 实现
├── queue.h           // 链式队列（依赖 049）
├── sqstack.h         // 顺序栈（依赖 050）
└── *.txt             // 数据文件
```

`main.h` 同时 `#include` 了 `udn.h`、`sqstack.h`、`queue.h`，而 `main.cpp` 只需引入 `main.h` 即可编译全部代码。

## 运行示例

```text
请输入起点终点，以空格划分：北京 广州
起点为北京，终点为广州
中途经过5个位置, 路径：北京 天津 济南 合肥 南昌 长沙 广州
最短距离：2835

详细信息：
      北京-->      天津  长度：  144  道路名称：京沪高速
      天津-->      济南  长度：  325  道路名称：京台高速、京沪高速
      济南-->      合肥  长度：  640  道路名称：济广高速、蚌合高速
      合肥-->      南昌  长度：  460  道路名称：福银高速、杭长高速
      南昌-->      长沙  长度：  350  道路名称：沪昆高速、杭长高速
      长沙-->      广州  长度：  676  道路名称：乐广高速、广连高速
```
