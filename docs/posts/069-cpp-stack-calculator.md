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

# 顺序栈实现表达式求值

用两个顺序栈——运算符栈 OPTR 和操作数栈 OPND——实现算术表达式的求值，支持加减乘除与括号。

- 使用依赖：[<code>sqstack 顺序栈</code>](https://moita2025.github.io/docs-programming/2026/06/01/068-cpp-seq-stack-core/#修正后完整代码)

<!-- more -->

原计算器代码将栈元素类型定义为 `char`，导致操作数被截断（如结果 256 存入 char 变为 0）。修正后将 `selemtype` 统一为 `int`，并复用前一篇的顺序栈操作。表达式解析已支持多位数读取。

## 完整代码

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
typedef int selemtype;                                   // 修正：改为 int，避免操作数截断

// ===== 顺序栈操作（来自 顺序栈核心操作） =====

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

status gettop(sqstack s)
{
    if (s.top == s.base) return ERROR;
    return *(s.top - 1);
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

// ===== 运算符优先级表 =====

char priority[8][8] =
{
    ' ','+','-','*','/','(',')','#',
    '+','>','>','<','<','<','>','>',
    '-','>','>','<','<','<','>','>',
    '*','>','>','>','>','<','>','>',
    '/','>','>','>','>','<','>','>',
    '(','<','<','<','<','<','=',' ',
    ')','>','>','>','>',' ','>','>',
    '#','<','<','<','<','<',' ','='
};

status precede(char m, char n)
{
    int mvalue, nvalue;
    switch (m)
    {
        case '+': mvalue = 1; break;
        case '-': mvalue = 2; break;
        case '*': mvalue = 3; break;
        case '/': mvalue = 4; break;
        case '(': mvalue = 5; break;
        case ')': mvalue = 6; break;
        case '#': mvalue = 7; break;
    }
    switch (n)
    {
        case '+': nvalue = 1; break;
        case '-': nvalue = 2; break;
        case '*': nvalue = 3; break;
        case '/': nvalue = 4; break;
        case '(': nvalue = 5; break;
        case ')': nvalue = 6; break;
        case '#': nvalue = 7; break;
    }
    return priority[mvalue][nvalue];
}

int operate(int a, char theta, int b)                    // 修正：返回 int 而非 char
{
    switch (theta)
    {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return a / b;
    }
    return 0;
}

int evaluate()
{
    sqstack OPTR, OPND;
    initstack(OPTR);
    push(OPTR, '#');
    initstack(OPND);
    char c = getchar();
    int x;
    char theta;
    while (c != '#' || gettop(OPTR) != '#')
    {
        if (c >= '0' && c <= '9')
        {
            char z[20] = {0};
            int i = 0;
            while (c >= '0' && c <= '9')
            {
                z[i++] = c;
                c = getchar();
            }
            z[i] = 0;
            push(OPND, atoi(z));
        }
        else
        {
            switch (precede(gettop(OPTR), c))
            {
                case '<':
                    push(OPTR, c);
                    c = getchar();
                    break;
                case '=':
                    pop(OPTR, x);
                    c = getchar();
                    break;
                case '>':
                    theta = gettop(OPTR);
                    pop(OPTR, theta);
                    int b, a;
                    pop(OPND, b);
                    pop(OPND, a);
                    push(OPND, operate(a, theta, b));
                    break;
            }
        }
    }
    return gettop(OPND);
}

int main()
{
    printf("输入算术表达式（以#结束），如 3-(4/2*3-1)+2*7#\n");
    int result = evaluate();
    printf("结果为：%d\n", result);
    return 0;
}
```

### 算法流程

1. 初始化 OPTR 栈（压入 `#`）和 OPND 栈
2. 逐字符读取表达式：
   - **数字**：持续读取组成多位数，`atoi` 转换后压入 OPND
   - **运算符**：查优先级表，若当前运算符优先级 ≤ 栈顶则先计算（从 OPND 弹出两操作数 + OPTR 弹出一运算符，结果压回 OPND），否则压入 OPTR
3. 读到 `#` 且 OPTR 栈顶也为 `#` 时结束，OPND 栈顶即为结果

### 修正点

- `selemtype` 由 `char` 改为 `int`，消除操作数存入 `char` 型栈时的截断 bug
- `operate` 返回类型由 `char` 改为 `int`
- 栈操作声明为前一篇的依赖，避免代码重复
