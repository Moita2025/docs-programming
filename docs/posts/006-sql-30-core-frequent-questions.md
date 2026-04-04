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

# SQL 面试最常问的 30 个核心知识点

下面整理了一份 **SQL 面试最常问的 30 个核心知识点**（偏后端 / 数据库工程师 / 大厂面试）。我按 **6 大模块**整理，这样复习效率最高。🚀

<!-- more -->

## 一、SQL 基础（5题）

### 1. 什么是 SQL？

SQL 是 **结构化查询语言**，用于操作关系型数据库，例如：

* MySQL
* PostgreSQL
* Oracle Database
* Microsoft SQL Server

SQL 主要包括：

| 类型  | 作用      |
| --- | ------- |
| DDL | 定义数据库结构 |
| DML | 操作数据    |
| DCL | 权限控制    |
| TCL | 事务控制    |

---

### 2. DELETE、TRUNCATE、DROP 区别

| 命令       | 类型  | 作用    |
| -------- | --- | ----- |
| DELETE   | DML | 删除表数据 |
| TRUNCATE | DDL | 清空表   |
| DROP     | DDL | 删除表结构 |

关键区别：

| 特性       | DELETE | TRUNCATE |
| -------- | ------ | -------- |
| rollback | ✅      | ❌        |
| where    | ✅      | ❌        |
| 速度       | 慢      | 快        |

---

### 3. WHERE 和 HAVING 的区别

|        | WHERE | HAVING |
| ------ | ----- | ------ |
| 执行阶段   | 分组前   | 分组后    |
| 是否支持聚合 | ❌     | ✅      |

例子：

```sql
SELECT dept, COUNT(*)
FROM employees
GROUP BY dept
HAVING COUNT(*) > 5;
```

---

### 4. INNER JOIN vs LEFT JOIN

**INNER JOIN**

```sql
SELECT *
FROM A
INNER JOIN B
ON A.id = B.id
```

只返回 **两表都有的数据**

---

**LEFT JOIN**

```sql
SELECT *
FROM A
LEFT JOIN B
ON A.id = B.id
```

返回：

```
A全部 + B匹配
```

---

### 5. GROUP BY 的执行流程

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

面试经常问 ⚠️

---

## 二、索引（6题）

### 6. 什么是索引？

索引类似：

```
书的目录
```

作用：

```
提高查询速度
```

---

### 7. 索引的底层结构

大部分数据库使用：

**B+Tree**

例如：

* MySQL InnoDB
* PostgreSQL

原因：

* 查询稳定
* 支持范围查询
* 磁盘IO少

---

### 8. B+Tree vs B-Tree

| 特点    | B-Tree | B+Tree |
| ----- | ------ | ------ |
| 数据存储  | 所有节点   | 叶子节点   |
| 范围查询  | 一般     | 非常好    |
| 数据库使用 | 少      | 多      |

---

### 9. 什么是覆盖索引

如果查询字段：

```
全部在索引里
```

数据库就 **不用回表**。

例：

```sql
SELECT id,name
FROM user
WHERE name='Tom'
```

如果索引：

```
(name,id)
```

就是 **覆盖索引**。

---

### 10. 什么是最左前缀原则

联合索引：

```
(a,b,c)
```

能用索引：

```
a
a,b
a,b,c
```

不能用：

```
b
c
b,c
```

---

### 11. 索引失效情况

常见：

1️⃣ 使用函数

```sql
WHERE YEAR(create_time)=2024
```

2️⃣ 使用 `%` 前缀

```sql
LIKE '%abc'
```

3️⃣ 类型不匹配

4️⃣ OR 条件

---

## 三、事务（5题）

### 12. 什么是事务

事务是：

```
一组 SQL 要么全部成功
要么全部失败
```

---

### 13. ACID 特性

事务四大特性：

| 特性          | 含义  |
| ----------- | --- |
| Atomicity   | 原子性 |
| Consistency | 一致性 |
| Isolation   | 隔离性 |
| Durability  | 持久性 |

---

### 14. SQL 四个隔离级别

| 隔离级别             | 问题    |
| ---------------- | ----- |
| READ UNCOMMITTED | 脏读    |
| READ COMMITTED   | 不可重复读 |
| REPEATABLE READ  | 幻读    |
| SERIALIZABLE     | 无     |

默认：

* MySQL → REPEATABLE READ

---

### 15. 什么是 MVCC

MVCC：

```
Multi Version Concurrency Control
多版本并发控制
```

作用：

```
提高并发性能
避免读写冲突
```

常见数据库：

* MySQL
* PostgreSQL

---

### 16. 什么是死锁

两个事务互相等待锁。

例：

```
事务A 锁表1
事务B 锁表2
A 等待 表2
B 等待 表1
```

数据库会 **自动检测并回滚一个事务**。

---

## 四、锁机制（4题）

### 17. 行锁 vs 表锁

| 类型 | 特点  |
| -- | --- |
| 行锁 | 并发高 |
| 表锁 | 并发低 |

---

### 18. 共享锁 vs 排他锁

| 锁      | 作用   |
| ------ | ---- |
| 共享锁（S） | 可以读  |
| 排他锁（X） | 可以读写 |

---

### 19. 什么是间隙锁（Gap Lock）

用于防止：

```
幻读
```

出现于：

* MySQL InnoDB

---

### 20. Next-Key Lock

Next-Key Lock =

```
行锁 + 间隙锁
```

作用：

```
解决幻读
```

---

## 五、SQL 优化（5题）

### 21. SQL 优化方法

常见：

1️⃣ 建立索引
2️⃣ 避免 `SELECT *`
3️⃣ 避免子查询
4️⃣ 使用分页
5️⃣ 减少 JOIN

---

### 22. EXPLAIN 是什么

用于查看：

```
SQL 执行计划
```

例如：

```sql
EXPLAIN SELECT * FROM user WHERE id=1;
```

可以看到：

* 是否走索引
* 扫描行数

---

### 23. 慢查询怎么排查

常用方法：

1️⃣ 开启慢查询日志
2️⃣ 用 EXPLAIN
3️⃣ 看索引
4️⃣ 看扫描行数

---

### 24. 什么是回表查询

查询流程：

```
先查索引
再查主键
再回表
```

会导致：

```
性能下降
```

---

### 25. 什么是索引下推

优化：

```
Index Condition Pushdown
```

在 **索引层过滤数据**。

数据库：

* MySQL

---

## 六、数据库设计（5题）

### 26. 什么是三范式

数据库设计原则：

| 范式   | 作用     |
| ---- | ------ |
| 第一范式 | 字段不可分  |
| 第二范式 | 消除部分依赖 |
| 第三范式 | 消除传递依赖 |

---

### 27. 什么是反范式

为了 **性能优化**：

```
允许冗余
```

例如：

```
订单表存用户名
```

---

### 28. 什么是分库分表

当数据量太大：

```
单表 > 千万级
```

解决方案：

```
水平拆分
```

常见方案：

```
user_001
user_002
user_003
```

---

### 29. 什么是读写分离

架构：

```
主库：写
从库：读
```

提高性能。

---

### 30. 什么是主键设计

推荐：

```
自增ID 或 雪花ID
```

避免：

```
UUID 随机
```

原因：

```
B+Tree 插入效率低
```
