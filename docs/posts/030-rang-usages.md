---
date: 2026-05-20
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - CMD
---

# rang 基本用法

项目地址：[rang](https://github.com/agauniyal/rang)

`rang` 是一个用于简化 C++ 控制台颜色和样式的库。以下是一些基本用法示例。

1. 设置文本颜色
2. 设置背景色
3. 添加样式（如粗体、下划线）
4. 组合多种样式
5. 重置样式

<!-- more -->

## 1. 设置文本颜色

```cpp
#include "rang.hpp"
#include <iostream>

int main() {
    std::cout << rang::fg::red << "这是红色文本" << rang::fg::reset << std::endl;
    std::cout << rang::fg::green << "这是绿色文本" << rang::fg::reset << std::endl;
    return 0;
}
```

## 2. 设置背景色

```cpp
#include "rang.hpp"
#include <iostream>

int main() {
    std::cout << rang::bg::yellow << "背景为黄色" << rang::bg::reset << std::endl;
    return 0;
}
```

## 3. 添加样式（粗体、下划线）

```cpp
#include "rang.hpp"
#include <iostream>

int main() {
    std::cout << rang::style::bold << "这是粗体文本" << rang::style::reset << std::endl;
    std::cout << rang::style::underline << "这是带下划线的文本" << rang::style::reset << std::endl;
    return 0;
}
```

## 4. 组合多种样式

```cpp
#include "rang.hpp"
#include <iostream>

int main() {
    std::cout << rang::fg::blue << rang::bg::white << rang::style::bold << "蓝色字体，白色背景，粗体" << rang::style::reset << rang::bg::reset << rang::fg::reset << std::endl;
    return 0;
}
```

## 5. 使用 `rang::style` 进行复杂样式

```cpp
#include "rang.hpp"
#include <iostream>

int main() {
    std::cout << rang::style::bold << rang::style::underline << "粗体且带下划线" << rang::style::reset << std::endl;
    return 0;
}
```
