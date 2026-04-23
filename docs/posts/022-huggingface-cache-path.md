---
date: 2026-03-08
authors:
  - moita
categories:
  - 人工智能
tags:
  - Pandas
  - Python
  - Hugging Face
---

# Hugging Face 缓存目录设置

要让 Hugging Face（包括 sentence-transformers）模型的缓存目录**永久**改到非 C 盘（例如 D:\HF_cache 或 E:\huggingface_hub），最推荐、最干净的方式是**设置系统级或用户级的环境变量 `HF_HOME`**。这样所有 Hugging Face 相关的库（transformers、sentence-transformers、huggingface_hub、datasets 等）都会自动使用新路径，无需每次在代码里写 `cache_dir=...`。

<!-- more -->

## 推荐方案：设置 `HF_HOME` 环境变量（永久生效）

1. 按 Windows 键，搜索并打开 **“编辑系统环境变量”** 或 **“环境变量”**（英文系统是 “Edit the system environment variables”）。
2. 在弹出的“系统属性”窗口，点击下方 **“环境变量”** 按钮。
3. 在 **“用户变量”**（只影响当前用户）或 **“系统变量”**（影响所有用户，需要管理员权限）区域：
    - 点击 **“新建(N)”**
    - 变量名（Variable name）：输入 `HF_HOME`（全大写）
    - 变量值（Variable value）：输入你想要的路径，例如：
        ```
        D:\HF_cache
        ```
        或
        ```
        E:\AI_Models\huggingface_hub
        ```
        （建议新建一个专门的文件夹，不要用已有项目文件夹，避免混乱）
4. 点击 **确定** → **确定** → **确定** 关闭所有窗口。
5. **重要**：关闭并重新打开你的 IDE（VS Code、PyCharm、Jupyter）、命令提示符 / PowerShell / Anaconda Prompt，让新环境变量生效，可能需要重启电脑。

以后 sentence-transformers 加载模型时，就会把所有下载的文件（model.safetensors、tokenizer.json、config 等）存到你指定的 `HF_HOME/hub` 目录下。
