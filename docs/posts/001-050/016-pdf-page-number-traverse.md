---
date: 2026-01-30
authors:
  - moita
categories:
  - 文件系统
tags:
  - Python
  - 遍历
  - Tkinter
  - PDF
---

# 查询指定路径下，所有 PDF 文件的页数

- 使用 `tkinter` 调用文件夹选择对话框
	- 支持设定初始默认路径
- 使用 `PyPDF2` 获取 PDF 文件的页数
	- [Welcome to PyPDF2 — PyPDF2  documentation](https://pypdf2.readthedocs.io/en/3.x/)
	- [PyPDF2 · PyPI](https://pypi.org/project/PyPDF2/)

<!-- more -->

```py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader

def get_pdf_page_count(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return 0

def main():
    # 初始化 Tkinter
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 弹出文件夹选择对话框
    initial_dir = r'...' # 初始默认路径
    folder_path = filedialog.askdirectory(
        initialdir=initial_dir, title="选择文件夹"
    )
    
    # 如果用户没有选择文件夹
    if not folder_path:
        messagebox.showerror("错误", "未选择文件夹，程序将结束。")
        return
    
    # 列出文件夹中的文件
    pdf_files = [
        f for f in os.listdir(folder_path) 
            if f.lower().endswith('.pdf')
    ]
    
    # 如果文件夹中没有PDF文件
    if not pdf_files:
        messagebox.showerror("错误", "文件夹中没有PDF文件，程序将结束。")
        return
    
    # 记录每个PDF文件的页数
    pdf_page_counts = {}
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        page_count = get_pdf_page_count(pdf_path)
        pdf_page_counts[pdf_file] = page_count
    
    # 输出文件名和其对应的PDF页数
    for pdf_file, page_count in pdf_page_counts.items():
        print(f"{pdf_file}: {page_count} 页")

if __name__ == "__main__":
    main()
```
