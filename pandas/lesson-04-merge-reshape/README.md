# Pandas Lesson 04 — Merge & Reshape

> **Estimated time:** 40–50 minutes  
> **Run exercises:** `python pandas/lesson-04-merge-reshape/lesson.py`

---

## merge() — Joining DataFrames

```python
# Inner join (default)
pd.merge(left_df, right_df, on="employee_id")

# Left join
pd.merge(left_df, right_df, on="employee_id", how="left")

# Different column names
pd.merge(left_df, right_df, left_on="emp_id", right_on="employee_id")
```

| how= | Rows kept |
|------|-----------|
| `"inner"` | only matching rows (default) |
| `"left"` | all left rows + matching right |
| `"right"` | all right rows + matching left |
| `"outer"` | all rows from both sides |

```python
# After a left join, find rows with no match (anti-join)
merged = pd.merge(emp, contracts, on="department", how="left")
no_match = merged[merged["contract_id"].isna()]
```

---

## concat() — Stacking DataFrames

```python
# Stack rows vertically (default axis=0)
combined = pd.concat([df1, df2], ignore_index=True)

# Stack columns horizontally
combined = pd.concat([df1, df2], axis=1)
```

> `ignore_index=True` resets the index after stacking — almost always what you want.

---

## pivot_table() — Reshape to Wide Format

Turns rows into columns. Like a spreadsheet pivot.

```python
# Average salary by department (rows) and clearance (columns)
pivot = pd.pivot_table(
    emp,
    values="salary",
    index="department",
    columns="clearance",
    aggfunc="mean",
    fill_value=0,
)
```

```
clearance    Confidential    Secret    Top Secret
department
Cyber               0.0    118000.0    132000.0
Engineering     95000.0     97000.0    120000.0
```

---

## melt() — Reshape to Long Format (reverse of pivot)

```python
# Wide format:
#   dept    Q1       Q2
#   Cyber   120000   125000
#
# After melt:
#   dept    quarter  salary
#   Cyber   Q1       120000
#   Cyber   Q2       125000

pd.melt(
    wide_df,
    id_vars=["department"],    # columns to keep as-is
    value_vars=["Q1", "Q2"],   # columns to unpivot
    var_name="quarter",        # name for the new "variable" column
    value_name="salary",       # name for the new "value" column
)
```

---

## ✅ You're Ready When You Can Answer

- What is the default join type for pd.merge()?
- How do you do a left join in pandas?
- How do you find rows in a left join that had no match on the right?
- What is the difference between merge() and concat()?
- When would you use pivot_table() vs melt()?

---

**Next:** `python pandas/lesson-04-merge-reshape/lesson.py`
