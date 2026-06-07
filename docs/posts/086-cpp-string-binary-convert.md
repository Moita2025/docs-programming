---
date: 2026-06-07
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - 字符串
---

# C++ 字符串与二进制串相互转换

两份实现相同功能的代码——把字符串展成二进制串，再从二进制串还原。一份硬编码 64 位、只认 8 字符；另一份用 `vector<bool>` 动态扩容、支持任意长度。

<!-- more -->

## 版本一：硬编码 64 位

```cpp
#include <iostream>
#include <bitset>
#include <string>
#include <algorithm>
using namespace std;

string StrToBitStr(string str)
{
    bitset<64> bstr;
    for (int i = 0; i < 8; i++)
    {
        bitset<8> bits = bitset<8>(str[i]);
        for (int j = 0; j < 8; j++)
            bstr[i * 8 + j] = bits[7 - j];
    }
    string s = bstr.to_string();
    reverse(begin(s), end(s));
    return s;
}

string BitStrToStr(string bstr)
{
    string str = "";
    int sum;
    for (int i = 0; i < bstr.size(); i += 8)
    {
        sum = 0;
        for (int j = 0; j < 8; j++)
            if (bstr[i + j] == '1')
                sum = sum * 2 + 1;
            else
                sum = sum * 2;
        str = str + char(sum);
    }
    return str;
}

int main()
{
    string bstr = StrToBitStr("generate");       // 恰好 8 个字符
    cout << bstr << endl;
    cout << BitStrToStr(bstr) << endl;
}
```

### 问题

**`bitset<64>` 把容量写死了**。传入字符串必须恰好 8 个字符。少一个——`str[i]` 读到未定义区域；多一个——只取前 8 个。实际使用时几乎不可能控制输入长度。

**`reverse` 无条件执行**。`bitset` 的 `to_string()` 输出是高位在左（类似 `01100111...`），`reverse` 后低位在左。还原时也必须先反转才能按相同逻辑解析。这个约定在程序中没有任何说明，调用者无从知晓。

**`sum` 用 `int`**。`char(sum)` 在 `sum ≥ 128` 时被解释为有符号值，虽在多数平台上不影响字节内容，但类型选择不够精确，改用 `unsigned char` 更准确。

## 版本二：动态长度 + 测试套件

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <bitset>

using namespace std;

string StrToBitStr(const string& src, bool isReverse = false)
{
    const size_t totalBits = src.size() * 8;
    vector<bool> bits(totalBits);

    for (size_t i = 0; i < src.size(); ++i) {
        bitset<8> chBits(static_cast<unsigned char>(src[i]));
        for (size_t j = 0; j < 8; ++j) {
            bits[i * 8 + j] = chBits[7 - j];
        }
    }

    string bin;
    bin.reserve(totalBits);
    for (bool b : bits) bin.push_back(b ? '1' : '0');

    if (isReverse) reverse(bin.begin(), bin.end());

    return bin;
}

string BitStrToStr(const string& bin, bool isReverse = false)
{
    string rev = bin;
    if (isReverse) reverse(rev.begin(), rev.end());

    string out;
    out.reserve(rev.size() / 8);

    for (size_t i = 0; i < rev.size(); i += 8) {
        unsigned char value = 0;
        for (size_t j = 0; j < 8; ++j) {
            value = static_cast<unsigned char>(
                (value << 1) | (rev[i + j] == '1' ? 1 : 0));
        }
        out.push_back(static_cast<char>(value));
    }
    return out;
}

int main()
{
    vector<string> tests = {
        "a", "ab", "abc", "hello", "world!", "generate",
        "this is a longer test string"
    };

    for (const auto& t : tests) {
        string bin = StrToBitStr(t);
        string back = BitStrToStr(bin);
        cout << "orig: \"" << t << "\"\n"
             << "  bits (" << bin.size() << "): " << bin << "\n"
             << "  back: \"" << back << "\"\n"
             << (t == back ? "  OK\n" : "  MISMATCH!\n")
             << string(40, '-') << '\n';
    }
}
```

版本二的核心改进：

- **`vector<bool>` 动态扩容**，输入多长就分配多少位，不再限死 8 字符
- **反转设为可选项**，`isReverse` 默认 `false`，调用者显式传入时才翻转
- **`value` 使用 `unsigned char`**，逐位拼入时不受符号位干扰
- **`reserve` 预分配**字符串容量，减少多次 push_back 的重新分配开销
- **测试用例覆盖**单字符、短串、带空格长串，自动比对往返结果

## 转换原理

两版遵循同一核心流程：

**正向（字符串 → 二进制串）：**

1. 取出字符的 ASCII 码（如 `'a'` = 97）
2. 用 `bitset<8>` 展开为 8 位二进制（97 = `01100001`）
3. 按 `bitset` 的序号惯例，`bits[0]` 是最低位，所以用 `bits[7-j]` 让高位排在左边
4. 每位转为 `'0'` 或 `'1'` 拼入结果串

**反向（二进制串 → 字符串）：**

1. 每 8 个 `'0'`/`'1'` 为一组
2. 累加 `value = value * 2 + bit`，还原出原始字节
3. 将字节 `static_cast<char>` 追加到输出串

两份代码计算的二进制内容完全相同，差别仅在容量边界和工程细节上。
