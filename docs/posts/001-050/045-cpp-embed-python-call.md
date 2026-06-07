---
date: 2026-05-31
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - Python
  - 跨语言
---

# C++ 嵌入 Python 调用

CPython 提供了 C API，让 C++ 程序可以直接嵌入 Python 解释器，执行 Python 代码、调用 Python 函数、获取返回值。这在需要利用 Python 生态库的 C++ 项目中非常实用。

下面从"执行简单语句 → 获取变量值 → 调用自定义模块函数"三步，记录 C++ 嵌入 Python 的基本用法。

<!-- more -->

## 环境准备

### Python 端

写一个简单的 Python 模块 `myadd.py`：

```python
def AdditionFc(a, b):
    print("Now is in python module")
    print("{} + {} = {}".format(a, b, a+b))
    return a + b
```

### C++ 编译选项

编译时需链接 Python 库：

```text
-static-libgcc -std=c++11 -L .\libs\*
```

头文件路径指向 `include/Python.h` 所在目录。

## 1. 执行 Python 语句

最基础的用法——启动解释器，执行一行 Python 代码，然后关闭：

```cpp
#include "include/Python.h"

int main(int argc, char *argv[]) 
{
  Py_Initialize();
  PyRun_SimpleString("print('hello world in python and c')");
  Py_Finalize();
  return 0;
}
```

`Py_Initialize` 和 `Py_Finalize` 必须成对调用。`PyRun_SimpleString` 直接传入 Python 语句字符串。

## 2. 执行 Python 代码并取出变量

`PyRun_SimpleString` 执行的代码中的变量会保存在主模块的 dict 中，可以通过以下方式取出：

```cpp
#include "include/Python.h"
#include <stdio.h>

int main()
{
    int number1 = 10;
    int number2 = 32;
    Py_Initialize();

    char input[100];
    sprintf(input, "number3 = %d + %d", number1, number2);
    PyRun_SimpleString(input);

    PyObject * module = PyImport_AddModule("__main__");
    PyObject * dictionary = PyModule_GetDict(module);
    PyObject * result = PyDict_GetItemString(dictionary, "number3");
    long number3 = PyLong_AS_LONG(result);
    printf("%d\n", (int)number3);

    Py_Finalize();
}
```

关键流程：

1. `PyImport_AddModule("__main__")` 获取 Python 主模块对象
2. `PyModule_GetDict` 获取模块的全局命名空间
3. `PyDict_GetItemString` 按变量名取出值
4. `PyLong_AS_LONG` 将 Python 整数转为 C 的 `long`

## 3. 导入 Python 模块并调用函数

前面的方式是运行字符串再取变量，更好的方式是导入 `.py` 模块，直接调用其中的函数：

```cpp
#include "include/Python.h" 
#include <iostream>
using namespace std;
 
int main()
{
    Py_Initialize();
    
    // 添加当前目录到 Python 搜索路径
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");
    
    // 导入 myadd 模块（不要写 .py 后缀）
    PyObject* pModule = PyImport_ImportModule("myadd");
    
    // 获取函数对象
    PyObject* pFunc = PyObject_GetAttrString(pModule, "AdditionFc");
    
    // 构建参数元组
    PyObject* pArgs = PyTuple_New(2);
    PyTuple_SetItem(pArgs, 0, Py_BuildValue("i", 2));
    PyTuple_SetItem(pArgs, 1, Py_BuildValue("i", 4));
    
    // 调用函数
    PyObject* pReturn = PyEval_CallObject(pFunc, pArgs);
    
    // 解析返回值
    int nResult;
    PyArg_Parse(pReturn, "i", &nResult);
    cout << "return result is " << nResult << endl;
    
    Py_Finalize();
}
```

这个流程是 C++ 嵌入 Python 的标准模式：

| 步骤 | API | 作用 |
|-----|-----|------|
| 初始化 | `Py_Initialize` | 启动 Python 解释器 |
| 设搜索路径 | `sys.path.append` | 确保能 import 到 `.py` 文件 |
| 导入模块 | `PyImport_ImportModule` | 加载 `.py` 为模块对象 |
| 取函数 | `PyObject_GetAttrString` | 从模块中取出函数对象 |
| 构建参数 | `PyTuple_New` + `Py_BuildValue` | 将 C 值打包为 Python 对象 |
| 调用 | `PyEval_CallObject` | 执行 Python 函数 |
| 解析结果 | `PyArg_Parse` | 将返回值转回 C 类型 |
| 关闭 | `Py_Finalize` | 释放 Python 资源 |

## Py_BuildValue 格式速查

`Py_BuildValue("i", 42)` 中的格式字符决定了 C 类型到 Python 对象的转换：

| 格式字符 | C 类型 | Python 类型 |
|---------|-------|------------|
| `i` | int | int |
| `l` | long | int |
| `d` | double | float |
| `s` | char* | str |
| `f` | float | float |

同理，`PyArg_Parse` 使用相同的格式字符将返回值转回 C 类型。第三个参数要传指针（`&nResult`）。

## 注意事项

调用 `Py_Finalize` 后不能再使用任何 Python API。如果有多次初始化的需求，可以用 `Py_IsInitialized` 检查解释器状态。

如果 `PyImport_ImportModule` 返回 NULL，通常是模块路径不在 `sys.path` 内，需要确认 `sys.path.append` 的路径是否正确。
