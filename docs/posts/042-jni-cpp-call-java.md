---
date: 2026-05-31
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - Java
  - 跨语言
---

# C++ 通过 JNI 调用 Java

JNI（Java Native Interface）最常见的用法是从 Java 调用 C/C++ 原生代码。反向操作——从 C++ 主动创建 JVM 并调用 Java 方法——虽然不常见，但在某些场景下很有用，比如已有的 C++ 应用需要复用 Java 生态的库。

下面记录一个完整的 C++ 调用 Java 的例子。

<!-- more -->

## Java 端：Demo 类

准备一个简单的 Java 类，包含静态字段、实例方法、数组操作和异常抛出：

```java
public class Demo 
{
    public static int COUNT = 8;

    private String msg;
    private int[] counts;

    public Demo() {
        this("default constructor");
    }

    public Demo(String msg) {
        this.msg = msg;
        this.counts = null;
    }

    public String getMessage() {
        return msg;
    }

    public static String getHelloWorld() {
        return "hello world!";
    }

    public String append(String str, int i) {
        return str + i;
    }

    public int[] getCounts() {
        return counts;
    }

    public void setCounts(int[] counts) {
        this.counts = counts;
    }

    public void throwExcp() throws IllegalAccessException {
        throw new IllegalAccessException("exception occurs");
    }
}
```

编译为 class 文件：

```bash
javac Demo.java
```

## C++ 端：创建 JVM 并调用 Java 方法

### 1. 加载 JVM 动态库

Windows 下需要加载 `jvm.dll`，然后通过 `GetProcAddress` 获取 `JNI_CreateJavaVM` 函数指针：

```cpp
#include <Windows.h> 
#include "include/jni.h"
#include <string> 
#include <iostream>

using namespace std;

jstring NewJString(JNIEnv * env, LPCTSTR str);
string JStringToCString(JNIEnv * env, jstring str);

int main() {
    typedef jint(WINAPI * PFunCreateJavaVM)(JavaVM **, void **, void *);

    JavaVMInitArgs vm_args;
    JavaVMOption options[3];
    JavaVM * jvm;
    JNIEnv * env;

    options[0].optionString = (char *)"-Djava.compiler=NONE";
    options[1].optionString = (char *)"-Djava.class.path=.;./Demo.class";
    options[2].optionString = (char *)"-verbose:NONE";

    vm_args.version = JNI_VERSION_1_4;
    vm_args.nOptions = 3;
    vm_args.options = options;
    vm_args.ignoreUnrecognized = JNI_TRUE;

    HINSTANCE hInstance = ::LoadLibrary(
        "C:\\Program Files\\Java\\jdk1.7.0_07\\jre\\bin\\server\\jvm.dll");
    if (hInstance == NULL)
        return 10;

    PFunCreateJavaVM funCreateJavaVM = 
        (PFunCreateJavaVM)::GetProcAddress(hInstance, "JNI_CreateJavaVM");

    int res = (*funCreateJavaVM)(&jvm, (void **)&env, &vm_args);
    if (res < 0) {
        return -1;
    }
```

关键配置项是 `-Djava.class.path`，需要指向 `Demo.class` 所在目录，否则 `FindClass` 会失败。

### 2. 调用实例方法

JNI 方法签名的格式比较特殊，例如 `append` 方法签名 `(Ljava/lang/String;I)Ljava/lang/String;` 表示参数为 String 和 int，返回 String：

```cpp
    jclass cls = env->FindClass("Demo");
    jobject obj = env->AllocObject(cls);

    jmethodID mid = env->GetMethodID(cls, "append", 
        "(Ljava/lang/String;I)Ljava/lang/String;");

    const char szTest[] = "HELLO WORLD";
    jstring arg = NewJString(env, szTest);
    jstring msg = (jstring)env->CallObjectMethod(obj, mid, arg, 12);
    cout << JStringToCString(env, msg);

    jvm->DestroyJavaVM();
    ::FreeLibrary(hInstance);
    return 0;
}
```

`AllocObject` 会调用默认构造函数创建对象，然后通过 `CallObjectMethod` 调用实例方法。

### 3. C++ 与 Java 字符串互转

JNI 中的字符串是 `jstring` 类型，不能直接在 C++ 中使用，需要转换：

```cpp
string JStringToCString(JNIEnv * env, jstring str)
{
    if (str == NULL) {
        return "";
    }

    int len = env->GetStringLength(str);
    wchar_t * w_buffer = new wchar_t[len + 1];
    char * c_buffer = new char[2 * len + 1];
    ZeroMemory(w_buffer, (len + 1) * sizeof(wchar_t));

    const jchar * jcharString = env->GetStringChars(str, 0);
    wcscpy(w_buffer, (wchar_t *)jcharString);
    env->ReleaseStringChars(str, jcharString);

    ZeroMemory(c_buffer, (2 * len + 1) * sizeof(char));
    len = WideCharToMultiByte(CP_ACP, 0, w_buffer, len, 
        c_buffer, 2 * len, NULL, NULL);
    string cstr = c_buffer;

    delete[] w_buffer;
    delete[] c_buffer;
    return cstr;
}

jstring NewJString(JNIEnv * env, LPCTSTR str) {
    if (!env || !str) {
        return 0;
    }
    int slen = strlen(str);
    jchar * buffer = new jchar[slen];
    int len = MultiByteToWideChar(CP_ACP, 0, str, strlen(str), 
        (LPWSTR)buffer, slen);
    if (len > 0 && len < slen) {
        buffer[len] = 0;
    }
    jstring js = env->NewString(buffer, len);
    delete[] buffer;
    return js;
}
```

Java 内部使用 UTF-16 编码，Windows 下 C++ 默认使用 ANSI 编码，因此通过 `MultiByteToWideChar` / `WideCharToMultiByte` 完成编码转换。

## JNI 方法签名速查

JNI 使用一种特定的类型描述符格式：

| Java 类型 | 签名 |
|-----------|------|
| `void` | `V` |
| `int` | `I` |
| `long` | `J` |
| `boolean` | `Z` |
| `String` | `Ljava/lang/String;` |
| `int[]` | `[I` |
| `String[]` | `[Ljava/lang/String;` |

方法签名格式为 `(参数签名)返回值签名`。例如 `int doSomething(String s, long n)` 对应 `(Ljava/lang/String;J)I`。

使用 `javap -s Demo` 可以自动生成类中所有方法的签名，避免手写出错。

## 常见问题

**`FindClass` 返回 NULL**

通常是 classpath 配置不正确。JVM 无法找到 `.class` 文件。确认 `-Djava.class.path` 指向了正确的目录，并且该目录下存在 `Demo.class`。

**`GetMethodID` 返回 NULL**

通常是方法签名写错。用 `javap -s Demo` 检查正确的方法签名。

**加载 `jvm.dll` 失败**

`jvm.dll` 路径依赖于 JDK 安装位置和版本。不同 JDK 版本的路径可能不同：

```text
jdk1.7: jre\bin\server\jvm.dll
jdk1.8: jre\bin\server\jvm.dll
jdk11+: lib\server\jvm.dll
```
