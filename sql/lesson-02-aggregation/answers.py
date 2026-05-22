"""
SQL Lesson 02 — Aggregation — ANSWER KEY
=========================================
⚠️  Attempt every exercise yourself first.
"""

sql_1_1 = """
SELECT
    COUNT(*)             AS total_employees,
    ROUND(AVG(salary),2) AS avg_salary,
    MIN(salary)          AS min_salary,
    MAX(salary)          AS max_salary,
    SUM(salary)          AS total_payroll
FROM employees
"""

sql_1_2 = """
SELECT
    clearance,
    COUNT(*) AS employee_count
FROM employees
GROUP BY clearance
ORDER BY employee_count DESC
"""

sql_1_3 = """
SELECT COUNT(DISTINCT event_type) AS unique_event_types
FROM security_events
"""

sql_2_1 = """
SELECT
    department,
    COUNT(*)             AS headcount,
    ROUND(AVG(salary),0) AS avg_salary,
    MIN(salary)          AS min_salary,
    MAX(salary)          AS max_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC
"""

sql_2_2 = """
SELECT
    severity,
    COUNT(*) AS event_count
FROM security_events
GROUP BY severity
ORDER BY event_count DESC
"""

sql_2_3 = """
SELECT
    department,
    COUNT(*) AS top_secret_count
FROM employees
WHERE clearance = 'Top Secret'
GROUP BY department
ORDER BY top_secret_count DESC
"""

sql_3_1 = """
SELECT
    department,
    ROUND(AVG(salary),0) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 100000
ORDER BY avg_salary DESC
"""

sql_3_2 = """
SELECT
    event_type,
    COUNT(*) AS event_count
FROM security_events
GROUP BY event_type
HAVING COUNT(*) > 60
ORDER BY event_count DESC
"""

sql_3_3 = """
SELECT
    department,
    COUNT(*)             AS active_count,
    ROUND(AVG(salary),0) AS avg_salary
FROM employees
WHERE active = 1
GROUP BY department
HAVING COUNT(*) > 8
   AND AVG(salary) > 95000
ORDER BY active_count DESC
"""

sql_4_1 = """
SELECT
    COUNT(*)          AS total_events,
    COUNT(resolved)   AS resolved_count,
    COUNT(*) - COUNT(resolved) AS unresolved
FROM security_events
"""

sql_4_2 = """
SELECT
    department,
    COUNT(*)          AS total_employees,
    COUNT(clearance)  AS employees_with_clearance
FROM employees
GROUP BY department
ORDER BY department
"""

sql_challenge = """
SELECT
    severity,
    COUNT(*)                    AS event_count,
    COUNT(DISTINCT employee_id) AS unique_employees,
    COUNT(DISTINCT event_type)  AS unique_event_types,
    SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) AS resolved_count
FROM security_events
GROUP BY severity
HAVING COUNT(*) > 50
ORDER BY event_count DESC
"""

"""
KEY THINGS TO REMEMBER:

1. WHERE vs HAVING
   WHERE  → filters rows BEFORE grouping   (can't use aggregate functions)
   HAVING → filters groups AFTER grouping  (can use aggregate functions)

2. COUNT(*) vs COUNT(col)
   COUNT(*)   → counts every row, including NULLs
   COUNT(col) → counts only non-NULL values in that column

3. GROUP BY rule
   Every SELECT column must either be in GROUP BY or wrapped in an aggregate.

4. NULLs in aggregates
   SUM, AVG, MIN, MAX, COUNT(col) all ignore NULL values automatically.

5. Conditional counting
   SUM(CASE WHEN condition THEN 1 ELSE 0 END)
   This pattern counts rows matching a condition — very common on tests.
"""
