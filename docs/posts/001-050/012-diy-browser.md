---
date: 2026-01-30
authors:
  - moita
categories:
  - 网页开发
tags:
  - Electron
  - JavaScript
---

# 基于白名单机制的自制浏览器

<div class="quote-card">
    <div class="quote-content">
		我如果希望自制浏览器，是否可以：
		<ol>
			<li>建立网址白名单机制，只有白名单以内的网址在浏览器中可以访问</li>
			<li>白名单以内的网址，其网页内容在浏览器渲染时，a 标签的 href 属性可以进行特别处理</li>
		</ol>
    </div>
</div>

你这个设想是完全可行的，自制一个浏览器来：

<!-- more -->

1. **限制只能访问白名单中的网址** ✅
2. **对网页中的 `<a>` 标签的 `href` 属性进行特别处理** ✅

这两个需求在技术上都是可以实现的。接下来我分别给你说明怎么实现这两个功能。

---

## 一、建立“网址白名单”机制

### 实现思路

你可以使用现成的浏览器引擎（如 **Chromium**）进行开发，然后加上访问控制逻辑：

* 捕获每次网页加载请求（包括点击链接、跳转、JS 发出的请求）
* 判断目标 URL 是否在白名单中
* 如果不在白名单中，就阻止请求并提示用户

### 实现方式举例（用 Electron + Chromium）

**Electron（Node.js + Chromium）中，你可以这样做：**

```javascript
const { session } = require('electron');

const whiteList = ['https://example.com', 'https://openai.com'];

session.defaultSession.webRequest.onBeforeRequest((details, callback) => {
	const url = details.url;

	const allowed = whiteList.some(
		allowedUrl => url.startsWith(allowedUrl)
	);

	if (allowed) {
	    callback({ cancel: false });  // 允许加载
	} else {
		callback({ cancel: true });   // 阻止加载
	}
});
```

## 二、处理 `<a href>` 的特殊逻辑

这个更灵活了，关键在于你能控制浏览器内的渲染流程，并操作 DOM。

### 在加载网页后注入 JavaScript，修改所有 `<a>` 标签的行为

**伪代码示意（仍以 Electron 为例）：**

```javascript
webContents.executeJavaScript(`
	document.querySelectorAll('a').forEach(a =>{
		const originalHref = a.getAttribute('href');
	
		// 举例：为 href 添加前缀
		a.setAttribute(
			'href', '/special-handler?target=' + 
				encodeURIComponent(originalHref)
		);
	
		// 或者阻止默认行为，自定义点击逻辑
		a.addEventListener('click',
		function(e) {
			e.preventDefault();
			const url = this.href;
			// 自定义跳转逻辑，比如发送到主进程处理
			window.myCustomRouter.navigate(url);
		});
	});
`);
```

当然你可以设置任何自定义规则，比如：

* 添加跳转前确认
* 记录点击日志
* 改变 href 跳转到你自己的路由系统
* 加密或隐藏链接信息等

## 小结

| 目标                 | 可实现性 | 技术方式                                   |
| ------------------ | ---- | -------------------------------------- |
| 限制只访问白名单网址         | ✅    | 使用 `webRequest.onBeforeRequest` 过滤 URL |
| 自定义 `<a href>` 的行为 | ✅    | 注入 JS 脚本操作 DOM                         |

