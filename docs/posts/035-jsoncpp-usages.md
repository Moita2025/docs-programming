---
date: 2026-05-22
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - CPP
  - JSON
---

# jsoncpp 基本用法

项目地址：[jsoncpp](https://github.com/open-source-parsers/jsoncpp)

JsonCpp是一个用C++编写的库，用于操作JSON数据。它支持JSON的序列化（将JSON对象转换为字符串）和反序列化（从字符串解析出JSON对象），并且可以保留注释，适合存储用户配置文件等。

<!-- more -->

## 基本用法

### 引入头文件

```cpp
#include <json/json.h>
```

### 创建JSON对象

```cpp
Json::Value root;
root["name"] = "ChatGPT";
root["age"] = 3;
root["skills"] = Json::arrayValue;
root["skills"].append("NLP");
root["skills"].append("Machine Learning");
```

### 解析JSON字符串

```cpp
std::string jsonStr = "{\"name\": \"ChatGPT\", \"age\": 3}";
Json::CharReaderBuilder readerBuilder;
Json::Value root;
std::string errs;
std::istringstream s(jsonStr);
if (Json::parseFromStream(readerBuilder, s, &root, &errs)) {
    // 解析成功
    std::cout << root["name"].asString() << std::endl;
}
```

### 序列化JSON对象为字符串

```cpp
Json::StreamWriterBuilder writerBuilder;
std::string output = Json::writeString(writerBuilder, root);
std::cout << output << std::endl;
```

## 进阶用法

### 读取文件中的JSON

```cpp
std::ifstream file("config.json");
Json::Value root;
file >> root;
```

### 写入JSON到文件

```cpp
std::ofstream file("output.json");
Json::StreamWriterBuilder writerBuilder;
file << Json::writeString(writerBuilder, root);
```

### 访问数组元素

```cpp
Json::Value skills = root["skills"];
for (const auto& skill : skills) {
    std::cout << skill.asString() << std::endl;
}
```

## 其他信息

- 支持多平台和多编译器
- 提供Amalgamated源代码，方便集成
- 详细文档和示例请参考[官方文档](http://open-source-parsers.github.io/jsoncpp-docs/doxygen/index.html)
