---
date: 2026-05-31
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - 面向对象
---

# C++ 面向对象基础：Student 与 Light 示例

两个简洁的 C++ 类示例，覆盖了面向对象编程的核心机制：构造函数重载、运算符重载、友元函数、继承与方法覆盖。

<!-- more -->

## 示例一：Student 类——运算符重载与友元

```cpp
#include <stdio.h>
#include <string>
#include <iostream>

using namespace std;

class student
{
    public:
        string name;
        int sub1;
        int sub2;
        student();
        student(string val_name, int val_sub1, int val_sub2);
        student operator +(student& stu_right);
        friend void avg(student& val_stu, int num);
        void display();
};

student::student()
{
    name = "Null";
    sub1 = 60;
    sub2 = 60;
}

student::student(string val_name, int val_sub1, int val_sub2)
{
    name = val_name;
    sub1 = val_sub1;
    sub2 = val_sub2;
}

student student::operator +(student& stu_right)
{
    student new_stu("Null",
        this->sub1 + stu_right.sub1,
        this->sub2 + stu_right.sub2);
    return new_stu;
}

void avg(student& val_stu, int num)
{
    val_stu.sub1 /= num;
    val_stu.sub2 /= num;
    printf("%-10s %2d %2d\n", "AvgScore:", val_stu.sub1, val_stu.sub2);
}

void student::display()
{
    printf("%-10s %2d %2d\n", name.c_str(), sub1, sub2);
}

int main()
{
    student s1("Wang", 78, 82), s2("Li", 75, 62);
    student s3("Zeng", 89, 87), s4("Xu", 54, 78), s;

    cout << "Student score: " << endl;
    s1.display();  s2.display();  s3.display();  s4.display();

    s = s1 + s2 + s3 + s4;
    avg(s, 4);

    return 0;
}
```

### 知识点

**构造函数重载**

两个构造函数：无参默认构造和有参构造。各自提供不同的初始化路径：

```cpp
student();                                          // 默认值 "Null", 60, 60
student(string val_name, int val_sub1, int val_sub2); // 外部赋值
```

**运算符重载**

重载 `+` 运算符，实现两个 `student` 对象的成绩逐科相加。支持链式调用 `s1 + s2 + s3 + s4`：

```cpp
student student::operator +(student& stu_right)
{
    student new_stu("Null",
        this->sub1 + stu_right.sub1,
        this->sub2 + stu_right.sub2);
    return new_stu;
}
```

**友元函数**

`avg` 不是类成员，但被声明为 `friend`，可以访问私有成员 `sub1`、`sub2`，直接修改对象值：

```cpp
friend void avg(student& val_stu, int num);
```

输出结果：

```text
Student score:
Wang       78 82
Li         75 62
Zeng       89 87
Xu         54 78
AvgScore:  74 77
```

## 示例二：Light 类——继承与方法覆盖

```cpp
#include <stdio.h>
#include <string>

using namespace std;

class Light
{
    public:
        int watts;
        bool indicator;
        Light(int w);
        Light(int w, bool ind);
        void switchOn();
        void switchOff();
        void printInfo();
};

Light::Light(int w)
{
    watts = w;
    indicator = true;
}

Light::Light(int w, bool ind)
{
    watts = w;
    indicator = ind;
}

void Light::switchOn()
{
    if (indicator == false)
        indicator = true;
}

void Light::switchOff()
{
    if (indicator == true)
        indicator = false;
}

void Light::printInfo()
{
    printf("watts:%d, indicator:%d\n", watts, indicator);
}

class TubeLight : public Light
{
    public:
        int tubeLength;
        string color;
        TubeLight(int w, int tl, string c);
        void printInfo();
};

TubeLight::TubeLight(int w, int tl, string c) : Light(w)
{
    tubeLength = tl;
    color = c;
}

void TubeLight::printInfo()
{
    printf("watts:%d, indicator:%d, tubelength:%d, color:%s\n",
        watts, indicator, tubeLength, color.c_str());
}

int main()
{
    TubeLight(32, 50, "white").printInfo();
    return 0;
}
```

### 知识点

**继承**

`TubeLight` 通过 `public` 继承自 `Light`，获得基类的 `watts`、`indicator` 成员和 `switchOn`、`switchOff` 方法：

```cpp
class TubeLight : public Light { ... };
```

**子类构造中的基类初始化**

子类构造函数通过初始化列表调用基类构造函数：

```cpp
TubeLight::TubeLight(int w, int tl, string c) : Light(w)
{
    tubeLength = tl;
    color = c;
}
```

这里调用的是 `Light(int w)`，`indicator` 会被默认设为 `true`。

**方法覆盖（Overriding）**

`TubeLight` 重新定义了 `printInfo`，输出更多字段。调用时根据对象类型自动匹配子类版本：

```cpp
TubeLight(32, 50, "white").printInfo();
// 输出：watts:32, indicator:1, tubelength:50, color:white
```

## 对比总结

| 特性 | Student 示例 | Light 示例 |
|------|-------------|-----------|
| 构造函数重载 | 有（默认 + 有参） | 有（含瓦数 / 含瓦数+状态） |
| 运算符重载 | `+` 支持链式累加 | 无 |
| 友元函数 | `avg` 直接修改私有成员 | 无 |
| 继承 | 无 | `TubeLight` 继承 `Light` |
| 方法覆盖 | 无 | `printInfo` 子类覆盖 |
