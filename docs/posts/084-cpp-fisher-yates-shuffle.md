---
date: 2026-06-07
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
---

# C++ 随机不重复生成（Fisher–Yates 洗牌）

一段用 Fisher–Yates 算法从指定范围随机抽取不重复整数的代码。核心逻辑正确，但存在几个工程上的粗心之处。

<!-- more -->

## 原始代码

```cpp
#include <iostream>
#include <stdlib.h>
#include <time.h>

using namespace std;

int a[50], j[50];

int main()
{
    void shuiji(int, int);
    shuiji(20, 50);
    for (int i = 0; i < 35 - 20 + 1; i++)
        cout << j[i] << " ";
    getchar();
}

void shuiji(int min, int max)
{
    int num = max - min + 1;
    int index;
    for (int i = 0; i < num; i++)
        a[i] = i + min;
    srand((int)time(0));
    for (int i = 0; i < num; i++)
    {
        index = (int)((float)(num - i) * rand() / (RAND_MAX + 1.0));
        j[i] = a[index];
        a[index] = a[num - 1 - i];
    }
}
```

## 算法解析

这段代码实现的是 **Fisher–Yates 洗牌算法** 的部分抽取版本：

1. 将 `[min, max]` 范围内的整数依次放入数组 `a`
2. 设 `num = max - min + 1`，第 i 轮在 `a[0 .. num-i-1]` 中随机抽一个下标 `index`
3. 将 `a[index]` 存入结果数组 `j[i]`
4. 用当前未抽区间的最后一个元素 `a[num-1-i]` 填补被抽走的位置
5. 下一轮未抽区间缩短一个元素，重复直到抽完

每个数恰好被选中一次，保证了不重复。每次抽取的概率均等。

## 问题

### srand 放在函数内部

`srand` 应在整个程序生命周期内只调用一次（通常放在 `main` 开头）。放在 `shuiji` 内部意味着如果连续多次调用 `shuiji`，且两次调用发生在同一秒内，`time(0)` 返回相同的种子，两轮随机序列完全一样。

### 打印循环与生成范围不匹配

```cpp
shuiji(20, 50);                          // 生成 31 个数
for (int i = 0; i < 35 - 20 + 1; i++)    // 35-20+1 = 16，只打了 16 个
```

打印循环的范围 `35` 与函数调用的 `50` 不一致，像是改参数后忘记同步。应该用变量统一管理。

### 全局数组硬编码大小

`a[50]` 和 `j[50]` 写死了 50。如果 `max - min + 1 > 50`，数组越界。应在运行期分配或至少做边界检查。

### C 风格头文件

`<stdlib.h>` 和 `<time.h>` 在 C++ 中对应 `<cstdlib>` 和 `<ctime>`。

## 修正后代码

```cpp
#include <iostream>
#include <cstdlib>                             // 修正：C++ 风格头文件
#include <ctime>                               // 修正：C++ 风格头文件

using namespace std;

void shuiji(int min, int max, int result[])    // 修正：结果数组由调用方传入
{
    int num = max - min + 1;
    int *a = new int[num];                     // 修正：动态分配，消除硬编码
    for (int i = 0; i < num; i++)
        a[i] = i + min;
    for (int i = 0; i < num; i++)
    {
        int index = rand() % (num - i);         // 修正：简化随机下标计算
        result[i] = a[index];
        a[index] = a[num - 1 - i];
    }
    delete[] a;                                // 新增：释放临时数组
}

int main()
{
    srand((unsigned int)time(0));              // 修正：种子只设一次
    const int MIN = 20, MAX = 50;              // 新增：用常量统一范围
    const int NUM = MAX - MIN + 1;

    int *j = new int[NUM];                     // 修正：动态分配结果数组
    shuiji(MIN, MAX, j);

    for (int i = 0; i < NUM; i++)              // 修正：打印范围与生成范围一致
        cout << j[i] << " ";
    cout << endl;

    delete[] j;                                // 新增：释放结果数组
    return 0;
}
```

改动汇总：

| 位置 | 原写法 | 修正 |
| :--- | :--- | :--- |
| 头文件 | `<stdlib.h>` `<time.h>` | `<cstdlib>` `<ctime>` |
| `srand` 位置 | `shuiji` 内部每次调用 | `main` 开头仅一次 |
| 数组 | 全局 `a[50]` `j[50]` | 动态分配 `new int[num]` |
| 打印范围 | 硬编码 `35-20+1` | 使用 `NUM` 变量 |
| 随机下标 | `(int)((float)...)` | `rand() % (num - i)` |

核心算法 `shuiji` 本身没有变动——Fisher–Yates 的实现是正确的，修正集中在边界管理和工程规范上。
