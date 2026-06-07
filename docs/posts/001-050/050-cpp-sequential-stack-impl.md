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

# C++ 顺序栈实现

用一个头文件实现基于动态数组的顺序栈，支持自动扩容、压栈、出栈和取栈顶。代码检查后，存在几处需要加固的细节。

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
    ~sqstack();                                    // 新增：析构函数释放内存
    status gettop(selemtype &e);                   // 修正：通过引用返回，用 status 区分空栈
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

sqstack::~sqstack()                                // 新增
{
    free(base);
}

status sqstack::gettop(selemtype &e)               // 修正：返回值改为 status，元素通过引用传出
{
    if (top == base) return ERROR;
    e = *(top - 1);
    return OK;                                     // 新增：正常返回 OK
}

status sqstack::push(selemtype e)
{
    if (top - base >= stacksize)
    {
        selemtype *newbase = (selemtype *)realloc(  // 修正：用临时变量接收 realloc 结果
            base, (stacksize + STACKINCREMENT) * sizeof(selemtype));
        if (!newbase) return OVERFLOW;             // 修正：失败时返回而非 exit，保留原内存
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
```

## 操作说明

### 构造与析构

构造函数分配初始容量 `STACK_INIT_SIZE`，`top == base` 表示空栈。原代码缺失析构函数，`free` 永远不会执行，导致内存泄漏。

```cpp
sqstack::sqstack()
{
    base = (selemtype *)malloc(STACK_INIT_SIZE * sizeof(selemtype));
    top = base;
    stacksize = STACK_INIT_SIZE;
}
```

### 取栈顶

原代码 `gettop` 返回 `selemtype`，空栈时返回 `ERROR`（值为 0）。但 0 本身可能是合法栈顶元素，调用方无法区分。改为返回 `status`，元素通过引用传出：

```cpp
status sqstack::gettop(selemtype &e)
{
    if (top == base) return ERROR;
    e = *(top - 1);
    return OK;
}
```

### 压栈与扩容

`push` 在栈满时用 `realloc` 扩容。原代码 `base = realloc(...)` 有一个隐患：如果 `realloc` 失败返回 NULL，原 `base` 指针被覆盖，之前的数据全部丢失。用临时指针接收可以保住原内存：

```cpp
selemtype *newbase = (selemtype *)realloc(base, ...);
if (!newbase) return OVERFLOW;
base = newbase;
```

`realloc` 可能改变内存地址，扩容后需重新计算 `top`。由于栈已满（`top - base == stacksize`），`top = base + stacksize` 恰好指向有效元素末尾的下一个位置。

### 出栈

前移 `top` 指针即可，不销毁数据（可被后续 push 覆盖）。空栈时返回 `ERROR`：

```cpp
status sqstack::pop(selemtype &e)
{
    if (top == base) return ERROR;
    e = *--top;
    return OK;
}
```

## 使用示例

```cpp
int main()
{
    sqstack s;

    s.push(1);
    s.push(2);
    s.push(3);

    selemtype e;
    s.gettop(e);
    printf("top: %d\n", e);  // 3

    s.pop(e);
    printf("pop: %d\n", e);  // 3

    s.pop(e);
    printf("pop: %d\n", e);  // 2

    return 0;
}
```
