---
date: 2026-03-06
authors:
  - moita
categories:
  - 数据库
tags:
  - SQL
---

# SQL 8 道最经典手写题

我给你整理 **8 道最经典 SQL 手写题（带思路 + SQL）**，难度从简单到偏难，基本覆盖大厂面试常见题型。🚀

<!-- more -->

## 1️⃣ 找出每个部门工资最高的员工（经典 Top1）

### 表结构

```sql
Employee
id | name | salary | dept_id
```

### 要求

找出 **每个部门工资最高的员工**。

---

### 解法1：子查询（最经典）

```sql
SELECT *
FROM Employee e
WHERE salary = (
    SELECT MAX(salary)
    FROM Employee
    WHERE dept_id = e.dept_id
);
```

思路：

```text
每一行员工
→ 找该部门最高工资
→ 如果等于最高工资就返回
```

---

### 解法2：JOIN（性能更好）

```sql
SELECT e.*
FROM Employee e
JOIN (
    SELECT dept_id, MAX(salary) AS max_salary
    FROM Employee
    GROUP BY dept_id
) t
ON e.dept_id = t.dept_id
AND e.salary = t.max_salary;
```

---

## 2️⃣ 找每个部门工资 Top3 员工

### 方法：排名

```sql
SELECT *
FROM (
    SELECT *,
           DENSE_RANK() OVER (
               PARTITION BY dept_id
               ORDER BY salary DESC
           ) AS r
    FROM Employee
) t
WHERE r <= 3;
```

关键：

```text
PARTITION BY dept_id
```

意思：

```text
每个部门单独排名
```

---

## 3️⃣ 查找重复邮箱

经典题（LeetCode SQL）。

### 表

```sql
Person
id | email
```

### 要求

找出 **重复邮箱**。

---

### SQL

```sql
SELECT email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

核心：

```text
GROUP BY + HAVING
```

---

## 4️⃣ 找出没有订单的用户

### 表

```sql
Users
Orders
```

---

### SQL

```sql
SELECT u.*
FROM Users u
LEFT JOIN Orders o
ON u.id = o.user_id
WHERE o.id IS NULL;
```

思路：

```text
LEFT JOIN
订单为空
```

---

## 5️⃣ SQL 排行榜（Top N）

### 表

```sql
Score
id | score
```

要求：

```text
分数排名
相同分数相同排名
```

---

### SQL

```sql
SELECT score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS ranking
FROM Score;
```

排名函数：

| 函数         | 说明    |
| ---------- | ----- |
| ROW_NUMBER | 不允许并列 |
| RANK       | 跳排名   |
| DENSE_RANK | 不跳排名  |

---

## 6️⃣ 查询连续登录 7 天用户（难度较高）

### 表

```sql
Login
user_id | login_date
```

---

### 思路

核心技巧：

```text
日期 - 排名 = 连续组
```

---

### SQL

```sql
SELECT user_id
FROM (
    SELECT user_id,
           login_date,
           DATE_SUB(login_date,
           INTERVAL ROW_NUMBER() OVER (
               PARTITION BY user_id
               ORDER BY login_date
           ) DAY) AS grp
    FROM Login
) t
GROUP BY user_id, grp
HAVING COUNT(*) >= 7;
```

核心思想：

```text
连续日期
→ 分组
→ count >= 7
```

这是 **大厂 SQL 面试高频题**。

---

## 7️⃣ 查询第二高工资

经典题。

---

### 方法1

```sql
SELECT MAX(salary)
FROM Employee
WHERE salary < (
    SELECT MAX(salary)
    FROM Employee
);
```

---

### 方法2（推荐）

```sql
SELECT salary
FROM Employee
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

解释：

```text
OFFSET 1
跳过第一名
```

---

## 8️⃣ 统计每天新增用户

### 表

```sql
Users
id | register_date
```

---

### SQL

```sql
SELECT register_date,
       COUNT(*) AS new_users
FROM Users
GROUP BY register_date
ORDER BY register_date;
```

---

## ⭐ 面试 SQL 四大题型总结

SQL 手写题基本只有 4 类：

| 类型    | 技巧                |
| ----- | ----------------- |
| 分组统计  | GROUP BY          |
| 排名问题  | ROW_NUMBER / RANK |
| Top N | ORDER BY + LIMIT  |
| 连续问题  | 日期 - ROW_NUMBER   |

记住口诀：

```text
统计 → GROUP BY
排名 → 窗口函数
TopN → ORDER BY LIMIT
连续 → 日期差
```
