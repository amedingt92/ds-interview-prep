"""SQL Lesson 04 — CTEs & Subqueries — ANSWER KEY"""

sql_1_1 = """
SELECT name, department, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC
"""

sql_1_2 = """
SELECT name, department
FROM employees
WHERE department IN (
    SELECT DISTINCT department FROM contracts WHERE status = 'Active'
)
"""

sql_2_1 = """
SELECT department, avg_salary
FROM (
    SELECT department, ROUND(AVG(salary),0) AS avg_salary
    FROM employees
    GROUP BY department
) dept_summary
WHERE avg_salary > 100000
ORDER BY avg_salary DESC
"""

sql_3_1 = """
WITH dept_summary AS (
    SELECT department, ROUND(AVG(salary),0) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT department, avg_salary
FROM dept_summary
WHERE avg_salary > 100000
ORDER BY avg_salary DESC
"""

sql_3_2 = """
WITH ranked AS (
    SELECT
        name,
        department,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
    FROM employees
)
SELECT name, department, salary, dept_rank
FROM ranked
WHERE dept_rank <= 3
ORDER BY department, dept_rank
"""

sql_3_3 = """
WITH active_employees AS (
    SELECT * FROM employees WHERE active = 1
),
dept_summary AS (
    SELECT
        department,
        COUNT(*) AS headcount,
        ROUND(AVG(salary),0) AS avg_salary
    FROM active_employees
    GROUP BY department
)
SELECT department, headcount, avg_salary
FROM dept_summary
WHERE avg_salary > 95000
"""

sql_4_1 = """
SELECT e1.name, e1.department, e1.salary
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e1.department
)
ORDER BY e1.department, e1.salary DESC
"""

sql_challenge = """
WITH high_value_employees AS (
    SELECT *
    FROM employees
    WHERE active = 1
      AND clearance = 'Top Secret'
      AND salary > (SELECT AVG(salary) FROM employees)
),
their_events AS (
    SELECT
        hve.employee_id,
        hve.name,
        hve.department,
        hve.salary,
        COUNT(se.event_id)                                           AS total_events,
        SUM(CASE WHEN se.severity = 'CRITICAL' THEN 1 ELSE 0 END)  AS critical_events
    FROM high_value_employees hve
    INNER JOIN security_events se ON hve.employee_id = se.employee_id
    GROUP BY hve.employee_id, hve.name, hve.department, hve.salary
)
SELECT name, department, salary, total_events, critical_events
FROM their_events
WHERE total_events >= 1
ORDER BY critical_events DESC, total_events DESC
"""
