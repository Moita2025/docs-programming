---
date: 2026-05-09
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - C
  - C++
  - GCC
  - CMD
---

# CMD GCC 编译代码

- 使用依赖：[<code>path_parser_lib.bat</code>](https://moita2025.github.io/docs-programming/026-cmd-file-path-str-parse/#%E6%A8%A1%E5%9D%97%E5%9E%8B)

<!-- more -->

```cmd
@echo off
chcp 65001 >nul
setlocal

title C++ 编译工具

:: GCC 参数
set "PARAM=-std=c++11"

:: 输入文件
set /p "SRC=请输入 cpp 文件路径："

if not defined SRC (
    echo 输入不能为空
    pause
    exit /b
)

:: 调用路径解析器
call path_parser_lib.bat "%SRC%"

:: 生成 exe 路径
set "EXEFILE=%PARSER_DIR%%PARSER_FILENAME%.exe"

echo.
echo ========= 编译信息 =========
echo 源文件 ：%SRC%
echo 输出文件：%EXEFILE%
echo ============================

:: GCC 路径
cd /d "[路径]\GCC\bin"

echo.
echo 开始编译...
echo.

g++ "%SRC%" ^
-o "%EXEFILE%" ^
-I"[路径]\GCC\include" ^
-I"[路径]\GCC\x86_64-w64-mingw32\include" ^
-L"[路径]\GCC\lib" ^
-L"[路径]\GCC\x86_64-w64-mingw32\lib" ^
-static-libgcc ^
%PARAM%

echo.
if exist "%EXEFILE%" (
    echo 编译成功！
) else (
    echo 编译失败！
)

pause
endlocal
```
