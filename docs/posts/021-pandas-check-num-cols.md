---
date: 2026-04-20
authors:
  - moita
categories:
  - 数据科学
tags:
  - Pandas
  - Python
---

# Pandas 检验数值列的数据质量

* 输出每列：
  * 缺失值数量（NaN）
  * 无穷值数量（Inf）
  * 唯一值数量（Unique）

* 检测并打印：
  * 任意列包含 NaN 或 Inf 的行（最多前 10 条）

<!-- more -->

```py
import pandas as pd
import numpy as np

def check_num_cols(df, num_cols):
    """
    检查指定列：
    - NaN 数量
    - Inf 数量
    - 唯一值数量
    - 打印存在 NaN / Inf 的前10行
    """

    print("\n=== Column Summary ===")

    for col in num_cols:
        if col not in df.columns:
            print(f"  ERROR: Column '{col}' not found!")
            continue

        na_count = df[col].isna().sum()
        inf_count = np.isinf(df[col]).sum()
        unique_count = df[col].nunique(dropna=True)

        print(
            f"{col:20} -> NaN: {na_count:5d} | Inf: {inf_count:5d} | Unique: {unique_count}"
        )

    # === 行级问题检测 ===
    problem_mask = (
        df[num_cols].isna().any(axis=1)
        | np.isinf(df[num_cols]).any(axis=1)
    )

    if problem_mask.any():
        print(f"\n⚠️ Found {problem_mask.sum()} rows with NaN or Inf. Showing first 10:")
        print(df.loc[problem_mask, num_cols].head(10))
    else:
        print("\n✅ No NaN or Inf found in given columns.")
```
