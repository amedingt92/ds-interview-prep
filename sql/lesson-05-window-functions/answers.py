"""SQL Lesson 05 — Window Functions — ANSWER KEY"""

sql_1_1 = """
SELECT
    name, department, salary,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees
ORDER BY department, dept_rank
"""

sql_1_2 = """
WITH ranked AS (
    SELECT name, department, salary,
           DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
    FROM employees
)
SELECT name, department, salary, dept_rank
FROM ranked
WHERE dept_rank <= 2
"""

sql_1_3 = """
SELECT name, department, salary,
       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees
QUALIFY dept_rank <= 2
"""

sql_2_1 = """
SELECT
    name, department, salary,
    SUM(salary) OVER (PARTITION BY department)             AS dept_total_salary,
    ROUND(AVG(salary) OVER (PARTITION BY department), 0)   AS dept_avg_salary
FROM employees
ORDER BY department, salary DESC
"""

sql_2_2 = """
SELECT
    name, department, salary, hire_date,
    SUM(salary) OVER (PARTITION BY department ORDER BY hire_date) AS running_dept_salary
FROM employees
ORDER BY department, hire_date
"""

sql_3_1 = """
SELECT
    name, department, hire_date, salary,
    LAG(salary, 1, 0) OVER (PARTITION BY department ORDER BY hire_date) AS prev_salary,
    salary - LAG(salary, 1, 0) OVER (PARTITION BY department ORDER BY hire_date) AS salary_diff
FROM employees
ORDER BY department, hire_date
"""

sql_3_2 = """
SELECT * FROM (
    SELECT
        name, department, salary, hire_date,
        LEAD(salary) OVER (PARTITION BY department ORDER BY hire_date) AS next_hire_salary
    FROM employees
) t
WHERE salary < next_hire_salary
  AND next_hire_salary IS NOT NULL
"""

sql_challenge = """
SELECT
    name, department, salary, hire_date,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC)           AS dept_rank,
    ROUND(AVG(salary) OVER (PARTITION BY department), 0)                       AS dept_avg_salary,
    ROUND(salary - AVG(salary) OVER (PARTITION BY department), 0)              AS vs_dept_avg,
    LAG(salary, 1, 0) OVER (PARTITION BY department ORDER BY hire_date)        AS prev_hire_salary
FROM employees
QUALIFY DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) <= 3
ORDER BY department ASC, dept_rank ASC
"""
