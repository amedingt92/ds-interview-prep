"""
SQL Lesson 01 — SELECT & Filtering
====================================
Read README.md first, then work through each exercise below.

HOW TO USE:
  1. Read the comment above each exercise carefully
  2. Replace  sql = \"\"\" ... \"\"\"  with your own query
  3. Run: python lesson.py
  4. Fix any ❌ before moving to the next section
  5. If stuck, check answers.py — but try first

RUNNING:
  python sql/lesson-01-select-filtering/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary

import duckdb

# ── Load data ─────────────────────────────────────────────────────────────────
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")

con = duckdb.connect()
con.execute(f"CREATE TABLE employees   AS SELECT * FROM read_csv_auto('{DATA}/employees.csv')")
con.execute(f"CREATE TABLE departments AS SELECT * FROM read_csv_auto('{DATA}/departments.csv')")
con.execute(f"CREATE TABLE contracts   AS SELECT * FROM read_csv_auto('{DATA}/contracts.csv')")
con.execute(f"CREATE TABLE security_events AS SELECT * FROM read_csv_auto('{DATA}/security_events.csv')")

def q(sql):
    """Run SQL, return a pandas DataFrame. Returns None on empty/missing query."""
    sql = sql.strip()
    if not sql or sql.startswith("--"):
        return None
    return con.execute(sql).df()

# Quick peek at the data
print("\n── employees (first 5 rows) ────────────────────────────────────────────")
print(q("SELECT * FROM employees LIMIT 5").to_string(index=False))
print(f"\n── Total employees: {q('SELECT COUNT(*) AS n FROM employees').iloc[0,0]}")
print("────────────────────────────────────────────────────────────────────────\n")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Basic SELECT
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Basic SELECT ─────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Select only the name, department, and salary columns from employees.
# Return all rows.

sql_1_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Select name and salary, but rename salary to annual_salary.
# Also add a new column called monthly_salary that is salary divided by 12.
# Return all rows.

sql_1_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Return a list of all UNIQUE department names from the employees table.
# Sort them alphabetically.

sql_1_3 = """
-- YOUR QUERY HERE
"""

# ── Checks ────────────────────────────────────────────────────────────────────
try:
    df = q(sql_1_1)
    check_df(df, {"columns": ["name", "department", "salary"], "rows": 74},
             "1.1 — name, department, salary — all 74 rows")
except Exception as e:
    print(f"  ❌  1.1 — Error: {e}")

try:
    df = q(sql_1_2)
    check_df(df, {"columns": ["name", "annual_salary", "monthly_salary"]},
             "1.2 — annual_salary and monthly_salary columns present")
    if df is not None and "annual_salary" in df.columns and "monthly_salary" in df.columns:
        ratio = round(df["annual_salary"].iloc[0] / df["monthly_salary"].iloc[0])
        check(ratio, 12, "1.2 — monthly_salary = annual_salary / 12",
              hint="Use: salary / 12 AS monthly_salary")
except Exception as e:
    print(f"  ❌  1.2 — Error: {e}")

try:
    df = q(sql_1_3)
    check_df(df, {"columns": ["department"]}, "1.3 — single column: department")
    if df is not None:
        check(len(df), 6, "1.3 — exactly 6 unique departments",
              hint="Use SELECT DISTINCT department FROM employees")
        check(list(df["department"]), sorted(list(df["department"])),
              "1.3 — sorted alphabetically",
              hint="Add ORDER BY department")
except Exception as e:
    print(f"  ❌  1.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — WHERE Filtering
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: WHERE Filtering ──────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Return name, department, salary for all Cyber department employees.

sql_2_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Return name, salary, clearance for employees earning MORE than 120000.
# Sort by salary descending.

sql_2_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.3 ──────────────────────────────────────────────────────────────
# Return name, department, active for employees who are NOT active.
# (active = 0 means inactive)

sql_2_3 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.4 ──────────────────────────────────────────────────────────────
# Return name, department, salary, hire_date for employees who:
#   - work in Engineering OR Cyber
#   - AND have a salary >= 100000
# Sort by department, then salary descending.

sql_2_4 = """
-- YOUR QUERY HERE
"""

# ── Checks ────────────────────────────────────────────────────────────────────
try:
    df = q(sql_2_1)
    check_df(df, {"columns": ["name", "department", "salary"]}, "2.1 — correct columns")
    if df is not None:
        check(df["department"].unique().tolist(), ["Cyber"],
              "2.1 — only Cyber rows returned",
              hint="WHERE department = 'Cyber'")
except Exception as e:
    print(f"  ❌  2.1 — Error: {e}")

try:
    df = q(sql_2_2)
    check_df(df, {"columns": ["name", "salary", "clearance"]}, "2.2 — correct columns")
    if df is not None:
        check((df["salary"] > 120000).all(), True,
              "2.2 — all salaries > 120000",
              hint="WHERE salary > 120000")
        check(df["salary"].is_monotonic_decreasing, True,
              "2.2 — sorted by salary DESC",
              hint="ORDER BY salary DESC")
except Exception as e:
    print(f"  ❌  2.2 — Error: {e}")

try:
    df = q(sql_2_3)
    check_df(df, {"columns": ["name", "department", "active"]}, "2.3 — correct columns")
    if df is not None:
        check((df["active"] == 0).all(), True,
              "2.3 — all rows are inactive (active = 0)",
              hint="WHERE active = 0  or  WHERE NOT active = 1")
except Exception as e:
    print(f"  ❌  2.3 — Error: {e}")

try:
    df = q(sql_2_4)
    check_df(df, {"columns": ["name", "department", "salary", "hire_date"]}, "2.4 — correct columns")
    if df is not None:
        valid_depts = set(df["department"].unique())
        check(valid_depts.issubset({"Engineering", "Cyber"}), True,
              "2.4 — only Engineering and Cyber rows",
              hint="WHERE department IN ('Engineering', 'Cyber')")
        check((df["salary"] >= 100000).all(), True,
              "2.4 — all salaries >= 100000",
              hint="AND salary >= 100000")
except Exception as e:
    print(f"  ❌  2.4 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — IN, BETWEEN, LIKE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: IN, BETWEEN, LIKE ────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Return name and clearance for employees with Secret OR Top Secret clearance.
# Use IN (not OR).

sql_3_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Return name, salary for employees with salary BETWEEN 80000 and 100000 (inclusive).
# Sort by salary ascending.

sql_3_2 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Return name, role for employees whose role contains the word 'Analyst'.
# Use LIKE.

sql_3_3 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.4 ──────────────────────────────────────────────────────────────
# Return name, department for employees NOT in Finance or Logistics.
# Use NOT IN.

sql_3_4 = """
-- YOUR QUERY HERE
"""

# ── Checks ────────────────────────────────────────────────────────────────────
try:
    df = q(sql_3_1)
    check_df(df, {"columns": ["name", "clearance"]}, "3.1 — correct columns")
    if df is not None:
        valid = set(df["clearance"].unique())
        check(valid.issubset({"Secret", "Top Secret"}), True,
              "3.1 — only Secret and Top Secret rows",
              hint="WHERE clearance IN ('Secret', 'Top Secret')")
except Exception as e:
    print(f"  ❌  3.1 — Error: {e}")

try:
    df = q(sql_3_2)
    check_df(df, {"columns": ["name", "salary"]}, "3.2 — correct columns")
    if df is not None:
        check((df["salary"] >= 80000).all() and (df["salary"] <= 100000).all(), True,
              "3.2 — all salaries between 80000 and 100000 inclusive",
              hint="WHERE salary BETWEEN 80000 AND 100000")
        check(df["salary"].is_monotonic_increasing, True,
              "3.2 — sorted by salary ASC")
except Exception as e:
    print(f"  ❌  3.2 — Error: {e}")

try:
    df = q(sql_3_3)
    check_df(df, {"columns": ["name", "role"]}, "3.3 — correct columns")
    if df is not None:
        check(df["role"].str.contains("Analyst").all(), True,
              "3.3 — all roles contain 'Analyst'",
              hint="WHERE role LIKE '%Analyst%'")
except Exception as e:
    print(f"  ❌  3.3 — Error: {e}")

try:
    df = q(sql_3_4)
    check_df(df, {"columns": ["name", "department"]}, "3.4 — correct columns")
    if df is not None:
        excluded = {"Finance", "Logistics"}
        check(len(set(df["department"].unique()) & excluded), 0,
              "3.4 — Finance and Logistics not in results",
              hint="WHERE department NOT IN ('Finance', 'Logistics')")
except Exception as e:
    print(f"  ❌  3.4 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — NULL Handling
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: NULL Handling ────────────────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# The security_events table has a 'resolved' column.
# Return event_id, event_type, severity for events where resolved IS NULL.
# (There may be none — that's fine. The syntax is what matters here.)

sql_4_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# Return name, department, clearance for employees where clearance IS NOT NULL.
# How many rows do you get?

sql_4_2 = """
-- YOUR QUERY HERE
"""

# ── Checks ────────────────────────────────────────────────────────────────────
try:
    df = q(sql_4_1)
    check_df(df, {"columns": ["event_id", "event_type", "severity"]},
             "4.1 — correct columns (IS NULL syntax)",
             hint="WHERE resolved IS NULL   (never use = NULL)")
except Exception as e:
    print(f"  ❌  4.1 — Error: {e}")

try:
    df = q(sql_4_2)
    check_df(df, {"columns": ["name", "department", "clearance"]}, "4.2 — correct columns")
    if df is not None:
        check(df["clearance"].isna().sum(), 0,
              "4.2 — no NULL values in clearance column",
              hint="WHERE clearance IS NOT NULL")
except Exception as e:
    print(f"  ❌  4.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — ORDER BY and LIMIT
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 5: ORDER BY and LIMIT ───────────────────────────────────────\n")

# ── Exercise 5.1 ──────────────────────────────────────────────────────────────
# Return the top 10 highest-paid employees.
# Columns: name, department, salary
# Sorted: salary descending

sql_5_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 5.2 ──────────────────────────────────────────────────────────────
# Return name, department, hire_date for all employees,
# sorted by department ASC, then hire_date ASC (earliest first within each dept).

sql_5_2 = """
-- YOUR QUERY HERE
"""

# ── Checks ────────────────────────────────────────────────────────────────────
try:
    df = q(sql_5_1)
    check_df(df, {"columns": ["name", "department", "salary"], "rows": 10},
             "5.1 — exactly 10 rows")
    if df is not None:
        check(df["salary"].is_monotonic_decreasing, True,
              "5.1 — sorted by salary DESC",
              hint="ORDER BY salary DESC LIMIT 10")
except Exception as e:
    print(f"  ❌  5.1 — Error: {e}")

try:
    df = q(sql_5_2)
    check_df(df, {"columns": ["name", "department", "hire_date"], "rows": 74},
             "5.2 — all 74 employees")
    if df is not None:
        check(df["department"].is_monotonic_increasing, True,
              "5.2 — sorted by department ASC first",
              hint="ORDER BY department ASC, hire_date ASC")
except Exception as e:
    print(f"  ❌  5.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE — Combine everything from this lesson
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Write a single query that returns:
#   name, department, role, salary, clearance, hire_date
#
# Filters:
#   - Department must be Cyber, Engineering, or Intelligence
#   - Salary must be between 90000 and 140000 (inclusive)
#   - Clearance must be Secret or Top Secret
#   - Employee must be active (active = 1)
#   - Role must contain the word 'Analyst' OR 'Engineer'
#
# Sort: department ASC, salary DESC
# Limit: top 15 rows

sql_challenge = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_challenge)
    check_df(df, {
        "columns": ["name", "department", "role", "salary", "clearance", "hire_date"],
        "min_rows": 1,
    }, "Challenge — correct columns and at least 1 row")

    if df is not None and len(df) > 0:
        check(set(df["department"].unique()).issubset({"Cyber", "Engineering", "Intelligence"}),
              True, "Challenge — only target departments")
        check((df["salary"] >= 90000).all() and (df["salary"] <= 140000).all(),
              True, "Challenge — salary between 90k and 140k")
        check(set(df["clearance"].unique()).issubset({"Secret", "Top Secret"}),
              True, "Challenge — only Secret / Top Secret")
        check((df["active"] == 1).all() if "active" in df.columns else True,
              True, "Challenge — only active employees")
        analyst_or_engineer = df["role"].str.contains("Analyst|Engineer").all()
        check(analyst_or_engineer, True,
              "Challenge — role contains Analyst or Engineer",
              hint="WHERE (role LIKE '%Analyst%' OR role LIKE '%Engineer%')")
        check(len(df) <= 15, True, "Challenge — max 15 rows (LIMIT 15)")
        check(df["department"].is_monotonic_increasing, True,
              "Challenge — sorted by department ASC")

        print()
        print(df.to_string(index=False))

except Exception as e:
    print(f"  ❌  Challenge — Error: {e}")


# ── Final score ───────────────────────────────────────────────────────────────
summary()
