---
date: 2026-06-07
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
---

# C++ 将 initializer_list 作为函数参数

一段简短示例，演示 C++11 的 `std::initializer_list` 如何让函数接受花括号初始化列表 `{1,2,3,4,5}` 作为参数。

<!-- more -->

## 原始代码

```cpp
#include <stdio.h>
#include <iostream>

void func(std::initializer_list<int> a)
{
    for (auto i = a.begin(); i < a.end(); i++)
        printf("%d ", *i);
}

int main()
{
    func({1, 2, 3, 4, 5});
    return 0;
}
```

## 问题

### 缺少 `#include <initializer_list>`

`std::initializer_list` 的完整定义在 `<initializer_list>` 头文件中。虽然许多编译器在引入 `<iostream>` 时会间接包含它，但 C++ 标准不保证这一点。缺失该头文件在某些环境下会导致编译失败。

### 迭代器比较用 `<` 而非 `!=`

`initializer_list` 的迭代器是随机访问迭代器，`<` 比较在此处能正常工作。但习惯上应使用 `!=`——它适用于所有迭代器类别，且是范围 for 循环展开后的等价写法。

### 混用 C 与 C++ 输出

同时包含 `<stdio.h>` 和 `<iostream>`，却只用 `printf`。可以统一为 `std::cout` 以保持 C++ 风格。

## 修正后代码

```cpp
#include <initializer_list>                     // 新增：显式包含头文件
#include <iostream>

void func(std::initializer_list<int> a)
{
    for (auto i = a.begin(); i != a.end(); i++) // 修正：!= 替代 <
        std::cout << *i << " ";                 // 修正：cout 替代 printf
}

int main()
{
    func({1, 2, 3, 4, 5});
    return 0;
}
```

三处改动都很小，但让代码在不同编译环境下更可靠，风格也更统一。

`std::initializer_list` 本身是一个轻量级的只读容器，不支持修改元素，底层通常指向编译器生成的临时数组。除了作为函数参数，它也广泛用于标准库容器的列表构造——比如 `std::vector<int> v = {1, 2, 3}` 正是通过接收 `initializer_list` 的构造函数实现的。
