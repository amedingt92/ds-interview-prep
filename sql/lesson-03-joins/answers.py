"""SQL Lesson 03 — JOINs — ANSWER KEY"""

sql_1_1 = """
SELECT e.name, e.department, d.division, e.salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
ORDER BY d.division, e.name
"""

sql_1_2 = """
SELECT se.event_id, se.event_type, se.severity, e.name, e.department
FROM security_events se
INNER JOIN employees e ON se.employee_id = e.employee_id
WHERE se.severity IN ('HIGH','CRITICAL')
ORDER BY se.severity, se.event_id
"""

sql_2_1 = """
SELECT e.name, e.department, c.contract_name, ec.role AS contract_role
FROM employees e
LEFT JOIN employee_contracts ec ON e.employee_id = ec.employee_id
LEFT JOIN contracts c           ON ec.contract_id = c.contract_id
ORDER BY e.name
"""

sql_2_2 = """
SELECT e.employee_id, e.name, e.department
FROM employees e
LEFT JOIN employee_contracts ec ON e.employee_id = ec.employee_id
WHERE ec.employee_id IS NULL
ORDER BY e.department, e.name
"""

sql_3_1 = """
SELECT e.name, e.department, c.contract_name, c.value, c.status
FROM employees e
INNER JOIN employee_contracts ec ON e.employee_id = ec.employee_id
INNER JOIN contracts c           ON ec.contract_id = c.contract_id
WHERE c.status = 'Active'
ORDER BY c.value DESC
"""

sql_3_2 = """
SELECT
    d.division,
    COUNT(DISTINCT e.employee_id)                                    AS employee_count,
    ROUND(AVG(e.salary), 0)                                          AS avg_salary,
    COUNT(CASE WHEN se.severity = 'CRITICAL' THEN 1 END)             AS critical_event_count
FROM employees e
INNER JOIN departments d     ON e.department_id  = d.department_id
LEFT JOIN  security_events se ON e.employee_id   = se.employee_id
GROUP BY d.division
ORDER BY critical_event_count DESC
"""

sql_4_1 = """
SELECT c.contract_name, c.status, COUNT(*) AS assigned_count
FROM contracts c
INNER JOIN employee_contracts ec ON c.contract_id = ec.contract_id
GROUP BY c.contract_name, c.status
HAVING COUNT(*) >= 5
ORDER BY assigned_count DESC
"""

sql_4_2 = """
SELECT
    e.name,
    e.department,
    COUNT(se.event_id)                                               AS total_events,
    SUM(CASE WHEN se.severity = 'CRITICAL' THEN 1 ELSE 0 END)       AS critical_events
FROM employees e
INNER JOIN security_events se ON e.employee_id = se.employee_id
GROUP BY e.name, e.department
HAVING SUM(CASE WHEN se.severity = 'CRITICAL' THEN 1 ELSE 0 END) >= 1
ORDER BY critical_events DESC, e.name
"""

sql_challenge = """
SELECT
    e.department,
    d.division,
    COUNT(DISTINCT e.employee_id)                                        AS headcount,
    COUNT(se.event_id)                                                   AS total_events,
    SUM(CASE WHEN se.severity IN ('HIGH','CRITICAL') THEN 1 ELSE 0 END) AS high_critical_events,
    SUM(CASE WHEN se.resolved = 0 THEN 1 ELSE 0 END)                    AS unresolved_events,
    ROUND(AVG(DISTINCT e.salary), 0)                                     AS avg_salary
FROM employees e
INNER JOIN departments d      ON e.department_id  = d.department_id
LEFT JOIN  security_events se ON e.employee_id    = se.employee_id
GROUP BY e.department, d.division
HAVING SUM(CASE WHEN se.severity IN ('HIGH','CRITICAL') THEN 1 ELSE 0 END) >= 1
ORDER BY high_critical_events DESC
"""

"""
KEY THINGS TO REMEMBER:

1. INNER vs LEFT JOIN
   INNER: only matching rows on both sides
   LEFT:  all rows from left table, NULLs on right if no match

2. Anti-join pattern
   LEFT JOIN ... WHERE right_table.key IS NULL
   Finds rows in left table with no match in right table.

3. Filter placement matters with LEFT JOIN
   WHERE right.col = 'X'   → turns it into an INNER JOIN (drops non-matching rows)
   ON ... AND right.col='X' → keeps all left rows, just restricts what joins

4. Multi-table joins
   Chain them: FROM a JOIN b ON ... JOIN c ON ...
   Each JOIN adds columns from the new table.

5. COUNT(DISTINCT) across joins
   When joining 1-to-many, use COUNT(DISTINCT e.employee_id)
   to avoid inflating counts due to duplicate rows.
"""
