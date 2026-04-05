---
date: 2026-03-07
authors:
  - moita
categories:
  - 数据库
tags:
  - SQL
  - LeetCode
---

# LeetCode 高频 SQL 50 题（基础版）

- 囊括数据库面试中的基本知识点
- 精选 50 道高频面试基础题目
- 应对普通面试中的数据库考核
- 适合需要在 1 个月以内准备面试的用户

<!-- more -->

## 查询

### 1757. 可回收且低脂的产品

```sql
--https://leetcode.com/problems/recyclable-and-low-fat-products/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Products;
CREATE TABLE IF NOT EXISTS Products ( 
	product_id INT, 
	low_fats ENUM ( 'Y', 'N' ), 
	recyclable ENUM ( 'Y', 'N' ) 
);
TRUNCATE TABLE Products;
INSERT INTO Products ( product_id, low_fats, recyclable )
VALUES
	( 0, 'Y', 'N' ),
	( 1, 'Y', 'Y' ),
	( 2, 'N', 'Y' ),
	( 3, 'Y', 'Y' ),
	( 4, 'N', 'N' );
  
SELECT product_id FROM Products 
WHERE low_fats = 'Y' AND recyclable = 'Y';
```

### 584. 寻找用户推荐人

MySQL 对于比较有三种结果`TRUE, FLASE, UNKNOWN`，其中`NULL`和任何值比较（包含`NULL`）结果均是`UNKNOWN`。在MySQL中判断一个值是不是`NULL`应该使用`IS NULL, IS NOT NULL`两种

```sql
--https://leetcode.com/problems/find-customer-referee/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Customer;
CREATE TABLE IF NOT EXISTS Customer ( 
	id INT, 
	name VARCHAR ( 25 ), 
	referee_id INT 
);
TRUNCATE TABLE Customer;
INSERT INTO Customer ( id, name, referee_id )
VALUES
	( 1, 'Will', NULL ),
	( 2, 'Jane', NULL ),
	( 3, 'Alex', 2 ),
	( 4, 'Bill', NULL ),
	( 5, 'Zack', 1 ),
	( 6, 'Mark', 2 );

SELECT name FROM Customer 
WHERE referee_id IS NULL OR referee_id != 2;
```

### 595. 大的国家

```sql
--https://leetcode.com/problems/big-countries/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS World;
CREATE TABLE IF NOT EXISTS World ( 
	name VARCHAR ( 255 ), 
	continent VARCHAR ( 255 ), 
	area INT, 
	population INT, 
	gdp BIGINT 
);
TRUNCATE TABLE World;
INSERT INTO World ( name, continent, area, population, gdp )
VALUES
	( 'Afghanistan', 'Asia', 652230, 25500100, 20343000000 ),
	( 'Albania', 'Europe', 28748, 2831741, 12960000000 ),
	( 'Algeria', 'Africa', 2381741, 37100000, 188681000000 ),
	( 'Andorra', 'Europe', 468, 78115, 3712000000 ),
	( 'Angola', 'Africa', 1246700, 20609294, 100990000000 );

SELECT name, population, area FROM World 
WHERE area >= 3000000 OR population >= 25000000;
```

### 1148. 文章浏览 I

```sql
--https://leetcode.com/problems/article-views-i/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Views;
CREATE TABLE IF NOT EXISTS Views ( 
	article_id INT, 
	author_id INT, 
	viewer_id INT, 
	view_date DATE 
);
TRUNCATE TABLE Views;
INSERT INTO Views ( article_id, author_id, viewer_id, view_date )
VALUES
	( 1, 3, 5, '2019-08-01' ),
	( 1, 3, 6, '2019-08-02' ),
	( 2, 7, 7, '2019-08-01' ),
	( 2, 7, 6, '2019-08-02' ),
	( 4, 7, 1, '2019-07-22' ),
	( 3, 4, 4, '2019-07-21' ),
	( 3, 4, 4, '2019-07-21' );

SELECT DISTINCT author_id AS id 
FROM Views 
WHERE author_id = viewer_id 
ORDER BY author_id;
```

### 1683. 无效的推文

这里的`LENGTH`是返回的是字节的长度，但是会有一些字符长度不是一个字节的，比如`￥`。如果遇到了这种情况可以使用`CHAR_LENGTH`，这个函数是返回的字符的个数。

```sql
--https://leetcode.com/problems/invalid-tweets/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Tweets;
CREATE TABLE IF NOT EXISTS Tweets ( 
	tweet_id INT, 
	content VARCHAR ( 50 ) 
);
TRUNCATE TABLE Tweets;
INSERT INTO Tweets ( tweet_id, content )
VALUES
	( 1, 'Vote for Biden' ),
	( 2, 'Let us make America great again!' );

SELECT tweet_id FROM Tweets 
WHERE CHAR_LENGTH(content) > 15;
```

## 连接

### 1378. 使用唯一标识码替换员工ID

题目要求了输出所有的名字，没有唯一标识的用`NULL`填充，因此用`Employees`作为左表，采用左连接。

```sql
--https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employees, EmployeeUNI;
CREATE TABLE IF NOT EXISTS Employees ( 
	id int, 
	name varchar ( 20 ) 
);
CREATE TABLE IF NOT EXISTS EmployeeUNI ( 
	id int, 
	unique_id int, 
	UNIQUE ( id ) 
);
TRUNCATE TABLE Employees;
TRUNCATE TABLE EmployeeUNI;
INSERT INTO Employees ( id, name )
VALUES
	( '1', 'Alice' ),
	( '7', 'Bob' ),
	( '11', 'Meir' ),
	( '90', 'Winston' ),
	( '3', 'Jonathan' );
INSERT INTO EmployeeUNI ( id, unique_id )
VALUES
	( '3', '1' ),
	( '11', '2' ),
	( '90', '3' );

SELECT EmployeeUNI.unique_id, Employees.name 
FROM Employees 
LEFT JOIN EmployeeUNI 
ON Employees.id = EmployeeUNI.id;
```

### 1068. 产品销售分析 I

```sql
--https://leetcode.com/problems/product-sales-analysis-i/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Sales, Product;
CREATE TABLE IF NOT EXISTS Sales ( 
	sale_id INT, 
	product_id INT, 
	year INT, 
	quantity INT, 
	price INT 
);
CREATE TABLE IF NOT EXISTS Product ( 
	product_id INT, 
	product_name VARCHAR ( 10 ) 
);
TRUNCATE TABLE Sales;
TRUNCATE TABLE Product;
INSERT INTO Sales ( sale_id, product_id, year, quantity, price )
VALUES
	( '1', 100, 2008, 10, 5000 ),
	( '2', 100, 2009, 12, 5000 ),
	( '7', 200, 2011, 15, 9000 );
INSERT INTO Product ( product_id, product_name )
VALUES
	( 100, 'Nokia' ),
	( 200, 'Apple' ),
	( 300, 'Samsung' );

SELECT Product.product_name, Sales.year, Sales.price 
FROM Sales 
LEFT JOIN Product 
ON Sales.product_id = Product.product_id;
```

### 1581. 进店却未进行过交易的顾客

```sql
--https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Visits, Transactions;
CREATE TABLE IF NOT EXISTS Visits ( 
	visit_id INT, 
	customer_id INT 
);
CREATE TABLE IF NOT EXISTS Transactions ( 
	transaction_id INT, 
	visit_id INT, 
	amount INT 
);
TRUNCATE TABLE Visits;
INSERT INTO Visits ( visit_id, customer_id )
VALUES
	( 1, 23 ),
	( 2, 9 ),
	( 4, 30 ),
	( 5, 54 ),
	( 6, 96 ),
	( 7, 54 ),
	( 8, 54 );
TRUNCATE TABLE Transactions;
INSERT INTO Transactions ( transaction_id, visit_id, amount )
VALUES
	( 2, 5, 310 ),
	( 3, 5, 300 ),
	( 9, 5, 200 ),
	( 12, 1, 910 ),
	( 13, 2, 970 );

SELECT Visits.*, Transactions.* 
FROM Visits 
LEFT JOIN Transactions 
ON Transactions.visit_id = Visits.visit_id;
```

### 197. 上升的温度

这个题有一个特点就是表要和自己链接，其实我们可以当作是两个表，一个是今天`w1`，一个是昨天`w2`。

```sql
--https://leetcode.com/problems/rising-temperature/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Weather;
CREATE TABLE IF NOT EXISTS Weather ( 
	id INT, 
	recordDate DATE, 
	temperature INT 
);
TRUNCATE TABLE Weather;
INSERT INTO Weather ( id, recordDate, temperature )
VALUES
	( 1, '2015-01-01', 10 ),
	( 2, '2015-01-02', 25 ),
	( 3, '2015-01-03', 20 ),
	( 4, '2015-01-04', 30 );

SELECT w1.id 
FROM Weather AS w1 
LEFT JOIN
	--多解性
	Weather AS w2 ON ADDDATE(w2.recordDate, INTERVAL 1 DAY) = w1.recordDate
	Weather AS w2 ON w2.recordDate = SUBDATE(w1.recordDate, INTERVAL 1 DAY)
	Weather AS w2 ON DATEDIFF(w1.recordDate, w2.recordDate) = 1 
	Weather AS w2 ON TIMESTAMPDIFF(DAY, w2.recordDate, w1.recordDate) = 1
	--多解性
WHERE 
	w2.id IS NOT NULL AND 
	w1.temperature > w2.temperature;
```

要注意，`DATEDIFF`和`TIMESTAMPDIFF`的返回结果都不是绝对值。

### 1661. 每台机器的进程平均运行时间

```sql
--https://leetcode.com/problems/average-time-of-process-per-machine/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Activity;
CREATE TABLE IF NOT EXISTS Activity ( 
	machine_id int, 
	process_id int, 
	activity_type ENUM ( 'start', 'end' ), 
	timestamp float 
);
TRUNCATE TABLE Activity;
INSERT INTO Activity ( machine_id, process_id, activity_type, timestamp )
VALUES
	( '0', '0', 'start', 0.712 ),
	( '0', '0', 'end', 1.52 ),
	( '0', '1', 'start', 3.14 ),
	( '0', '1', 'end', 4.12 ),
	( '1', '0', 'start', 0.55 ),
	( '1', '0', 'end', 1.55 ),
	( '1', '1', 'start', 0.43 ),
	( '1', '1', 'end', 1.42 ),
	( '2', '0', 'start', 4.1 ),
	( '2', '0', 'end', 4.512 ),
	( '2', '1', 'start', 2.5 ),
	( '2', '1', 'end', 5 );

SELECT 
	a1.machine_id, 
	ROUND(AVG(a2.timestamp - a1.timestamp), 3) AS processing_time 
FROM Activity AS a1 
INNER JOIN Activity AS a2 
ON 
	a1.machine_id = a2.machine_id AND 
	a1.process_id = a2.process_id AND 
	a1.activity_type = 'start' AND 
	a2.activity_type = 'end' 
GROUP BY a1.machine_id;
```

### 577. 员工奖金

```sql
--https://leetcode.com/problems/employee-bonus/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employee, Bonus;
CREATE TABLE IF NOT EXISTS Employee ( 
	empId INT, 
	name VARCHAR ( 255 ), 
	supervisor INT, 
	salary INT 
);
CREATE TABLE IF NOT EXISTS Bonus ( 
	empId INT, 
	bonus INT 
);
TRUNCATE TABLE Employee;
INSERT INTO Employee ( empId, name, supervisor, salary )
VALUES
	( 3, 'Brad', NULL, 4000 ),
	( 1, 'John', 3, 1000 ),
	( 2, 'Dan', 3, 2000 ),
	( 4, 'Thomas', 3, 4000 );
TRUNCATE TABLE Bonus;
INSERT INTO Bonus ( empId, bonus )
VALUES
	( 2, 500 ),
	( 4, 2000 );

SELECT e.name, b.bonus 
FROM Employee AS e 
LEFT JOIN Bonus AS b 
ON e.empId = B.empId 
WHERE b.bonus IS NULL OR b.bonus < 1000;
```

### 1280. 学生们参加各科测试的次数

```sql
--https://leetcode.com/problems/students-and-examinations/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Students, Subjects;
CREATE TABLE IF NOT EXISTS Students ( 
	student_id INT, 
	student_name VARCHAR ( 20 ) 
);
CREATE TABLE IF NOT EXISTS Subjects ( 
	subject_name VARCHAR ( 20 ) 
);
CREATE TABLE IF NOT EXISTS Examinations ( 
	student_id INT, 
	subject_name VARCHAR ( 20 ) 
);
TRUNCATE TABLE Students;
INSERT INTO Students ( student_id, student_name )
VALUES
	( 1, 'Alice' ),
	( 2, 'Bob' ),
	( 13, 'John' ),
	( 6, 'Alex' );
TRUNCATE TABLE Subjects;
INSERT INTO Subjects ( subject_name )
VALUES
	( 'Math' ),
	( 'Physics' ),
	( 'Programming' );
TRUNCATE TABLE Examinations;
INSERT INTO Examinations ( student_id, subject_name )
VALUES
	( 1, 'Math' ),
	( 1, 'Physics' ),
	( 1, 'Programming' ),
	( 2, 'Programming' ),
	( 1, 'Physics' ),
	( 1, 'Math' ),
	( 13, 'Math' ),
	( 13, 'Programming' ),
	( 13, 'Physics' ),
	( 2, 'Math' ),
	( 1, 'Math' );

SELECT 
	Students.student_id, 
	Students.student_name, 
	Subjects.subject_name, 
	IFNULL(Counted.attended_exams, 0) AS attended_exams 
FROM Students 
CROSS JOIN Subjects 
LEFT JOIN( 
	SELECT 
		student_id, 
		subject_name, 
		COUNT(*) AS attended_exams 
	FROM Examinations 
	GROUP BY student_id, subject_name 
) AS Counted 
ON 
	Students.student_id = Counted.student_id AND 
	Subjects.subject_name = Counted.subject_name 
ORDER BY Students.student_id, Subjects.subject_name;
```

### 570. 至少有5名直接下属的经理

```sql
--https://leetcode.com/problems/managers-with-at-least-5-direct-reports/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employee;
CREATE TABLE Employee ( 
	id INT, 
	name VARCHAR ( 255 ), 
	department VARCHAR ( 255 ), 
	managerId INT 
);
TRUNCATE TABLE Employee;
INSERT INTO Employee ( id, name, department, managerId )
VALUES
	( 101, 'John', 'A', NULL ),
	( 102, 'Dan', 'A', 101 ),
	( 103, 'James', 'A', 101 ),
	( 104, 'Amy', 'A', 101 ),
	( 105, 'Anne', 'A', 101 ),
	( 106, 'Ron', 'B', 101 );

SELECT e1.name FROM Employee AS e1 
INNER JOIN Employee AS e2 
ON e2.managerId = e1.id 
GROUP BY e2.managerId
HAVING COUNT(*) >= 5;
```

### 1934. 确认率

```sql
--https://leetcode.com/problems/confirmation-rate/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Signups, Confirmations;
CREATE TABLE Signups ( 
	user_id INT, 
	time_stamp DATETIME 
);
CREATE TABLE Confirmations ( 
	user_id INT, 
	time_stamp DATETIME, 
	action ENUM ( 'confirmed', 'timeout' ) 
);
TRUNCATE TABLE Signups;
INSERT INTO Signups ( user_id, time_stamp )
VALUES
	( 3, '2020-03-21 10:16:13' ),
	( 7, '2020-01-04 13:57:59' ),
	( 2, '2020-07-29 23:09:44' ),
	( 6, '2020-12-09 10:39:37' );
TRUNCATE TABLE Confirmations;
INSERT INTO Confirmations ( user_id, time_stamp, action )
VALUES
	( 3, '2021-01-06 03:30:46', 'timeout' ),
	( 3, '2021-07-14 14:00:00', 'timeout' ),
	( 7, '2021-06-12 11:57:29', 'confirmed' ),
	( 7, '2021-06-13 12:58:28', 'confirmed' ),
	( 7, '2021-06-14 13:59:27', 'confirmed' ),
	( 2, '2021-01-22 00:00:00', 'confirmed' ),
	( 2, '2021-02-28 23:59:59', 'timeout' );

SELECT 
	Signups.user_id, 
	ROUND(AVG(IF( c.action = "confirmed", 1, 0 )) / COUNT(*), 2) AS confirmation_rate 
FROM Signups 
LEFT JOIN Confirmations 
ON Confirmations.user_id = Signups.user_id 
GROUP BY Signups.user_id;
```

## 聚合函数

### 620. 有趣的电影

```sql
--https://leetcode.com/problems/not-boring-movies/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS cinema;
CREATE TABLE cinema ( 
	id INT, 
	movie VARCHAR ( 255 ), 
	description VARCHAR ( 255 ), 
	rating FLOAT ( 2, 1 ) 
);
TRUNCATE TABLE cinema;
INSERT INTO cinema ( id, movie, description, rating )
VALUES
	( 1, 'War', 'great 3D', 8.9 ),
	( 2, 'Science', 'fiction', 8.5 ),
	( 3, 'irish', 'boring', 6.2 ),
	( 4, 'Ice song', 'Fantacy', 8.6 ),
	( 5, 'House card', 'Interesting', 9.1 );

SELECT * FROM cinema 
WHERE 
	MOD(id, 2) = 1 AND 
	description != 'boring' 
ORDER BY rating DESC;
```

### 1251. 平均售价

```sql
--https://leetcode.com/problems/average-selling-price/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Prices;
CREATE TABLE Prices ( 
	product_id INT, 
	start_date DATE, 
	end_date DATE, 
	price INT 
);
DROP TABLE IF EXISTS UnitsSold;
CREATE TABLE UnitsSold ( 
	product_id INT, 
	purchase_date DATE, 
	units INT 
);
INSERT INTO Prices ( product_id, start_date, end_date, price )
VALUES
	( 1, '2019-02-17', '2019-02-28', 5 ),
	( 1, '2019-03-01', '2019-03-22', 20 ),
	( 2, '2019-02-01', '2019-02-20', 15 ),
	( 2, '2019-02-21', '2019-03-31', 30 );
INSERT INTO UnitsSold ( product_id, purchase_date, units )
VALUES
	( 1, '2019-02-25', 100 ),
	( 1, '2019-03-01', 15 ),
	( 2, '2019-02-10', 200 ),
	( 2, '2019-03-22', 30 );

SELECT 
	Prices.product_id, 
	ROUND(IFNULL(SUM(Prices.price * UnitsSold.units) / SUM(UnitsSold.units), 0), 2) AS average_price 
FROM Prices 
LEFT JOIN UnitsSold 
ON 
	UnitsSold.product_id = Prices.product_id AND 
	(UnitsSold.purchase_date BETWEEN Prices.start_date AND Prices.end_date) 
GROUP BY Prices.product_id;
```

### 1075. 项目员工 I

```sql
--https://leetcode.com/problems/project-employees-i/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Employee;
CREATE TABLE IF NOT EXISTS Project ( 
	project_id INT, 
	employee_id INT 
);
CREATE TABLE IF NOT EXISTS Employee ( 
	employee_id INT, 
	name VARCHAR ( 10 ), 
	experience_years INT 
);
TRUNCATE TABLE Project;
INSERT INTO Project ( project_id, employee_id )
VALUES
	( 1, 1 ),
	( 1, 2 ),
	( 1, 3 ),
	( 2, 1 ),
	( 2, 4 );
TRUNCATE TABLE Employee;
INSERT INTO Employee ( employee_id, name, experience_years )
VALUES
	( 1, 'Khaled', 3 ),
	( 2, 'Ali', 2 ),
	( 3, 'John', 1 ),
	( 4, 'Doe', 2 );

SELECT 
	Project.project_id, 
	ROUND(AVG(Employee.experience_years), 2) AS average_years 
FROM Project 
INNER JOIN Employee 
ON Employee.employee_id = Project.employee_id 
GROUP BY Project.project_id;
```

### 1633. 各赛事的用户注册率

```sql
--https://leetcode.com/problems/percentage-of-users-attended-a-contest/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
	user_id INT,
	user_name VARCHAR ( 20 )
);
INSERT INTO Users ( user_id, user_name )
VALUES
	( 6, 'Alice' ),
	( 2, 'Bob' ),
	( 7, 'Alex' );
DROP TABLE IF EXISTS Register;
CREATE TABLE Register ( 
	contest_id INT, 
	user_id INT 
);
INSERT INTO Register ( contest_id, user_id )
VALUES
	( 215, 6 ),
	( 209, 2 ),
	( 208, 2 ),
	( 210, 6 ),
	( 208, 6 ),
	( 209, 7 ),
	( 209, 6 ),
	( 215, 7 ),
	( 208, 7 ),
	( 210, 2 ),
	( 207, 2 ),
	( 210, 7 );

SELECT 
	contest_id, 
	ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM Users), 2) AS percentage 
FROM Register 
GROUP BY contest_id 
ORDER BY percentage DESC, contest_id;
```

### 1211. 查询结果的质量和占比

```sql
--https://leetcode.com/problems/queries-quality-and-percentage/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Queries;
CREATE TABLE Queries ( 
	query_name VARCHAR ( 30 ), 
	result VARCHAR ( 50 ), 
	position INT, 
	rating INT 
);
INSERT INTO Queries ( query_name, result, position, rating )
VALUES
	( 'Dog', 'Golden Retriever', 1, 5 ),
	( 'Dog', 'German Shepherd', 2, 5 ),
	( 'Dog', 'Mule', 200, 1 ),
	( 'Cat', 'Shirazi', 5, 2 ),
	( 'Cat', 'Siamese', 3, 3 ),
	( 'Cat', 'Sphynx', 7, 4 );

SELECT 
	query_name, 
	ROUND(AVG(rating / position),2) AS quality, 
	ROUND(AVG(IF(rating < 3, 1, 0)) * 100, 2) AS poor_query_percentage 
FROM Queries 
GROUP BY query_name;
```

### 1193. 每月交易 I

```sql
--https://leetcode.com/problems/monthly-transactions-i/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Transactions;
CREATE TABLE Transactions ( 
	id INT, country VARCHAR ( 4 ), 
	state ENUM ( 'approved', 'declined' ), 
	amount INT, 
	trans_date DATE 
);
INSERT INTO Transactions ( id, country, state, amount, trans_date )
VALUES
	( 121, 'US', 'approved', 1000, '2018-12-18' ),
	( 122, 'US', 'declined', 2000, '2018-12-19' ),
	( 123, 'US', 'approved', 2000, '2019-01-01' ),
	( 124, 'DE', 'approved', 2000, '2019-01-07' );

SELECT 
	--多解性
	LEFT(trans_date, 7) AS month, 
	DATE_FORMAT(trans_date, "%Y-%m") AS month,
	--多解性
	country, 
	COUNT(*) AS trans_count, 
	SUM(IF(state = "approved", 1, 0)) AS approved_count, 
	SUM(amount) AS trans_total_amount, 
	SUM(IF(state = "approved", 1, 0) * amount) AS approved_total_amount 
FROM Transactions 
GROUP BY month, country;
```

### 1174. 即时食物配送 II

```sql
--https://leetcode.com/problems/immediate-food-delivery-ii/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Delivery;
CREATE TABLE Delivery ( 
	delivery_id INT, 
	customer_id INT, 
	order_date DATE, 
	customer_pref_delivery_date DATE 
);
TRUNCATE TABLE Delivery;
INSERT INTO Delivery ( delivery_id, customer_id, order_date, customer_pref_delivery_date )
VALUES
	( 1, 1, '2019-08-01', '2019-08-02' ),
	( 2, 2, '2019-08-02', '2019-08-02' ),
	( 3, 1, '2019-08-11', '2019-08-12' ),
	( 4, 3, '2019-08-24', '2019-08-24' ),
	( 5, 3, '2019-08-21', '2019-08-22' ),
	( 6, 2, '2019-08-11', '2019-08-13' ),
	( 7, 4, '2019-08-09', '2019-08-09' );

SELECT 
	ROUND(AVG(order_date = customer_pref_delivery_date) * 100, 2) AS immediate_percentage 
FROM Delivery 
WHERE 
	(customer_id, order_date) IN ( 
		SELECT customer_id, MIN(order_date) 
		FROM Delivery 
		GROUP BY customer_id 
	);
```

### 550. 游戏玩法分析 IV

```sql
--https://leetcode.com/problems/game-play-analysis-iv/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Activity;
CREATE TABLE Activity ( 
	player_id INT, 
	device_id INT, 
	event_date DATE, 
	games_played INT 
);
INSERT INTO Activity ( player_id, device_id, event_date, games_played )
VALUES
	( 1, 2, '2016-03-01', 5 ),
	( 1, 2, '2016-03-02', 6 ),
	( 2, 3, '2017-06-25', 1 ),
	( 3, 1, '2016-03-02', 0 ),
	( 3, 4, '2018-07-03', 5 );

SELECT 
	ROUND( SUM(IF(Expected.second_date IS NOT NULL, 1, 0)) / 
	COUNT(DISTINCT Activity.player_id) , 2 ) AS fraction 
FROM Activity 
LEFT JOIN ( 
	SELECT 
		player_id, 
		DATE_ADD(MIN(event_date), INTERVAL 1 DAY) AS second_date 
	FROM Activity 
	GROUP BY player_id 
) AS Expected 
ON 
	Activity.player_id = Expected.player_id AND 
	Activity.event_date = Expected.second_date;
```

## 排序和分组

### 2356. 每位教师所教授的科目种类的数量

```sql
--https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Teacher;
CREATE TABLE Teacher ( 
	teacher_id INT, 
	subject_id INT, 
	dept_id INT 
);
INSERT INTO Teacher ( teacher_id, subject_id, dept_id )
VALUES
	( 1, 2, 3 ),
	( 1, 2, 4 ),
	( 1, 3, 3 ),
	( 2, 1, 1 ),
	( 2, 2, 1 ),
	( 2, 3, 1 ),
	( 2, 4, 1 );

SELECT 
	teacher_id, 
	COUNT(DISTINCT subject_id) AS cnt 
FROM Teacher 
GROUP BY teacher_id;
```

### 1141. 查询近30天活跃用户数

```sql
--https://leetcode.com/problems/user-activity-for-the-past-30-days-i/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Activity;
CREATE TABLE Activity ( 
	user_id INT, 
	session_id INT, 
	activity_date DATE, 
	activity_type ENUM ( 'open_session', 'end_session', 'scroll_down', 'send_message' ) 
);
TRUNCATE TABLE Activity;
INSERT INTO Activity ( user_id, session_id, activity_date, activity_type )
VALUES
	( 1, 1, '2019-07-20', 'open_session' ),
	( 1, 1, '2019-07-20', 'scroll_down' ),
	( 1, 1, '2019-07-20', 'end_session' ),
	( 2, 4, '2019-07-20', 'open_session' ),
	( 2, 4, '2019-07-21', 'send_message' ),
	( 2, 4, '2019-07-21', 'end_session' ),
	( 3, 2, '2019-07-21', 'open_session' ),
	( 3, 2, '2019-07-21', 'send_message' ),
	( 3, 2, '2019-07-21', 'end_session' ),
	( 4, 3, '2019-06-25', 'open_session' ),
	( 4, 3, '2019-06-25', 'end_session' );

SELECT 
	activity_date AS day, 
	COUNT(DISTINCT user_id) AS active_users 
FROM Activity 
GROUP BY activity_date 
HAVING DATEDIFF("2019-07-27", activity_date) BETWEEN 0 AND 29;
```

### 1084. 销售分析 III

```sql
--https://leetcode.com/problems/product-sales-analysis-iii/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Sales;
CREATE TABLE IF NOT EXISTS Sales ( 
	sale_id INT, 
	product_id INT, 
	year INT, 
	quantity INT, 
	price INT 
);
INSERT INTO Sales ( sale_id, product_id, year, quantity, price )
VALUES
	( 1, 100, 2008, 10, 5000 ),
	( 2, 100, 2009, 12, 5000 ),
	( 7, 200, 2011, 15, 9000 );
DROP TABLE IF EXISTS Product;
CREATE TABLE IF NOT EXISTS Product ( 
	product_id INT, 
	product_name VARCHAR ( 10 ) 
);
INSERT INTO Product ( product_id, product_name )
VALUES
	( 100, 'Nokia' ),
	( 200, 'Apple' ),
	( 300, 'Samsung' );

SELECT
	s.product_id,
	s.year AS first_year,
	s.quantity,
	s.price 
FROM Sales AS s 
WHERE
	( s.product_id, year ) in (
		SELECT 
			t.product_id,
			min( t.year ) 
		FROM Sales AS t 
		GROUP BY t.product_id 
	);
```

### 596. 超过 5 名学生的课

```sql
--https://leetcode.com/problems/classes-more-than-5-students/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Courses;
CREATE TABLE Courses ( 
	student VARCHAR ( 255 ), 
	class VARCHAR ( 255 ) 
);
TRUNCATE TABLE Courses;
INSERT INTO Courses ( student, class )
VALUES
	( 'A', 'Math' ),
	( 'B', 'English' ),
	( 'C', 'Math' ),
	( 'D', 'Biology' ),
	( 'E', 'Math' ),
	( 'F', 'Computer' ),
	( 'G', 'Math' ),
	( 'H', 'Math' ),
	( 'I', 'Math' );

SELECT class 
FROM Courses 
GROUP BY class 
HAVING COUNT(*) >= 5;
```

### 1729. 求关注者的数量

```sql
--https://leetcode.com/problems/find-followers-count/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Followers;
CREATE TABLE Followers ( 
	user_id INT, 
	follower_id INT 
);
INSERT INTO Followers ( user_id, follower_id )
VALUES
	( 0, 1 ),
	( 1, 0 ),
	( 2, 0 ),
	( 2, 1 );

SELECT 
	user_id, 
	COUNT(*) AS followers_count 
FROM Followers 
GROUP BY user_id 
ORDER BY user_id;
```

### 619. 只出现一次的最大数字

```sql
--https://leetcode.com/problems/biggest-single-number/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS MyNumbers;
CREATE TABLE MyNumbers ( num INT );
INSERT INTO MyNumbers ( num )
VALUES
	( 8 ),
	( 8 ),
	( 3 ),
	( 3 ),
	( 1 ),
	( 4 ),
	( 5 ),
	( 6 );

SELECT MAX(num) AS num 
FROM( 
	SELECT num 
	FROM MyNumbers 
	GROUP BY num 
	HAVING COUNT(*) = 1 
) AS OnlyoneNum;
```

### 1045. 买下所有产品的客户

```sql
--https://leetcode.com/problems/customers-who-bought-all-products/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Product;
CREATE TABLE Customer ( 
	customer_id INT, 
	product_key INT 
);
CREATE TABLE Product ( product_key INT );
INSERT INTO Customer ( customer_id, product_key )
VALUES
	( 1, 5 ),
	( 2, 6 ),
	( 3, 5 ),
	( 3, 6 ),
	( 1, 6 );
INSERT INTO Product ( product_key )
VALUES
	( 5 ),
	( 6 );

SELECT customer_id 
FROM Customer 
GROUP BY customer_id 
HAVING 
	COUNT(DISTINCT product_key) = ( SELECT COUNT(*) FROM Product );
```

## 高级查询和连接

### 1731. 每位经理的下属员工数量

```sql
--https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employees;
CREATE TABLE Employees ( 
	employee_id INT, 
	name VARCHAR ( 20 ), 
	reports_to VARCHAR ( 20 ), 
	age INT 
);
INSERT INTO Employees ( employee_id, name, reports_to, age )
VALUES
	( 9, 'Hercy', 'None', 43 ),
	( 6, 'Alice', '9', 41 ),
	( 4, 'Bob', '9', 36 ),
	( 2, 'Winston', 'None', 37 );

SELECT 
	e1.employee_id, 
	e1.name, 
	COUNT(*) AS reports_count, 
	ROUND(AVG(e2.age)) AS average_age 
FROM Employees e1 
INNER JOIN Employees e2 
ON e2.reports_to = e1.employee_id 
GROUP BY e1.employee_id 
ORDER BY e1.employee_id;
```

### 1789. 员工的直属部门

```sql
--https://leetcode.com/problems/primary-department-for-each-employee/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employee;
CREATE TABLE IF NOT EXISTS Employee ( 
	employee_id INT, 
	department_id INT, 
	primary_flag ENUM ( 'Y', 'N' ) 
);
TRUNCATE TABLE Employee;
INSERT INTO Employee ( employee_id, department_id, primary_flag )
VALUES
	( 1, 1, 'N' ),
	( 2, 1, 'Y' ),
	( 2, 2, 'N' ),
	( 3, 3, 'N' ),
	( 4, 2, 'N' ),
	( 4, 3, 'Y' ),
	( 4, 4, 'N' );

SELECT 
	employee_id, 
	department_id 
FROM( 
	SELECT 
		employee_id, 
		department_id, 
		primary_flag, 
		COUNT(*) OVER(PARTITION BY employee_id) AS count_dep 
	FROM Employee 
) AS Counted 
WHERE primary_flag = 'Y' OR count_dep = 1;
```

### 610. 判断三角形

```sql
--https://leetcode.com/problems/triangle-judgement/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Triangle;
CREATE TABLE IF NOT EXISTS Triangle ( 
	x INT, 
	y INT, 
	z INT 
);
TRUNCATE TABLE Triangle;
INSERT INTO Triangle ( x, y, z )
VALUES
	( '13', '15', '30' ),
	( '10', '20', '15' );

SELECT 
	*, 
	IF(
		x + y > z AND 
		x + z > y AND 
		y + z > x, 
		"Yes", "No"
	) AS triangle 
FROM Triangle;
```

### 180. 连续出现的数字

```sql
--https://leetcode.com/problems/consecutive-numbers/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Logs;
CREATE TABLE IF NOT EXISTS Logs ( 
	id INT, 
	num INT 
);
TRUNCATE TABLE Logs;
INSERT INTO Logs ( id, num )
VALUES
	( '1', '1' ),
	( '2', '1' ),
	( '3', '1' ),
	( '4', '2' ),
	( '5', '1' ),
	( '6', '2' ),
	( '7', '2' );

SELECT DISTINCT l1.num AS ConsecutiveNums 
FROM Logs l1, Logs l2, Logs l3 
WHERE 
	l2.id = l1.id + 1 AND 
	l3.id = l2.id + 1 AND 
	l1.num = l2.num AND 
	l2.num = l3.num;
```

### 1164. 指定日期的产品价格

```sql
--https://leetcode.com/problems/product-price-at-a-given-date/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Products;
CREATE TABLE IF NOT EXISTS Products ( 
	product_id INT, 
	new_price INT, 
	change_date DATE 
);
INSERT INTO Products ( product_id, new_price, change_date )
VALUES
	( 1, 20, '2019-08-14' ),
	( 2, 50, '2019-08-14' ),
	( 1, 30, '2019-08-15' ),
	( 1, 35, '2019-08-16' ),
	( 2, 65, '2019-08-17' ),
	( 3, 20, '2019-08-18' );

SELECT 
	p1.product_id, 
	IFNULL(p2.new_price, 10) AS price 
FROM ( 
	SELECT DISTINCT product_id FROM Products 
) AS p1 
LEFT JOIN ( 
	SELECT product_id, new_price 
	FROM Products 
	WHERE 
		(product_id,change_date) IN ( 
			SELECT product_id, MAX(change_date) 
			FROM Products 
			WHERE change_date <= "2019-08-16" 
			GROUP BY product_id 
		) 
) AS p2 
ON p1.product_id = p2.product_id;
```

### 1204. 最后一个能进入巴士的人

```sql
--https://leetcode.com/problems/last-person-to-fit-in-the-bus/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Queue;
CREATE TABLE Queue ( 
	person_id INT, 
	person_name VARCHAR ( 30 ), 
	weight INT, 
	turn INT 
);
INSERT INTO Queue ( person_id, person_name, weight, turn )
VALUES
	( '5', 'Alice', '250', '1' ),
	( '4', 'Bob', '175', '5' ),
	( '3', 'Alex', '350', '2' ),
	( '6', 'John Cena', '400', '3' ),
	( '1', 'Winston', '500', '6' ),
	( '2', 'Marie', '200', '4' );

SELECT person_name 
FROM ( 
	SELECT 
		person_name, 
		turn, 
		SUM( weight ) OVER ( ORDER BY turn ) AS sum_weight 
	FROM queue 
) p1 
WHERE sum_weight <= 1000 
ORDER BY turn desc 
LIMIT 1;
```

### 1907. 按分类统计薪水

```sql
--https://leetcode.com/problems/count-salary-categories/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Accounts;
CREATE TABLE Accounts ( 
	account_id INT, 
	income INT 
);
TRUNCATE TABLE Accounts;
INSERT INTO Accounts ( account_id, income )
VALUES
	( '3', '108939' ),
	( '2', '12747' ),
	( '8', '87709' ),
	( '6', '91796' );

SELECT
	'Low Salary' AS category,
	( 
		SELECT COUNT(*) 
		FROM Accounts 
		WHERE income < 20000 
	) AS accounts_count 
UNION
SELECT
	'Average Salary' AS category,
	( 
		SELECT COUNT(*) 
		FROM Accounts 
		WHERE income >= 20000 and income <= 50000 
	) AS accounts_count 
UNION
SELECT
	'High Salary' AS category,
	( 
		SELECT COUNT(*) 
		FROM Accounts 
		WHERE income > 50000 
	) AS accounts_count;
```

## 子查询

### 1978. 上级经理已离职的公司员工

```sql
--https://leetcode.com/problems/employees-whose-manager-left-the-company/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employees;
CREATE TABLE Employees ( 
	employee_id INT, 
	name VARCHAR ( 20 ), 
	manager_id INT, 
	salary INT 
);
TRUNCATE TABLE Employees;
INSERT INTO Employees ( employee_id, name, manager_id, salary )
VALUES
	( '3', 'Mila', '9', '60301' ),
	( '12', 'Antonella', NULL, '31000' ),
	( '13', 'Emery', NULL, '67084' ),
	( '1', 'Kalel', '11', '21241' ),
	( '9', 'Mikaela', NULL, '50937' ),
	( '11', 'Joziah', '6', '28485' );

SELECT t.employee_id 
FROM Employees AS t 
WHERE
	t.salary < 30000 and 
	t.manager_id NOT IN ( 
		SELECT employee_id FROM Employees 
	) 
ORDER BY t.employee_id ASC;
```

### 626. 换座位

```sql
--https://leetcode.com/problems/exchange-seats/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Seat;
CREATE TABLE Seat (
	id INT,
	student VARCHAR ( 255 )
);
TRUNCATE TABLE Seat;
INSERT INTO Seat ( id, student )
VALUES
	( 1, 'Abbot' ),
	( 2, 'Doris' ),
	( 3, 'Emerson' ),
	( 4, 'Green' ),
	( 5, 'Jeames' );

SELECT
	a.id,
	IFNULL( b.student, a.student ) AS student 
FROM Seat a
LEFT JOIN (
	SELECT
		t.id,
		t.student,
		if
		(
			SUM( 1 ) OVER ( ORDER BY t.id ) % 2 = 1,
			t.id + 1,
			t.id - 1 
		) AS new_id 
	FROM Seat AS t 
) AS b 
ON a.id = b.new_id 
ORDER BY a.id ASC;
```

### 1341. 电影评分

```sql
--https://leetcode.com/problems/movie-rating/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS MovieRating;
CREATE TABLE IF NOT EXISTS Movies ( 
	movie_id INT, 
	title VARCHAR ( 30 ) 
);
CREATE TABLE IF NOT EXISTS Users ( 
	user_id INT, 
	name VARCHAR ( 30 ) 
);
CREATE TABLE IF NOT EXISTS MovieRating ( 
	movie_id INT, 
	user_id INT, 
	rating INT, 
	created_at DATE 
);
TRUNCATE TABLE Movies;
INSERT INTO Movies ( movie_id, title )
VALUES
	( 1, 'Avengers' ),
	( 2, 'Frozen 2' ),
	( 3, 'Joker' );
TRUNCATE TABLE Users;
INSERT INTO Users ( user_id, name )
VALUES
	( 1, 'Daniel' ),
	( 2, 'Monica' ),
	( 3, 'Maria' ),
	( 4, 'James' );
TRUNCATE TABLE MovieRating;
INSERT INTO MovieRating ( movie_id, user_id, rating, created_at )
VALUES
	( 1, 1, 3, '2020-01-12' ),
	( 1, 2, 4, '2020-02-11' ),
	( 1, 3, 2, '2020-02-12' ),
	( 1, 4, 1, '2020-01-01' ),
	( 2, 1, 5, '2020-02-17' ),
	( 2, 2, 2, '2020-02-01' ),
	( 2, 3, 2, '2020-03-01' ),
	( 3, 1, 3, '2020-02-22' ),
	( 3, 2, 4, '2020-02-25' );

SELECT a.name AS results 
FROM (
	SELECT
		u.name,
		COUNT(*) AS cnt 
	FROM
		Users AS u,
		MovieRating AS mr 
	WHERE u.user_id = mr.user_id 
	GROUP BY u.user_id, u.name 
	ORDER BY cnt desc, u.name ASC 
	LIMIT 1 
) AS a 
UNION ALL
SELECT b.title AS results 
FROM (
	SELECT
		m.title,
		AVG( mr.rating ) AS avg_rating 
	FROM
		Movies AS m,
		MovieRating AS mr 
	WHERE
		m.movie_id = mr.movie_id and 
		LEFT ( mr.created_at, 7 )= '2020-02' 
	GROUP BY m.movie_id, m.title 
	ORDER BY avg_rating desc, m.title ASC 
	LIMIT 1 
) AS b;
```

### 1321. 餐馆营业额变化增长

```sql
--https://leetcode.com/problems/restaurant-growth/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Customer;
CREATE TABLE Customer ( 
	customer_id INT, 
	name VARCHAR ( 20 ), 
	visited_on DATE, 
	amount INT 
);
TRUNCATE TABLE Customer;
INSERT INTO Customer ( customer_id, name, visited_on, amount )
VALUES
	( '1', 'Jhon', '2019-01-01', '100' ),
	( '2', 'Daniel', '2019-01-02', '110' ),
	( '3', 'Jade', '2019-01-03', '120' ),
	( '4', 'Khaled', '2019-01-04', '130' ),
	( '5', 'Winston', '2019-01-05', '110' ),
	( '6', 'Elvis', '2019-01-06', '140' ),
	( '7', 'Anna', '2019-01-07', '150' ),
	( '8', 'Maria', '2019-01-08', '80' ),
	( '9', 'Jaze', '2019-01-09', '110' ),
	( '1', 'Jhon', '2019-01-10', '130' ),
	( '3', 'Jade', '2019-01-10', '150' );

SELECT
	a.visited_on,
	a.amount,
	ROUND( a.amount / 7, 2 ) AS average_amount 
	FROM (
		SELECT t1.visited_on,
		(
			SELECT SUM( t2.amount ) 
			FROM Customer AS t2 
			WHERE
				t2.visited_on <= t1.visited_on and 
				t2.visited_on >= DATE_SUB( t1.visited_on, interval 6 day )
		) AS amount 
		FROM Customer AS t1 
		WHERE
			t1.visited_on >= DATE_ADD(
				( SELECT MIN( visited_on ) FROM Customer ), 
				interval 6 day 
			) 
		GROUP BY t1.visited_on 
	) AS a 
ORDER BY a.visited_on ASC;
```

### 602. 好友申请 II ：谁有最多的好友

```sql
--https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS RequestAccepted;
CREATE TABLE IF NOT EXISTS RequestAccepted ( 
	requester_id INT NOT NULL, 
	accepter_id INT NULL, 
	accept_date DATE NULL 
);
INSERT INTO RequestAccepted ( requester_id, accepter_id, accept_date )
VALUES
	( '1', '2', '2016-06-03' ),
	( '1', '3', '2016-06-08' ),
	( '2', '3', '2016-06-08' ),
	( '3', '4', '2016-06-09' );

SELECT
	a.accepter_id AS id,
	COUNT(*) num 
FROM ( 
	SELECT t1.accepter_id 
	FROM RequestAccepted AS t1 
	UNION ALL 
	SELECT t2.requester_id AS accepter_id 
	FROM RequestAccepted AS t2 
) AS a 
GROUP BY a.accepter_id 
ORDER BY num desc 
LIMIT 1;
```

### 585. 2016年的投资

```sql
--https://leetcode.com/problems/investments-in-2016/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Insurance;
CREATE TABLE IF NOT EXISTS Insurance ( 
	pid int, 
	tiv_2015 float, 
	tiv_2016 float, 
	lat float, 
	lon float 
);
INSERT INTO Insurance ( pid, tiv_2015, tiv_2016, lat, lon )
VALUES
	( '1', 10, 5, 10, 10 ),
	( '2', 20, 20, 20, 20 ),
	( '3', 10, 30, 20, 20 ),
	( '4', 10, 40, 40, 40 );

SELECT ROUND( SUM( t.tiv_2016 ), 2 ) AS tiv_2016 
FROM Insurance AS t 
WHERE
	EXISTS ( 
		SELECT 1 
		FROM Insurance AS t2 
		WHERE 
			t.pid != t2.pid and 
			t.tiv_2015 = t2.tiv_2015 
		) 
	AND NOT EXISTS (
		SELECT 1 
		FROM Insurance AS t3 
		WHERE
			t.pid != t3.pid AND 
			t.lat = t3.lat AND 
			t.lon = t3.lon 
	);
```

### 185. 部门工资前三高的所有员工

```sql
--https://leetcode.com/problems/department-top-three-salaries/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employee, Department;
CREATE TABLE IF NOT EXISTS Department ( 
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	name varchar ( 255 ) NOT NULL 
);
CREATE TABLE IF NOT EXISTS Employee (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar ( 255 ) NOT NULL,
	salary int NOT NULL,
	departmentId int NOT NULL,
	FOREIGN KEY ( departmentId ) REFERENCES Department ( id ) 
);
INSERT INTO Department ( id, name )
VALUES
	( '1', 'IT' ),
	( '2', 'Sales' );
INSERT INTO Employee ( id, name, salary, departmentId )
VALUES
	( '1', 'Joe', '85000', '1' ),
	( '2', 'Henry', '80000', '2' ),
	( '3', 'Sam', '60000', '2' ),
	( '4', 'Max', '90000', '1' ),
	( '5', 'Janet', '69000', '1' ),
	( '6', 'Randy', '85000', '1' ),
	( '7', 'Will', '70000', '1' );

SELECT
	d.name AS Department,
	e.name AS Employee,
	e.salary AS Salary 
FROM
	Employee e,
	Department AS d 
WHERE
	e.departmentId = d.id and 
	( 
		SELECT COUNT( DISTINCT salary ) 
		FROM Employee AS ie 
		WHERE 
			ie.departmentId = e.departmentId and 
			ie.salary >= e.salary 
	) <= 3 
ORDER BY
	e.departmentId,
	e.salary DESC;
```

## 高级字符串函数 / 正则表达式 / 子句

### 1667. 修复表中的名字

```sql
--https://leetcode.com/problems/fix-names-in-a-table/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Users;
CREATE TABLE Users ( 
	user_id INT, 
	name VARCHAR ( 40 ) 
);
TRUNCATE TABLE Users;
INSERT INTO Users ( user_id, name )
VALUES
	( '1', 'aLice' ),
	( '2', 'bOB' );

SELECT
	t.user_id,
	CONCAT(
		UPPER(
			SUBSTRING( t.name, 1, 1 )
		),
		LOWER(
			SUBSTRING( t.name, 2, LENGTH( t.name ) - 1 )
		)
	) AS name 
FROM Users AS t 
ORDER BY t.user_id ASC;
```

### 1527. 患某种疾病的患者

```sql
--https://leetcode.com/problems/patients-with-a-condition/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Patients;
CREATE TABLE IF NOT EXISTS Patients ( 
	patient_id INT, 
	patient_name VARCHAR ( 30 ), 
	conditions VARCHAR ( 100 ) 
);
INSERT INTO Patients ( patient_id, patient_name, conditions )
VALUES
	( '1', 'Daniel', 'YFEV COUGH' ),
	( '2', 'Alice', '' ),
	( '3', 'Bob', 'DIAB100 MYOP' ),
	( '4', 'George', 'ACNE DIAB100' ),
	( '5', 'Alain', 'DIAB201' );

SELECT
	patient_id,
	patient_name,
	conditions 
FROM Patients AS t 
WHERE
	t.conditions LIKE 'DIAB1%' OR 
	t.conditions LIKE '% DIAB1%'; 
```

### 196. 删除重复的电子邮箱

```sql
--https://leetcode.com/problems/delete-duplicate-emails/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Person;
CREATE TABLE IF NOT EXISTS Person ( 
	Id INT, 
	Email VARCHAR ( 255 ) 
);
TRUNCATE TABLE Person;
INSERT INTO Person ( Id, Email )
VALUES
	( '1', 'john@example.com' ),
	( '2', 'bob@example.com' ),
	( '3', 'john@example.com' );

DELETE FROM Person 
WHERE
	Id NOT IN ( 
		SELECT a.Id 
		FROM ( 
			SELECT MIN( Id ) AS Id 
			FROM Person 
			GROUP BY Email 
		) AS a 
	);
```

### 176. 第二高的薪水

```sql
--https://leetcode.com/problems/second-highest-salary/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Employee;
CREATE TABLE Employee ( 
	id INT, 
	salary INT 
);
TRUNCATE TABLE Employee;
INSERT INTO Employee ( id, salary )
VALUES
	( '1', '100' ),
	( '2', '200' ),
	( '3', '300' );

( 
	SELECT t.salary SecondHighestSalary 
	FROM Employee AS t 
	GROUP BY t.salary 
	ORDER BY t.salary DESC 
	LIMIT 1, 1 
) 
UNION ALL
( 
	SELECT null AS SecondHighestSalary 
) 
ORDER BY SecondHighestSalary DESC 
LIMIT 1;
```

### 1484. 按日期分组销售产品

```sql
--https://leetcode.com/problems/group-sold-products-by-the-date/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Activities;
CREATE TABLE IF NOT EXISTS Activities ( 
	sell_date DATE, 
	product VARCHAR ( 20 ) 
);
TRUNCATE TABLE Activities;
INSERT INTO Activities ( sell_date, product )
VALUES
	( '2020-05-30', 'Headphone' ),
	( '2020-06-01', 'Pencil' ),
	( '2020-06-02', 'Mask' ),
	( '2020-05-30', 'Basketball' ),
	( '2020-06-01', 'Bible' ),
	( '2020-06-02', 'Mask' ),
	( '2020-05-30', 'T-Shirt' );

SELECT
	t.sell_date,
	COUNT( DISTINCT t.product ) AS num_sold,
	GROUP_CONCAT( DISTINCT t.product ) AS products 
FROM Activities AS t 
GROUP BY t.sell_date 
ORDER BY t.sell_date ASC;
```

### 1327. 列出指定时间段内所有的下单产品

```sql
--https://leetcode.com/problems/list-the-products-ordered-in-a-period/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Orders;
CREATE TABLE IF NOT EXISTS Products ( 
	product_id INT, 
	product_name VARCHAR ( 40 ), 
	product_category VARCHAR ( 40 ) 
);
CREATE TABLE IF NOT EXISTS Orders ( 
	product_id INT, 
	order_date DATE, 
	unit INT 
);
TRUNCATE TABLE Products;
TRUNCATE TABLE Orders;
INSERT INTO Products ( product_id, product_name, product_category )
VALUES
	( '1', 'Leetcode Solutions', 'Book' ),
	( '2', 'Jewels of Stringology', 'Book' ),
	( '3', 'HP', 'Laptop' ),
	( '4', 'Lenovo', 'Laptop' ),
	( '5', 'Leetcode Kit', 'T-shirt' );
INSERT INTO Orders ( product_id, order_date, unit )
VALUES
	( '1', '2020-02-05', '60' ),
	( '1', '2020-02-10', '70' ),
	( '2', '2020-01-18', '30' ),
	( '2', '2020-02-11', '80' ),
	( '3', '2020-02-17', '2' ),
	( '3', '2020-02-24', '3' ),
	( '4', '2020-03-01', '20' ),
	( '4', '2020-03-04', '30' ),
	( '4', '2020-03-04', '60' ),
	( '5', '2020-02-25', '50' ),
	( '5', '2020-02-27', '50' ),
	( '5', '2020-03-01', '50' );

SELECT
	p.product_name,
	SUM( o.unit ) AS unit 
FROM
	Products AS p,
	Orders AS o 
WHERE
	p.product_id = o.product_id and 
	LEFT ( o.order_date, 7 ) = '2020-02' 
GROUP BY p.product_id, p.product_name 
HAVING unit >= 100;
```

### 1517. 查找拥有有效邮箱的用户

```sql
# https://leetcode.com/problems/find-users-with-valid-e-mails/description/?envType=study-plan-v2&envId=top-sql-50
DROP TABLE IF EXISTS Users;
CREATE TABLE Users ( 
	user_id INT, 
	name VARCHAR ( 30 ), 
	mail VARCHAR ( 50 ) 
);
TRUNCATE TABLE Users;
INSERT INTO Users ( user_id, name, mail )
VALUES
	( '1', 'Winston', 'winston@leetcode.com' ),
	( '2', 'Jonathan', 'jonathanisgreat' ),
	( '3', 'Annabelle', 'bella-@leetcode.com' ),
	( '4', 'Sally', 'sally.come@leetcode.com' ),
	( '5', 'Marwan', 'quarz#2020@leetcode.com' ),
	( '6', 'David', 'david69@gmail.com' ),
	( '7', 'Shapiro', '.shapo@leetcode.com' ),
	( '8', 'Benjamin', 'Benjamin._2@leetcode.com' ),
	( '8', 'Winston', 'winston@leetcode?com' );

SELECT * 
FROM Users AS t 
WHERE
	t.mail REGEXP '^[a-zA-Z][-._a-zA-Z0-9]*@leetcode\\.com$';
```
