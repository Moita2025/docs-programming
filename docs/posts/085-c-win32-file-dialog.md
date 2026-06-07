---
date: 2026-06-07
authors:
  - moita
categories:
  - 工程实践
tags:
  - C
  - UI
---

# C 语言调用 Win32 文件选择对话框

通过 `GetOpenFileName` 和 `OPENFILENAME` 结构体调出 Windows 原生文件选择窗口。编译时需链接 `comdlg32`。

<!-- more -->

## 原始代码

```c
// Dev C++ 下，工具栏-编译选项-编译器，勾选"在连接器命令行加入以下命令"
// 加入 "-lcomdlg32"

#include <windows.h>
#include <Commdlg.h>
#include <stdio.h>

OPENFILENAME ofn;
char szFile[100];

int main()
{
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = "All\0*.*\0Text\0*.TXT\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;
    if (GetOpenFileName(&ofn))
    {
        MessageBox(NULL, ofn.lpstrFile, "File Name", MB_OK);
    }
    else
    {
        printf("user cancel the operation\n");
    }
    return 0;
}
```

## OPENFILENAME 字段说明

| 字段 | 值 | 含义 |
| :--- | :--- | :--- |
| `lStructSize` | `sizeof(ofn)` | 结构体大小，必填 |
| `hwndOwner` | `NULL` | 父窗口句柄，NULL 表示无父窗口 |
| `lpstrFile` | `szFile` | 接收选中文件路径的缓冲区 |
| `nMaxFile` | `sizeof(szFile)` | 缓冲区大小 |
| `lpstrFilter` | 见下文 | 文件类型过滤器 |
| `nFilterIndex` | `1` | 默认选中第几个过滤器 |
| `lpstrInitialDir` | `NULL` | 初始目录，NULL 为系统默认 |
| `Flags` | `OFN_PATHMUSTEXIST \| OFN_FILEMUSTEXIST` | 路径和文件必须存在 |

### 过滤器字符串格式

```c
"All\0*.*\0Text\0*.TXT\0"
```

过滤器由成对的描述和通配符组成，每段以 `\0` 分隔，整体以双 `\0` 结尾：

- `"All"` — 下拉列表中显示的名称
- `"*.*"` — 对应的匹配模式
- `"Text"` — 第二个条目名称
- `"*.TXT"` — 对应模式
- 末尾 C 字符串自带 `\0`，与最后一个 `\0` 构成双空终止

## 问题与修正

### 文件名缓冲区过小

`szFile[100]` 仅能容纳 100 字节的路径，Windows 的 `MAX_PATH` 为 260。应使用 `MAX_PATH` 或至少 260。

### 头文件大小写

`<Commdlg.h>` 在 Windows 上因文件系统大小写不敏感能正常编译，但标准写法是 `<commdlg.h>`。

### 全局变量

`ofn` 和 `szFile` 定义为全局变量，对于单文件演示无碍，但移入 `main` 更规范。

### 修正后代码

```c
#include <windows.h>
#include <commdlg.h>                           // 修正：标准小写头文件名
#include <stdio.h>

int main()
{
    OPENFILENAME ofn;                          // 修正：移为局部变量
    char szFile[MAX_PATH];                     // 修正：用 MAX_PATH 替代 100
    char szFilter[] = "All\0*.*\0Text\0*.TXT\0"; // 新增：过滤器用 char 数组更清晰

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = szFilter;
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

    if (GetOpenFileName(&ofn))
    {
        MessageBox(NULL, ofn.lpstrFile, "File Name", MB_OK);
    }
    else
    {
        printf("user cancel the operation\n");
    }
    return 0;
}
```

## 编译命令

需要链接 `comdlg32`：

```bash
gcc main.c -o filedialog.exe -lcomdlg32
```

若不想弹出控制台窗口，可加 `-mwindows`（此时 `printf` 输出不再可见，取消分支的提示也需改为 `MessageBox`）。
