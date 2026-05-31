---
date: 2026-05-22
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - C
  - UI
---

# Nuklear 基本用法

项目地址：[Nuklear](https://github.com/Immediate-Mode-UI/Nuklear)

Nuklear 是一个用 ANSI C 编写的单头文件即时模式图形用户界面（GUI）库，设计目标是提供一个轻量级、可嵌入、跨平台的UI解决方案。

<!-- more -->

## 1. 引入和初始化

### 1.1 引入头文件

在你的项目中包含 `nuklear.h`，可以选择只在一个源文件中定义实现宏 `NK_IMPLEMENTATION` 来启用实现部分。

```c
#define NK_IMPLEMENTATION
#include "nuklear.h"
```

### 1.2 初始化上下文

使用 `nk_init_fixed()` 或 `nk_init()` 初始化 `nk_context`，为UI状态分配内存。

```c
struct nk_context ctx;
nk_init_fixed(&ctx, calloc(1, MAX_MEMORY), MAX_MEMORY, &font);
```

## 2. 创建UI窗口

### 2.1 开始窗口

使用 `nk_begin()` 创建一个窗口，参数包括窗口名、位置和尺寸。

```c
if (nk_begin(&ctx, "Show", nk_rect(50, 50, 220, 220),
    NK_WINDOW_BORDER|NK_WINDOW_MOVABLE|NK_WINDOW_CLOSABLE)) {
    // 在这里添加UI控件
}
nk_end(&ctx);
```

### 2.2 结束窗口

每个窗口的UI控件都应在 `nk_begin()` 和 `nk_end()` 之间。

## 3. 布局管理

### 3.1 固定宽度布局

使用 `nk_layout_row_static()` 设置一行中控件的像素宽度。

```c
nk_layout_row_static(&ctx, 30, 80, 1);
```

### 3.2 动态宽度布局

使用 `nk_layout_row_dynamic()` 设置一行中控件的比例宽度。

```c
nk_layout_row_dynamic(&ctx, 30, 2);
```

### 3.3 自定义布局

使用 `nk_layout_row_begin()` 和 `nk_layout_row_push()` 进行自定义布局。

```c
nk_layout_row_begin(&ctx, NK_STATIC, 30, 2);
nk_layout_row_push(&ctx, 50);
nk_label(&ctx, "Volume:", NK_TEXT_LEFT);
nk_layout_row_push(&ctx, 110);
nk_slider_float(&ctx, 0, &value, 1.0f, 0.1f);
nk_layout_row_end(&ctx);
```

## 4. 常用控件

### 4.1 按钮

使用 `nk_button_label()` 创建按钮。

```c
if (nk_button_label(&ctx, "button")) {
    // 按钮事件
}
```

### 4.2 选项按钮

使用 `nk_option_label()` 创建单选项。

```c
if (nk_option_label(&ctx, "easy", op == EASY)) op = EASY;
if (nk_option_label(&ctx, "hard", op == HARD)) op = HARD;
```

### 4.3 滑块

使用 `nk_slider_float()` 创建浮点数滑块。

```c
nk_slider_float(&ctx, 0, &value, 1.0f, 0.1f);
```

### 4.4 标签

使用 `nk_label()` 添加文本标签。

```c
nk_label(&ctx, "Volume:", NK_TEXT_LEFT);
```

## 5. 渲染和清理

### 5.1 渲染

在每一帧结束后调用 `nk_render()` 进行渲染（具体渲染后端由用户实现）。

### 5.2 释放资源

在程序退出时调用 `nk_free()` 释放资源。

```c
nk_free(&ctx);
```

## 6. 其他功能

- **字体管理**：可以加载自定义字体。
- **皮肤定制**：支持皮肤和样式定制。
- **多平台支持**：无需依赖特定平台，用户需自行实现输入和渲染后端。

## 7. 例子总结

完整示例流程：

```c
/* 初始化 */
struct nk_context ctx;
nk_init_fixed(&ctx, calloc(1, MAX_MEMORY), MAX_MEMORY, &font);

/* 在每一帧中 */
if (nk_begin(&ctx, "Show", nk_rect(50, 50, 220, 220),
    NK_WINDOW_BORDER|NK_WINDOW_MOVABLE|NK_WINDOW_CLOSABLE)) {
    nk_layout_row_static(&ctx, 30, 80, 1);
    if (nk_button_label(&ctx, "button")) {
        // 事件处理
    }
    nk_layout_row_dynamic(&ctx, 30, 2);
    if (nk_option_label(&ctx, "easy", op == EASY)) op = EASY;
    if (nk_option_label(&ctx, "hard", op == HARD)) op = HARD;
    nk_layout_row_begin(&ctx, NK_STATIC, 30, 2);
    nk_layout_row_push(&ctx, 50);
    nk_label(&ctx, "Volume:", NK_TEXT_LEFT);
    nk_layout_row_push(&ctx, 110);
    nk_slider_float(&ctx, 0, &value, 1.0f, 0.1f);
    nk_layout_row_end(&ctx);
}
nk_end(&ctx);

/* 渲染和清理 */
nk_render();
nk_free(&ctx);
```
