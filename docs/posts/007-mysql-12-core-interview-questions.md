---
date: 2026-03-06
authors:
  - moita
categories:
  - 数据库
tags:
  - MySQL
  - 理论概念
---

# MySQL 面试常见的 12 个底层问题

下面整理一份 **MySQL 面试最难的 12 个底层问题（大厂常问）**。
这些问题在后端 / 数据库岗位面试中非常常见，尤其涉及 MySQL 的 **InnoDB 引擎底层原理**。🚀

<!-- more -->

---

## 一、索引原理（4题）

### 1. 为什么数据库索引使用 B+Tree？

数据库（如 MySQL、PostgreSQL）通常使用 **B+Tree** 作为索引结构，而不是：

* 二叉树
* AVL树
* 红黑树
* 哈希表

原因主要有 3 个：

#### （1）磁盘 IO 更少

数据库数据存储在 **磁盘页（Page）** 中。

B+Tree：

```
一个节点 ≈ 16KB
一个节点可以存几百个 key
```

所以树高度非常低：

```
1千万数据
B+Tree高度 ≈ 3~4
```

查询：

```
最多 3~4 次磁盘 IO
```

---

#### （2）范围查询效率高

B+Tree 的叶子节点：

```
双向链表
```

结构：

```
1 → 2 → 3 → 4 → 5
```

所以：

```sql
SELECT * FROM user
WHERE id BETWEEN 10 AND 100
```

非常高效。

---

#### （3）查询稳定

二叉树：

```
最坏 O(n)
```

B+Tree：

```
稳定 O(log n)
```

---

### 2. 为什么 B+Tree 高度一般只有 3~4 层？

在 MySQL InnoDB 中：

一个节点：

```
16KB
```

假设：

```
一个key = 8字节
指针 = 8字节
```

一个节点可存：

```
16KB / 16B ≈ 1000 key
```

所以：

```
第一层: 1000
第二层: 1000 × 1000
第三层: 1000 × 1000 × 1000
```

≈ **10亿数据**

因此：

```
B+Tree高度通常 3~4
```

---

### 3. 什么是聚簇索引？

在 MySQL 的 **InnoDB** 中：

**主键索引 = 聚簇索引**

特点：

```
索引 + 数据 在一起
```

结构：

```
B+Tree
  └── 叶子节点 = 整行数据
```

例如：

```
id name age
1  Tom  20
```

存储在叶子节点。

---

### 4. 什么是非聚簇索引（二级索引）

二级索引结构：

```
key → 主键ID
```

例如：

```
name = Tom → id=1
```

查询流程：

```
二级索引
   ↓
主键ID
   ↓
聚簇索引
```

这叫：

```
回表查询
```

---

## 二、事务与 MVCC（4题）

### 5. 什么是 MVCC？

MVCC：

```
Multi-Version Concurrency Control
多版本并发控制
```

用于：

```
提高并发性能
避免读写冲突
```

使用数据库：

* MySQL
* PostgreSQL

---

### 6. MVCC 的核心结构

MVCC 依赖三个组件：

#### 1️⃣ Undo Log

记录：

```
数据旧版本
```

例如：

```
value=10 → 20 → 30
```

Undo log 保存：

```
10
20
```

---

#### 2️⃣ 隐藏字段

InnoDB 每行数据有隐藏字段：

```
trx_id
roll_pointer
```

含义：

```
trx_id = 事务ID
roll_pointer = undo log 指针
```

---

#### 3️⃣ Read View

Read View 记录：

```
当前活跃事务
```

判断：

```
这条数据是否可见
```

---

### 7. MVCC 解决了什么问题？

解决：

```
读写冲突
```

传统锁：

```
读写互斥
```

MVCC：

```
读不加锁
```

优点：

```
高并发
```

---

### 8. 什么是快照读 vs 当前读

在 MySQL 中：

#### 快照读

使用：

```
MVCC
```

例如：

```sql
SELECT * FROM user;
```

---

#### 当前读

读取最新数据并加锁：

```sql
SELECT * FROM user FOR UPDATE;
```

或

```sql
UPDATE user SET age=20;
```

---

## 三、锁机制（2题）

### 9. MySQL 如何解决幻读？

理论上：

```
REPEATABLE READ 会产生幻读
```

但 MySQL 通过：

```
Next-Key Lock
```

解决。

Next-Key Lock：

```
行锁 + 间隙锁
```

例子：

```sql
SELECT * FROM user
WHERE id BETWEEN 10 AND 20
FOR UPDATE
```

锁住：

```
10~20 区间
```

别人不能插入：

```
id=15
```

因此：

```
避免幻读
```

---

### 10. 什么是 Gap Lock（间隙锁）

Gap Lock：

```
锁住索引之间的空隙
```

例如：

```
id: 10 20 30
```

锁住：

```
(10,20)
```

禁止插入：

```
15
```

作用：

```
防止幻读
```

---

## 四、SQL 执行与优化（2题）

### 11. SQL 执行流程

SQL 执行顺序：

```
FROM
JOIN
WHERE
GROUP BY
HAVING
SELECT
ORDER BY
LIMIT
```

例如：

```sql
SELECT name
FROM user
WHERE age>20
ORDER BY age;
```

实际执行：

```
1 FROM
2 WHERE
3 SELECT
4 ORDER BY
```

---

### 12. 什么是覆盖索引？

如果查询字段：

```
全部在索引里
```

数据库：

```
不需要回表
```

例：

索引：

```
(name,age)
```

SQL：

```sql
SELECT name,age
FROM user
WHERE name='Tom'
```

查询：

```
只查索引
```

速度非常快。
