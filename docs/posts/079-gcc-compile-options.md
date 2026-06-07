---
date: 2026-06-07
authors:
  - moita
categories:
  - 工程实践
tags:
  - GCC
  - CMD
  - CPP
---

# GCC / MinGW 常用编译选项

- 使用依赖：[<code>CMD GCC 编译代码</code>](https://moita2025.github.io/docs-programming/2026/05/09/027-cmd-gcc-compile)

<!-- more -->

以下编译选项来自一个 Windows 下基于 MinGW 的 EasyX 图形程序编译命令：

```text
-static-libgcc -leasyx -std=c++11 -lgdi32 -lcomdlg32 -mwindows
```

下面逐条展开说明。

## `-std=c++11`

指定 C++ 语言标准为 C++11。GCC 支持的值包括 `c++98`、`c++11`、`c++14`、`c++17`、`c++20`、`c++23` 等。不指定时 GCC 使用其默认标准（不同版本默认值不同），显式指定可以避免因编译器版本差异导致的行为不一致。

## `-static-libgcc`

静态链接 `libgcc`。`libgcc` 是 GCC 的底层运行时库，提供 64 位整数的乘除取模、浮点模拟等编译器内部函数。不加此选项时，生成的 exe 依赖 `libgcc_s_seh-1.dll`（或类似名称的动态库）；加上后这些代码直接嵌入 exe，分发给他人时不需要附带额外的 DLL。

代价是 exe 体积略大，但省去了"缺少 xxx.dll"的麻烦。

## `-leasyx`

链接 EasyX 图形库。`-l` 指定库名（去掉 `lib` 前缀和 `.a` 后缀）。EasyX 是 Windows 平台上一个轻量级 C++ 图形库，封装了 GDI 绘图，用法接近旧式 Turbo C 的 `graphics.h`，常见于国内 C 语言教学场景中的图形编程练习。

## `-lgdi32`

链接 Windows 系统库 `gdi32.dll`（Graphics Device Interface）。提供画线、填充、文字输出等底层绘图函数。EasyX 内部依赖 GDI32，因此必须显式链接。

## `-lcomdlg32`

链接 Windows 系统库 `comdlg32.dll`（Common Dialog Box）。提供文件打开/保存对话框、颜色选择器、字体选择器、打印对话框等标准窗口。如果程序用到了 EasyX 中涉及文件选择的功能，或自行调用了 `GetOpenFileName` / `ChooseColor` 等 API，就需要这个库。

## `-mwindows`

指定生成 Windows GUI 子系统程序。效果是程序启动时不显示控制台黑窗口，`main` 入口仍有效（MinGW 会自动处理）。不加此选项时，程序以控制台子系统运行，双击 exe 会先弹出一个命令行窗口。

适合纯图形界面程序。如果程序需要 `printf` 输出到控制台调试，应去掉此选项。

## 一个完整的编译命令示例

```bash
g++ main.cpp -o app.exe -std=c++11 -static-libgcc -leasyx -lgdi32 -lcomdlg32 -mwindows
```

若 EasyX 头文件和库文件不在 MinGW 默认搜索路径中，还需要额外指定 `-I` 和 `-L`：

```bash
g++ main.cpp -o app.exe \
    -I "D:\EasyX\include" \
    -L "D:\EasyX\lib" \
    -std=c++11 -static-libgcc \
    -leasyx -lgdi32 -lcomdlg32 -mwindows
```

## 选项速查

| 选项 | 作用 |
| :--- | :--- |
| `-std=c++11` | 指定 C++11 语言标准 |
| `-static-libgcc` | 静态链接 GCC 运行时 |
| `-l<name>` | 链接指定库 |
| `-mwindows` | GUI 子系统，无控制台窗口 |
| `-I<dir>` | 添加头文件搜索路径 |
| `-L<dir>` | 添加库文件搜索路径 |
