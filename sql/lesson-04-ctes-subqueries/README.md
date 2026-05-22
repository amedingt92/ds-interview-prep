# SQL Lesson 04 — CTEs & Subqueries

> **Estimated time:** 40–50 minutes  
> **Run exercises:** `python sql/lesson-04-ctes-subqueries/lesson.py`  
> **Tables used:** all five tables

---

## The Problem CTEs Solve

Complex queries get deeply nested and hard to read fast.  
CTEs (Common Table Expressions) let you name intermediate results and build queries in layers.

```sql
-- Hard to read — nested subquery
SELECT name, dept_avg
FROM (
    SELECT name, AVG(salary) OVER (PARTITION BY department) AS dept_avg
    FROM (
        SELECT * FROM employees WHERE active = 1
    ) active_emps
) t
WHERE dept_avg > 100000;

-- Same thing with CTEs — much cleaner
WITH active_emps AS (
    SELECT * FROM employees WHERE active = 1
),
dept_averages AS (
    SELECT name, department, AVG(salary) OVER (PARTITION BY department) AS dept_avg
    FROM active_emps
)
SELECT name, dept_avg
FROM dept_averages
WHERE dept_avg > 100000;
```

---

## CTE Syntax

```sql
WITH cte_name AS (
    SELECT ...
    FROM ...
    WHERE ...
),
second_cte AS (       -- you can chain as many as you need
    SELECT ...
    FROM cte_name     -- reference earlier CTEs like regular tables
    JOIN ...
)
SELECT *
FROM second_cte;
```

> ⚠️ The final SELECT after the CTEs is required — a CTE alone isn't a complete query.

---

## Subqueries

A subquery is a query nested inside another query.  
They appear in three places:

### 1. In WHERE (most common)
```sql
-- Employees earning more than the company average
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### 2. In FROM (inline view)
```sql
SELECT dept, avg_sal
FROM (
    SELECT department AS dept, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY department
) dept_summary
WHERE avg_sal > 100000;
```

### 3. In SELECT (scalar subquery)
```sql
-- Each employee's salary vs company average
SELECT
    name,
    salary,
    (SELECT AVG(salary) FROM employees) AS company_avg,
    salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

---

## CTEs vs Subqueries — When to Use Each

| | CTE | Subquery |
|--|-----|---------|
| Readability | ✅ Much cleaner for complex logic | ❌ Gets nested and hard to read |
| Reusability | ✅ Can reference the same CTE multiple times | ❌ Must repeat the subquery |
| Performance | Similar in most modern databases | Similar |
| Simple one-off filter | Overkill | ✅ Fine |

**Rule of thumb:** If your subquery is more than 3-4 lines, use a CTE instead.

---

## The "Top N Per Group" Pattern

One of the most common interview patterns — uses a CTE + RANK:

```sql
WITH ranked AS (
    SELECT
        name,
        department,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rnk <= 3;
```

---

## Correlated vs Uncorrelated Subqueries

**Uncorrelated** — the inner query runs once and returns a single value:
```sql
WHERE salary > (SELECT AVG(salary) FROM employees)
--              ^^^^ runs once, returns one number
```

**Correlated** — the inner query references the outer query and runs once per row:
```sql
-- Employees earning more than their own department average
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department = e1.department  -- references outer query's row
)
```

> Correlated subqueries are slower but sometimes necessary. Know the concept — it shows up on tests.

---

## ✅ You're Ready When You Can Answer

- What is the syntax for a CTE? Where does the final SELECT go?
- Can you reference one CTE inside another CTE in the same WITH block?
- What is the difference between a correlated and uncorrelated subquery?
- When would you choose a CTE over a subquery?
- How do you implement "top 3 per group" using a CTE?

---

**Next:** `python sql/lesson-04-ctes-subqueries/lesson.py`
