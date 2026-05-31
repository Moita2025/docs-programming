---
date: 2026-05-31
authors:
  - moita
categories:
  - 工程实践
tags:
  - GitHub
  - CPP
---

# MkDocs Material 部署导致 .git 膨胀的排查与解决

CI 中用了 `--no-history` 避免 gh-pages 历史膨胀，但本地 `.git/objects/pack` 仍然每次 commit 后恶性增大。SpaceSniffer 锁定膨胀源是 pack 文件。

<!-- more -->

## 根因：git fetch 默认拉取所有分支

问题的链条是这样的：

1. CI 每次 push 触发 `mkdocs gh-deploy`，将整站产物（HTML、CSS、JS、字体、搜索索引等）作为一个 commit 推送到 `gh-pages` 分支
2. `--no-history` 只控制 gh-pages 自身不保留历史，但**每次部署仍会产生约 10～30 MB 的新 git 对象**
3. 本地执行 `git fetch`（或 IDE 自动 fetch）时，默认会拉取**所有远程分支**的更新，包括 `gh-pages`
4. 每次 fetch 都把新的 gh-pages 站点对象下载到本地 `D:\GitHubRepo\docs-programming\.git\objects\pack\` 下

即使 `--no-history` 让远程 gh-pages 只有 1 个 commit，本地 fetch 下来的 git 对象并不会自动被旧对象替代——`git gc` 需要手动触发才会清理不可达对象。

## 解决：禁止 fetch gh-pages 分支

修改本地仓库的 fetch refspec，只拉 main/master 而不拉 gh-pages：

```bash
# 先看当前配置
git config --get-regexp "remote.origin.fetch"

# 清掉默认的"拉所有分支"配置
git config --unset-all remote.origin.fetch

# 只拉 main 和 master
git config --add remote.origin.fetch "+refs/heads/main:refs/remotes/origin/main"
git config --add remote.origin.fetch "+refs/heads/master:refs/remotes/origin/master"
```

此后 `git fetch` 只会拉 main/master 的对象，gh-pages 的整站产物不再进入本地 `.git`。

### 清理已有的膨胀

配置修改后，之前 fetch 进来的 gh-pages 对象仍然占据磁盘空间：

```bash
# 删除本地 gh-pages 的远程跟踪引用
git branch -r -d origin/gh-pages

# 强制垃圾回收，清除不可达对象
git gc --aggressive --prune=now

# 可选：进一步压缩 pack 文件
git repack -a -d --depth=250 --window=250
```

执行后 `D:\GitHubRepo\docs-programming\.git\objects\pack\` 体积应显著缩小。

## CI 端不需要改动

现有的 CI 配置已经做了正确的优化：

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 1          # CI 环境只拉最新 commit

- run: mkdocs build --clean  # 构建前清理 site/

- run: mkdocs gh-deploy --force --clean --no-history
  # --clean      部署前清理 gh-pages 上的旧文件残留
  # --no-history 强制覆盖历史，gh-pages 分支始终保持 1 个 commit
```

CI 端的膨胀在容器销毁后自然消失，不存在积累问题。需要修复的一直是本地。

## 补充：确保 site/ 不意外提交

当前 `.gitignore` 只有一行 `prompt`，建议追加：

```text
site/
```

防止本地 `mkdocs build` 产物被误提交到主分支，进一步减少 pack 膨胀风险。
