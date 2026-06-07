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

# lest 基本用法

项目地址：[lest](https://github.com/martinmoene/lest)

一个现代化的、C++11原生的、仅包含头文件的、小巧的单元测试、TDD 和 BDD 框架（包含 C++98 变体）

<!-- more -->

## 1. 引入和基础示例

```cpp
#include "lest/lest.hpp"

using namespace std;

const lest::test specification[] =
{
    CASE( "示例测试：字符串长度" )
    {
        EXPECT( 0 == string( ).length() );
        EXPECT( 0 == string("").length() );
    }
};

int main( int argc, char * argv[] )
{
    return lest::run( specification, argc, argv );
}
```

## 2. 测试用例定义

### 2.1 使用 `CASE` 宏定义测试

- **语法：**

```cpp
CASE( "测试描述" )
{
    // 测试代码和断言
}
```

- **示例：**

```cpp
CASE( "整数相加" )
{
    EXPECT( (2 + 2) == 4 );
}
```

### 2.2 自动注册测试用例

- **用法：**

```cpp
lest::CASE( "描述" )
{
    // 测试内容
}
```

- **说明：** 这种方式会自动注册测试，无需手动添加到数组中。

## 3. 断言宏

### 3.1 常用断言

| 宏名 | 描述 | 示例 |
|--------|--------|--------|
| `EXPECT(expr)` | 断言表达式为真，失败则报告 | `EXPECT( x == 10 );` |
| `EXPECT_NOT(expr)` | 断言表达式为假 | `EXPECT_NOT( ptr == nullptr );` |
| `EXPECT_THROWS(expr)` | 断言表达式抛出异常 | `EXPECT_THROWS( throw std::runtime_error("error") );` |
| `EXPECT_THROWS_AS(expr, exception_type)` | 断言抛出特定类型异常 | `EXPECT_THROWS_AS( throw std::bad_alloc(), std::bad_alloc );` |
| `EXPECT_NO_THROW(expr)` | 断言表达式不抛出异常 | `EXPECT_NO_THROW( some_function() );` |

### 3.2 断言示例

```cpp
EXPECT( 1 + 1 == 2 );
EXPECT_NOT( false );
EXPECT_THROWS( throw std::runtime_error("fail") );
EXPECT_THROWS_AS( throw std::bad_alloc(), std::bad_alloc );
EXPECT_NO_THROW( some_function() );
```

## 4. 其他宏和功能

### 4.1 浮点数近似比较

- **使用 `approx` 类：**

```cpp
EXPECT( 3.14 == approx( 3.14 ) );
EXPECT( 3.14 != approx( 3.15 ).epsilon( 0.01 ) );
```

### 4.2 使用测试夹具（Fixtures）

- **定义：**

```cpp
SETUP( "初始化" )
{
    // 初始化代码
}
SECTION( "测试子场景" )
{
    // 测试内容
}
```

- **示例：**

```cpp
SETUP( "准备环境" )
{
    int x = 0;
    SECTION( "测试加法" )
    {
        x += 1;
        EXPECT( x == 1 );
    }
}
```

### 4.3 行为驱动开发（BDD）风格宏

```cpp
SCENARIO( "用户登录流程" )
{
    GIVEN( "用户未登录" )
    {
        // 设置
        WHEN( "用户输入正确的凭据" )
        {
            // 操作
            THEN( "登录成功" )
            {
                // 断言
            }
        }
    }
}
```

## 5. 运行测试

- **定义测试规格：**

```cpp
const lest::test specification[] = {
    CASE( "示例" )
    {
        EXPECT( true );
    }
};
```

- **执行：**

```cpp
int main( int argc, char *argv[] )
{
    return lest::run( specification, argc, argv );
}
```

- **命令行参数支持：**

    - `-h`：显示帮助
    - `-a`：遇到第一个失败即停止
    - `-c`：统计测试数量
    - `-p`：显示所有通过的测试
    - `-t`：显示测试耗时
    - `--order=declared|lexical|random`：控制测试顺序
    - `--random-seed=n`：随机种子
    - `--repeat=n`：重复测试次数

## 6. 其他高级特性

- **模块化测试：**

```cpp
MODULE( "模块名", specification );
```

- **自定义报告器：**

可以自定义测试报告输出。

- **支持多平台：**

支持 Windows、Linux、macOS 等。

## 7. 参考资料

- [示例代码](https://github.com/martinmoene/lest/tree/master/example)
