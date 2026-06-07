---
date: 2026-05-22
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - 测试
---

# GoogleTest 基本用法

项目地址：[googletest](https://github.com/google/googletest)

GoogleTest（简称GTest）是由Google开发的C++测试框架，主要用于单元测试。它支持自动测试发现、丰富的断言、参数化测试等功能，适用于各种平台。以下是详细的用法介绍：

<!-- more -->

## 1. 基本结构

1. 测试用例（Test Case）：定义一组相关的测试
2. 测试（Test）：具体的测试函数
3. 断言（Assertion）：验证条件是否成立

## 2. 编写测试示例

```cpp
#include <gtest/gtest.h>

// 测试用例：TestSuiteName
// 测试：TestName
TEST(TestSuiteName, TestName) {
    int a = 1;
    int b = 2;
    EXPECT_EQ(a + b, 3); // 断言：相等
}
```

## 3. 常用断言

| 断言                     | 描述                                   | 示例                     |
|--------------------------|----------------------------------------|--------------------------|
| `EXPECT_EQ(val1, val2)`    | 期望两个值相等                         | `EXPECT_EQ(a, b);`        |
| `EXPECT_NE(val1, val2)`    | 期望两个值不相等                       | `EXPECT_NE(a, b);`        |
| `EXPECT_TRUE(cond)`        | 期望条件为真                           | `EXPECT_TRUE(ptr != nullptr);` |
| `EXPECT_FALSE(cond)`       | 期望条件为假                           | `EXPECT_FALSE(flag);`     |
| `EXPECT_THROW(stmt, exception_type)` | 期望语句抛出特定异常 | `EXPECT_THROW(func(), std::runtime_error);` |
| `EXPECT_NO_THROW(stmt)`    | 期望语句不抛出异常                     | `EXPECT_NO_THROW(func());` |

## 4. 参数化测试

- 值参数化：用不同参数多次运行同一测试

```cpp
class MyTest : public ::testing::TestWithParam<int> {};

TEST_P(MyTest, TestWithParam) {
    int n = GetParam();
    EXPECT_GT(n, 0);
}

INSTANTIATE_TEST_SUITE_P(PositiveNumbers, MyTest, ::testing::Values(1, 2, 3));
```

- 类型参数化：用不同数据类型测试

```cpp
template <typename T>
class MyTypeTest : public ::testing::Test {};

TYPED_TEST_SUITE_P(MyTypeTest);

TYPED_TEST_P(MyTypeTest, Test) {
    // 测试内容
}

REGISTER_TYPED_TEST_SUITE_P(MyTypeTest, Test);
```

## 5. 运行测试

- 使用`RUN_ALL_TESTS()`函数运行所有注册的测试

```cpp
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

## 6. 其他功能

- Death Tests：验证程序崩溃行为
- 自定义断言：定义自己的断言
- 测试过滤：只运行特定测试
- 并行测试：加快测试速度

## 7. 文档与资源
- 官方文档：[https://google.github.io/googletest/](https://google.github.io/googletest/)
- Primer教程：[https://google.github.io/googletest/primer.html](https://google.github.io/googletest/primer.html)
