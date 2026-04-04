---
date: 2026-03-06
authors:
  - moita
categories:
  - 数据库
tags:
  - SQL
  - 理论概念
---

# SQL 的四个隔离级别

数据库事务隔离级别是为了控制 **并发事务之间互相影响的程度**。
标准来自 **ANSI SQL**。

<!-- more -->

四个隔离级别：

| 隔离级别             | 是否允许脏读 | 是否允许不可重复读 | 是否允许幻读 |
| ---------------- | ------ | --------- | ------ |
| READ UNCOMMITTED | ✅      | ✅         | ✅      |
| READ COMMITTED   | ❌      | ✅         | ✅      |
| REPEATABLE READ  | ❌      | ❌         | ✅      |
| SERIALIZABLE     | ❌      | ❌         | ❌      |

## 三种并发问题

先理解三种并发问题：

### （1）脏读（Dirty Read）

读取了 **未提交事务的数据**。

例子：

```
事务A: UPDATE account SET money=1000
事务B: SELECT money (读到1000)
事务A: ROLLBACK
```

B读到的数据是假的。

---

### （2）不可重复读（Non-repeatable Read）

同一事务 **两次读取同一数据结果不同**。

例子：

```
事务A: SELECT money = 100
事务B: UPDATE money = 200 COMMIT
事务A: 再次 SELECT money = 200
```

---

### （3）幻读（Phantom Read）

同一事务 **两次查询记录数量不同**。

例子：

```
事务A: SELECT count(*) = 10
事务B: INSERT 新记录 COMMIT
事务A: SELECT count(*) = 11
```

像出现了“幻影”。

---

## 四个隔离级别解释

### 1️⃣ READ UNCOMMITTED（读未提交）

* 可以读未提交数据
* 性能最好
* 但数据一致性最差

几乎不用。

---

### 2️⃣ READ COMMITTED（读已提交）

* 只能读 **已提交数据**
* 防止脏读
* 但仍有不可重复读

很多数据库默认：

* Oracle Database
* Microsoft SQL Server

---

### 3️⃣ REPEATABLE READ（可重复读）

* 同一事务读取同一行数据结果一致
* 防止脏读 + 不可重复读
* 可能出现幻读

默认级别：

* MySQL（InnoDB）

---

### 4️⃣ SERIALIZABLE（串行化）

最高隔离级别：

* 所有事务 **按顺序执行**
* 完全避免并发问题

缺点：

* **性能很差**
* 锁非常多

---

## 总结

**SQL 四个隔离级别**

```
READ UNCOMMITTED
READ COMMITTED
REPEATABLE READ
SERIALIZABLE
```

隔离级别越高：

```
一致性越好
性能越低
```
