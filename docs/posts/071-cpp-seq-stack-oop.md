---
date: 2026-06-01
authors:
  - moita
categories:
  - 算法
tags:
  - CPP
  - 数据结构
  - 面向对象
---

# 顺序栈面向对象封装

将顺序栈操作用 C++ 类重新组织：构造函数分配初始空间，成员函数 `push` / `pop` / `gettop` 封装入栈与出栈逻辑。

原代码缺少析构函数，`base` 指向的堆空间在对象销毁时泄漏。

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
typedef int selemtype;

class sqstack
{
public:
    selemtype *base;
    selemtype *top;
    int stacksize;
    sqstack();
    ~sqstack() { free(base); }                           // 新增：析构函数释放内存
    status gettop(selemtype &e);
    status push(selemtype e);
    status pop(selemtype &e);
};

sqstack::sqstack()
{
    base = (selemtype *)malloc(STACK_INIT_SIZE * sizeof(selemtype));
    if (!base) exit(OVERFLOW);
    top = base;
    stacksize = STACK_INIT_SIZE;
}

status sqstack::gettop(selemtype &e)
{
    if (top == base) return ERROR;
    e = *(top - 1);
    return OK;
}

status sqstack::push(selemtype e)
{
    if (top - base >= stacksize)
    {
        selemtype *newbase = (selemtype *)realloc(base,
            (stacksize + STACKINCREMENT) * sizeof(selemtype));
        if (!newbase) exit(OVERFLOW);
        base = newbase;
        top = base + stacksize;
        stacksize += STACKINCREMENT;
    }
    *top++ = e;
    return OK;
}

status sqstack::pop(selemtype &e)
{
    if (top == base) return ERROR;
    e = *--top;
    return OK;
}

int main()
{
    sqstack S;
    selemtype e;
    S.push(10);
    S.push(20);
    S.push(30);
    S.gettop(e);
    printf("栈顶: %d\n", e);
    while (S.pop(e) == OK)
        printf("出栈: %d\n", e);
    return 0;
}
```

与 C 风格版本相比，OOP 版将 `initstack` 逻辑移入构造函数，省略了显式初始化调用。`gettop` 改为通过引用参数 `e` 返回栈顶值，避免了原代码中返回值与错误码混淆的问题。

### 修正点

- 新增析构函数 `~sqstack() { free(base); }`，防止内存泄漏
