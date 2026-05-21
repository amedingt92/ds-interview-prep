"""
SQL Lesson 01 — SELECT & Filtering — ANSWER KEY
================================================
⚠️  Attempt every exercise yourself before opening this file.
    The struggle is where the learning happens.
"""

# ── 1.1 ───────────────────────────────────────────────────────────────────────
sql_1_1 = """
SELECT name, department, salary
FROM employees
"""

# ── 1.2 ───────────────────────────────────────────────────────────────────────
sql_1_2 = """
SELECT
    name,
    salary AS annual_salary,
    salary / 12 AS monthly_salary
FROM employees
"""

# ── 1.3 ───────────────────────────────────────────────────────────────────────
sql_1_3 = """
SELECT DISTINCT department
FROM employees
ORDER BY department
"""

# ── 2.1 ───────────────────────────────────────────────────────────────────────
sql_2_1 = """
SELECT name, department, salary
FROM employees
WHERE department = 'Cyber'
"""

# ── 2.2 ───────────────────────────────────────────────────────────────────────
sql_2_2 = """
SELECT name, salary, clearance
FROM employees
WHERE salary > 120000
ORDER BY salary DESC
"""

# ── 2.3 ───────────────────────────────────────────────────────────────────────
sql_2_3 = """
SELECT name, department, active
FROM employees
WHERE active = 0
"""

# ── 2.4 ───────────────────────────────────────────────────────────────────────
sql_2_4 = """
SELECT name, department, salary, hire_date
FROM employees
WHERE department IN ('Engineering', 'Cyber')
  AND salary >= 100000
ORDER BY department ASC, salary DESC
"""

# ── 3.1 ───────────────────────────────────────────────────────────────────────
sql_3_1 = """
SELECT name, clearance
FROM employees
WHERE clearance IN ('Secret', 'Top Secret')
"""

# ── 3.2 ───────────────────────────────────────────────────────────────────────
sql_3_2 = """
SELECT name, salary
FROM employees
WHERE salary BETWEEN 80000 AND 100000
ORDER BY salary ASC
"""

# ── 3.3 ───────────────────────────────────────────────────────────────────────
sql_3_3 = """
SELECT name, role
FROM employees
WHERE role LIKE '%Analyst%'
"""

# ── 3.4 ───────────────────────────────────────────────────────────────────────
sql_3_4 = """
SELECT name, department
FROM employees
WHERE department NOT IN ('Finance', 'Logistics')
"""

# ── 4.1 ───────────────────────────────────────────────────────────────────────
sql_4_1 = """
SELECT event_id, event_type, severity
FROM security_events
WHERE resolved IS NULL
"""

# ── 4.2 ───────────────────────────────────────────────────────────────────────
sql_4_2 = """
SELECT name, department, clearance
FROM employees
WHERE clearance IS NOT NULL
"""

# ── 5.1 ───────────────────────────────────────────────────────────────────────
sql_5_1 = """
SELECT name, department, salary
FROM employees
ORDER BY salary DESC
LIMIT 10
"""

# ── 5.2 ───────────────────────────────────────────────────────────────────────
sql_5_2 = """
SELECT name, department, hire_date
FROM employees
ORDER BY department ASC, hire_date ASC
"""

# ── Challenge ─────────────────────────────────────────────────────────────────
sql_challenge = """
SELECT name, department, role, salary, clearance, hire_date
FROM employees
WHERE department IN ('Cyber', 'Engineering', 'Intelligence')
  AND salary BETWEEN 90000 AND 140000
  AND clearance IN ('Secret', 'Top Secret')
  AND active = 1
  AND (role LIKE '%Analyst%' OR role LIKE '%Engineer%')
ORDER BY department ASC, salary DESC
LIMIT 15
"""

# ── Key things to remember ────────────────────────────────────────────────────
"""
COMMON MISTAKES:

1. NULL comparison
   WRONG:   WHERE clearance = NULL
   CORRECT: WHERE clearance IS NULL
   Why: NULL is the absence of a value. It doesn't equal anything, including itself.

2. AND vs OR precedence
   AND evaluates before OR — use parentheses when mixing them.
   WHERE dept = 'Cyber' OR dept = 'Engineering' AND salary > 100000
   reads as:
   WHERE dept = 'Cyber' OR (dept = 'Engineering' AND salary > 100000)

3. BETWEEN is inclusive
   BETWEEN 80000 AND 100000 includes both 80000 and 100000.

4. LIKE wildcards
   %  = any number of characters (including zero)
   _  = exactly one character
   '%Analyst%' matches 'Analyst I', 'Senior Analyst', 'Threat Analyst'

5. SELECT * in production
   Fine for exploration. On the test, use specific columns when asked —
   it shows you read the question carefully.
"""
