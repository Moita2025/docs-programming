---
date: 2026-05-20
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - IO
  - 字符串
---

# fmt 基本用法

项目地址：[fmt](https://github.com/fmtlib/fmt)

fmt 的核心功能是：格式化字符串。

<!-- more -->

## 1. 安装 `fmt` 库

=== "vcpkg"

    ```bash
    vcpkg install fmt
    ```

=== "Conan"

    ```bash
    conan install fmt/9.1.0@
    ```

## 2. 基本用法示例

### 包含头文件

```cpp
#include <fmt/core.h>
#include <iostream>
```

### 简单格式化字符串

```cpp
std::string name = "Alice";
int age = 30;
std::string message = fmt::format("Hello, {}! You are {} years old.", name, age);
std::cout << message << std::endl;
```

### 直接打印到控制台

```cpp
fmt::print("This is a number: {}\n", 42);
```

## 3. 格式化选项

`fmt` 支持丰富的格式化选项，类似于 Python 的格式化语法。

### 数字格式化

```cpp
double pi = 3.1415926535;
fmt::print("Pi approximately: {:.2f}\n", pi); // 保留两位小数
```

### 宽度和对齐

```cpp
fmt::print("|{:10}|{:>10}|{:^10}|\n", "left", "right", "center");
```

### 填充字符

```cpp
fmt::print("{:*^20}\n", "Centered");
```

### 数字千位分隔符

```cpp
int large_number = 1234567890;
fmt::print("{:L}\n", large_number); // 需要启用 locale 支持
```

### 进制表示

```cpp
int num = 255;
fmt::print("Hex: {:#x}, Oct: {:#o}\n", num, num);
```

## 4. 高级用法示例

### 自定义类型的格式化

```cpp
struct Point {
    int x, y;
};

template <>
struct fmt::formatter<Point> {
    // 解析格式字符串（这里不使用特殊格式，直接忽略）
    constexpr auto parse(fmt::format_parse_context& ctx) { return ctx.begin(); }

    // 格式化输出
    auto format(const Point& p, fmt::format_context& ctx) {
        return fmt::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};

Point p{10, 20};
fmt::print("Point: {}\n", p);
```

### 复合类型（如容器）

```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
fmt::print("Vector: [{}]\n", fmt::join(vec, ", "));
```

### 处理异常

`fmt` 会在格式化错误时抛出异常，可以捕获处理：
```cpp
try {
    fmt::print("Number: {0}\n", "not a number");
} catch (const fmt::format_error& e) {
    std::cerr << "Format error: " << e.what() << std::endl;
}
```

## 5. 其他常用函数

| 函数 | 描述 | 示例 |
|--------|--------|--------|
| `fmt::format()` | 返回格式化字符串 | `auto s = fmt::format("Hello, {}!", "world");` |
| `fmt::print()` | 直接输出格式化内容 | `fmt::print("Number: {}\n", 42);` |
| `fmt::format_to()` | 格式化到输出迭代器 | `fmt::format_to(std::back_inserter(vec), "{}", 123);` |
| `fmt::join()` | 连接容器元素 | `fmt::join(vec, ", ")` |
