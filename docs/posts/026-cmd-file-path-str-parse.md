---
date: 2026-05-09
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - CMD
---

# CMD 解析 文件路径字符串

* 完美支持空格路径
* 完善输入校验
    * 禁止直接回车空输入
    *  自动去除首尾双引号

<!-- more -->

## 演示型

`path_parser_cli.bat`

```cmd
@echo off
chcp 65001
title 文件路径拆分工具
:: 开启变量延迟，处理特殊输入
setlocal enabledelayedexpansion

:input
cls
set "var="
set /p "var=请输入文件的完整路径/名称（支持含空格路径）："

:: 校验：禁止空输入
if not defined var (
    echo ⚠️  输入不能为空，请重新输入！
    pause
    goto input
)

:: 校验：去除首尾双引号（处理输入自带引号的情况）
if "!var:~0,1!"=="""" set "var=!var:~1!"
if "!var:~-1!"=="""" set "var=!var:~0,-1!"

:: 校验：自动给带空格内容加引号，兼容参数传递
set "temp_var=!var!"
if "!temp_var: =!" neq "!temp_var!" set "temp_var="!temp_var!""

:: 调用子过程
call :extract !temp_var!

pause
endlocal
exit /b

:extract
echo.
echo ========== 拆分结果 ==========
:: 处理参数扩展，兼容引号
set "full_path=%~1"

:: 输出各部分，处理空值提示
set "dir_path=%~dp1"
if defined dir_path (echo 📂 所在目录：!dir_path!) else (echo 📂 所在目录：[无])

set "drive=%~d1"
if defined drive (echo 💿 所在盘符：!drive!) else (echo 💿 所在盘符：[无])

set "file_name=%~n1"
if defined file_name (echo 📄 纯文件名：!file_name!) else (echo 📄 纯文件名：[无])

set "ext_name=%~x1"
if defined ext_name (echo 🔖 扩展名  ：!ext_name!) else (echo 🔖 扩展名  ：[无])

echo ==============================
goto :eof
```

## 模块型

`path_parser_lib.bat`

```cmd
@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ==============================
:: path_parser.bat
:: 文件路径解析工具
::
:: 用法1（交互）：
::   path_parser.bat
::
:: 用法2（外部调用）：
::   call path_parser.bat "xxx.cpp"
::
:: 返回变量：
::   PARSER_FULLPATH
::   PARSER_DIR
::   PARSER_DRIVE
::   PARSER_FILENAME
::   PARSER_EXT
:: ==============================

:: 如果带参数，则直接解析
if not "%~1"=="" (
    set "INPUT_PATH=%~1"
    goto parse
)

:: ===== 交互输入 =====
:input
cls
set "INPUT_PATH="

set /p "INPUT_PATH=请输入文件完整路径："

if not defined INPUT_PATH (
    echo 输入不能为空
    pause
    goto input
)

:: 去除首尾引号
if "!INPUT_PATH:~0,1!"=="""" set "INPUT_PATH=!INPUT_PATH:~1!"
if "!INPUT_PATH:~-1!"=="""" set "INPUT_PATH=!INPUT_PATH:~0,-1!"

:parse

:: ========== 解析 ==========
set "PARSER_FULLPATH=%~f1"

for %%i in ("%INPUT_PATH%") do (

    set "PARSER_DIR=%%~dpi"
    set "PARSER_DRIVE=%%~di"
    set "PARSER_FILENAME=%%~ni"
    set "PARSER_EXT=%%~xi"
)

:: ===== 输出结果 =====
echo.
echo ========= 解析结果 =========
echo 完整路径：!PARSER_FULLPATH!
echo 所在目录：!PARSER_DIR!
echo 所在盘符：!PARSER_DRIVE!
echo 文件名  ：!PARSER_FILENAME!
echo 扩展名  ：!PARSER_EXT!
echo ============================

:: ===== 返回变量给调用者 =====
endlocal & (
    set "PARSER_FULLPATH=%PARSER_FULLPATH%"
    set "PARSER_DIR=%PARSER_DIR%"
    set "PARSER_DRIVE=%PARSER_DRIVE%"
    set "PARSER_FILENAME=%PARSER_FILENAME%"
    set "PARSER_EXT=%PARSER_EXT%"
)

exit /b
```
