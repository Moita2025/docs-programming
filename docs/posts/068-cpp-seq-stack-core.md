---
date: 2026-06-01
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - C
  - 数据结构
---

# 顺序栈核心操作

实现动态扩容的顺序栈，包含初始化、入栈、出栈、取栈顶与销毁五个核心操作。栈底指针 `base` 指向分配空间的首地址，栈顶指针 `top` 指向下一个可写入位置。

原代码使用 `char` 作为元素类型且 `main()` 为空，这里改为 `int` 并补充演示与销毁逻辑。

<!-- more -->

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASIBLE -1
#define OVERFLOW -2

#define STACK_INIT_SIZE 100
#define STACKINCREMENT 10

typedef int status;
typedef int selemtype;                                   // 修正：改为 int，适配通用场景

typedef struct
{
    selemtype *base;
    selemtype *top;
    int stacksize;
} sqstack;

status initstack(sqstack &s)
{
    s.base = (selemtype *)malloc(STACK_INIT_SIZE * sizeof(selemtype));
    if (!s.base) exit(OVERFLOW);
    s.top = s.base;
    s.stacksize = STACK_INIT_SIZE;
    return OK;
}

status gettop(sqstack s, selemtype &e)
{
    if (s.top == s.base) return ERROR;
    e = *(s.top - 1);
    return OK;
}

status push(sqstack &s, selemtype e)
{
    if (s.top - s.base >= s.stacksize)
    {
        selemtype *newbase = (selemtype *)realloc(s.base,
            (s.stacksize + STACKINCREMENT) * sizeof(selemtype));
        if (!newbase) exit(OVERFLOW);
        s.base = newbase;
        s.top = s.base + s.stacksize;
        s.stacksize += STACKINCREMENT;
    }
    *s.top++ = e;
    return OK;
}

status pop(sqstack &s, selemtype &e)
{
    if (s.top == s.base) return ERROR;
    e = *--s.top;
    return OK;
}

status destroystack(sqstack &s)                          // 新增：释放栈空间
{
    free(s.base);
    s.base = s.top = NULL;
    s.stacksize = 0;
    return OK;
}

int main()
{
    sqstack S;
    selemtype e;
    initstack(S);
    push(S, 10);
    push(S, 20);
    push(S, 30);
    gettop(S, e);
    printf("栈顶: %d\n", e);
    while (pop(S, e) == OK)
        printf("出栈: %d\n", e);
    destroystack(S);
    return 0;
}
```

`push` 在空间不足时通过 `realloc` 扩容 `STACKINCREMENT` 个单元，并重新计算 `top` 相对于新 `base` 的偏移。`pop` 先将 `top` 回退一位再取值。`gettop` 只读取不修改。

### 修正点

- `selemtype` 由 `char` 改为 `int`，使栈适用于整数场景（后续计算器可直接复用）
- 新增 `destroystack` 释放动态内存
- 补充 `main()` 演示入栈、取栈顶、出栈的完整流程
