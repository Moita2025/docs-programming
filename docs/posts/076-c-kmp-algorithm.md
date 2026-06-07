---
date: 2026-06-07
authors:
  - moita
categories:
  - 算法
tags:
  - C
  - 字符串
  - 数据结构
---

# C 语言 KMP 字符串匹配

一段 KMP 算法的 C 实现，在 `"ababcabcacbab"` 中查找 `"abcac"`。代码逻辑正确，但存在一个严重性能问题和一个硬编码隐患。

<!-- more -->

## 原始代码

```c
#include <stdio.h>
#include <string.h>

void Next(char *T, int *next)
{
    int i = 1;
    next[1] = 0;
    int j = 0;
    while (i < strlen(T))
    {
        if (j == 0 || T[i - 1] == T[j - 1])
        {
            i++;
            j++;
            next[i] = j;
        }
        else
        {
            j = next[j];
        }
    }
}

int KMP(char *S, char *T)
{
    int next[10];
    Next(T, next);
    int i = 1;
    int j = 1;
    while (i <= strlen(S) && j <= strlen(T))
    {
        if (j == 0 || S[i - 1] == T[j - 1])
        {
            i++;
            j++;
        }
        else
        {
            j = next[j];
        }
    }
    if (j > strlen(T))
    {
        return i - (int)strlen(T);
    }
    return -1;
}

int main()
{
    int i = KMP("ababcabcacbab", "abcac");
    printf("%d", i);
    return 0;
}
```

## 问题

### `strlen` 在循环条件中重复调用

`Next` 和 `KMP` 两个函数的 `while` 条件里都直接写了 `strlen(T)` 或 `strlen(S)`。`strlen` 本身是 O(k) 操作——它需要遍历整个字符串才能得到长度。每次循环迭代都调用一次 `strlen`，KMP 的 O(n+m) 复杂度直接退化成了 O(n*m)。

KMP 算法的核心优势正是利用已匹配信息避免主串指针回退，而循环条件里的 `strlen` 恰好抵消了这个优势。每次迭代都做一次全字符串扫描，和朴素匹配没有本质区别。

### `next[10]` 硬编码大小

模式串长度超过 9 时（1-indexed 下 `next` 需要 `lenT+1` 个元素），数组越界。虽然测试用例中 `"abcac"` 只有 5 个字符没问题，但作为通用实现，这个硬编码值是个隐患。

## 修正后代码

```c
#include <stdio.h>
#include <string.h>

#define MAX_PATTERN 100                            // 新增：模式串最大长度

void Next(char *T, int *next, int len)              // 修正：增加 len 参数
{
    int i = 1;
    next[1] = 0;
    int j = 0;
    while (i < len)                                 // 修正：使用参数替代 strlen
    {
        if (j == 0 || T[i - 1] == T[j - 1])
        {
            i++;
            j++;
            next[i] = j;
        }
        else
        {
            j = next[j];
        }
    }
}

int KMP(char *S, char *T)
{
    int lenS = (int)strlen(S);                      // 修正：缓存长度
    int lenT = (int)strlen(T);                      // 修正：缓存长度
    if (lenT + 1 > MAX_PATTERN)                     // 新增：越界检查
        return -1;
    int next[MAX_PATTERN];                          // 修正：用宏替代硬编码 10
    Next(T, next, lenT);                            // 修正：传入长度
    int i = 1;
    int j = 1;
    while (i <= lenS && j <= lenT)                  // 修正：使用缓存值
    {
        if (j == 0 || S[i - 1] == T[j - 1])
        {
            i++;
            j++;
        }
        else
        {
            j = next[j];
        }
    }
    if (j > lenT)                                   // 修正：使用缓存值
        return i - lenT;
    return -1;
}

int main()
{
    int i = KMP("ababcabcacbab", "abcac");
    printf("%d", i);
    return 0;
}
```

核心修正只有两处：**把 `strlen` 调用提到循环外缓存**，以及**用 `#define` 替换硬编码的数组大小**。前者恢复了 KMP 应有的 O(n+m) 复杂度，后者消除了越界风险。

## 关于 1-indexed

代码全程使用 1-indexed 下标——`next[1]` 而非 `next[0]`，主串和模式串也从位置 1 开始匹配。这是许多 KMP 教材中的写法，好处是 next 值的含义与下标编号直观对应（`next[i]` 直接表示第 i 个字符失配时跳转到的位置）。代价是 C 数组的第 0 个元素始终闲置，且数组大小需要比串长多 1。
