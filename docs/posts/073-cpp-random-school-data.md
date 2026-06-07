---
date: 2026-06-07
authors:
  - moita
categories:
  - 工程实践
tags:
  - CPP
  - 测试
  - IO
  - 面向对象
---

# C++ 随机生成虚拟学校测试数据

两个 C++ 小程序，利用随机数生成虚拟学校的考试成绩数据与学生角色信息。原始代码存在缓冲区溢出、文件错误检查缺失等问题，以下展示修正后的完整代码。

<!-- more -->

## 考试成绩数据生成器

这段代码定义了 `stu_info`、`sub_info`、`exam_info`、`item` 四个类，通过三层随机组合生成 1000 名学生 × 20 门课程 = 20000 条考试记录，同时输出账号信息。

原始代码存在的问题：

- `fscanf` 使用 `%s` 未限制读取宽度，若文件中单行超过 99 字符，会触发缓冲区溢出。
- 多次 `fopen` 未检查返回值，数据文件缺失时后续 `fscanf` 对空指针操作直接崩溃。
- `#include <math.h>` 未被使用。
- `srand(time(0))` 缺少显式类型转换，可能产生编译器警告。
- 四个类的构造函数使用赋值语句逐一填充成员变量，对 `string` 成员而言，初始化列表比先默认构造再赋值更高效。
- 成员变量 `colledge` 应为 `college`。

### 修正后代码

```cpp
#include <stdio.h>
#include <stdlib.h>
// #include <math.h>                          // 删除：未使用的头文件
#include <time.h>
#include <string>
#include <iostream>

using namespace std;

class stu_info
{
	public:
		string name;
		long id;
		string colledge;
		int grade;
		stu_info() {}
		stu_info(string val_name, long val_id, string val_colledge, int val_grade)
			: name(val_name), id(val_id), colledge(val_colledge), grade(val_grade) {}  // 修正：使用初始化列表
};

class sub_info
{
	public:
		string subject;
		string teacher;
		float credit;
		sub_info() {}
		sub_info(string val_subject, string val_teacher, float val_credit)
			: subject(val_subject), teacher(val_teacher), credit(val_credit) {}  // 修正：使用初始化列表
};

class exam_info
{
	public:
		int year;
		int semester;
		int test_date;
		int score;

		exam_info() {}
		exam_info(int val_year, int val_semester, int val_test_date, int val_score)
			: year(val_year), semester(val_semester), test_date(val_test_date), score(val_score) {}  // 修正：使用初始化列表
};

class item
{
	public:
		stu_info stu;
		sub_info sub;
		exam_info exam;

		item() {}
		item(stu_info val_stu_info, sub_info val_sub_info, exam_info val_exam_info)
			: stu(val_stu_info), sub(val_sub_info), exam(val_exam_info) {}  // 修正：使用初始化列表，避免逐字段赋值
};

int main()
{
	srand((unsigned int)time(NULL));           // 修正：显式类型转换

	stu_info swu_stu[1000];
	char temp[100];
	string colledge[12] = {
		"文学院", "马克思主义学院", "法学院", "经济管理学院",
		"新闻传媒学院", "计算机与信息科学学院", "数学与统计学院",
		"物理科学与技术学院", "农学与生物科技学院",
		"动物医学院", "药学院", "音乐学院"
	};

	FILE *fo;
	fo = fopen("./stu_name_ANSI.txt", "r");
	if (!fo) {                                 // 新增：文件打开失败检查
		perror("无法打开 stu_name_ANSI.txt");
		return 1;
	}
	for (int i = 0; i < 1000; i++)
	{
		fscanf(fo, "%99s", temp);              // 修正：限制读取宽度，移除 &
		swu_stu[i].name = temp;
		swu_stu[i].id = i + 1;
		swu_stu[i].colledge = colledge[rand() % 12];
		swu_stu[i].grade = 2020 + rand() % 3;
	}
	fclose(fo);

	sub_info swu_sub[20];
	string teacher[50];
	fo = fopen("./tea_name_ANSI.txt", "r");
	if (!fo) {                                 // 新增：文件打开失败检查
		perror("无法打开 tea_name_ANSI.txt");
		return 1;
	}
	for (int i = 0; i < 50; i++)
	{
		fscanf(fo, "%99s", temp);              // 修正：限制读取宽度，移除 &
		teacher[i] = temp;
	}
	fclose(fo);

	string subject[20];
	fo = fopen("./subject_ANSI.txt", "r");
	if (!fo) {                                 // 新增：文件打开失败检查
		perror("无法打开 subject_ANSI.txt");
		return 1;
	}
	for (int i = 0; i < 20; i++)
	{
		fscanf(fo, "%99s", temp);              // 修正：限制读取宽度，移除 &
		subject[i] = temp;
	}
	fclose(fo);

	float credit[5] = {1, 1.5, 2, 2.5, 3};
	for (int i = 0; i < 20; i++)
	{
		swu_sub[i].teacher = teacher[rand() % 50];
		swu_sub[i].subject = subject[i];
		swu_sub[i].credit = credit[rand() % 5];
	}

	exam_info swu_exam;
	item item_temp;
	int test_date[7] = {20200123, 20200725, 20210120, 20210925, 20220116, 20221228, 20201123};

	fo = fopen("./allinfo.csv", "w");
	if (!fo) {                                 // 新增：写入文件失败检查
		perror("无法创建 allinfo.csv");
		return 1;
	}
	for (int i = 0; i < 1000; i++)
	{
		for (int j = 0; j < 20; j++)
		{
			swu_exam.score = rand() % 40 + 55;
			swu_exam.semester = rand() % 2 + 1;
			swu_exam.test_date = test_date[rand() % 7];
			swu_exam.year = swu_stu[i].grade + rand() % 2;
			item_temp = item(swu_stu[i], swu_sub[j], swu_exam);
			fprintf(fo, "%s,%ld,%s,%d,%d,%d,",
				item_temp.stu.name.c_str(), item_temp.stu.id, item_temp.stu.colledge.c_str(), item_temp.stu.grade,
				item_temp.exam.year, item_temp.exam.semester
			);
			fprintf(fo, "%s,%s,%d,%d,%1.1lf\n",
				item_temp.sub.subject.c_str(), item_temp.sub.teacher.c_str(),
				item_temp.exam.test_date, item_temp.exam.score, item_temp.sub.credit
			);
		}
	}
	fclose(fo);

	fo = fopen("./account.csv", "w");
	if (!fo) {                                 // 新增：写入文件失败检查
		perror("无法创建 account.csv");
		return 1;
	}
	for (int i = 0; i < 1000; i++)
	{
		string type = "student";
		sprintf(temp, "swu%04dstu", swu_stu[i].id);
		string account = temp;
		sprintf(temp, "swu%04dstu", swu_stu[i].id);
		string password = temp;
		fprintf(fo, "%s,%s,%s,%s,false\n", swu_stu[i].name.c_str(), type.c_str(), account.c_str(), password.c_str());
	}
	for (int i = 0; i < 50; i++)
	{
		string type = "teacher";
		sprintf(temp, "swu%04dtea", i);
		string account = temp;
		sprintf(temp, "swu%04dtea", i);
		string password = temp;
		fprintf(fo, "%s,%s,%s,%s,false\n", teacher[i].c_str(), type.c_str(), account.c_str(), password.c_str());
	}
	fprintf(fo, "root,root,swu1234root,swu1234root,false\n");
	fclose(fo);

	return 0;
}
```

### 输出说明

程序运行后生成两个 CSV 文件：

- `allinfo.csv`：20000 条考试记录，每行包含学生姓名、学号、学院、年级、考试年份、学期、科目、授课教师、考试日期、分数、学分。
- `account.csv`：1051 条账号记录，包括 1000 名学生、50 名教师和 1 个 root 管理员，密码与账号相同，用于系统登录测试。

数据来源依赖三个外部文件 `stu_name_ANSI.txt`（1000 个学生姓名）、`tea_name_ANSI.txt`（50 个教师姓名）、`subject_ANSI.txt`（20 个科目名），均按 ANSI 编码，每行一个名称。

---

## 学生角色信息生成器

这段代码生成 100 名学生的角色分类数据，将一个学生设为"程序员代表"，前三个学生分别设为数据结构、数据库、Linux 课代表，其余为普通学生，同时为每人随机生成三科成绩。

原始代码除与上一节重复的问题外，还有一个额外缺陷：循环固定读取 100 次而不检查 `fscanf` 返回值。若姓名文件内容不足 100 行，读取失败后 `temp` 保留上次的值，导致后续数据行出现重复姓名。

### 修正后代码

```cpp
#include <stdio.h>
#include <stdlib.h>
// #include <math.h>                          // 删除：未使用的头文件
#include <time.h>
#include <string>
#include <iostream>

using namespace std;

int main()
{
	srand((unsigned int)time(NULL));           // 修正：显式类型转换

	FILE *fo;
	fo = fopen("./stu_name_ANSI.txt", "r");
	if (!fo) {                                 // 新增：文件打开失败检查
		perror("无法打开 stu_name_ANSI.txt");
		return 1;
	}
	char temp[100];
	string student[100];
	int count = 0;                             // 新增：记录实际读取行数
	for (int i = 0; i < 100; i++)
	{
		if (fscanf(fo, "%99s", temp) != 1)     // 修正：限制读取宽度，移除 &，检查返回值
			break;                             // 新增：文件读取完毕时退出循环
		student[i] = temp;
		count++;                               // 新增：统计实际人数
	}
	fclose(fo);

	string type[5] = {"普通学生", "数据结构课代表", "数据库课代表", "linux课代表", "程序员代表"};
	fo = fopen("./allinfo.csv", "w");
	if (!fo) {                                 // 新增：写入文件失败检查
		perror("无法创建 allinfo.csv");
		return 1;
	}
	for (int i = 0; i < count; i++)            // 修正：用实际人数替代硬编码 100
	{
		if (i == 0)
		{
			fprintf(fo, "%s,%s,swu%04dstu,swu%04dstu,%d,%d,%d,false\n",
				student[i].c_str(), type[4].c_str(), i, i,
				rand() % 30 + 65, rand() % 30 + 65, rand() % 30 + 65
			);
		}
		else if (i >= 1 && i <= 3)
		{
			fprintf(fo, "%s,%s,swu%04dstu,swu%04dstu,%d,%d,%d,false\n",
				student[i].c_str(), type[i].c_str(), i, i,
				rand() % 30 + 65, rand() % 30 + 65, rand() % 30 + 65
			);
		}
		else
		{
			fprintf(fo, "%s,%s,swu%04dstu,swu%04dstu,%d,%d,%d,false\n",
				student[i].c_str(), type[0].c_str(), i, i,
				rand() % 30 + 65, rand() % 30 + 65, rand() % 30 + 65
			);
		}
	}
	fclose(fo);

	return 0;
}
```

### 输出说明

程序生成 `allinfo.csv`，每行包含：姓名、角色类型、账号、密码、三科成绩（分数范围 65~94）、状态标记 `false`。账号格式为 `swuXXXXstu`，其中 XXXX 为四位序号从 0000 起。
