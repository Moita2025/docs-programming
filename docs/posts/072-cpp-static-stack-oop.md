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

# 静态数组栈面向对象实现

用 C++ 的 `new[]` / `delete[]` 实现定长数组栈，构造函数支持自定义容量。与顺序栈的动态扩容不同，静态栈容量固定，溢出时需明确报错。

原代码 `push` 无溢出检查，`pop` 只打印不出参——将出栈值通过引用返回，并在入栈时增加容量校验。

<!-- more -->

## 修正后完整代码

```cpp
#include <stdio.h>

typedef int selemtype;

class stack
{
public:
    stack();
    stack(int val_size);
    ~stack() { delete[] a; };
    selemtype *a;
    int top;
    int capacity;                                        // 新增：记录实际容量
    int push(selemtype elem);
    int pop(selemtype &elem);                            // 修正：出栈值通过引用返回
};

stack::stack()
{
    capacity = 100;
    a = new selemtype[capacity];
    top = -1;
}

stack::stack(int val_size)
{
    capacity = val_size;
    a = new selemtype[capacity];
    top = -1;
}

int stack::push(selemtype elem)
{
    if (top + 1 >= capacity)                             // 修正：增加溢出检查
    {
        printf("栈满\n");
        return -1;
    }
    a[++top] = elem;
    return top;
}

int stack::pop(selemtype &elem)
{
    if (top == -1)
    {
        printf("空栈\n");
        return -1;
    }
    elem = a[top];                                       // 修正：将出栈值赋给引用参数
    printf("出栈元素：%d\n", a[top]);
    top--;
    return top;
}

int main()
{
    stack test = stack(5);
    selemtype e;
    test.push(1);
    test.push(2);
    test.push(3);
    test.push(4);
    test.pop(e);
    test.pop(e);
    test.pop(e);
    test.pop(e);
    return 0;
}
```

`top` 从 -1 起始，入栈时先自增再赋值（`a[++top] = elem`），出栈时先取值再自减。与顺序栈的 `top` 指向"下一空位"不同，这里 `top` 指向"当前栈顶元素"。

### 修正点

- `push` 增加 `top + 1 >= capacity` 溢出检查
- `pop` 将出栈元素通过 `selemtype &elem` 引用传出，而非仅打印
- 新增 `capacity` 成员记录栈的实际容量
