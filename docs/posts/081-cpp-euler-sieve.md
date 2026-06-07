---
date: 2026-06-07
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数学
---

# C++ 欧拉线性筛求素数

一段欧拉筛（线性筛）的实现，在筛选 2~n 之间素数的同时记录每个数的最小质因子。时间复杂度 O(n)，是已知最快的素数筛法之一。

<!-- more -->

## 原始代码

```cpp
#include <cstdio>
#include <iostream>
#include <cstring>
using namespace std;
#define MAXN_N 1000001
int v[MAXN_N], primes[MAXN_N];
int main()
{
    int n, m = 0;
    cout << "输入 n 的值：" << endl;
    scanf("%d", &n);
    memset(v, 0, sizeof(v));
    for (int i = 2; i <= n; i++)
    {
        if (v[i] == 0)
        {
            v[i] = i;
            primes[++m] = i;
        }
        for (int j = 1; j <= m; j++)
        {
            if (primes[j] > v[i] || primes[j] > n / i) break;
            v[i * primes[j]] = primes[j];
        }
    }
    for (int i = 1; i <= m; i++) cout << primes[i] << " ";
    return 0;
}
```

## 算法思路

欧拉筛的核心在于**每个合数只被它的最小质因子筛掉一次**，从而将复杂度压到 O(n)。

逐行解读：

**`v[i] == 0`** —— `v` 数组初始全零。遍历到 i 时如果 `v[i]` 仍为 0，说明之前没有任何质数能"标记"它，那它本身就是素数。随即记录 `primes[++m] = i` 并将 `v[i]` 设为 i。

**内层循环** —— 用已知素数 `primes[j]` 去标记合数 `i * primes[j]`，将其最小质因子记录为 `primes[j]`。两个 break 条件：

- `primes[j] > v[i]`：i 的最小质因子比当前的 `primes[j]` 还小，说明继续用更大的质数标记会产生"被非最小质因子筛掉"的重复操作。此时退出，保证每个合数只被筛一次。
- `primes[j] > n / i`：`i * primes[j]` 已超出范围，无需继续。

## 与埃氏筛的对比

经典的埃拉托色尼筛在标记 2 的倍数、3 的倍数、5 的倍数时，会重复标记 6、12、18 这样的数——每个合数被它的各个质因子各筛一次。复杂度为 O(n log log n)。

欧拉筛通过 `primes[j] > v[i]` 这条约束，让内层循环提前退出，保证每个合数只在遇到其**最小质因子**时被标记。例如合数 12 的最小质因子是 2，当 i=6、primes[j]=2 时被标记为 `v[12]=2`；而当 i=4、primes[j]=3 时，因为 `v[4]=2 < 3`，循环直接 break，避免了重复标记。

## 问题与修正

### 缺少输入范围校验

用户输入 n ≥ MAXN_N 时会越界访问 `v[n]`。增加检查：

```cpp
scanf("%d", &n);
if (n >= MAXN_N)                            // 新增：越界检查
{
    cout << "n 不能超过 " << MAXN_N - 1 << endl;
    return 1;
}
```

### primes 数组尺寸过大

`primes[MAXN_N]` 预留了约 100 万个位置，但 π(10⁶) 只有约 7.8 万个素数。修正为适度大小：

```cpp
#define MAXN_N 1000001
#define MAX_PRIMES 80000                    // 新增：π(10^6) ≈ 78498
int v[MAXN_N], primes[MAX_PRIMES];
```

### iostream 与 C I/O 混用

`cout` 和 `scanf` 共用同一程序时，若后续调用 `ios::sync_with_stdio(false)` 关闭同步，输出顺序可能错乱。这里未关闭同步，实际运行无问题，但更一致的写法是统一使用 C++ 风格 `cin >> n`。

## 修正后代码

```cpp
#include <cstdio>
#include <iostream>
#include <cstring>
using namespace std;
#define MAXN_N 1000001
#define MAX_PRIMES 80000                    // 新增：合理分配素数数组大小

int v[MAXN_N], primes[MAX_PRIMES];

int main()
{
    int n, m = 0;
    cout << "输入 n 的值：" << endl;
    scanf("%d", &n);
    if (n >= MAXN_N)                         // 新增：越界检查
    {
        cout << "n 不能超过 " << MAXN_N - 1 << endl;
        return 1;
    }
    memset(v, 0, sizeof(v));
    for (int i = 2; i <= n; i++)
    {
        if (v[i] == 0)
        {
            v[i] = i;
            primes[++m] = i;
        }
        for (int j = 1; j <= m; j++)
        {
            if (primes[j] > v[i] || primes[j] > n / i) break;
            v[i * primes[j]] = primes[j];
        }
    }
    for (int i = 1; i <= m; i++)
        cout << primes[i] << " ";
    return 0;
}
```
