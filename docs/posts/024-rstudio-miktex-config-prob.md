---
date: 2026-03-14
authors:
  - moita
categories:
  - 工程实践
tags:
  - LaTeX
---

# RStudio 调用 MiKTeX 问题

??? failure "控制台报错"

    ```
    command line: E:\LaTeX\MiKTeX\miktex\bin\x64\pdflatex.exe -halt-on-error -interaction=batchmode ***.tex
    2026-xx-xx xx:xx:xx,580+1300 INFO pdflatex - running on Windows 10.0.19045
    2026-xx-xx xx:xx:xx,594+1300 WARN pdflatex - security risk: running with elevated privileges
    2026-xx-xx xx:xx:xx,597+1300 INFO pdflatex - this is MiKTeX-PDFTEX 4.26.0 (1.40.29) (MiKTeX 26.2)
    2026-xx-xx xx:xx:xx,601+1300 INFO pdflatex - allowing known shell commands
    2026-xx-xx xx:xx:xx,872+1300 FATAL pdflatex.core - GUI framework cannot be initialized.
    2026-xx-xx xx:xx:xx,872+1300 FATAL pdflatex.core - Data:
    2026-xx-xx xx:xx:xx,872+1300 FATAL pdflatex.core - Source: Libraries\MiKTeX\UI\Qt\mikuiqt.cpp:126
    2026-xx-xx xx:xx:xx,872+1300 FATAL pdflatex - GUI framework cannot be initialized.
    2026-xx-xx xx:xx:xx,873+1300 FATAL pdflatex - Info:
    2026-xx-xx xx:xx:xx,873+1300 FATAL pdflatex - Source: Libraries\MiKTeX\UI\Qt\mikuiqt.cpp
    2026-xx-xx xx:xx:xx,873+1300 FATAL pdflatex - Line: 126
    2026-xx-xx xx:xx:xx,873+1300 INFO pdflatex - this process (4200) finishes with exit code 1
    2026-xx-xx xx:xx:xx,874+1300 ERROR pdflatex - major issue: So far, you have not checked for MiKTeX updates.
    2026-xx-xx xx:xx:xx,874+1300 WARN pdflatex.core - still open: ***.tex
    2026-xx-xx xx:xx:xx,874+1300 WARN pdflatex.core - still open: ***.log
    ```

为什么会这样？RStudio + MikTex 遇到了以上的报错

<!-- more -->

这个错误 **“GUI framework cannot be initialized”** 是 MiKTeX 历史上非常经典且反复出现的问题，尤其在**非交互式环境**（比如 RStudio 的 Knit、R Markdown 转 PDF、cmd check、后台调用 pdflatex）下特别容易触发。

你的日志已经很清楚了：

- MiKTeX 版本是 **26.2**
- 错误发生在 `mikuiqt.cpp:126` → 这就是 MiKTeX 试图弹出 Qt GUI 窗口失败了
- Rterm（R 的终端）在调用 pdflatex → 属于**无图形界面的子进程**，没法显示弹窗

## 最常见的原因（99% 的情况都是这个）

MiKTeX 的“**Install missing packages on-the-fly**”（自动安装缺失包）设置成了 **“Ask me first”**（每次问我）。

如果你使用的是 TexStudio + MiKTeX，通常不会出现这样的问题

当你的 .tex 文档需要某个没装的包（比如 amsmath、geometry、ulem、float、caption 之类很常见的），pdflatex 想弹窗问你是否允许下载，但因为是在 RStudio/Rterm 后台跑的，根本**没有桌面环境可以显示弹窗** → 直接崩溃，报 GUI framework cannot be initialized。

## 解决办法（最简单）

- 开始菜单找到 **MiKTeX Console**（不是 MiKTeX Settings，是 Console）
- 打开后点 **Settings**（右上角齿轮）
- 选 **Packages** 标签
- 把 **Install missing packages on-the-fly** 改成 **Yes**（或 Install）
- 确定 → 关闭
- **最好两个都改**：普通用户模式 和 Administrator 模式（右上角可以切换 User / Admin）
