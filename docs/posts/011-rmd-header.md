---
date: 2026-01-30
authors:
  - moita
categories:
  - 工程实践
  - 数据科学
tags:
  - Markdown
---

# RMD 文件标头

当将普通的 Markdown（`.md`）文件修改为 R Markdown（`.rmd`）文件后，需要在文件开头添加 YAML 标头（YAML header），用于控制文档的基本信息和输出格式。

<!-- more -->

## 1. 标头作用

YAML 标头主要用于：

* 设置文档标题、作者、日期
* 指定输出格式（HTML / Word / PDF）
* 控制目录（TOC）显示
* 配置文档渲染选项

## 2. 基本示例

```yaml
---
title: "标题"
author: "作者"
date: "`r format(Sys.Date())`"
output:
  html_document:
    toc: true        # 显示目录
    toc_depth: 3     # 目录层级（最多3级）
    toc_float: true  # 浮动目录（侧边栏）
  word_document: default
  pdf_document: default
---
```

## 3. 关键字段说明

* `title`：文档标题
* `author`：作者名称
* `date`：日期，可使用 R 代码动态生成
* `output`：指定输出格式，可同时生成多种格式

HTML 输出常用参数：

* `toc: true`：生成目录
* `toc_depth`：目录层级深度
* `toc_float: true`：目录固定在侧边栏（适合长文档）

## 4. 注意事项

* YAML 标头必须放在文件最顶部，且用 `---` 包裹
* 缩进必须严格（使用空格，不能用 Tab）
* `date` 中的 R 代码需要用反引号包裹
* 若不需要某种格式，可删除对应 `output` 项

## 5. 进阶扩展（可选）

可以根据需要增加更多配置，例如：

```yaml
  theme: cosmo        # HTML主题
  highlight: tango    # 代码高亮样式
  number_sections: true  # 标题编号
```

## 6. 渲染方式

添加标头后，可以通过以下方式生成文档：

* 在 RStudio 中点击 **Knit**
* 或使用函数：

```r
rmarkdown::render("文件名.Rmd")
```
