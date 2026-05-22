# Pandas Lesson 05 — Datetime & Advanced Pandas

> **Estimated time:** 35–45 minutes  
> **Run exercises:** `python pandas/lesson-05-datetime-advanced/lesson.py`

---

## Datetime Basics

```python
# Convert string column to datetime
df["hire_date"] = pd.to_datetime(df["hire_date"])

# The .dt accessor unlocks datetime properties
df["hire_date"].dt.year         # year as int
df["hire_date"].dt.month        # month as int (1–12)
df["hire_date"].dt.day          # day of month
df["hire_date"].dt.dayofweek    # 0=Monday, 6=Sunday
df["hire_date"].dt.quarter      # 1–4
df["hire_date"].dt.date         # date part only (no time)

# Arithmetic
df["days_employed"] = (pd.Timestamp("today") - df["hire_date"]).dt.days
df["tenure_years"]  = df["days_employed"] / 365.25
```

---

## Filtering by Date

```python
df[df["hire_date"] >= "2020-01-01"]
df[df["hire_date"].dt.year == 2022]
df[df["hire_date"].between("2021-01-01", "2022-12-31")]
```

---

## resample() — Time Series Aggregation

`resample()` is like `groupby()` but for time periods. Requires a datetime index.

```python
df = df.set_index("hire_date")

df["salary"].resample("Y").mean()    # annual mean
df["salary"].resample("M").count()  # monthly count
df["salary"].resample("Q").sum()    # quarterly sum
```

Frequency aliases: `"D"` day, `"W"` week, `"M"` month, `"Q"` quarter, `"Y"` year.

---

## Method Chaining

Pandas is designed for chaining — each method returns a DataFrame you can continue calling methods on.

```python
result = (
    df
    .query("active == 1")                              # filter
    .assign(salary_band=lambda x: x["salary"].apply(band_fn))  # add column
    .groupby("department")                             # group
    .agg(headcount=("employee_id","count"),
         avg_salary=("salary","mean"))                 # aggregate
    .reset_index()
    .sort_values("avg_salary", ascending=False)        # sort
    .head(5)                                           # top 5
)
```

> Method chaining is more readable than step-by-step variable assignment for linear pipelines.

---

## query() — Readable Filtering

```python
# Instead of: df[(df["dept"]=="Cyber") & (df["salary"] > 100000)]
df.query("department == 'Cyber' and salary > 100000")
df.query("clearance in ['Secret', 'Top Secret']")
df.query("active == 1 and salary > @threshold")  # @ references a Python variable
```

---

## ✅ You're Ready When You Can Answer

- How do you extract the year from a datetime column?
- What is the difference between resample() and groupby()?
- How do you calculate the number of days between two datetime columns?
- What does .assign() do in a method chain?
- How does query() differ from boolean mask filtering?

---

**Next:** `python pandas/lesson-05-datetime-advanced/lesson.py`
