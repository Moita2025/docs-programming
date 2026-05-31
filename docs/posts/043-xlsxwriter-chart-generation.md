---
date: 2026-05-31
authors:
  - moita
categories:
  - 数据科学
tags:
  - Python
  - 数据可视化
  - Excel
---

# Python 使用 xlsxwriter 生成 Excel 图表

`xlsxwriter` 是一个纯 Python 的 Excel 写入库，支持图表、格式化和公式。当需要把数据写入 Excel 并同时生成可视化图表时，它比 `openpyxl` 更简洁。

下面用排序算法性能对比的场景，演示如何将数据写入 Excel 并生成柱状图。

<!-- more -->

## 完整代码

```python
# -*- coding:utf-8 -*-
import xlsxwriter
 
def create_graph(a,b,c,d,e,f):
    workbook = xlsxwriter.Workbook("排序算法比较结果.xlsx")
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': 1})

    headings = ["排序方法", "排序时间"]
    data = [
        ["简单选择排序", "直接插入排序", "冒泡排序", "快速排序", "两路合并排序", "堆排序"],
        [a,b,c,d,e,f]
    ]
     
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
  
    chart_col = workbook.add_chart({'type': 'column'})
    chart_col.add_series({
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$7',
        'values': '=Sheet1!$B$2:$B$7',
        'line': {'color': 'red'},
    })

    chart_col.set_title({'name': "排序算法结果"})
    chart_col.set_x_axis({'name': "排序方法"})
    chart_col.set_y_axis({'name': "花费时间(ms)"})
    chart_col.set_style(1)

    worksheet.insert_chart('A10', chart_col, {'x_offset': 25, 'y_offset': 10})
     
    workbook.close()
    return 0
 
if __name__ == "__main__":
    create_graph(10, 40, 50, 20, 10, 50)
```

## 关键步骤说明

### 写入表格数据

`xlsxwriter` 支持按行、按列批量写入。`write_row` 和 `write_column` 比逐单元格写入更简洁：

```python
worksheet.write_row('A1', headings, bold)   # 写入表头，应用粗体样式
worksheet.write_column('A2', data[0])        # 纵向写入排序方法名称
worksheet.write_column('B2', data[1])        # 纵向写入对应时间
```

### 创建柱状图

通过 `add_chart({'type': 'column'})` 创建柱状图。`add_series` 配置数据系列时，引用的是当前 Sheet 的单元格区域：

```python
chart_col.add_series({
    'name': '=Sheet1!$B$1',               # 系列名称，引用表头
    'categories': '=Sheet1!$A$2:$A$7',    # X 轴标签
    'values': '=Sheet1!$B$2:$B$7',        # Y 轴数值
    'line': {'color': 'red'},             # 可选：边框线颜色
})
```

注意 `Sheet1` 是未指定名称时的默认 Sheet 名。如果在 `add_worksheet()` 时传入了名称，这里要对应修改。

### 设置图表样式

```python
chart_col.set_title({'name': "排序算法结果"})
chart_col.set_x_axis({'name': "排序方法"})
chart_col.set_y_axis({'name': "花费时间(ms)"})
chart_col.set_style(1)
```

`set_style(1)` 是 48 种预设风格中的一种。不同数字对应不同配色方案，从 1 到 48 可选。

### 插入图表到指定位置

```python
worksheet.insert_chart('A10', chart_col, {'x_offset': 25, 'y_offset': 10})
```

图表左上角对齐 A10 单元格，并向右偏移 25px、向下偏移 10px 进行微调。

## 支持的图表类型

`xlsxwriter` 内置多种图表类型，常用的有：

| 类型 | `type` 参数 |
|------|------------|
| 柱状图 | `column` |
| 条形图 | `bar` |
| 折线图 | `line` |
| 饼图 | `pie` |
| 散点图 | `scatter` |
| 面积图 | `area` |

换成折线图只需改为 `{'type': 'line'}`，其他配置完全不变。

## 注意事项

`xlsxwriter` 只支持写入，不能读取已有 Excel 文件。如果需要对已有文件进行读写操作，需要搭配 `openpyxl` 使用。

安装方式：

```bash
pip install xlsxwriter
```
