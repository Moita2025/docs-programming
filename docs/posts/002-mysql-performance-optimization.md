---
date: 2026-03-06
authors:
  - moita
categories:
  - 数据库
tags:
  - MySQL
  - 性能优化
---

# MySQL 性能优化

下面是 **8 条在 MySQL 中特别重要（但在其他数据库不一定成立或没那么重要）的 SQL 优化技巧**。
很多来自 MySQL 的 **存储引擎设计 + 优化器特点**，在面试或实际调优中非常常见。

<!-- more -->

---

## 1. 利用最左前缀原则（Leftmost Prefix Rule）

MySQL 的 **联合索引必须从最左列开始使用**。

例如：

```sql
CREATE INDEX idx_user ON user (name, age, city);
```

有效：

```sql
WHERE name = 'Tom'
WHERE name = 'Tom' AND age = 20
WHERE name = 'Tom' AND age = 20 AND city = 'NY'
```

仍然可用（部分索引）：

```sql
WHERE name = 'Tom' AND city = 'NY'
```

但下面 **完全不能用索引**：

```sql
WHERE age = 20
WHERE city = 'NY'
```

原因：
MySQL 的 **B+Tree 索引是按 `(name, age, city)` 排序**。

这一点在 PostgreSQL 和 Oracle Database 中虽然也有类似概念，但 **优化器更智能，限制没这么强**。

---

## 2. 避免 `OR` 导致索引失效

MySQL 遇到 `OR` 时经常会放弃索引。

例如：

```sql
SELECT * FROM user
WHERE name = 'Tom' OR age = 20;
```

可能变成：

```
全表扫描
```

优化方式：

```sql
SELECT * FROM user WHERE name='Tom'
UNION ALL
SELECT * FROM user WHERE age=20;
```

MySQL 对 `UNION` 的优化通常 **比 OR 好很多**。

---

## 3. 避免隐式类型转换

MySQL **会自动做类型转换**，但这可能导致索引失效。

例如：

```sql
phone VARCHAR(20)
```

SQL：

```sql
SELECT * FROM user WHERE phone = 13800138000;
```

MySQL 会执行：

```
CAST(phone AS INT)
```

于是：

```
索引失效
```

正确写法：

```sql
WHERE phone = '13800138000'
```

---

## 4. `LIMIT` 大分页性能问题

MySQL 在大 offset 时性能很差。

```sql
SELECT * FROM article
ORDER BY id
LIMIT 100000, 20;
```

执行流程：

```
扫描 100020 行
丢弃前 100000
返回 20
```

优化方式：

### 延迟关联

```sql
SELECT * FROM article
WHERE id > (
    SELECT id FROM article
    ORDER BY id
    LIMIT 100000,1
)
LIMIT 20;
```

或者使用：

```
seek pagination
```

---

## 5. `COUNT(*)` 比 `COUNT(column)` 快

在 MySQL 中：

```sql
COUNT(*)
```

是特殊优化路径。

而：

```sql
COUNT(column)
```

需要判断：

```
column 是否 NULL
```

所以：

```
COUNT(*) 通常最快
```

注意：

在 PostgreSQL 中：

```
COUNT(*) 仍然需要扫描
```

没有 MySQL 那种特殊优化。

---

## 6. InnoDB 主键影响所有二级索引

在 MySQL 默认存储引擎 **InnoDB** 中：

二级索引结构是：

```
index -> 主键值
```

例如：

```
index(name)
```

结构：

```
name -> id
```

查询流程：

```
二级索引 -> 主键 -> 回表
```

所以：

**主键越大，所有索引都会变大。**

推荐：

```
INT AUTO_INCREMENT
```

不推荐：

```
UUID
```

---

## 7. `LIKE` 前缀匹配才能用索引

```sql
WHERE name LIKE 'Tom%'
```

可以用索引。

但：

```sql
WHERE name LIKE '%Tom%'
```

索引失效。

原因：

B+Tree 只能做 **前缀匹配**。

解决方案：

* 倒排索引
* 全文索引
* 搜索系统

例如：

Elasticsearch。

---

## 8. `ORDER BY` + `LIMIT` 必须走同一个索引

例如：

```sql
SELECT * FROM user
WHERE age = 20
ORDER BY create_time
LIMIT 10;
```

如果索引：

```sql
(age, create_time)
```

MySQL 可以：

```
索引扫描 + 排序完成
```

否则：

```
filesort
```

`filesort` 在 MySQL 中是一个 **常见性能瓶颈**。

---

## 总结（MySQL 特别重要的 8 条）

| 优化点              | MySQL 特别原因      |
| ---------------- | --------------- |
| 最左前缀原则           | B+Tree 联合索引限制明显 |
| 避免 OR            | 优化器较弱           |
| 避免隐式转换           | 容易导致索引失效        |
| LIMIT 大分页        | offset 扫描       |
| COUNT(*)         | 特殊优化            |
| 主键设计             | InnoDB 聚簇索引     |
| LIKE 前缀          | B+Tree 限制       |
| ORDER BY + LIMIT | filesort 代价高    |
