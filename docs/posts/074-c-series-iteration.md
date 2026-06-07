---
date: 2026-06-07
authors:
  - moita
categories:
  - 算法
tags:
  - C
  - 理论概念
  - 数学
---

# C 语言无穷级数逼近：单循环与双重循环

两个 C 程序以不同循环结构计算同一无穷级数的部分和。双重循环版本每次从头累乘，时间复杂度 O(n²)；单循环版本利用递推关系，时间复杂度 O(n)。两者结果一致，但运行效率差异显著。

<!-- more -->

## 数学背景

程序计算的级数为：

\[
S_n = 1 + \left(-\frac{1}{x}\right) + \left(-\frac{1}{x}\right)^2 + \left(-\frac{1}{x}\right)^3 + \dots + \left(-\frac{1}{x}\right)^n = \sum_{i=0}^{n} \left(-\frac{1}{x}\right)^i
\]

当 \(|x| > 1\) 时，无穷级数收敛于：

\[
S_{\infty} = \frac{1}{1 - (-\frac{1}{x})} = \frac{x}{x + 1}
\]

两个程序通过 `scanf` 读入 \(x\) 和项数 \(n\)，输出部分和及运行耗时。

---

## 双重循环版本 O(n²)

每一项从 1 开始，内层循环逐次乘以 \(-\frac{1}{x}\) 共 \(i\) 次，等于独立重算每一项的幂。

```c
#include <stdio.h>
#include <sys/timeb.h>

int main()
{
    struct timeb t1, t2;
    long t;
    double x, sum = 1, sum1;
    int i, j, n;

    printf("enter x and n\n");
    scanf("%lf %d", &x, &n);
    ftime(&t1);
    for (i = 1; i <= n; i++)
    {
        sum1 = 1;
        for (j = 1; j <= i; j++)
            sum1 = -sum1 / x;
        sum += sum1;
    }
    ftime(&t2);
    t = (t2.time - t1.time) * 1000 + (t2.millitm - t1.millitm);
    printf("sum = %lf 用时 %ld 毫秒\n", sum, t);

    return 0;
}
```

### 修正后代码

原始代码缺少输入验证，且 `scanf` 未检查返回值。若用户输入非数字或 `x = 0`，程序会静默出错或除零崩溃。

```c
#include <stdio.h>
#include <sys/timeb.h>

int main()
{
    struct timeb t1, t2;
    long t;
    double x, sum = 1, sum1;
    int n;

    printf("enter x and n\n");
    if (scanf("%lf %d", &x, &n) != 2)          // 新增：检查输入是否成功读入两个值
    {
        printf("输入格式错误\n");
        return 1;
    }
    if (x == 0)                                // 新增：防止除零错误
    {
        printf("x 不能为 0\n");
        return 1;
    }

    ftime(&t1);
    for (int i = 1; i <= n; i++)               // 修正：变量声明移至使用位置
    {
        sum1 = 1;
        for (int j = 1; j <= i; j++)           // 修正：变量声明移至使用位置
            sum1 = -sum1 / x;
        sum += sum1;
    }
    ftime(&t2);
    t = (t2.time - t1.time) * 1000 + (t2.millitm - t1.millitm);
    printf("sum = %lf 用时 %ld 毫秒\n", sum, t);

    return 0;                                  // 新增：显式返回值
}
```

外循环 \(n\) 次，第 \(i\) 次迭代时内循环执行 \(i\) 次，总操作次数为 \(1 + 2 + \dots + n = \frac{n(n+1)}{2}\)，即 \(O(n^2)\)。

---

## 单循环版本 O(n)

观察级数的递推关系：第 \(i\) 项与第 \(i-1\) 项仅差一个因子 \(-\frac{1}{x}\)。因此无需从头重算，直接在前一项基础上乘一次即可。

```c
#include <stdio.h>
#include <sys/timeb.h>

int main()
{
    struct timeb t1, t2;
    long t;
    double x, sum = 1, sum1 = 1;
    int i, n;

    printf("enter x and n\n");
    scanf("%lf %d", &x, &n);
    ftime(&t1);
    for (i = 1; i <= n; i++)
    {
        sum1 = -sum1 / x;
        sum += sum1;
    }
    ftime(&t2);
    t = (t2.time - t1.time) * 1000 + (t2.millitm - t1.millitm);
    printf("sum = %lf 用时 %ld 毫秒\n", sum, t);

    return 0;
}
```

### 修正后代码

```c
#include <stdio.h>
#include <sys/timeb.h>

int main()
{
    struct timeb t1, t2;
    long t;
    double x, sum = 1, sum1 = 1;
    int n;

    printf("enter x and n\n");
    if (scanf("%lf %d", &x, &n) != 2)          // 新增：检查输入
    {
        printf("输入格式错误\n");
        return 1;
    }
    if (x == 0)                                // 新增：防止除零错误
    {
        printf("x 不能为 0\n");
        return 1;
    }

    ftime(&t1);
    for (int i = 1; i <= n; i++)               // 修正：变量声明移至使用位置
    {
        sum1 = -sum1 / x;
        sum += sum1;
    }
    ftime(&t2);
    t = (t2.time - t1.time) * 1000 + (t2.millitm - t1.millitm);
    printf("sum = %lf 用时 %ld 毫秒\n", sum, t);

    return 0;                                  // 新增：显式返回值
}
```

循环体内只有常数次操作，总复杂度 \(O(n)\)。当 \(n\) 较大时，与双重循环版本的速度差异会非常明显。

---

## 复杂度对比

| 版本 | 循环结构 | 时间复杂度 | 说明 |
| :--- | :--- | :--- | :--- |
| 双重循环 | 内外两层 `for` | \(O(n^2)\) | 每一项独立从头计算 |
| 单循环 | 单层 `for` | \(O(n)\) | 利用前一项递推下一项 |

两种写法得到相同的数值结果，但单循环版本避免了大量重复的浮点乘除运算。这个例子展示了"找到递推关系"在数值计算中的重要性——当内层循环的逻辑可以合并到外层时，复杂度往往能从平方级降至线性级。

程序使用 `ftime` 记录运行前后的毫秒级时间戳，方便直接对比两种实现的耗时差异。
