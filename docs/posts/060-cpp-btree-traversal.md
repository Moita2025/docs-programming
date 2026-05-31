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

# 二叉树的链式存储与遍历

介绍二叉树的链式存储结构，以及前序、中序、后序三种遍历的递归与非递归（栈）实现。原代码的非递归前序遍历缺少空树判断和栈顶复位，另外整体缺少释放函数。

<!-- more -->

二叉树通过 `lchild` 和 `rchild` 左右孩子指针构成链式存储。遍历的核心区别在于访问根结点的时机：先根为前序、中间为中序、最后为后序。非递归版本用顺序栈模拟递归调用栈。

## 修正后完整代码

```cpp
#include <stdio.h>
#include <stdlib.h>

#define telemtype int

typedef struct bitnode
{
    telemtype data;
    struct bitnode *lchild, *rchild;
} bitnode, *bitree;

void createbitree(bitree *t)
{
    *t = (bitnode*)malloc(sizeof(bitnode));
    (*t)->data = 1;
    (*t)->lchild = (bitnode*)malloc(sizeof(bitnode));
    (*t)->rchild = (bitnode*)malloc(sizeof(bitnode));

    (*t)->lchild->data = 2;
    (*t)->lchild->lchild = (bitnode*)malloc(sizeof(bitnode));
    (*t)->lchild->rchild = (bitnode*)malloc(sizeof(bitnode));
    (*t)->lchild->rchild->data = 5;
    (*t)->lchild->rchild->lchild = NULL;
    (*t)->lchild->rchild->rchild = NULL;
    (*t)->rchild->data = 3;
    (*t)->rchild->lchild = (bitnode*)malloc(sizeof(bitnode));
    (*t)->rchild->lchild->data = 6;
    (*t)->rchild->lchild->lchild = NULL;
    (*t)->rchild->lchild->rchild = NULL;
    (*t)->rchild->rchild = (bitnode*)malloc(sizeof(bitnode));
    (*t)->rchild->rchild->data = 7;
    (*t)->rchild->rchild->lchild = NULL;
    (*t)->rchild->rchild->rchild = NULL;
    (*t)->lchild->lchild->data = 4;
    (*t)->lchild->lchild->lchild = NULL;
    (*t)->lchild->lchild->rchild = NULL;
}

void displayelem(bitnode* elem)
{
    printf("%d ", elem->data);
}

// ===== 递归遍历 =====

void preordertraverse_recursion(bitree t)
{
    if (t)
    {
        displayelem(t);
        preordertraverse_recursion(t->lchild);
        preordertraverse_recursion(t->rchild);
    }
}

void inordertraverse_recursion(bitree t)
{
    if (t)
    {
        inordertraverse_recursion(t->lchild);
        displayelem(t);
        inordertraverse_recursion(t->rchild);
    }
}

void postordertraverse_recursion(bitree t)
{
    if (t)
    {
        postordertraverse_recursion(t->lchild);
        postordertraverse_recursion(t->rchild);
        displayelem(t);
    }
}

// ===== 非递归遍历（栈实现） =====

int top = -1;

void push(bitnode** a, bitnode* elem)
{
    a[++top] = elem;
}

void pop()
{
    if (top == -1) return;
    top--;
}

bitnode* gettop(bitnode** a)
{
    return a[top];
}

void preordertraverse(bitree tree)
{
    bitnode* a[20];
    bitnode * p;
    top = -1;                                            // 修正：每次调用复位栈顶
    if (!tree) return;                                   // 修正：空树直接返回
    push(a, tree);
    while (top != -1)
    {
        p = gettop(a);
        pop();
        while (p)
        {
            displayelem(p);
            if (p->rchild)
                push(a, p->rchild);
            p = p->lchild;
        }
    }
}

void inordertraverse(bitree tree)
{
    bitnode* a[20];
    bitnode * p;
    p = tree;
    top = -1;
    while (p || top != -1)
    {
        if (p)
        {
            push(a, p);
            p = p->lchild;
        }
        else
        {
            p = gettop(a);
            pop();
            displayelem(p);
            p = p->rchild;
        }
    }
}

typedef struct snode
{
    bitree p;
    int tag;
} snode;

void postpush(snode *a, snode sdata)
{
    a[++top] = sdata;
}

void postordertraverse(bitree tree)
{
    snode a[20];
    bitnode * p;
    int tag;
    snode sdata;
    p = tree;
    top = -1;
    while (p || top != -1)
    {
        while (p)
        {
            sdata.p = p;
            sdata.tag = 0;
            postpush(a, sdata);
            p = p->lchild;
        }
        sdata = a[top];
        pop();
        p = sdata.p;
        tag = sdata.tag;
        if (tag == 0)
        {
            sdata.p = p;
            sdata.tag = 1;
            postpush(a, sdata);
            p = p->rchild;
        }
        else
        {
            displayelem(p);
            p = NULL;
        }
    }
}

// ===== 释放 =====

void freebitree(bitree *t)                               // 新增：递归释放二叉树所有结点
{
    if (*t)
    {
        freebitree(&(*t)->lchild);
        freebitree(&(*t)->rchild);
        free(*t);
        *t = NULL;
    }
}

// ===== 使用示例 =====

int main()
{
    bitree tree;
    createbitree(&tree);

    printf("前序 递归: ");
    preordertraverse_recursion(tree);
    printf("\n");

    printf("前序 非递归: ");
    preordertraverse(tree);
    printf("\n");

    printf("中序 递归: ");
    inordertraverse_recursion(tree);
    printf("\n");

    printf("中序 非递归: ");
    inordertraverse(tree);
    printf("\n");

    printf("后序 递归: ");
    postordertraverse_recursion(tree);
    printf("\n");

    printf("后序 非递归: ");
    postordertraverse(tree);
    printf("\n");

    freebitree(&tree);                                   // 新增：释放内存
    return 0;
}
```

`createbitree` 构造了一棵 7 个结点的满二叉树，结构为：

```text
    1
   / \
  2   3
 / \ / \
4  5 6  7
```

### 遍历策略

**递归遍历** 三种方式结构一致，仅 `displayelem` 调用位置不同：前序在递归左右子树之前、中序在两者之间、后序在两者之后。

**非递归遍历** 均用数组模拟栈：

- **前序**：根入栈，出栈后先访问，再将右孩子、左孩子依次入栈（后进先出保证左先于右）。
- **中序**：沿左链一路压栈到底，出栈访问后再转向右子树。
- **后序**：结点带 `tag` 标志位，初次出栈时 `tag=0` 表示左子树已处理、需转向右子树，改 `tag=1` 后重新入栈；再次出栈时 `tag=1` 表示左右均处理完毕，此时访问。

### 修正点

- 非递归前序遍历补充了 `top = -1` 复位和空树 `return`，防止栈状态混乱与空指针访问。
- 新增 `freebitree` 对整棵树做后序释放，避免内存泄漏。
