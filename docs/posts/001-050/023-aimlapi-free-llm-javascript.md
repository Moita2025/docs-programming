---
date: 2026-03-14
authors:
  - moita
categories:
  - 人工智能
  - 网页开发
tags:
  - AI/ML API
  - API
---

# AI/ML API 免费 大语言模型 Javascript 调用代码

[AI/ML API](https://aimlapi.com/ai-ml-api-pricing) 提供了三个免费小参数 LLM 模型的调用接口。

<!-- more -->

## 模型列表

| 模型名称           | 链接                                                                                       |
| -------------- | ---------------------------------------------------------------------------------------- |
| ERNIE 4.5 0.3B | [https://aimlapi.com/models/ernie-4-5-0-3b](https://aimlapi.com/models/ernie-4-5-0-3b)   |
| Gemma 3n 4B    | [https://aimlapi.com/models/gemma-3n-4b](https://aimlapi.com/models/gemma-3n-4b)         |
| Gemma 3 (4B)   | [https://aimlapi.com/models/gemma-3-4b-api](https://aimlapi.com/models/gemma-3-4b-api)   |

## 通用 JavaScript 示例

```javascript
const { OpenAI } = require('openai');

const api = new OpenAI({
  baseURL: 'https://api.aimlapi.com/v1',
  apiKey: '<YOUR_API_KEY>',
});

async function run(model) {
  const result = await api.chat.completions.create({
    model,
    messages: [
      {
        role: 'system',
        content: 'You are an AI assistant who knows everything.',
      },
      {
        role: 'user',
        content: 'Tell me, why is the sky blue?',
      },
    ],
  });

  console.log(`Model: ${model}`);
  console.log(`Assistant: ${result.choices[0].message.content}`);
  console.log('-----------------------------');
}

async function main() {
  const models = [
    'baidu/ernie-4-5-0-3b',
    'google/gemma-3n-e4b-it',
    'google/gemma-3-4b-it'
  ];

  for (const model of models) {
    await run(model);
  }
}

main();
```
