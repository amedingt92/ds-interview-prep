"""SQL Lesson 06 — Advanced SQL — ANSWER KEY"""

sql_1_1 = """
SELECT name, department, salary,
    CASE
        WHEN salary >= 130000 THEN 'Senior'
        WHEN salary >= 100000 THEN 'Mid'
        ELSE 'Junior'
    END AS salary_band
FROM employees
ORDER BY salary DESC
"""

sql_1_2 = """
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN salary >= 130000 THEN 1 ELSE 0 END) AS senior_count,
    SUM(CASE WHEN salary >= 100000 AND salary < 130000 THEN 1 ELSE 0 END) AS mid_count,
    SUM(CASE WHEN salary < 100000 THEN 1 ELSE 0 END) AS junior_count
FROM employees
GROUP BY department
ORDER BY total_employees DESC
"""

sql_2_1 = """
SELECT name, hire_date,
       DATEDIFF('day', hire_date, CURRENT_DATE) AS days_employed
FROM employees
ORDER BY days_employed DESC
LIMIT 10
"""

sql_2_2 = """
SELECT
    DATE_TRUNC('year', hire_date::DATE) AS hire_year,
    COUNT(*) AS hires
FROM employees
GROUP BY DATE_TRUNC('year', hire_date::DATE)
ORDER BY hire_year ASC
"""

sql_3_1 = """
SELECT
    name,
    department,
    UPPER(name) || ' — ' || department AS display_label
FROM employees
"""

sql_3_2 = """
SELECT DISTINCT
    event_type,
    SPLIT_PART(source_ip, '.', 1) || '.' || SPLIT_PART(source_ip, '.', 2) AS ip_prefix
FROM security_events
ORDER BY event_type, ip_prefix
"""

sql_challenge = """
WITH employee_base AS (
    SELECT
        e.employee_id, e.name, e.department, e.salary, e.clearance, e.hire_date,
        d.division,
        CASE
            WHEN e.salary >= 130000 THEN 'Senior'
            WHEN e.salary >= 100000 THEN 'Mid'
            ELSE 'Junior'
        END AS salary_band,
        DATEDIFF('day', e.hire_date, CURRENT_DATE) AS days_employed
    FROM employees e
    INNER JOIN departments d ON e.department_id = d.department_id
    WHERE e.active = 1
      AND e.clearance IN ('Secret', 'Top Secret')
),
event_summary AS (
    SELECT
        employee_id,
        COUNT(*)                                                    AS total_events,
        SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END)    AS critical_events,
        SUM(CASE WHEN resolved = 0 THEN 1 ELSE 0 END)             AS unresolved_events
    FROM security_events
    GROUP BY employee_id
)
SELECT
    eb.name, eb.department, eb.division, eb.salary, eb.salary_band,
    eb.days_employed, es.total_events, es.critical_events, es.unresolved_events
FROM employee_base eb
INNER JOIN event_summary es ON eb.employee_id = es.employee_id
WHERE es.total_events >= 1
ORDER BY es.critical_events DESC, eb.salary DESC
"""
