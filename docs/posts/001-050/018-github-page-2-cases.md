---
date: 2026-04-20
authors:
  - moita
categories:
  - 工程实践
  - 网页开发
tags:
  - GitHub
---

# GitHub Pages 托管的两种常见情况

GitHub Pages 是一种静态网站托管服务，可以直接从 GitHub 仓库托管网站。以下是两种常见的 GitHub Pages 托管情况：

<!-- more -->

## 1. 普通图片、代码、文本仓库

对于托管普通文件（如图片、代码片段、文档等）的仓库，配置 GitHub Pages 的步骤如下：

*   **进入设置 (Settings)**：在您的 GitHub 仓库页面，点击右上角的 "Settings" 选项。
*   **选择构建和部署 (Build and deployment)**：在左侧导航栏中，找到并点击 "Build and deployment"。
*   **选择源 (Source)**：在 "Source" 选项下，选择 "Deploy from a branch"。
*   **选择分支 (Branch)**：在 "Branch" 选项下，选择您希望用于部署的分支（通常是 `main` 或 `master`），并在后面的路径选择器中选择 `/` (根目录)。

完成以上设置后，GitHub Pages 会自动将您指定分支根目录下的文件部署为静态网站。

## 2. MkDocs Material 博客

如果您使用 MkDocs Material 构建博客，部署流程会稍有不同，通常需要等待 GitHub Actions 自动完成第一次部署：

*   **首次 Commit 和 Action 运行**：在您进行第一次 `commit` 并推送到仓库后，GitHub Actions 会自动触发 "Page Deployment" 工作流。请等待此工作流成功运行。
*   **进入设置 (Settings)**：在您的 GitHub 仓库页面，点击右上角的 "Settings" 选项。
*   **选择构建和部署 (Build and deployment)**：在左侧导航栏中，找到并点击 "Build and deployment"。
*   **选择源 (Source)**：在 "Source" 选项下，选择 "Deploy from a branch"。
*   **选择分支 (Branch)**：在 "Branch" 选项下，选择 `gh-pages` 分支，并在后面的路径选择器中选择 `/` (根目录)。

MkDocs Material 通常会将构建好的静态文件输出到 `gh-pages` 分支，因此需要将此分支设为 GitHub Pages 的部署源。等待 Action 成功运行后，您的 MkDocs 博客即可通过 GitHub Pages 访问。
