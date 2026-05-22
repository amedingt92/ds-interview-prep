"""
SQL Lesson 04 — CTEs & Subqueries
====================================
Read README.md first, then work through each exercise.
Run: python sql/lesson-04-ctes-subqueries/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import duckdb

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
con = duckdb.connect()
con.execute(f"CREATE TABLE employees          AS SELECT * FROM read_csv_auto('{DATA}/employees.csv')")
con.execute(f"CREATE TABLE departments        AS SELECT * FROM read_csv_auto('{DATA}/departments.csv')")
con.execute(f"CREATE TABLE contracts          AS SELECT * FROM read_csv_auto('{DATA}/contracts.csv')")
con.execute(f"CREATE TABLE employee_contracts AS SELECT * FROM read_csv_auto('{DATA}/employee_contracts.csv')")
con.execute(f"CREATE TABLE security_events    AS SELECT * FROM read_csv_auto('{DATA}/security_events.csv')")

def q(sql):
    sql = sql.strip()
    if not sql or sql.startswith("--"): return None
    return con.execute(sql).df()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Subqueries in WHERE
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Subqueries in WHERE ──────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Return name, department, salary for employees earning above the company average.
# Columns: name, department, salary
# Sort by salary descending.

sql_1_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Return name, department for employees in departments that have
# at least one Active contract.
# Use a subquery with IN.

sql_1_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_1_1)
    check_df(df, {"columns": ["name","department","salary"]}, "1.1 — correct columns")
    if df is not None:
        avg = q("SELECT AVG(salary) FROM employees").iloc[0,0]
        check((df["salary"] > avg).all(), True, "1.1 — all salaries above company average")
        check(df["salary"].is_monotonic_decreasing, True, "1.1 — sorted DESC")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    df = q(sql_1_2)
    check_df(df, {"columns": ["name","department"]}, "1.2 — correct columns")
    if df is not None:
        active_depts = set(q("SELECT DISTINCT department FROM contracts WHERE status='Active'")["department"].tolist())
        check(set(df["department"].unique()).issubset(active_depts), True,
              "1.2 — only employees in departments with Active contracts")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Subqueries in FROM
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: Subqueries in FROM ───────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Using a subquery in FROM, find departments where the average salary
# is above 100000.
# Columns: department, avg_salary
# Sort by avg_salary descending.

sql_2_1 = """
-- YOUR QUERY HERE
-- Hint: compute avg per department in a subquery, then filter in outer query
"""

try:
    df = q(sql_2_1)
    check_df(df, {"columns": ["department","avg_salary"]}, "2.1 — correct columns")
    if df is not None:
        check((df["avg_salary"] > 100000).all(), True, "2.1 — all avg_salary > 100000")
        check(df["avg_salary"].is_monotonic_decreasing, True, "2.1 — sorted DESC")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — CTEs
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: CTEs ─────────────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Rewrite Exercise 2.1 using a CTE instead of a subquery in FROM.
# Same result, cleaner structure.

sql_3_1 = """
-- YOUR QUERY HERE (use WITH ... AS (...))
"""

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Using a CTE, find the top 3 highest-paid employees per department.
# Columns: name, department, salary, dept_rank
# Sort by department, dept_rank.

sql_3_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Using TWO chained CTEs:
# CTE 1 — active_employees: filter employees where active = 1
# CTE 2 — dept_summary: from active_employees, compute per-department
#          headcount and avg_salary
# Final SELECT: return departments where avg_salary > 95000
# Columns: department, headcount, avg_salary

sql_3_3 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_3_1)
    check_df(df, {"columns": ["department","avg_salary"]}, "3.1 — correct columns (CTE version)")
    if df is not None:
        check((df["avg_salary"] > 100000).all(), True, "3.1 — all avg_salary > 100000")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    df = q(sql_3_2)
    check_df(df, {"columns": ["name","department","salary","dept_rank"]}, "3.2 — correct columns")
    if df is not None:
        check(df["dept_rank"].max(), 3, "3.2 — max rank = 3",
              hint="Use DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC)")
        check(df["department"].is_monotonic_increasing, True, "3.2 — sorted by department")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")

try:
    df = q(sql_3_3)
    check_df(df, {"columns": ["department","headcount","avg_salary"]}, "3.3 — correct columns")
    if df is not None:
        check((df["avg_salary"] > 95000).all(), True, "3.3 — avg_salary > 95000")
except Exception as e: print(f"  ❌  3.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Correlated Subquery
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: Correlated Subquery ──────────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Find employees who earn MORE than the average salary of their own department.
# (Each row compares against its own department's average — correlated subquery)
# Columns: name, department, salary
# Sort by department, salary descending.

sql_4_1 = """
-- YOUR QUERY HERE
-- Hint: in the subquery, reference the outer query's department:
-- WHERE e2.department = e1.department
"""

try:
    df = q(sql_4_1)
    check_df(df, {"columns": ["name","department","salary"]}, "4.1 — correct columns")
    if df is not None:
        check(len(df) > 0, True, "4.1 — returned some rows")
        # Spot-check: verify one employee is truly above their dept avg
        dept_avgs = q("SELECT department, AVG(salary) AS avg_sal FROM employees GROUP BY department")
        dept_avg_map = dict(zip(dept_avgs["department"], dept_avgs["avg_sal"]))
        all_above = all(row["salary"] > dept_avg_map[row["department"]] for _, row in df.iterrows())
        check(all_above, True, "4.1 — all employees earn above their dept average")
except Exception as e: print(f"  ❌  4.1 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Using CTEs, build a high-value employee threat report.
#
# CTE 1 — high_value_employees:
#   Active employees with Top Secret clearance AND salary above company average
#
# CTE 2 — their_events:
#   Security events for those employees, with event count and critical count per employee
#
# Final SELECT:
#   name, department, salary, total_events, critical_events
#   Only include employees who have at least 1 security event.
#   Sort by critical_events DESC, total_events DESC.
#
# Spiral: CTEs (this lesson) + JOIN + aggregation + WHERE subquery

sql_challenge = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_challenge)
    check_df(df, {
        "columns": ["name","department","salary","total_events","critical_events"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if df is not None and len(df) > 0:
        check(df["critical_events"].is_monotonic_decreasing, True, "Challenge — sorted by critical_events DESC")
        check((df["total_events"] >= 1).all(), True, "Challenge — all have at least 1 event")
        print()
        print(df.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
