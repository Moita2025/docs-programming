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

# spdlog 基本用法

项目地址：[spdlog](https://github.com/gabime/spdlog)

spdlog 是一个快速的C++日志库，支持多种日志目标（控制台、文件、syslog等），具有丰富的格式化功能。以下是它的基本用法示例：

<!-- more -->

## 1. 引入头文件

```cpp
#include "spdlog/spdlog.h"
```

## 2. 简单日志输出

```cpp
spdlog::info("Welcome to spdlog!");
spdlog::error("Some error message with arg: {}", 1);
```

## 3. 设置日志级别和格式

```cpp
spdlog::set_level(spdlog::level::debug); // 设置全局日志级别
spdlog::set_pattern("[%H:%M:%S %z] [%n] [%^---%L---%$] [thread %t] %v");
```

## 4. 创建不同类型的日志器

- 控制台彩色输出

```cpp
auto console = spdlog::stdout_color_mt("console");
console->info("This is a console logger");
```

- 文件日志（基本文件日志）

```cpp
auto file_logger = spdlog::basic_logger_mt("file_logger", "logs/basic-log.txt");
file_logger->info("Logging to a file");
```

- 旋转文件日志

```cpp
auto rotating_logger = spdlog::rotating_logger_mt("rotating_logger", "logs/rotating.txt", 1024*1024*5, 3);
rotating_logger->info("Rotating log file");
```

- 每日日志

```cpp
auto daily_logger = spdlog::daily_logger_mt("daily_logger", "logs/daily.txt", 2, 30);
daily_logger->info("Daily log");
```

## 5. 多目标日志（多 sinks）

```cpp
auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>("logs/multisink.txt");
spdlog::logger logger("multi_sink", {console_sink, file_sink});
logger.set_level(spdlog::level::debug);
logger.warn("This message appears in both console and file");
```

## 6. 异步日志

```cpp
spdlog::init_thread_pool(8192, 1);
auto async_logger = spdlog::create_async<spdlog::sinks::basic_file_sink_mt>("async_logger", "logs/async_log.txt");
async_logger->info("Async logging");
```
