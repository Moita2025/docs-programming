---
date: 2026-03-06
authors:
  - moita
categories:
  - 数据库
tags:
  - SQL
  - 性能优化
---

# SQL 性能优化

<div class="quote-card">
    <div class="quote-content">
        <ol>
            <li>Select 语句中最好不用 *，只选取要用的列</li>
            <li>Where 子句里不要使用函数</li>
        </ol>
        这两个sql性能优化tips，是 mysql 的“特性”，还是其他 sql 数据库通用的？
    </div>
</div>

这两个 SQL 优化建议 **不是只针对 MySQL 的特性**，而是 **大多数关系型数据库通用的经验**。包括：

<!-- more -->

* MySQL
* PostgreSQL
* Oracle Database
* Microsoft SQL Server

基本都适用，不过**原因和影响程度在不同数据库里会略有差别**。下面分别解释。

---

## 1. SELECT 最好不要用 `*`

```sql
SELECT * FROM user;
```

建议写成：

```sql
SELECT id, name, email FROM user;
```

### 为什么这样更好

#### 1️⃣ 减少 I/O 和网络传输

数据库需要读取的列越多，磁盘读取和网络传输越大。

例如表：

```
user
id
name
email
address
avatar_blob
create_time
```

如果只需要 `id,name` 却 `SELECT *`：

* 数据库仍然读取所有列
* 可能包含 **大字段（TEXT/BLOB）**
* 结果传输更大

在所有数据库中都会影响性能。

---

#### 2️⃣ 有利于 **覆盖索引（Covering Index）**

例如：

```sql
SELECT id, name FROM user WHERE name='Tom'
```

如果有索引：

```
index(name, id)
```

数据库可以：

**直接从索引返回结果，不访问表数据**

这叫 **覆盖索引**。

如果写：

```sql
SELECT *
```

数据库就必须：

```
索引 → 找到行 → 回表读取所有列
```

这一点在：

* MySQL（尤其明显）
* PostgreSQL
* Microsoft SQL Server

都成立。

---

#### 3️⃣ schema 变更风险

如果以后表增加列：

```
ALTER TABLE user ADD column ...
```

`SELECT *` 可能导致：

* 程序解析错误
* ORM 映射错误
* 返回数据变大

这是工程实践问题，不只是性能。

---

## 2. WHERE 子句不要对列使用函数

例如：

```sql
SELECT * FROM user
WHERE DATE(create_time) = '2024-01-01';
```

这样会导致 **索引失效**。

原因：

数据库必须：

```
对每一行执行 DATE(create_time)
再比较
```

索引结构存的是：

```
create_time
```

不是：

```
DATE(create_time)
```

所以无法利用索引。

---

### 推荐写法

```sql
SELECT * FROM user
WHERE create_time >= '2024-01-01'
AND create_time < '2024-01-02'
```

这样：

* 可以利用 `create_time` 索引
* 只扫描索引范围

---

### 这条规则在哪些数据库适用

几乎全部：

* MySQL
* PostgreSQL
* Oracle Database
* Microsoft SQL Server

但有一些**例外优化机制**：

#### PostgreSQL

支持 **函数索引（Expression Index）**

```sql
CREATE INDEX idx ON user (date(create_time));
```

这样下面的 SQL 也能走索引：

```sql
WHERE DATE(create_time)='2024-01-01'
```

---

#### MySQL 8+

支持 **函数索引**

```sql
CREATE INDEX idx ON user ((DATE(create_time)));
```

不过仍然不建议乱用。

---

## 总结

| 优化建议         | 是否 MySQL 特性 | 是否通用      |
| ------------ | ----------- | --------- |
| SELECT 不用 *  | ❌           | ✅ 几乎所有数据库 |
| WHERE 不对列用函数 | ❌           | ✅ 几乎所有数据库 |

它们属于：

**关系型数据库 + B-Tree 索引的通用优化原则**

而不是 MySQL 独有。
