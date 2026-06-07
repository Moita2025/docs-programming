---
date: 2026-05-23
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - CPP
  - JSON
---

# rapidjson 基本用法

项目地址：[rapidjson](https://github.com/Tencent/rapidjson)

RapidJSON是一个用C++编写的高性能JSON解析和生成库，支持SAX和DOM两种API风格。它具有体积小、速度快、内存友好、支持Unicode等优点，广泛应用于各种C++项目中。

<!-- more -->

## 1. 核心特性

- **支持DOM和SAX两种API**
- **高性能**：性能可与 `strlen()` 媲美，支持SSE2/SSE4.2加速
- **头文件-only**：无需依赖外部库
- **内存高效**：每个JSON值占用16字节（大部分平台）
- **Unicode支持**：支持UTF-8、UTF-16、UTF-32，支持转码和检测

## 2. 基本用法

### 2.1 解析JSON字符串为DOM

```cpp
#include "rapidjson/document.h"
using namespace rapidjson;

const char* json = "{\"name\":\"John\",\"age\":30}";
Document d;
d.Parse(json);
```

### 2.2 访问和修改DOM

```cpp
Value& name = d["name"];
std::cout << name.GetString() << std::endl; // 输出 John

// 修改值
d["age"].SetInt(31);
```

### 2.3 将DOM转为JSON字符串

```cpp
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"

StringBuffer buffer;
Writer<StringBuffer> writer(buffer);
d.Accept(writer);
std::cout << buffer.GetString() << std::endl;
```

## 3. DOM API详细用法

### 3.1 创建JSON对象

```cpp
Document d;
d.SetObject();
Document::AllocatorType& allocator = d.GetAllocator();

d.AddMember("name", "Alice", allocator);
d.AddMember("age", 25, allocator);
```

### 3.2 遍历对象和数组

```cpp
for (Value::ConstMemberIterator itr = d.MemberBegin(); itr != d.MemberEnd(); ++itr) {
    std::cout << itr->name.GetString() << ": " << itr->value.GetInt() << std::endl;
}
```

### 3.3 复杂结构示例

```cpp
Value arr(kArrayType);
arr.PushBack(1, allocator).PushBack(2, allocator).PushBack(3, allocator);
d.AddMember("numbers", arr, allocator);
```

## 4. SAX API用法

### 4.1 定义事件处理器

```cpp
#include "rapidjson/reader.h"

class MyHandler : public rapidjson::BaseReaderHandler<> {
public:
    bool StartObject() { /* 处理开始对象 */ return true; }
    bool Key(const char* str, SizeType length, bool) { /* 处理键 */ return true; }
    bool String(const char* str, SizeType length, bool) { /* 处理字符串值 */ return true; }
    bool EndObject(SizeType memberCount) { /* 结束对象 */ return true; }
};
```

### 4.2 解析示例

```cpp
rapidjson::Reader reader;
MyHandler handler;
const char* json = "{\"name\":\"Bob\"}";
StringStream ss(json);
reader.Parse(ss, handler);
```

## 5. 高级用法

### 5.1 使用JSON指针

```cpp
// 获取特定路径的值
Value* ptr = Document().Parse(json).FindMember("/path/to/value");
```

### 5.2 使用JSON Schema验证

详见[官方文档](https://github.com/Tencent/rapidjson/blob/master/doc/schema.md)

### 5.3 处理UTF编码

RapidJSON支持UTF-8、UTF-16、UTF-32，自动检测和转码。

## 6. 其他示例和资源

- [官方示例代码](https://github.com/Tencent/rapidjson/tree/master/example)
- [详细教程](https://github.com/Tencent/rapidjson/blob/master/doc/tutorial.md)
- [API参考](https://github.com/Tencent/rapidjson/blob/master/doc/README.md)
