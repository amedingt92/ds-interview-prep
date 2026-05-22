# Pandas Lesson 02 — Cleaning & Transformation

> **Estimated time:** 35–45 minutes  
> **Run exercises:** `python pandas/lesson-02-cleaning-transformation/lesson.py`

---

## Handling NaN

```python
df.isna().sum()           # count NaNs per column
df.isna().any()           # True/False per column

df.dropna()               # drop rows with ANY NaN
df.dropna(subset=["col"]) # drop rows where col is NaN
df.dropna(thresh=5)       # keep rows with at least 5 non-NaN values

df.fillna(0)                          # fill all NaN with 0
df.fillna({"salary": 0, "name": "Unknown"})  # different values per column
df["col"].fillna(df["col"].median())  # fill with median
df["col"].fillna(method="ffill")      # forward fill
```

---

## Data Type Conversion

```python
df["salary"]   = df["salary"].astype(int)
df["hire_date"]= pd.to_datetime(df["hire_date"])
df["active"]   = df["active"].astype(bool)

# Check types
df.dtypes
```

---

## Renaming Columns

```python
df.rename(columns={"old_name": "new_name", "emp_id": "employee_id"})
df.columns = ["col1", "col2", "col3"]   # rename all at once
```

---

## apply() and map()

```python
# Apply a function to every value in a column
df["salary_band"] = df["salary"].apply(lambda s: "Senior" if s >= 130000 else "Mid" if s >= 100000 else "Junior")

# Apply a function row-by-row (axis=1)
df["label"] = df.apply(lambda row: f"{row['name']} ({row['department']})", axis=1)

# Map values using a dict (replace values)
severity_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
df["severity_score"] = df["severity"].map(severity_map)
```

---

## value_counts() and Other Useful Methods

```python
df["department"].value_counts()         # frequency table
df["department"].value_counts(normalize=True)  # as proportions
df.duplicated().sum()                   # count duplicate rows
df.drop_duplicates()                    # remove duplicate rows
df.sort_values("salary", ascending=False)
```

---

## ✅ You're Ready When You Can Answer

- What is the difference between dropna() and fillna()?
- How do you apply a custom function to every row of a DataFrame?
- What does map() do on a Series vs apply()?
- How do you convert a string column to datetime?
- What does value_counts(normalize=True) return?

---

**Next:** `python pandas/lesson-02-cleaning-transformation/lesson.py`
