---
date: 2026-05-31
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数据结构
---

# C++ 链式队列实现

用一个头文件实现基于单向链表的队列，包含初始化、入队、出队、判空、销毁操作。代码检查后，存在几处缺少边界保护的细节。

<!-- more -->

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

typedef struct queue
{
    int data;
    struct queue* next;
} queue;

void initqueue(queue** q)
{
    (*q) = (queue*)malloc(sizeof(queue));
    if (!(*q)) return;                                         // 新增：malloc 失败保护
    (*q)->next = NULL;
}

void enqueue(queue** q, int v)
{
    queue* temp = (*q);
    queue* element = (queue*)malloc(sizeof(queue));
    if (!element) return;                                      // 新增：malloc 失败保护
    element->data = v;
    element->next = NULL;
    while (temp->next != NULL)
    {
        temp = temp->next;
    }
    temp->next = element;
}

void dequeue(queue** q, int* u)
{
    if ((*q)->next == NULL) return;                            // 新增：空队列保护
    queue* del = (*q)->next;
    (*u) = del->data;                                          // 修正：使用 del->data，避免重复解引用
    (*q)->next = del->next;                                    // 修正：使用 del->next，避免重复解引用
    free(del);
}

bool queueempty(queue* q)
{
    if (!q) return true;                                       // 新增：NULL 指针保护
    if (q->next == NULL)
        return true;
    return false;
}

void delqueue(queue** q)                                       // 修正：参数改为 queue** 以置空外部指针
{
    if (!q || !(*q)) return;                                   // 新增：空指针保护
    queue* del = NULL;
    while ((*q)->next)
    {
        del = (*q)->next;
        (*q)->next = del->next;
        free(del);
    }
    free(*q);
    *q = NULL;                                                 // 新增：置空避免悬空指针
}
```

## 操作说明

### 初始化

`initqueue` 创建哑头节点（dummy head），`data` 字段不使用，`next` 指向 NULL。哑节点让入队和出队操作不需要区分"空队列"和"非空队列"的特殊情况。

### 入队

遍历到尾节点后在末尾追加新元素。由于有哑节点存在，即使队列为空，`temp` 也指向有效节点。

### 出队

移除头节点后的第一个元素（即哑节点的 `next`），将其数据通过 `u` 传出，然后释放。**原代码未判空**，在空队列上调用会访问 NULL 指针导致崩溃。

### 判空

检查 `next == NULL` 即可。哑节点的存在使判断简洁——无需区分"未初始化"和"已初始化无元素"。

### 销毁

遍历所有节点逐一释放，最后释放哑节点。原代码 `delqueue(queue* q)` 传值不传引用，`free(q)` 后外部指针仍指向已释放内存。改为 `queue**` 后可置 NULL。

## 为什么需要哑头节点

没有哑节点时，入队需要处理两种情况：

```cpp
void enqueue_no_dummy(queue** q, int v)
{
    // 空队列时需要特殊处理
    if (*q == NULL) {
        *q = new_node;
    } else {
        // 遍历到末尾
    }
}
```

有了哑节点，`*q` 永远非 NULL，入队始终追加到 `next`，逻辑统一。

## 使用示例

```cpp
int main()
{
    queue* q;
    initqueue(&q);

    enqueue(&q, 10);
    enqueue(&q, 20);
    enqueue(&q, 30);

    int val;
    dequeue(&q, &val);
    printf("%d\n", val);  // 10

    printf("%d\n", queueempty(q));  // 0 (false)

    delqueue(&q);
    return 0;
}
```
