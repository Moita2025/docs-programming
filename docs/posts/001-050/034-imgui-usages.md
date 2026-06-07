---
date: 2026-05-22
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - UI
---

# ImGui 基本用法

项目地址：[imgui](https://github.com/ocornut/imgui)

Dear ImGui（Immediate Mode GUI）是一个为C++设计的轻量级、无依赖的图形用户界面库，主要用于开发工具、调试界面和内容创作工具。它的核心思想是“即时模式”，即每一帧都重新绘制界面，而不是维护复杂的状态树。以下是详细的用法介绍：

<!-- more -->

## 1. 基本概念

- 轻量高效：只输出顶点缓冲区和少量的绘制命令，渲染开销小。
- 无状态同步：避免繁琐的状态同步，减少错误。
- 适合工具开发：快速迭代、动态界面、调试和可视化工具。

## 2. 集成步骤

1. 添加源文件

    将`imgui.cpp`、`imgui_draw.cpp`、`imgui_tables.cpp`、`imgui_widgets.cpp`和对应的头文件加入你的项目。

2. 选择后端

    根据你的平台和图形API，使用`backends/`目录下的后端（如`imgui_impl_win32.cpp`、`imgui_impl_dx11.cpp`等）。

3. 初始化

    在程序初始化时，创建ImGui上下文：

    ```cpp
    ImGui::CreateContext();
    ```

4. 绑定平台和渲染后端
    调用对应的初始化函数，例如：

    ```cpp
    ImGui_ImplWin32_Init(hWnd);
    ImGui_ImplDX11_Init(device, deviceContext);
    ```

5. 每帧开始
    在渲染循环中，调用：

    ```cpp
    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();
    ```

6. 构建界面
    在`ImGui::NewFrame()`之后，使用ImGui API创建界面元素。

7. 渲染
    在界面绘制完成后，调用：

    ```cpp
    ImGui::Render();
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
    ```

## 3. 常用API示例

```cpp
// 创建窗口
ImGui::Begin("My Window");
ImGui::Text("Hello, ImGui!");
if (ImGui::Button("Click Me")) {
    // 按钮点击事件
}
static float f = 0.0f;
ImGui::SliderFloat("Float", &f, 0.0f, 1.0f);
ImGui::End();
```

## 4. 常用控件

- `Text()`, `Button()`, `Checkbox()`, `RadioButton()`
- `InputText()`, `InputInt()`, `InputFloat()`
- `SliderFloat()`, `ProgressBar()`
- `ColorEdit3()`, `ColorEdit4()`
- `Begin()`, `End()`：定义界面区域
- `BeginChild()`, `EndChild()`：子区域
- `PlotLines()`, `PlotHistogram()`：绘制图表
- `MenuBar()`, `MenuItem()`：菜单

## 5. 示例代码

```cpp
ImGui::Begin("Example");
if (ImGui::Button("Press me")) {
    // 按钮事件
}
ImGui::ColorEdit4("Color", myColor);
float samples[100];
for (int n = 0; n < 100; n++)
    samples[n] = sinf(n * 0.2f + ImGui::GetTime() * 1.5f);
ImGui::PlotLines("Samples", samples, 100);
ImGui::End();
```

## 6. 扩展和定制

- 支持自定义字体、主题
- 可以集成到各种图形API和平台
- 支持扩展插件和自定义控件

## 7. 调试和演示

调用`ImGui::ShowDemoWindow()`可以弹出示例窗口，展示所有控件和功能。

## 8. 参考资源

- Wiki文档：[Getting Started](https://github.com/ocornut/imgui/wiki/Getting-Started)
