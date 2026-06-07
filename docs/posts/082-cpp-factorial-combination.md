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

# C++ 阶乘与排列组合

一段计算阶乘、排列和组合的 C 代码。核心公式存在错误，`a()` 和 `c()` 返回的结果与标准排列组合定义不符。

<!-- more -->

## 原始代码

```c
#include <stdio.h>

long long jc(int val)
{
    if (val == 0 || val == 1)
        return 1;
    else
        return val * jc(val - 1);
}

long long a(int n, int m)
{
    if (n >= m)
        return (jc(n) / jc(m));
    else
        return 1;
}

long long c(int n, int m)
{
    if (n >= m)
        return (a(n, m) / jc(m));
    else
        return 1;
}

int main()
{
    double ans = jc(20);
    printf("%lf", ans);
    return 0;
}
```

## 公式错误

排列的标准定义：

\[
A(n, m) = \frac{n!}{(n - m)!}
\]

即从 n 个元素中取出 m 个进行排列的方案数。代码中 `a()` 的分母是 `m!` 而非 `(n-m)!`，计算结果与标准排列无关。例如 A(5,2) = 5!/3! = 20，但 `a(5,2)` = 5!/2! = 60。

组合的标准定义：

\[
C(n, m) = \frac{n!}{m! \cdot (n - m)!}
\]

即从 n 个元素中选取 m 个的方案数。`c()` 基于错误的 `a()` 计算，结果为 n!/(m!·m!)。例如 C(5,2) = 10，但 `c(5,2)` = 5!/(2!·2!) = 30。

当 n < m 时两个函数均返回 1，而标准定义下应返回 0（无法从较少元素中取出较多元素排列或组合）。

### 修正

```c
long long a(int n, int m)
{
    if (n >= m)
        return jc(n) / jc(n - m);            // 修正：分母为 (n-m)! 而非 m!
    else
        return 0;                            // 修正：非法输入返回 0
}

long long c(int n, int m)
{
    if (n >= m)
        return a(n, m) / jc(m);              // 此时内部为 n!/((n-m)!·m!) 即标准组合公式
    else
        return 0;
}
```

---

## 拓展：避免阶乘溢出

`long long` 只能容纳到 20!。直接计算 n! 再相除，中间结果很容易溢出——即使最终结果在范围内。比如 C(30, 5) = 142506 远小于 2⁶³，但 30! 早已超过 `long long` 上限。

改用逐项乘除的方法，边乘边除，将中间值始终控制在结果附近：

```c
long long C_safe(int n, int m)
{
    if (m < 0 || m > n) return 0;
    if (m > n - m) m = n - m;                // 利用对称性 C(n,m)=C(n,n-m)，减少运算
    long long result = 1;
    for (int i = 1; i <= m; i++)
    {
        result = result * (n - m + i) / i;   // 逐项乘 (n-m+i) 再除 i，保证整除
    }
    return result;
}
```

以 C(30, 5) 为例，运算过程：

```
i=1: result = 1 * 26 / 1 = 26
i=2: result = 26 * 27 / 2 = 351
i=3: result = 351 * 28 / 3 = 3276
i=4: result = 3276 * 29 / 4 = 23751
i=5: result = 23751 * 30 / 5 = 142506
```

每一步的结果都恰好是组合数的中间值 `C(n-m+i, i)`，始终为整数，不会溢出。

同样地，阶乘本身也可改为迭代以消除递归开销：

```c
long long jc_iter(int val)
{
    long long result = 1;
    for (int i = 2; i <= val; i++)
        result *= i;
    return result;
}
```

## 完整修正版

```c
#include <stdio.h>

long long jc(int val)                          // 修正：改为迭代，避免递归栈开销
{
    long long result = 1;
    for (int i = 2; i <= val; i++)
        result *= i;
    return result;
}

long long A(int n, int m)                      // 修正：公式与返回值
{
    if (m < 0 || m > n) return 0;
    return jc(n) / jc(n - m);
}

long long C(int n, int m)                      // 修正：公式与返回值
{
    if (m < 0 || m > n) return 0;
    if (m > n - m) m = n - m;
    long long result = 1;
    for (int i = 1; i <= m; i++)
        result = result * (n - m + i) / i;
    return result;
}

int main()
{
    printf("A(5,2) = %lld\n", A(5, 2));        // 修正：%lld 而非 double
    printf("C(5,2) = %lld\n", C(5, 2));
    printf("C(30,5) = %lld\n", C(30, 5));
    return 0;
}
```
