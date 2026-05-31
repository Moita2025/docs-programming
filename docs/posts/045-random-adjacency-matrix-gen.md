---
date: 2026-05-31
authors:
  - moita
categories:
  - 算法
  - 文件系统
tags:
  - CPP
  - 图论
---

# C++ 随机生成邻接矩阵

写一个随机生成无向图邻接矩阵的小工具。矩阵规模固定 20×20，对角线为 0，随机生成最多 400 条带权边，最终输出矩阵并统计边数。

<!-- more -->

## 完整代码

两个版本，差别仅在于是否将结果写入文件。

=== "控制台输出版"

    ```cpp
    #include <stdio.h>
    #include <stdlib.h>
    #include <time.h>

    int main()
    {
        srand(time(NULL));
        int n = 20;
        const int inf = 99999;
        int a[n][n];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                a[i][j] = (i == j) ? 0 : inf;

        for (int m = 0; m < 400; m++)
        {
            int i = rand() % 20;
            int j = rand() % 20;
            int k = rand() % 40;
            if ((a[i][j] == inf && a[j][i] == inf) && i != j)
                a[i][j] = a[j][i] = k;
        }

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
                printf("%5d ", a[i][j]);
            printf("\n");
        }

        int arcsnum = 0;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < i; j++)
                if (a[i][j] != inf)
                    arcsnum++;
        printf("边数：%d", arcsnum);

        return 0;
    }
    ```

=== "文件输出版"

    ```cpp
    #include <stdio.h>
    #include <stdlib.h>
    #include <time.h>

    int main()
    {
        srand(time(NULL));
        int n = 20;
        const int inf = 99999;
        int a[n][n];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                a[i][j] = (i == j) ? 0 : inf;

        // 时间戳文件名
        time_t timep;
        struct tm *p;
        char filename[256] = {0};
        time(&timep);
        p = localtime(&timep);
        sprintf(filename, "邻接矩阵 %d-%02d%02d-%02d%02d%02d.txt",
                1900 + p->tm_year, 1 + p->tm_mon, p->tm_mday,
                p->tm_hour, p->tm_min, p->tm_sec);
        FILE *fp = fopen(filename, "w+");

        for (int m = 0; m < 400; m++)
        {
            int i = rand() % 20;
            int j = rand() % 20;
            int k = rand() % 40;
            if ((a[i][j] == inf && a[j][i] == inf) && i != j)
                a[i][j] = a[j][i] = k;
        }

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                fprintf(fp, "%5d ", a[i][j]);
                printf("%5d ", a[i][j]);
            }
            fprintf(fp, "\n");
            printf("\n");
        }

        int arcsnum = 0;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < i; j++)
                if (a[i][j] != inf)
                    arcsnum++;
        printf("边数：%d", arcsnum);

        fclose(fp);
        return 0;
    }
    ```

## 关键逻辑

### 矩阵初始化

无向图中节点到自身的距离为 0，其余位置先设为无穷大（这里用 `99999` 代替）：

```cpp
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        a[i][j] = (i == j) ? 0 : inf;
```

### 随机生成边

最多尝试 400 次，每次随机选两个节点和一个权值。只有两节点之间尚未连通且不是同一点时，才添加边。因为是**无向图**，矩阵需要保持对称：

```cpp
for (int m = 0; m < 400; m++)
{
    int i = rand() % 20;
    int j = rand() % 20;
    int k = rand() % 40;
    if ((a[i][j] == inf && a[j][i] == inf) && i != j)
        a[i][j] = a[j][i] = k;
}
```

权值范围 0～39，由 `rand() % 40` 控制。

### 统计边数

无向图中一条边对应矩阵中两个对称位置，统计时只需要遍历上三角（`j < i`）：

```cpp
int arcsnum = 0;
for (int i = 0; i < n; i++)
    for (int j = 0; j < i; j++)
        if (a[i][j] != inf)
            arcsnum++;
```

### 时间戳命名

文件输出版本用当前时间生成文件名，格式为 `邻接矩阵 YYYY-MMDD-HHMMSS.txt`，避免多次运行时覆盖旧结果：

```cpp
char filename[256] = {0};
time(&timep);
p = localtime(&timep);
sprintf(filename, "邻接矩阵 %d-%02d%02d-%02d%02d%02d.txt",
        1900 + p->tm_year, 1 + p->tm_mon, p->tm_mday,
        p->tm_hour, p->tm_min, p->tm_sec);
```

`tm_year` 是从 1900 年起算的偏移量，所以需要 `+1900`；`tm_mon` 从 0 起算，需要 `+1`。

## 输出示例

```text
    0    23 99999 99999    15 ...
   23     0 99999     8 99999 ...
99999 99999     0    33 99999 ...
99999     8    33     0     2 ...
   15 99999 99999     2     0 ...
...
边数：47
```

实际边数取决于随机生成的重复命中率，通常远小于 400 次尝试的上限。
