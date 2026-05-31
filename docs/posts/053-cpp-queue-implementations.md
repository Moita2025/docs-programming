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
  - 面向对象
---

# 队列的 C 风格与面向对象实现

介绍链式队列、顺序队列、循环队列的 C++ 实现，使用内容标签页对比 C 风格与面向对象两种写法。

<!-- more -->

## 链式队列

链式队列基于单向链表，通过头结点统一管理空队列和出队操作，使用尾插法入队。

```cpp
#include <stdio.h>
#include <stdlib.h>

typedef struct qnode
{
    int data;
    struct qnode * next;
} qnode;

qnode * initqueue()
{
    qnode * queue = (qnode*)malloc(sizeof(qnode));
    queue->next = NULL;
    return queue;
}

qnode* enqueue(qnode * rear, int data)
{
    qnode * enElem = (qnode*)malloc(sizeof(qnode));
    enElem->data = data;
    enElem->next = NULL;
    // 使用尾插法，新元素成为队尾元素
    rear->next = enElem;
    rear = enElem;
    return rear;
}

qnode* dequeue(qnode * top, qnode * rear)
{
    if (top->next == NULL)
    {
        printf("\n队列为空");
        return rear;
    }
    qnode * p = top->next;
    printf("%d ", p->data);
    top->next = p->next;
    if (rear == p)
    {
        rear = top;
    }
    free(p);
    return rear;
}

void destroyqueue(qnode * queue)                        // 新增：释放链式队列所有节点
{
    qnode * p = queue;
    while (p != NULL)
    {
        qnode * tmp = p;
        p = p->next;
        free(tmp);
    }
}

int main()
{
    qnode * queue, *top, *rear;
    queue = top = rear = initqueue();  // 创建头结点
    // 入队，使用尾插法，同时队尾指针指向最后一个元素
    rear = enqueue(rear, 1);
    rear = enqueue(rear, 2);
    rear = enqueue(rear, 3);
    rear = enqueue(rear, 4);
    // 出队
    rear = dequeue(top, rear);
    rear = dequeue(top, rear);
    rear = dequeue(top, rear);
    rear = dequeue(top, rear);
    rear = dequeue(top, rear);
    destroyqueue(queue);                                 // 新增：释放内存
    return 0;
}
```

`enqueue` 采用尾插法，新结点接到队尾之后并将 `rear` 后移。`dequeue` 从头结点之后取出元素，如果出队后队列变空，将 `rear` 重置为头结点。`destroyqueue` 遍历链表逐个释放结点，防止内存泄漏。

## 顺序队列

顺序队列基于定长数组，通过取模运算实现循环利用存储空间。下面将函数式写法和面向对象写法并列展示。

=== "C 风格"

    ```cpp
    #include <stdio.h>

    #define max 5  // 顺序队列的空间大小

    int enqueue(int *a, int front, int rear, int data)
    {
        // 队列满判断：如果 rear+1 与 front 重合，表示队列已满
        if ((rear + 1) % max == front)
        {
            printf("空间已满");
            return rear;
        }
        a[rear % max] = data;
        rear++;
        return rear;
    }

    int dequeue(int *a, int front, int rear)
    {
        // 队列空判断：如果 front == rear%max，表示队列为空
        if (front == rear % max)
        {
            printf("队列为空");
            return front;
        }
        printf("%d ", a[front]);
        front = (front + 1) % max;
        return front;
    }

    int main()
    {
        int a[max];
        int front, rear;
        // 初始化队头和队尾指针，队列无元素时两者指向同一位置
        front = rear = 0;
        // 入队
        rear = enqueue(a, front, rear, 1);
        rear = enqueue(a, front, rear, 2);
        rear = enqueue(a, front, rear, 3);
        rear = enqueue(a, front, rear, 4);
        // 出队
        front = dequeue(a, front, rear);
        // 再入队
        rear = enqueue(a, front, rear, 5);
        // 再出队
        front = dequeue(a, front, rear);
        // 再入队
        rear = enqueue(a, front, rear, 6);
        // 再出队
        front = dequeue(a, front, rear);
        front = dequeue(a, front, rear);
        front = dequeue(a, front, rear);
        front = dequeue(a, front, rear);
        return 0;
    }
    ```

=== "面向对象"

    ```cpp
    #include <stdio.h>

    #define max 50  // 顺序队列的空间大小

    typedef int elemtype;

    class queue
    {
    public:
        elemtype a[max];
        int front, rear;
        queue();

        int enqueue(elemtype data);
        int dequeue();
    };

    queue::queue()
    {
        front = rear = 0;
    }

    int queue::enqueue(elemtype data)
    {
        if ((rear + 1) % max == front)
        {
            printf("空间已满");
            return rear;
        }
        a[rear % max] = data;
        rear++;
        return rear;
    }

    int queue::dequeue()
    {
        if (front == rear % max)
        {
            printf("队列为空");
            return front;
        }
        printf("%d ", a[front]);
        front = (front + 1) % max;
        return front;
    }

    int main()
    {
        queue q = queue();
        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);
        q.enqueue(4);
        q.dequeue();
        q.enqueue(5);
        q.dequeue();
        q.enqueue(6);
        q.dequeue();
        q.dequeue();
        q.dequeue();
        q.dequeue();
        return 0;
    }
    ```

两种风格的核心逻辑一致：`enqueue` 将 `rear` 作为计数累加，通过 `rear % max` 定位写入位置；`dequeue` 对 `front` 取模，保证循环读取出队元素。C 风格将 `front` 和 `rear` 作为函数参数显式传递，面向对象则封装为成员变量。

## 循环队列

循环队列使用动态分配内存，不依赖固定数组，队列长度可灵活调整。同样将 C 风格与面向对象写法并列展示。

注意原代码中两个文件均忘记释放动态分配的内存，这里补充了释放逻辑。

=== "C 风格"

    ```cpp
    #include <stdio.h>
    #include <stdlib.h>

    #define MAXQSIZE 100

    typedef int qelemtype;
    typedef int status;

    typedef struct
    {
        qelemtype * base;
        int front;
        int rear;
    } sqqueue;

    status initqueue(sqqueue &q)
    {
        q.base = (qelemtype *)malloc(MAXQSIZE * sizeof(qelemtype));
        if (!q.base) exit(0);
        q.front = q.rear = 0;
        return 1;
    }

    void destroyqueue(sqqueue &q)                       // 新增：释放动态分配的存储空间
    {
        free(q.base);
        q.base = NULL;
    }

    int queuelength(sqqueue q)
    {
        return (q.rear - q.front + MAXQSIZE) % MAXQSIZE;
    }

    status enqueue(sqqueue &q, qelemtype e)
    {
        if ((q.rear + 1) % MAXQSIZE == q.front) return 0;
        q.base[q.rear] = e;
        printf("入队元素：%d\n", e);
        q.rear = (q.rear + 1) % MAXQSIZE;
        return 1;
    }

    status dequeue(sqqueue &q, qelemtype &e)
    {
        if (q.front == q.rear) return 0;
        e = q.base[q.front];
        printf("出队元素：%d\n", e);
        q.front = (q.front + 1) % MAXQSIZE;
        return 1;
    }

    int main()
    {
        sqqueue q;
        int i;
        initqueue(q);
        enqueue(q, 1);
        enqueue(q, 2);
        enqueue(q, 3);
        enqueue(q, 4);
        enqueue(q, 5);
        dequeue(q, i);
        dequeue(q, i);
        dequeue(q, i);
        dequeue(q, i);
        dequeue(q, i);
        destroyqueue(q);                                 // 新增：释放内存
        return 0;
    }
    ```

=== "面向对象"

    ```cpp
    #include <stdio.h>
    #include <stdlib.h>

    #define MAXQSIZE 100

    typedef int qelemtype;
    typedef int status;

    class sqqueue
    {
    public:
        qelemtype * base;
        int front;
        int rear;
        sqqueue();
        ~sqqueue();                                      // 新增：析构函数声明
        status initqueue();
        int length();
        status enqueue(qelemtype e);
        status dequeue(qelemtype &e);
    };

    sqqueue::sqqueue()
    {
        base = (qelemtype *)malloc(MAXQSIZE * sizeof(qelemtype));
        if (!base) exit(0);
        front = rear = 0;
    }

    sqqueue::~sqqueue()                                  // 新增：析构函数释放内存
    {
        free(base);
    }

    int sqqueue::length()
    {
        return (rear - front + MAXQSIZE) % MAXQSIZE;
    }

    status sqqueue::enqueue(qelemtype e)
    {
        if ((rear + 1) % MAXQSIZE == front) return 0;
        base[rear] = e;
        printf("入队元素：%d\n", e);
        rear = (rear + 1) % MAXQSIZE;
        return 1;
    }

    status sqqueue::dequeue(qelemtype &e)
    {
        if (front == rear) return 0;
        e = base[front];
        printf("出队元素：%d\n", e);
        front = (front + 1) % MAXQSIZE;
        return 1;
    }

    int main()
    {
        int i;
        sqqueue q = sqqueue();
        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);
        q.enqueue(4);
        q.enqueue(5);
        q.dequeue(i);
        q.dequeue(i);
        q.dequeue(i);
        q.dequeue(i);
        q.dequeue(i);
        return 0;
    }
    ```

C 风格通过 `struct` 聚合数据、独立函数操作队列，`initqueue` 和 `destroyqueue` 手动管理生命周期。面向对象将数据和操作封装为类，构造函数分配内存、析构函数自动释放。两者的 `enqueue` 和 `dequeue` 都对 `front` 和 `rear` 做取模处理，队列长度公式 `(rear - front + MAXQSIZE) % MAXQSIZE` 可在任意状态下计算元素个数。
