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

# 查询指定路径下，所有文件中包含关键词的行

- 支持多路径
- 支持筛选给定的多文件后缀名
- 支持多关键词
- 支持筛选给定的多排除关键词

<!-- more -->

```py
import os

def get_files_with_extensions(directory, extensions):
    """获取目录下指定扩展名的所有文件路径"""
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in extensions):
                file_path = os.path.join(root, file)
                matching_files.append(file_path)
    return matching_files

def search_strings_in_files(
        directory, search_strings, 
        extensions, exclude_keywords=None
    ):
    """在指定目录的文件中搜索字符串，支持排除关键字"""
    exclude_keywords = exclude_keywords or []  # 默认空列表
    
    files = get_files_with_extensions(directory, extensions)
    
    for file_path in files:
        relative_path = os.path.relpath(file_path, directory)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"无法读取文件 {relative_path}: {e}")
            continue
        
        for line_num, line in enumerate(lines, start=1):
            # 检查是否包含任意搜索字符串
            if any(search_str in line for search_str in search_strings):
                # 检查是否包含任意排除关键字
                if any(exclude_kw in line for exclude_kw in exclude_keywords):
                    continue  # 跳过包含排除关键字的行
                
                # 匹配成功，打印结果
                print(f"File: {relative_path} - Line {line_num}:")
                print(f"  {line.strip()}")
                print()  # 空行分隔

# 示例使用
directory_paths = [
    '...' # 路径字符串列表
]

search_strings = ['...'] # 要搜索的字符串列表
extensions = ['...'] # 支持的文件后缀名列表（不带点也可，代码会处理）
exclude_keywords = ['...'] # 不允许出现的排除关键字列表

for directory_path in directory_paths:
    if os.path.exists(directory_path):
        print(f"正在搜索目录: {directory_path}\n")
        search_strings_in_files(
            directory_path,
            search_strings,
            extensions,
            exclude_keywords
        )
    else:
        print(f"目录不存在: {directory_path}")
```

