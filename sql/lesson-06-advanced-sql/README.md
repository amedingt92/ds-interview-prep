# SQL Lesson 06 — Advanced SQL

> **Estimated time:** 40–50 minutes  
> **Run exercises:** `python sql/lesson-06-advanced-sql/lesson.py`  
> **Tables used:** all five tables

---

## CASE WHEN

`CASE WHEN` is SQL's if/else. Use it to create conditional columns or bucket values.

```sql
-- Simple bucketing
SELECT
    name,
    salary,
    CASE
        WHEN salary >= 130000 THEN 'Senior'
        WHEN salary >= 100000 THEN 'Mid'
        ELSE 'Junior'
    END AS salary_band
FROM employees;
```

### Conditional Aggregation

One of the most powerful patterns — count or sum only rows matching a condition:

```sql
SELECT
    department,
    COUNT(*) AS total,
    SUM(CASE WHEN clearance = 'Top Secret' THEN 1 ELSE 0 END) AS top_secret_count,
    SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) AS active_count
FROM employees
GROUP BY department;
```

---

## Date Functions

| Function | What it does | Example |
|----------|-------------|---------|
| `CURRENT_DATE` | today's date | `WHERE hire_date < CURRENT_DATE` |
| `DATEDIFF('day', start, end)` | days between two dates | `DATEDIFF('day', hire_date, CURRENT_DATE)` |
| `DATE_TRUNC('month', date)` | truncate to month/year/week | `DATE_TRUNC('year', hire_date)` |
| `STRFTIME(date, '%Y-%m')` | format date as string | year-month grouping |

```sql
-- Employees hired more than 3 years ago
SELECT name, hire_date,
       DATEDIFF('day', hire_date, CURRENT_DATE) AS days_employed
FROM employees
WHERE hire_date < CURRENT_DATE - INTERVAL '3 years';

-- Group hiring by year
SELECT
    DATE_TRUNC('year', hire_date) AS hire_year,
    COUNT(*) AS hires
FROM employees
GROUP BY DATE_TRUNC('year', hire_date)
ORDER BY hire_year;
```

---

## String Functions

| Function | What it does |
|----------|-------------|
| `UPPER(col)` / `LOWER(col)` | change case |
| `LENGTH(col)` | string length |
| `TRIM(col)` | remove leading/trailing spaces |
| `REPLACE(col, 'old', 'new')` | replace substring |
| `SUBSTRING(col, start, length)` | extract part of string |
| `CONCAT(a, b)` or `a \|\| b` | join strings |
| `LIKE` / `ILIKE` | pattern matching (ILIKE = case-insensitive) |

```sql
SELECT
    UPPER(name) AS name_upper,
    LENGTH(name) AS name_length,
    SUBSTRING(name, 1, 5) AS first_5_chars,
    name || ' — ' || department AS full_label
FROM employees;
```

---

## Query Optimization Basics

You won't be asked to write execution plans but knowing these concepts helps:

- **SELECT \*** is expensive — only select columns you need
- **Filtering early** — push WHERE conditions as early as possible
- **Indexing** — columns used in WHERE, JOIN ON, and ORDER BY benefit from indexes
- **Avoid functions on indexed columns in WHERE** — `WHERE YEAR(hire_date) = 2022` can't use an index; `WHERE hire_date BETWEEN '2022-01-01' AND '2022-12-31'` can

---

## ✅ You're Ready When You Can Answer

- How do you create salary bands (Junior/Mid/Senior) in a SELECT?
- What is conditional aggregation and how do you write it?
- How do you count days between two dates?
- How do you group records by hire year?
- What is the difference between LIKE and ILIKE?

---

**Next:** `python sql/lesson-06-advanced-sql/lesson.py`
