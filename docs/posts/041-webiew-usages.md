---
date: 2026-05-23
authors:
  - moita
categories:
  - 工程实践
  - 网页开发
tags:
  - C
  - CPP
  - HTML
---

# webview 基本用法

项目地址：[webview](https://github.com/webview/webview)

webview 库的用法主要包括初始化、设置界面、加载内容和运行事件循环。

<!-- more -->

## 1. 初始化webview对象

在C++中：

```cpp
webview::webview w(bool debug, void* window);
```

- `debug`：是否开启调试模式（通常设置为`false`）
- `window`：父窗口句柄，`nullptr`表示没有父窗口

在C中：

```c
webview_t w = webview_create(0, NULL);
```

## 2. 设置窗口属性

- 设置标题：

=== "C++"

    ```cpp
    w.set_title("标题");
    ```

=== "C"

    ```c
    webview_set_title(w, "标题");
    ```

- 设置窗口大小：

=== "C++"

    ```cpp
    w.set_size(宽度, 高度, WEBVIEW_HINT_NONE);
    ```

=== "C"

    ```c
    webview_set_size(w, 宽度, 高度, WEBVIEW_HINT_NONE);
    ```

- 设置HTML内容：

=== "C++"

    ```cpp
    w.set_html("HTML内容");
    ```

=== "C"

    ```c
    webview_set_html(w, "HTML内容");
    ```

## 3. 运行事件循环

=== "C++"

    ```cpp
    w.run();
    ```

=== "C"

    ```c
    webview_run(w);
    ```

## 4. 销毁webview对象（C语言）

```c
webview_destroy(w);
```

## 5. 示例代码

=== "C++"

    ```cpp
    #include "webview/webview.h"
    #include <iostream>

    int main() {
        try {
            webview::webview w(false, nullptr);
            w.set_title("示例");
            w.set_size(800, 600, WEBVIEW_HINT_NONE);
            w.set_html("<h1>Hello, WebView!</h1>");
            w.run();
        } catch (const webview::exception &e) {
            std::cerr << e.what() << std::endl;
            return 1;
        }
        return 0;
    }
    ```

=== "C"

    ```c
    #include "webview/webview.h"

    int main() {
        webview_t w = webview_create(0, NULL);
        webview_set_title(w, "示例");
        webview_set_size(w, 800, 600, WEBVIEW_HINT_NONE);
        webview_set_html(w, "<h1>Hello, WebView!</h1>");
        webview_run(w);
        webview_destroy(w);
        return 0;
    }
    ```

## 6. 其他功能

- 绑定JavaScript和C/C++的交互（支持双向绑定）
- 加载网页URL
- 处理事件和回调

## 7. 构建和使用

- 使用CMake配置项目
- 编译示例程序
- 根据平台安装依赖（如GTK、WebKitGTK、WebView2等）
