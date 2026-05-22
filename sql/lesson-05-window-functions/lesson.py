"""
SQL Lesson 05 — Window Functions
===================================
Read README.md first, then work through each exercise.
Run: python sql/lesson-05-window-functions/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import duckdb

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
con = duckdb.connect()
con.execute(f"CREATE TABLE employees       AS SELECT * FROM read_csv_auto('{DATA}/employees.csv')")
con.execute(f"CREATE TABLE security_events AS SELECT * FROM read_csv_auto('{DATA}/security_events.csv')")
con.execute(f"CREATE TABLE contracts       AS SELECT * FROM read_csv_auto('{DATA}/contracts.csv')")

def q(sql):
    sql = sql.strip()
    if not sql or sql.startswith("--"): return None
    return con.execute(sql).df()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — RANK / DENSE_RANK / ROW_NUMBER
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: RANK / DENSE_RANK / ROW_NUMBER ───────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Add a dept_rank column to every employee using DENSE_RANK,
# ranked by salary descending within their department.
# Columns: name, department, salary, dept_rank
# Sort by department, dept_rank.

sql_1_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Return only the top 2 employees per department by salary.
# Use a CTE + WHERE (no QUALIFY yet — practice the subquery pattern).
# Columns: name, department, salary, dept_rank

sql_1_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Same as 1.2 but rewrite using QUALIFY instead of a subquery.

sql_1_3 = """
-- YOUR QUERY HERE (use QUALIFY)
"""

try:
    df = q(sql_1_1)
    check_df(df, {"columns": ["name","department","salary","dept_rank"], "rows": 74}, "1.1 — all 74 rows with dept_rank")
    if df is not None:
        check(df["dept_rank"].min(), 1, "1.1 — minimum rank = 1")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    df = q(sql_1_2)
    check_df(df, {"columns": ["name","department","salary","dept_rank"]}, "1.2 — correct columns")
    if df is not None:
        check(df["dept_rank"].max() <= 2, True, "1.2 — max rank <= 2 (top 2 only)",
              hint="WHERE dept_rank <= 2 in outer query")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")

try:
    df = q(sql_1_3)
    check_df(df, {"columns": ["name","department","salary","dept_rank"]}, "1.3 — QUALIFY version correct columns")
    if df is not None:
        check(df["dept_rank"].max() <= 2, True, "1.3 — QUALIFY top 2 — max rank <= 2")
except Exception as e: print(f"  ❌  1.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — SUM/AVG OVER (running totals and partition aggregates)
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: SUM / AVG OVER ───────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# For each employee return:
#   name, department, salary, dept_total_salary, dept_avg_salary
# dept_total and dept_avg should be the same for all employees in the same dept.
# Sort by department, salary desc.

sql_2_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# For each employee return a running total of salary within their department,
# ordered by hire_date ascending.
# Columns: name, department, salary, hire_date, running_dept_salary

sql_2_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_2_1)
    check_df(df, {"columns": ["name","department","salary","dept_total_salary","dept_avg_salary"], "rows": 74}, "2.1 — all rows, correct columns")
    if df is not None:
        cyber = df[df["department"]=="Cyber"]["dept_total_salary"].unique()
        check(len(cyber), 1, "2.1 — all Cyber rows share same dept_total_salary",
              hint="SUM(salary) OVER (PARTITION BY department) — no ORDER BY")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    df = q(sql_2_2)
    check_df(df, {"columns": ["name","department","salary","hire_date","running_dept_salary"]}, "2.2 — correct columns")
    if df is not None:
        # First hire per dept: running total should equal their own salary
        first = df.sort_values("hire_date").groupby("department").first().reset_index()
        check((first["running_dept_salary"] == first["salary"]).all(), True,
              "2.2 — first hire's running total = their own salary",
              hint="SUM(salary) OVER (PARTITION BY department ORDER BY hire_date)")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — LAG and LEAD
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: LAG and LEAD ─────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Within each department ordered by hire_date, show each employee's salary
# and the salary of the person hired just before them (default 0).
# Columns: name, department, hire_date, salary, prev_salary, salary_diff

sql_3_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Find employees whose salary is LOWER than the next person hired in their dept.
# (They earn less than whoever came after them.)
# Columns: name, department, salary, hire_date, next_hire_salary
# Use LEAD. Exclude rows where next_hire_salary is NULL (last hire in dept).

sql_3_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_3_1)
    check_df(df, {"columns": ["name","department","hire_date","salary","prev_salary","salary_diff"]}, "3.1 — correct columns")
    if df is not None:
        first = df.sort_values("hire_date").groupby("department").first()
        check((first["prev_salary"] == 0).all(), True, "3.1 — first hire prev_salary = 0")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    df = q(sql_3_2)
    check_df(df, {"columns": ["name","department","salary","hire_date","next_hire_salary"]}, "3.2 — correct columns")
    if df is not None and len(df) > 0:
        check((df["salary"] < df["next_hire_salary"]).all(), True,
              "3.2 — salary < next_hire_salary for all rows")
        check(df["next_hire_salary"].isna().sum(), 0, "3.2 — no NULL next_hire_salary rows")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Build a complete salary analysis query.
# For each employee return:
#   name, department, salary, hire_date
#   dept_rank        — DENSE_RANK by salary desc within dept
#   dept_avg_salary  — avg salary for their department (rounded to 0)
#   vs_dept_avg      — salary minus dept avg (rounded to 0)
#   prev_hire_salary — salary of person hired just before them in dept (default 0)
#
# Filter to only top 3 per department (QUALIFY or subquery).
# Sort by department ASC, dept_rank ASC.
#
# Spiral: window functions (this lesson) + CTEs (Lesson 04)

sql_challenge = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_challenge)
    check_df(df, {
        "columns": ["name","department","salary","hire_date","dept_rank","dept_avg_salary","vs_dept_avg","prev_hire_salary"],
        "min_rows": 6,
    }, "Challenge — correct columns, at least 6 rows")
    if df is not None and len(df) > 0:
        check(df["dept_rank"].max(), 3, "Challenge — max dept_rank = 3")
        check(df["department"].is_monotonic_increasing, True, "Challenge — sorted by department")
        print()
        print(df.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
