---
date: 2026-01-30
authors:
  - moita
categories:
  - 文件系统
tags:
  - Python
  - 遍历
---

# 查询指定路径下，所有文件的后缀名

- 使用 Python 自带的集合数据结构
- 统一将后缀名转化为小写字母

<!-- more -->

```py
import os

def collect_extensions(directory):
    extensions = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                extensions.add(ext.lower())  # 加入后缀名，统一小写
    return extensions

# 示例路径
dir_path = "......"

exts = collect_extensions(dir_path)

print("找到的文件后缀名集合：")
print(exts)
```

- `for root, dirs, files in os.walk(directory):`: `os.walk()` 是一个生成器，它会遍历 `directory` 目录下的所有子目录。在每次迭代中，它会返回当前目录的路径 (`root`)、当前目录下的子目录列表 (`dirs`) 和当前目录下的文件列表 (`files`)。
- 其他数据结构: 除了集合，也可以使用列表（list）来存储后缀名，但这样会导致重复的后缀名被多次添加。如果需要统计每个后缀名的出现次数，可以使用字典（dict）。
