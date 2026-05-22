# Pandas Lesson 03 — GroupBy & Aggregation

> **Estimated time:** 35–45 minutes  
> **Run exercises:** `python pandas/lesson-03-groupby-aggregation/lesson.py`

---

## groupby() Basics

```python
# Single aggregation
df.groupby("department")["salary"].mean()

# Multiple aggregations
df.groupby("department")["salary"].agg(["mean","min","max","count"])

# Multiple columns + multiple aggs
df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    headcount=("employee_id", "count"),
)
```

---

## Named Aggregation (clean syntax)

```python
result = df.groupby("department").agg(
    avg_salary   = ("salary",      "mean"),
    total_payroll= ("salary",      "sum"),
    headcount    = ("employee_id", "count"),
    max_salary   = ("salary",      "max"),
).reset_index()
```

> Always call `.reset_index()` after groupby to turn the group keys back into columns.

---

## transform() vs agg()

This is a common test question.

```python
# agg() → collapses to one row per group
df.groupby("department")["salary"].agg("mean")
# Returns: Series with 6 values (one per dept)

# transform() → returns a value for EVERY row, same length as original
df["dept_avg"] = df.groupby("department")["salary"].transform("mean")
# Returns: Series with 74 values — each row gets its department's average
```

Use `transform()` when you want to add a group-level column back onto the original DataFrame.

---

## Multiple GroupBy Keys

```python
df.groupby(["department","clearance"]).agg(
    count=("employee_id","count"),
    avg_salary=("salary","mean"),
).reset_index()
```

---

## ✅ You're Ready When You Can Answer

- What does reset_index() do after a groupby?
- What is the difference between agg() and transform()?
- How do you compute multiple aggregations at once with named columns?
- How do you group by two columns at once?

---

**Next:** `python pandas/lesson-03-groupby-aggregation/lesson.py`
