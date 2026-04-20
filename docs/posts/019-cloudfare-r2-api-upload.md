---
date: 2026-04-20
authors:
  - moita
categories:
  - 工程实践
  - 网页开发
tags:
  - Cloudfare
  - Python
---

# Cloudflare R2 API 上传代码

这段 Python 代码旨在实现将本地文件高效地上传到 Cloudflare R2 存储桶。它利用了 boto3 库来与 R2 进行交互，并使用了多线程来加速上传过程。

<!-- more -->

*   在代码开头部分配置 R2 的访问凭证（`ACCOUNT_ID`, `ACCESS_KEY`, `SECRET_KEY`）、目标存储桶名称（`BUCKET_NAME`）、本地待上传目录（`LOCAL_DIR`）以及 R2 上的目标目录（`PREFIX`）。
*   **文件收集**: `collect_files` 函数会递归地遍历指定的本地目录，收集所有文件的完整路径及其相对于本地目录的相对路径。
*   **并发上传**: 由于使用 `ThreadPoolExecutor` 和 `as_completed`，代码能够并发地上传多个文件。而`MAX_WORKERS` 参数控制着并发线程的数量。
*   **错误处理**: `upload_file` 函数在上传单个文件时包含了基本的异常处理，能够捕获上传过程中可能出现的错误，并返回相应的成功或失败信息。
*   **进度反馈**: 在上传过程中，代码会实时打印出每个文件的上传状态（成功或失败），并显示当前进度（例如 `[1/100] ✅ file.txt`）。

```py
import boto3
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== 配置区 =====
ACCOUNT_ID = ""
ACCESS_KEY = ""
SECRET_KEY = ""
BUCKET_NAME = ""

LOCAL_DIR = ""   # 本地目录
PREFIX = ""                  # R2 目标目录（同名）

MAX_WORKERS = 16  # 并发数（可调 8~32）

# ===== 初始化 S3 客户端（连接 R2）=====
s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="auto"
)

# ===== 收集所有文件 =====
def collect_files(base_dir):
    file_list = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_dir)
            file_list.append((full_path, rel_path))
    return file_list

# ===== 上传单个文件 =====
def upload_file(local_path, rel_path):
    r2_key = f"{PREFIX}/{rel_path}".replace("\\", "/")
    try:
        s3.upload_file(local_path, BUCKET_NAME, r2_key)
        return f"✅ {r2_key}"
    except Exception as e:
        return f"❌ {r2_key} -> {e}"

# ===== 主流程 =====
def main():
    files = collect_files(LOCAL_DIR)
    total = len(files)
    print(f"📦 共 {total} 个文件，开始上传...\n")

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(upload_file, local, rel)
            for local, rel in files
        ]

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            print(f"[{i}/{total}] {result}")
            results.append(result)

    print("\n🎉 上传完成！")

if __name__ == "__main__":
    main()
```
