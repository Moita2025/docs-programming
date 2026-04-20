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

# Pandas 时间偏移 重要差别

Pandas 的 `DateOffset` 在 `n=0` 和 `n>0` 时行为有显著差异，理解这一点至关重要。

<!-- more -->

## `QuarterEnd(0)` 的特殊行为

- `n=0` 时，`QuarterEnd(0)` **不是** “前进 0 个季度”。
- 而是将日期 **调整到当前季度的最后一个月最后一天** （就地锚定）。
- 自动计算当前日期所在季度的结束日期。

## `MonthEnd(n)` 当 `n > 0` 时的行为

- `n ≥ 1` 时，`MonthEnd(n)` **是** “从当前日期开始，向前推进 n 个月，然后取那个月的最后一天”。
- **严格前进 n 个月**，而不是包含 n+1 个月。

## 常见错误及修正

- **错误:**  期望 `MonthEnd(5)` 包含 6 个月。
- **正确:**  使用 `MonthEnd(6)` 来包含 6 个月。
- **推荐:**  对于6个月周期，使用 `df['start_month'] + pd.offsets.MonthEnd(6)`。
