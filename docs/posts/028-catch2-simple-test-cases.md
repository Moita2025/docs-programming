---
date: 2026-05-09
authors:
  - moita
categories:
  - 工程实践
tags:
  - C++
  - Catch2
  - 测试
---

# Catch2 基本测试用例

Catch2 是一个现代 C++ 单元测试框架，支持 `TEST_CASE`、`SECTION`、BDD 风格等。

项目地址：[Catch2](https://github.com/catchorg/Catch2)

<!-- more -->

## 配置方法

### 1. GitHub Release amalgamated 版本

**1. 源代码文件 `test.cpp`**

```cpp
#define CATCH_CONFIG_MAIN
#include "catch_amalgamated.hpp"
```

**2. 编译命令**

```cmd
g++ test.cpp catch_amalgamated.cpp -std=c++17 -o test
```
### 2. CMake FetchContent

```cmake
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.5.2
)
```

然后：

```cpp
#include <catch2/catch_test_macros.hpp>
```

## 1. 最简单的测试

```cpp
#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>

int add(int a, int b)
{
    return a + b;
}

TEST_CASE("加法函数测试", "[math]")
{
    REQUIRE(add(1, 2) == 3);
    REQUIRE(add(-1, 1) == 0);
}
```

* `TEST_CASE` 定义测试用例
* `REQUIRE` 断言失败后立即终止当前测试
* `[math]` 是 tag，可用于过滤测试

## 2. CHECK 与 REQUIRE 的区别

```cpp
#include <catch2/catch_test_macros.hpp>

TEST_CASE("CHECK 示例")
{
    CHECK(1 + 1 == 2);
    CHECK(2 * 2 == 4);

    // 即使失败，也继续执行后面的检查
    CHECK(2 - 1 == 0);

    CHECK(10 / 2 == 5);
}
```

区别：

| 宏       | 失败后      |
| ------- | -------- |
| REQUIRE | 立即停止当前测试 |
| CHECK   | 继续执行     |

## 3. 使用 SECTION

适合复用初始化代码。

```cpp
#include <catch2/catch_test_macros.hpp>
#include <vector>

TEST_CASE("vector 测试")
{
    std::vector<int> vec = {1, 2, 3};

    SECTION("size 检查")
    {
        REQUIRE(vec.size() == 3);
    }

    SECTION("push_back 检查")
    {
        vec.push_back(4);

        REQUIRE(vec.size() == 4);
        REQUIRE(vec.back() == 4);
    }

    SECTION("clear 检查")
    {
        vec.clear();

        REQUIRE(vec.empty());
    }
}
```

`SECTION` 会分别运行，每次都会重新初始化 `vec`。 (Stack Overflow[^1])

## 4. 异常测试

```cpp
#include <catch2/catch_test_macros.hpp>
#include <stdexcept>

int divide(int a, int b)
{
    if (b == 0)
        throw std::runtime_error("divide by zero");

    return a / b;
}

TEST_CASE("异常测试")
{
    REQUIRE(divide(10, 2) == 5);

    REQUIRE_THROWS(divide(10, 0));

    REQUIRE_THROWS_AS(
        divide(10, 0),
        std::runtime_error
    );
}
```

常用宏：

| 宏                 | 作用        |
| ----------------- | --------- |
| REQUIRE_THROWS    | 要求抛异常     |
| REQUIRE_THROWS_AS | 要求抛指定类型异常 |
| REQUIRE_NOTHROW   | 不允许异常     |

## 5. 字符串测试

```cpp
#include <catch2/catch_test_macros.hpp>
#include <string>

TEST_CASE("字符串测试")
{
    std::string s = "hello";

    REQUIRE(s.size() == 5);

    CHECK(s == "hello");

    CHECK_FALSE(s.empty());
}
```

## 6. BDD 风格测试

Catch2 支持 Given/When/Then 风格。 (Builder.io[^2])

```cpp
#include <catch2/catch_test_macros.hpp>
#include <vector>

SCENARIO("vector 可以动态扩容")
{
    GIVEN("一个包含 3 个元素的 vector")
    {
        std::vector<int> v = {1, 2, 3};

        WHEN("插入一个新元素")
        {
            v.push_back(4);

            THEN("size 应该变为 4")
            {
                REQUIRE(v.size() == 4);
            }

            THEN("最后一个元素应该是 4")
            {
                REQUIRE(v.back() == 4);
            }
        }
    }
}
```

## 7. 参数化模板测试

适合泛型代码。 (DeepWiki[^3])

```cpp
#include <catch2/catch_template_test_macros.hpp>

template<typename T>
T square(T x)
{
    return x * x;
}

TEMPLATE_TEST_CASE(
    "square 测试",
    "[template]",
    int,
    float,
    double)
{
    REQUIRE(square(TestType(3)) == TestType(9));
}
```

## 8. 运行测试

编译：

```bash
g++ test.cpp -std=c++17
```

运行：

```bash
./a.out
```

按 tag 运行：

```bash
./a.out [math]
```

只运行某个测试：

```bash
./a.out "加法函数测试"
```

Catch2 支持通过名字和 tag 过滤测试。 (DeepWiki[^4])

[^1]: ["unit testing - [UT][Catch2] Several test cases or one with several sections - Stack Overflow"](https://stackoverflow.com/questions/74489992/utcatch2-several-test-cases-or-one-with-several-sections) 
[^2]: ["Catch2 Overview, Examples, Pros and Cons in 2025"](https://best-of-web.builder.io/library/catchorg/Catch2) 
[^3]: ["Template Test Cases | catchorg/Catch2 | DeepWiki"](https://deepwiki.com/catchorg/Catch2/2.2-template-test-cases) 
[^4]: ["Test Filtering | catchorg/Catch2 | DeepWiki"](https://deepwiki.com/catchorg/Catch2/6.1-test-filtering) 
