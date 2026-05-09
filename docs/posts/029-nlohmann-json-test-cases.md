---
date: 2026-05-09
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - C++
  - json
  - 测试
---

# nlohmann-json 基本测试用例

项目地址：[nlohmann-json](https://github.com/nlohmann/json)

下面给你一套比较完整的 `nlohmann-json.hpp` 测试用例，适合：

* 单元测试
* CI 测试
* 验证 JSON 功能
* 学习 API

我按“基础 → 常用 → 异常 → 高级”来写。

<!-- more -->

## 0. 配置方法

=== "GitHub Release 版本"

    ```cpp
    #include <nlohmann/json.hpp>
    //或者
    #include "json.hpp"
    ```

=== "CMake FetchContent"

    ```cmake
    cmake_minimum_required(VERSION 3.15)

    project(TestJson)

    set(CMAKE_CXX_STANDARD 17)

    include(FetchContent)

    FetchContent_Declare(
        json
        URL https://github.com/nlohmann/json/releases/download/v3.12.0/json.tar.xz
    )

    FetchContent_MakeAvailable(json)

    add_executable(main main.cpp)

    target_link_libraries(main PRIVATE nlohmann_json::nlohmann_json)
    ```

## 1. 空模板

```cpp
#include <iostream>
#include "json.hpp"   
 
using namespace std;
using json = nlohmann::json; 
 
int main() 
{
	
	return 0;
}
```

## 2. 基础对象测试

```cpp
#include <cassert>
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

void test_basic_object()
{
    json j;

    j["name"] = "Alice";
    j["age"] = 18;
    j["is_student"] = true;

    assert(j["name"] == "Alice");
    assert(j["age"] == 18);
    assert(j["is_student"] == true);

    std::cout << "test_basic_object passed\n";
}
```

## 3. JSON 数组测试

```cpp
void test_array()
{
    json j = {
        {"numbers", {1, 2, 3, 4}}
    };

    assert(j["numbers"].is_array());
    assert(j["numbers"].size() == 4);
    assert(j["numbers"][2] == 3);

    std::cout << "test_array passed\n";
}
```

## 4. JSON 字符串解析

```cpp
void test_parse()
{
    std::string text = R"(
    {
        "title": "JSON",
        "version": 3.12
    }
    )";

    json j = json::parse(text);

    assert(j["title"] == "JSON");
    assert(j["version"] == 3.12);

    std::cout << "test_parse passed\n";
}
```

## 5. dump 格式化测试

```cpp
void test_dump()
{
    json j = {
        {"hello", "world"},
        {"value", 123}
    };

    std::string s = j.dump(4);

    assert(s.find("hello") != std::string::npos);
    assert(s.find("world") != std::string::npos);

    std::cout << s << std::endl;
    std::cout << "test_dump passed\n";
}
```

## 6. 异常处理测试（重点）

```cpp
void test_parse_exception()
{
    std::string bad_json = R"(
        {
            "name": "Alice",
            "age":
        }
    )";

    try
    {
        json j = json::parse(bad_json);

        assert(false); // 不应该到这里
    }
    catch (const json::parse_error& e)
    {
        std::cout << "parse exception caught:\n";
        std::cout << e.what() << std::endl;

        assert(true);
    }
}
```

## 7. 类型检查测试

```cpp
void test_type_check()
{
    json j = {
        {"id", 100},
        {"name", "Bob"},
        {"online", false}
    };

    assert(j["id"].is_number());
    assert(j["name"].is_string());
    assert(j["online"].is_boolean());

    std::cout << "test_type_check passed\n";
}
```

## 8. 嵌套对象测试

```cpp
void test_nested()
{
    json j = {
        {"user",
            {
                {"name", "Tom"},
                {"email", "tom@test.com"}
            }
        }
    };

    assert(j["user"]["name"] == "Tom");
    assert(j["user"]["email"] == "tom@test.com");

    std::cout << "test_nested passed\n";
}
```

## 9. vector 自动转换

这是 `nlohmann::json` 很常用的功能。

```cpp
#include <vector>

void test_vector()
{
    std::vector<int> vec = {1,2,3,4};

    json j = vec;

    assert(j.is_array());
    assert(j[0] == 1);

    auto out = j.get<std::vector<int>>();

    assert(out.size() == 4);
    assert(out[3] == 4);

    std::cout << "test_vector passed\n";
}
```

## 10. map 自动转换

```cpp
#include <map>

void test_map()
{
    std::map<std::string, int> scores = {
        {"math", 90},
        {"english", 85}
    };

    json j = scores;

    assert(j["math"] == 90);

    auto restored =
        j.get<std::map<std::string, int>>();

    assert(restored["english"] == 85);

    std::cout << "test_map passed\n";
}
```

## 11. 自定义结构体序列化（核心高级功能）

这是企业项目最常用的。

```cpp
struct User
{
    std::string name;
    int age;
};

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(
    User,
    name,
    age
)

void test_custom_type()
{
    User u {"Jack", 20};

    json j = u;

    assert(j["name"] == "Jack");
    assert(j["age"] == 20);

    User u2 = j.get<User>();

    assert(u2.name == "Jack");
    assert(u2.age == 20);

    std::cout << "test_custom_type passed\n";
}
```

## 12. JSON Pointer 测试

```cpp
void test_json_pointer()
{
    json j = {
        {"user",
            {
                {"name", "Alice"}
            }
        }
    };

    json::json_pointer ptr("/user/name");

    assert(j[ptr] == "Alice");

    std::cout << "test_json_pointer passed\n";
}
```

## 13. 完整 main

```cpp
int main()
{
    test_basic_object();
    test_array();
    test_parse();
    test_dump();
    test_parse_exception();
    test_type_check();
    test_nested();
    test_vector();
    test_map();
    test_custom_type();
    test_json_pointer();

    std::cout << "\nALL TESTS PASSED\n";

    return 0;
}
```

## 14. 编译方法

=== "Linux / macOS"

    ```bash
    g++ test.cpp -std=c++17 -O2
    ./a.out
    ```

=== "Windows MSVC"

    ```bat
    cl /std:c++17 test.cpp
    ```
