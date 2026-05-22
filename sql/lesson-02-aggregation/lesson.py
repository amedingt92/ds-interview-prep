"""
SQL Lesson 02 — Aggregation
=============================
Read README.md first, then work through each exercise.
Run: python sql/lesson-02-aggregation/lesson.py
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

print("\n── Dataset sizes ───────────────────────────────────────────────────────")
print(f"  employees:       {q('SELECT COUNT(*) AS n FROM employees').iloc[0,0]} rows")
print(f"  security_events: {q('SELECT COUNT(*) AS n FROM security_events').iloc[0,0]} rows")
print(f"  contracts:       {q('SELECT COUNT(*) AS n FROM contracts').iloc[0,0]} rows")
print("────────────────────────────────────────────────────────────────────────\n")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Basic Aggregate Functions
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Aggregate Functions ─────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Return a single row with these columns from employees:
#   total_employees, avg_salary, min_salary, max_salary, total_payroll
# Round avg_salary to 2 decimal places.

sql_1_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Count how many employees have each clearance level.
# Columns: clearance, employee_count
# Sort by employee_count descending.

sql_1_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# How many DISTINCT event types exist in security_events?
# Return a single value in a column called unique_event_types.

sql_1_3 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_1_1)
    check_df(df, {"rows": 1, "columns": ["total_employees","avg_salary","min_salary","max_salary","total_payroll"]}, "1.1 — single summary row")
    if df is not None:
        check(int(df["total_employees"].iloc[0]), 74, "1.1 — total_employees = 74")
        check(df["max_salary"].iloc[0] >= df["min_salary"].iloc[0], True, "1.1 — max >= min")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    df = q(sql_1_2)
    check_df(df, {"columns": ["clearance","employee_count"]}, "1.2 — correct columns")
    if df is not None:
        check(df["employee_count"].is_monotonic_decreasing, True, "1.2 — sorted by count DESC")
        check(int(df["employee_count"].sum()), 74, "1.2 — counts sum to 74")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")

try:
    df = q(sql_1_3)
    check_df(df, {"rows": 1, "columns": ["unique_event_types"]}, "1.3 — single row, correct column")
    if df is not None:
        check(int(df["unique_event_types"].iloc[0]), 10, "1.3 — 10 unique event types",
              hint="SELECT COUNT(DISTINCT event_type) AS unique_event_types FROM security_events")
except Exception as e: print(f"  ❌  1.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — GROUP BY
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: GROUP BY ─────────────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# For each department, return:
#   department, headcount, avg_salary, min_salary, max_salary
# Round avg_salary to 0 decimal places.
# Sort by avg_salary descending.

sql_2_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Count security events by severity level.
# Columns: severity, event_count
# Sort by event_count descending.

sql_2_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.3 ──────────────────────────────────────────────────────────────
# For each department, count how many employees have Top Secret clearance.
# Columns: department, top_secret_count
# Sort by top_secret_count descending.

sql_2_3 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_2_1)
    check_df(df, {"rows": 6, "columns": ["department","headcount","avg_salary","min_salary","max_salary"]}, "2.1 — 6 departments, correct columns")
    if df is not None:
        check(int(df["headcount"].sum()), 74, "2.1 — headcounts sum to 74")
        check(df["avg_salary"].is_monotonic_decreasing, True, "2.1 — sorted by avg_salary DESC")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    df = q(sql_2_2)
    check_df(df, {"columns": ["severity","event_count"]}, "2.2 — correct columns")
    if df is not None:
        check(int(df["event_count"].sum()), 500, "2.2 — total events = 500")
        check(df["event_count"].is_monotonic_decreasing, True, "2.2 — sorted DESC")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")

try:
    df = q(sql_2_3)
    check_df(df, {"rows": 6, "columns": ["department","top_secret_count"]}, "2.3 — 6 departments")
    if df is not None:
        check(df["top_secret_count"].is_monotonic_decreasing, True, "2.3 — sorted DESC")
except Exception as e: print(f"  ❌  2.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — HAVING
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: HAVING ───────────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Return departments where the average salary is greater than 100000.
# Columns: department, avg_salary
# Sort by avg_salary descending.

sql_3_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Return event types that have appeared more than 60 times in security_events.
# Columns: event_type, event_count
# Sort by event_count descending.

sql_3_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# WHERE + GROUP BY + HAVING together:
# Among ACTIVE employees only (active = 1),
# return departments that have more than 8 active employees
# AND an average salary above 95000.
# Columns: department, active_count, avg_salary
# Sort by active_count descending.

sql_3_3 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_3_1)
    check_df(df, {"columns": ["department","avg_salary"]}, "3.1 — correct columns")
    if df is not None:
        check((df["avg_salary"] > 100000).all(), True, "3.1 — all avg_salary > 100000",
              hint="HAVING AVG(salary) > 100000")
        check(df["avg_salary"].is_monotonic_decreasing, True, "3.1 — sorted DESC")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    df = q(sql_3_2)
    check_df(df, {"columns": ["event_type","event_count"]}, "3.2 — correct columns")
    if df is not None:
        check((df["event_count"] > 60).all(), True, "3.2 — all counts > 60",
              hint="HAVING COUNT(*) > 60")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")

try:
    df = q(sql_3_3)
    check_df(df, {"columns": ["department","active_count","avg_salary"]}, "3.3 — correct columns")
    if df is not None:
        check((df["active_count"] > 8).all(), True, "3.3 — active_count > 8")
        check((df["avg_salary"] > 95000).all(), True, "3.3 — avg_salary > 95000")
except Exception as e: print(f"  ❌  3.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — COUNT(*) vs COUNT(col) and NULLs
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: COUNT(*) vs COUNT(col) ───────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Return a single row showing:
#   total_events   — total rows in security_events
#   resolved_count — count of events where resolved is NOT NULL
#   unresolved     — count where resolved IS NULL
# Hint: COUNT(col) ignores NULLs. COUNT(*) does not.

sql_4_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# Per department, show:
#   department, total_employees, employees_with_clearance
# where employees_with_clearance counts only non-NULL clearance values.
# Sort by department.

sql_4_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_4_1)
    check_df(df, {"rows": 1, "columns": ["total_events","resolved_count","unresolved"]}, "4.1 — correct columns")
    if df is not None:
        check(int(df["total_events"].iloc[0]), 500, "4.1 — total_events = 500")
        total = int(df["resolved_count"].iloc[0]) + int(df["unresolved"].iloc[0])
        check(total, 500, "4.1 — resolved_count + unresolved = 500")
except Exception as e: print(f"  ❌  4.1 — Error: {e}")

try:
    df = q(sql_4_2)
    check_df(df, {"rows": 6, "columns": ["department","total_employees","employees_with_clearance"]}, "4.2 — 6 rows, correct columns")
    if df is not None:
        check((df["employees_with_clearance"] <= df["total_employees"]).all(), True,
              "4.2 — employees_with_clearance <= total_employees")
except Exception as e: print(f"  ❌  4.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Build a security event summary by severity.
# For each severity level return:
#   severity, event_count, unique_employees, unique_event_types, resolved_count
#
# Filters:
#   - Only include severities with more than 50 events
#   - Only count resolved events where resolved = 1
#
# Sort by event_count descending.
#
# Spiral callback: this uses GROUP BY, HAVING, COUNT(DISTINCT), and
# conditional counting — all from this lesson.

sql_challenge = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_challenge)
    check_df(df, {
        "columns": ["severity","event_count","unique_employees","unique_event_types","resolved_count"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if df is not None and len(df) > 0:
        check((df["event_count"] > 50).all(), True, "Challenge — all event_count > 50")
        check(df["event_count"].is_monotonic_decreasing, True, "Challenge — sorted DESC")
        check((df["resolved_count"] <= df["event_count"]).all(), True,
              "Challenge — resolved_count <= event_count")
        print()
        print(df.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
