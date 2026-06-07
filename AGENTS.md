# MkDocs Material 博文写作规范

本文档定义本项目所有博客文章的编写规范。

## 文件命名

博文文件名格式：

```text
[三位阿拉伯数字]-[名称].md
```

示例：

```text
001-hello-world.md
015-openai-api-guide.md
128-mkdocs-material-tips.md
```

要求：

* 序号使用三位阿拉伯数字。
* 序号表示网页顺序。
* 名称由 2～5 个英文单词组成。
* 全部使用小写字母。
* 单词之间使用 `-` 连接。
* 不使用中文、下划线或空格。

---

## 目录组织

当 `docs/posts/` 下文件数量较多时，可将博文移入子文件夹，以减轻 VSCode 目录树的浏览负担。

子文件夹命名格式：

```text
[起始序号]-[结束序号]
```

示例：

```text
001-050/
051-100/
```

规则：

* 子文件夹位于 `docs/posts/` 下。
* MkDocs Material 仍能识别子文件夹内的 md 文件，无需修改配置文件。
* 子文件夹不影响博文的 URL 索引方式——URL 仍然基于 YAML 表头中的 `date` 和文件名生成，与子文件夹路径无关。
* 跨页面代码依赖的 URL 格式不受子文件夹影响。
* 新建博文时，可先放在 `docs/posts/` 根目录下，后续再按序号范围归入对应子文件夹。
* 搜索已有博文时，需同时检查 `docs/posts/` 根目录及其所有子文件夹。

---

## YAML Front Matter

每篇博文必须包含 YAML 表头：

```yaml
---
date: YYYY-MM-DD
authors:
  - moita
categories:
  - 分类名称
tags:
  - 标签名称
---
```

规则：

* `date` 使用当天日期。
* 日期格式必须为 `YYYY-MM-DD`。
* `authors` 固定为：

```yaml
authors:
  - moita
```

* `categories` 必须从以下配置中选择：

```text
mkdocs.base.yml
plugins -> blog -> categories_allowed
```

* 允许多个分类。

* 通常不超过两个分类。

* `tags` 必须从以下文件中选择：

```text
mkdocs.tags.txt
```

* 允许多个标签。

* 缺少标签时，在 `mkdocs.tags.txt` 添加新的标签。

---

## 标题规范

### 一级标题

每篇博文必须且只能存在一个一级标题：

```markdown
# 标题
```

规则：

* 一级标题作为网页 Title。
* 不允许出现多个一级标题。

### 其余标题

除一级标题外，允许使用二级至五级标题：

```markdown
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
```

规则：

* 标题层级范围：

```text
2 ≤ level ≤ 5
```

* 根据内容结构合理选择层级。
* 避免无意义的层级嵌套。

---

## 摘要规范

使用：

```html
<!-- more -->
```

作为摘要与正文的分隔点。

规则：

* `<!-- more -->` 之前的内容会显示在博客列表页。
* 需要保证其具有独立阅读价值。
* 通常控制为一句话或一段话。

示例：

```markdown
这是一篇介绍 OpenCode 使用经验的文章。

<!-- more -->
```

---

## GitHub 仓库介绍类文章

如果文章核心内容是介绍某个 GitHub 仓库，则在摘要区域最前面增加项目地址。

格式：

```markdown
项目地址：[仓库名称](GitHub 链接)

一句话介绍项目。

<!-- more -->
```

示例：

```markdown
项目地址：[OpenCode](https://github.com/opencode-ai/opencode)

一个面向终端场景的 AI Coding Agent。

<!-- more -->
```

规则：

* 位于 `<!-- more -->` 之前。
* 位于摘要第一行。
* 使用标准 Markdown 链接格式。

---

## Prompt 引用块

对于 LLM 对话、问答场景中的提问内容，使用以下 HTML 结构：

```html
<div class="quote-card">
    <div class="quote-content">
        文本内容
    </div>
</div>
```

用途：

* 用户提问
* Prompt 内容
* 对话中的问题描述

---

## Quote Card 内容规范

`quote-content` 内允许使用常见 HTML 标签，例如：

```html
<ul>
    <li>项目一</li>
    <li>项目二</li>
</ul>

<ol>
    <li>步骤一</li>
    <li>步骤二</li>
</ol>

<br>
```

要求：

* 无需考虑样式设计。
* 保证 HTML 结构正确即可。
* 以表达内容为优先。

---

## LLM 问答类文章规范

### 单次问答

结构：

```markdown
# 标题

<div class="quote-card">
    <div class="quote-content">
        用户提问
    </div>
</div>

<!-- more -->

回答内容
```

### 多次问答

首次提问直接使用 Quote Card。

从第二次提问开始，每个新问题前增加二级标题。

结构：

```markdown
# 标题

<div class="quote-card">
    <div class="quote-content">
        第一个问题
    </div>
</div>

<!-- more -->

回答内容

## 第二个问题

<div class="quote-card">
    <div class="quote-content">
        第二个问题
    </div>
</div>

回答内容

## 第三个问题

<div class="quote-card">
    <div class="quote-content">
        第三个问题
    </div>
</div>

回答内容
```

规则：

* 第一个问题不需要额外标题。
* 第二个问题及以后必须使用二级标题。
* 问题内容统一使用 Quote Card。
* 回答内容放置于对应问题之后。

---

## 简单代码介绍类文章规范

当文章以一个或多个源代码文件为核心，介绍代码功能、结构和实现细节时，遵循以下流程：

### 编写流程

1. 先检查代码，找出存在的问题。
2. 如果代码存在严重逻辑错误，在正文中指出问题并给出修正方案。
3. 如果代码仅存在小问题（如硬编码参数、内存泄漏、缩进不规范等），在正文中展示修正后的代码。
4. 修正后的代码中，所有被修改的位置使用行内注释标注。

### 修改注释格式

在修改过的代码行末尾增加注释，说明本行做了何种修改：

```cpp
HuffmanTree H(h, n);                            // 修正：用 n 替代硬编码 4
~HuffmanTree() { delete[] huffTree; }           // 新增：析构函数释放内存
for (int k = num; k < 2 * num - 1; k++)         // 未修改的行不添加注释
```

规则：

* 注释使用行内形式，放在被修改代码行的末尾。
* 注释内容简洁说明修改原因，如"修正"、"新增"、"删除"等。
* 未修改的代码行不添加额外注释。
* 保留原始代码注释，不与修改标注混淆。

---

## 跨页面代码依赖类文章规范

当文章中的代码引用了另一篇博文中的模块时，需要在 `<!-- more -->` 之前声明依赖关系。

### 格式

```markdown
- 使用依赖：[<code>模块名称</code>](https://moita2025.github.io/docs-programming/日期路径/文件名（无后缀）)
```

示例：

假设目标博文 `026-cmd-file-path-str-parse.md` 的 YAML 表头中 `date: 2026-05-09`，则日期路径为 `2026/05/09`：

```markdown
- 使用依赖：[<code>path_parser_lib.bat</code>](https://moita2025.github.io/docs-programming/2026/05/09/026-cmd-file-path-str-parse/#模块型)
```

### 规则

* 位于 `<!-- more -->` 之前。
* 位于摘要内容之后（如有），与摘要内容保持一个空行。
* URL 格式为 `https://moita2025.github.io/docs-programming/` + 目标页面 YAML 表头中 `date` 字段的值（格式 `yyyy/MM/dd`）+ `/` + 目标页面的文件名（去掉 `.md` 后缀）。
* 如果引用目标页面中的特定章节，可在 URL 末尾追加 `#锚点`。
* 模块名称使用 `<code>` 标签包裹。

### 完整结构

```markdown
# 标题

摘要内容。

- 使用依赖：[<code>模块名称</code>](https://moita2025.github.io/docs-programming/日期路径/文件名)

<!-- more -->

正文
```

---

## 中文排版规范

### 中英文混排

中文与英文之间保留一个空格。

正确：

```text
使用 OpenCode 编写文章
支持 MkDocs Material
调用 OpenAI API
```

错误：

```text
使用OpenCode编写文章
支持MkDocs Material
调用OpenAIAPI
```

### 中文与数字混排

中文与数字之间保留一个空格。

正确：

```text
共有 15 篇文章
支持 GPT-4 模型
```

错误：

```text
共有15篇文章
支持GPT-4模型
```

### 行内代码

行内代码前后保留空格。

正确：

```markdown
使用 `opencode run` 命令启动。
配置位于 `mkdocs.base.yml` 中。
```

错误：

```markdown
使用`opencode run`命令启动。
配置位于`mkdocs.base.yml`中。
```

---

## 代码块规范

所有代码块必须标注语言。

正确：

````markdown
```python
print("hello")
```

```yaml
site_name: blog
```

```bash
opencode run
```
````

错误：

````markdown
```
print("hello")
```
````

---

## MkDocs Material 扩展能力

允许使用项目已经启用的 MkDocs Material Markdown 扩展功能。

具体支持范围以配置文件为准：

```text
mkdocs.base.yml
markdown_extensions
```

编写文章时优先使用项目已启用能力，而不是自行设计 HTML 结构。

---

## 外部链接规范

使用标准 Markdown 链接格式：

```markdown
[链接名称](链接)
```

示例：

```markdown
参考官方文档：

[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
```

---

## 参考资料规范

引用外部资料时统一使用脚注。

正文：

```markdown
某句话。（出处网站[^1]）
```

示例：

```markdown
MkDocs Material 支持博客插件功能。（官方文档[^1]）
```

文章末尾：

```markdown
[^1]: [MkDocs Material Blog](https://squidfunk.github.io/mkdocs-material/plugins/blog/)
```

规则：

* 脚注序号按出现顺序递增。
* 所有脚注定义统一放在文章末尾。
* 优先使用脚注引用资料来源。
* 同一来源可复用同一个脚注编号。

---

## 内容风格规范

### 保持自然表达

文章应以技术分享、经验记录、问题解决为导向。

避免明显的 AI 写作痕迹，例如：

* 首先
* 其次
* 再次
* 最后
* 总的来说
* 综上所述
* 需要注意的是
* 值得一提的是
* 不难发现
* 通过以上内容可以看出

除非确有必要，否则不要使用模板化总结。

### 优先描述实际内容

优先回答：

* 遇到了什么问题
* 为什么会出现
* 如何解决
* 最终结果如何

避免大量铺垫性文字。

推荐：

```markdown
执行命令后出现权限错误。

原因是配置文件中的目录归属用户不正确。

修改目录权限后恢复正常。
```

不推荐：

```markdown
首先我们需要了解权限机制。

其次需要理解目录所有者。

最后进行修改。
```

### 避免无意义总结

如果正文已经完整表达清楚，则不强制编写总结章节。

允许文章直接结束。
