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

# 查询指定路径下，所有文件的最后修改日期 v1.0

- 支持多路径
- 支持筛选给定的多文件后缀名
- 支持筛选最早修改日期

<!-- more -->

```py
import os
from datetime import datetime

def get_files_with_extension(
        directory, extensions, cutoff_date = "1900-01-01"
    ):
    """获取目录下指定扩展名的文件"""
    matching_files = []
    cutoff_datetime = datetime.strptime(cutoff_date, "%Y-%m-%d")

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):

                file_path = os.path.join(root, file)
                modification_time = os.path.getmtime(file_path)
                modification_date = datetime.fromtimestamp(modification_time)

                if modification_date <= cutoff_datetime:
                    continue

                matching_files.append((file, modification_date))

    return matching_files

def print_files_by_modification_date(
        directories, formats, cutoff_date = "1900-01-01"
    ):
    files = []
    for directory in directories:
        files.extend(
            get_files_with_extension(
                directory, formats, cutoff_date
            )
        )

    files.sort(key=lambda item: item[1], reverse=True)

    last_printed_date = None
    for file, modification_date in files:
        current_date = modification_date.date()

        if current_date != last_printed_date:
            print(f"--- {current_date} ---")
            last_printed_date = current_date

        print(f"{file:<30}: {modification_date}")

directory_paths = [
    '...' # 路径字符串列表
]

file_formats = [
    '...' # 后缀名字符串列表
]

print_files_by_modification_date(
    directory_paths, file_formats, "2020-01-01"
)
```
