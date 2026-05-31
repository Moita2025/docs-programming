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

# SQL DDL 和 DML

SQL（Structured Query Language）通常按功能分为几类，其中最核心的是 **DDL** 和 **DML**。

<!-- more -->

## （1）DDL：数据定义语言（Data Definition Language）

DDL 用来 **定义和修改数据库结构**，例如表、索引、视图等。

常见命令：

| 命令       | 作用      |
| -------- | ------- |
| CREATE   | 创建数据库对象 |
| ALTER    | 修改数据库对象 |
| DROP     | 删除数据库对象 |
| TRUNCATE | 清空表数据   |

示例：

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
```

修改表结构：

```sql
ALTER TABLE users ADD email VARCHAR(100);
```

删除表：

```sql
DROP TABLE users;
```

特点：

* **操作的是结构（schema）**
* 执行后通常 **自动提交（auto commit）**
* 一般不能回滚（部分数据库除外）

---

## （2）DML：数据操作语言（Data Manipulation Language）

DML 用来 **操作表中的数据**。

常见命令：

| 命令     | 作用   |
| ------ | ---- |
| SELECT | 查询数据 |
| INSERT | 插入数据 |
| UPDATE | 更新数据 |
| DELETE | 删除数据 |

示例：

插入数据：

```sql
INSERT INTO users (id, name, age)
VALUES (1, 'Tom', 20);
```

更新数据：

```sql
UPDATE users
SET age = 21
WHERE id = 1;
```

删除数据：

```sql
DELETE FROM users
WHERE id = 1;
```

特点：

* **操作的是数据**
* 通常 **支持事务**
* 可以 **rollback 回滚**

---

## 总结

**DDL vs DML**

| 类型  | 作用      |
| --- | ------- |
| DDL | 定义数据库结构 |
| DML | 操作数据    |
