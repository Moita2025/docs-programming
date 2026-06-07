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

# C++ 哈夫曼树三种实现

哈夫曼树（Huffman Tree）是数据压缩中的经典算法，核心操作为"从候选节点中反复选取两个权值最小的节点合并"。下面是三种 C++ 实现方案，各自存在一些值得修正的问题。

<!-- more -->

## 实现一：类封装 + Select 内联

用 `ElemType` 结构体存储权值与父子关系，`Select` 以线性扫描找最小两节点。

### 查出的问题

1. `main` 中 `HuffmanTree H(h, 4)` 硬编码了 `4`，应改为 `n`
2. 构造函数 `new` 分配内存但缺少析构函数释放，造成内存泄漏
3. `Select` 函数内循环缩进容易误导

### 修正后代码

```cpp
#include <iostream>
using namespace std;

struct ElemType
{
    int weight;
    int parent, lchild, rchild;
};

class HuffmanTree
{
public:
    HuffmanTree(int w[], int n);
    ~HuffmanTree();
    void Print();
private:
    ElemType *huffTree;
    int num;
    void Select(int n, int &i1, int &i2);
};

void HuffmanTree::Select(int n, int &i1, int &i2)
{
    int temp;
    int i = 0;
    for (; i < n; i++)
        if (huffTree[i].parent == -1) { i1 = i; break; }
    for (i = i + 1; i < n; i++)
        if (huffTree[i].parent == -1) { i2 = i; break; }

    if (huffTree[i1].weight > huffTree[i2].weight)
    {
        temp = i1; i1 = i2; i2 = temp;
    }

    for (i = i + 1; i < n; i++)
    {
        if (huffTree[i].parent == -1)
        {
            if (huffTree[i].weight < huffTree[i1].weight)
            {
                i2 = i1; i1 = i;
            }
            else if (huffTree[i].weight < huffTree[i2].weight)
            {
                i2 = i;
            }
        }
    }
}

HuffmanTree::HuffmanTree(int w[], int n)
{
    num = n;
    huffTree = new ElemType[2 * n - 1];
    for (int i = 0; i < 2 * num - 1; i++)
    {
        huffTree[i].parent = -1;
        huffTree[i].lchild = huffTree[i].rchild = -1;
    }

    for (int i = 0; i < num; i++)
        huffTree[i].weight = w[i];

    for (int k = num; k < 2 * num - 1; k++)
    {
        int i1, i2;
        Select(k, i1, i2);
        huffTree[k].weight = huffTree[i1].weight + huffTree[i2].weight;
        huffTree[i1].parent = k;
        huffTree[i2].parent = k;
        huffTree[k].lchild = i1;
        huffTree[k].rchild = i2;
    }
}

HuffmanTree::~HuffmanTree()
{
    delete[] huffTree;
}

void HuffmanTree::Print()
{
    cout << "叶子到根的路径:" << endl;
    for (int i = 0; i < num; i++)
    {
        cout << huffTree[i].weight;
        int k = huffTree[i].parent;
        while (k != -1)
        {
            cout << "-->" << huffTree[k].weight;
            k = huffTree[k].parent;
        }
        cout << endl;
    }
}

int main()
{
    int n;
    cout << "输入叶子结点数：";
    cin >> n;
    int *h = new int[n];
    cout << "输入叶子结点权值：";
    for (int i = 0; i < n; i++)
        cin >> h[i];

    cout << "叶结点权值分别是：";
    for (int i = 0; i < n; i++)
        cout << h[i] << " ";
    cout << endl;

    HuffmanTree H(h, n);  // 修正：用 n 而非硬编码 4
    H.Print();

    delete[] h;
    return 0;
}
```

**修正点**：`HuffmanTree H(h, n)` 替代硬编码 `4`；新增析构函数 `~HuffmanTree()` 释放 `huffTree`。

---

## 实现二：map 辅助 Select + 编解码

使用 `map<int, int>` 按权值排序选最小两节点，并实现了完整的编码表生成与密文解码。

### 查出的问题

`Select` 中用 `map<int, int>` 以权值为 key，当两个节点权值相同时后插入的会被忽略（map 禁止重复 key），导致少选一个节点，哈夫曼树构建错误。这是关键 bug。

### 修正：用线性扫描替代 map

```cpp
void Select(HuffNode *HT, int n, int &T1, int &T2)
{
    T1 = T2 = 0;
    int min1 = 0x7fffffff, min2 = 0x7fffffff;
    for (int i = 1; i <= n; i++)
    {
        if (HT[i].parent == 0)
        {
            if (HT[i].weight < min1)
            {
                min2 = min1; T2 = T1;
                min1 = HT[i].weight; T1 = i;
            }
            else if (HT[i].weight < min2)
            {
                min2 = HT[i].weight; T2 = i;
            }
        }
    }
}
```

一次遍历同时维护最小和次小，正确处理了重复权值。其余代码保持不变。

---

## 实现三：非递归 Huffman 编码

遍历建树后，用非递归方式（模拟栈）生成哈夫曼编码，无需递归。

### 查出的问题

1. **`find` 中用 `m_parent = 1` 临时标记已选节点**——`1` 可能与有效节点下标冲突，属于脆弱的 hack
2. **`HuffmanCoding` 直接用 `weight` 字段做访问标记**——覆盖了原始权值，虽然编码时不再需要权值，但这种复用成员变量做状态标记的方式增加了维护风险
3. **缺少内存释放**——`HT.m_Htree` 和 `HC` 均为 `new` 分配但无 `delete`

### 修正后关键函数

`find` 改为不修改 `m_parent` 的版本：

```cpp
void find(HTree &HT, int pos, int &min1, int &min2)
{
    int m1 = -1, m2 = -1;
    for (int i = 0; i < pos; i++)
    {
        if (HT.m_Htree[i].m_parent != -1) continue;
        if (m1 == -1 || HT.m_Htree[i].weight < HT.m_Htree[m1].weight)
        {
            m2 = m1;
            m1 = i;
        }
        else if (m2 == -1 || HT.m_Htree[i].weight < HT.m_Htree[m2].weight)
        {
            m2 = i;
        }
    }
    min1 = m1;
    min2 = m2;
}
```

取消 `m_parent = 1` 的临时修改，`createHTree` 中紧随其后设置正确的 `m_parent`，逻辑不变且更清晰。

---

## 三个实现的对比

| 特性 | 实现一 | 实现二 | 实现三 |
|------|--------|--------|--------|
| Select 方式 | 线性扫描，手动维护 i1/i2 | ~~map（有 bug）~~ → 修正为线性扫描 | 线性扫描，但临时改 m_parent |
| 内存管理 | 定长数组 `new[]`，有析构 | 定长数组 `new[]`，无释放 | 定长数组 `new[]`，无释放 |
| 编码生成 | 无 | 有，递归栈翻转 | 有，非递归 DFS |
| 解码 | 无 | 有 | 无 |
| 主要问题 | 硬编码参数 + 泄漏 | Select 丢重复权值 | find hack + 泄漏 |

哈夫曼树的核心正确性在于 `Select` 能否在重复权值场景下正确选出两个节点。实现二的 map 方式是最隐蔽的 bug——不影响编译，但在特定输入下产生错误的编码表。
