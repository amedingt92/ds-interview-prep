# Snowflake 02 — Snowflake SQL Differences

> **Format:** Reference + self-check  
> These are the SQL functions and behaviors unique to Snowflake (vs standard SQL or DuckDB).

---

## Functions That Replace Standard SQL Equivalents

### IFF() — Inline IF

```sql
-- Standard SQL:
CASE WHEN condition THEN a ELSE b END

-- Snowflake shorthand:
IFF(condition, a, b)

-- Example:
SELECT name, IFF(salary >= 130000, 'Senior', 'Not Senior') AS band
FROM employees;
```

### ZEROIFNULL() / NULLIFZERO()

```sql
-- Instead of: COALESCE(col, 0)
ZEROIFNULL(col)        -- returns 0 if NULL

-- Instead of: NULLIF(col, 0)
NULLIFZERO(col)        -- returns NULL if 0

-- Example:
SELECT ZEROIFNULL(event_count) AS event_count FROM summary;
```

### NVL() — Alias for COALESCE with two args

```sql
NVL(col, 'default')    -- equivalent to COALESCE(col, 'default')
NVL2(col, a, b)        -- if col IS NOT NULL then a, else b
```

### ILIKE — Case-Insensitive LIKE

```sql
-- Standard SQL LIKE is case-sensitive:
WHERE name LIKE 'alex%'    -- misses "Alex", "ALEX"

-- Snowflake ILIKE is case-insensitive:
WHERE name ILIKE 'alex%'   -- matches "alex", "Alex", "ALEX"
```

---

## Aggregation Functions Unique to Snowflake

### ARRAY_AGG() — Collect values into an array

```sql
-- Collect all event types per employee into an array
SELECT
    employee_id,
    ARRAY_AGG(event_type) AS all_event_types,
    ARRAY_AGG(DISTINCT event_type) AS unique_event_types
FROM security_events
GROUP BY employee_id;
```

### LISTAGG() — Concatenate strings within a group

```sql
SELECT
    department,
    LISTAGG(name, ', ') WITHIN GROUP (ORDER BY name) AS employee_list
FROM employees
GROUP BY department;
```

### OBJECT_AGG() — Build a JSON object from rows

```sql
SELECT OBJECT_AGG(event_type, severity) FROM events;
-- {"login_failure": "LOW", "privilege_escalation": "CRITICAL", ...}
```

---

## QUALIFY — Filter Window Function Results (Covered in SQL Lesson 05)

Snowflake-native (also supported in DuckDB). Filters after window function computation without a subquery.

```sql
-- Top 2 earners per department
SELECT name, department, salary,
       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
FROM employees
QUALIFY rnk <= 2;
```

---

## String Functions Snowflake-Specific

```sql
SPLIT_PART(str, delimiter, position)   -- split and return the Nth part (1-indexed)
REGEXP_SUBSTR(str, pattern)            -- extract regex match
REGEXP_REPLACE(str, pattern, replacement)
INITCAP(str)                           -- Title Case
REPEAT(str, n)                         -- repeat string n times
LPAD(str, length, pad_char)            -- left-pad to length
RPAD(str, length, pad_char)            -- right-pad to length

-- Example:
SELECT SPLIT_PART('10.0.45.23', '.', 1)   -- returns '10'
SELECT SPLIT_PART('10.0.45.23', '.', 2)   -- returns '0'
```

---

## Date/Time Functions

```sql
DATEADD(unit, amount, date)
-- Example: DATEADD('day', 30, CURRENT_DATE)

DATEDIFF(unit, start_date, end_date)
-- Example: DATEDIFF('day', hire_date, CURRENT_DATE)

DATE_TRUNC('month', date)    -- truncate to start of month
DATE_TRUNC('year', date)     -- truncate to start of year
DATE_PART('month', date)     -- extract month as integer

CURRENT_DATE                 -- today's date
CURRENT_TIMESTAMP            -- current date + time
TO_DATE('2024-03-15')        -- parse string to date
```

---

## Semi-Structured Type Casting

Snowflake is strongly typed. Use `::type` or `CAST(col AS type)` to convert.

```sql
-- Cast string to integer
'95000'::INT

-- Cast to date
'2024-03-15'::DATE

-- Cast to float
salary::FLOAT
```

---

## Self-Check ✅

1. What is the difference between `IFF()` and `CASE WHEN`?
2. When would you use `ILIKE` instead of `LIKE`?
3. What does `ARRAY_AGG(DISTINCT event_type)` return?
4. What does `SPLIT_PART('192.168.1.100', '.', 3)` return?
5. How do you filter window function results without a subquery in Snowflake?

---

**Next:** `snowflake/03-semi-structured-data.md`
