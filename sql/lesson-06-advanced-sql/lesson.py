"""
SQL Lesson 06 — Advanced SQL
==============================
Read README.md first.
Run: python sql/lesson-06-advanced-sql/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import duckdb

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
con = duckdb.connect()
con.execute(f"CREATE TABLE employees          AS SELECT * FROM read_csv_auto('{DATA}/employees.csv')")
con.execute(f"CREATE TABLE departments        AS SELECT * FROM read_csv_auto('{DATA}/departments.csv')")
con.execute(f"CREATE TABLE security_events    AS SELECT * FROM read_csv_auto('{DATA}/security_events.csv')")
con.execute(f"CREATE TABLE contracts          AS SELECT * FROM read_csv_auto('{DATA}/contracts.csv')")
con.execute(f"CREATE TABLE employee_contracts AS SELECT * FROM read_csv_auto('{DATA}/employee_contracts.csv')")

def q(sql):
    sql = sql.strip()
    if not sql or sql.startswith("--"): return None
    return con.execute(sql).df()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — CASE WHEN
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: CASE WHEN ────────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Add a salary_band column to every employee:
#   'Senior'  if salary >= 130000
#   'Mid'     if salary >= 100000
#   'Junior'  otherwise
# Columns: name, department, salary, salary_band
# Sort by salary DESC.

sql_1_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Per department, use conditional aggregation to show:
#   department, total_employees, senior_count, mid_count, junior_count
# (using the same salary_band thresholds as above)
# Sort by total_employees DESC.

sql_1_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_1_1)
    check_df(df, {"columns": ["name","department","salary","salary_band"], "rows": 74}, "1.1 — all rows, correct columns")
    if df is not None:
        seniors = df[df["salary_band"]=="Senior"]["salary"]
        check((seniors >= 130000).all(), True, "1.1 — Senior = salary >= 130000")
        mids = df[df["salary_band"]=="Mid"]["salary"]
        check((mids >= 100000).all() and (mids < 130000).all(), True, "1.1 — Mid = 100000 to 129999")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    df = q(sql_1_2)
    check_df(df, {"rows": 6, "columns": ["department","total_employees","senior_count","mid_count","junior_count"]}, "1.2 — 6 rows, correct columns")
    if df is not None:
        check(int((df["senior_count"] + df["mid_count"] + df["junior_count"]).sum()), 74,
              "1.2 — band counts sum to 74")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Date Functions
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: Date Functions ───────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Return name, hire_date, and days_employed (days from hire_date to today).
# Sort by days_employed DESC (longest-tenured first).
# Limit to 10 rows.

sql_2_1 = """
-- YOUR QUERY HERE
-- Hint: DATEDIFF('day', hire_date, CURRENT_DATE) AS days_employed
"""

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Count how many employees were hired each year.
# Columns: hire_year, hires
# Sort by hire_year ASC.
# Hint: DATE_TRUNC('year', hire_date) AS hire_year

sql_2_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_2_1)
    check_df(df, {"columns": ["name","hire_date","days_employed"], "rows": 10}, "2.1 — 10 rows, correct columns")
    if df is not None:
        check(df["days_employed"].is_monotonic_decreasing, True, "2.1 — sorted by days_employed DESC")
        check((df["days_employed"] > 0).all(), True, "2.1 — all days_employed > 0")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    df = q(sql_2_2)
    check_df(df, {"columns": ["hire_year","hires"]}, "2.2 — correct columns")
    if df is not None:
        check(int(df["hires"].sum()), 74, "2.2 — hires sum to 74")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — String Functions
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: String Functions ─────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Return name, department and a new column called display_label:
#   format: "NAME — DEPARTMENT"  (uppercase name, original department)
#   Example: "ALEX CHEN — Cyber"
# Use UPPER() and string concatenation (|| or CONCAT).

sql_3_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Return event_type, source_ip, and a new column ip_prefix:
#   the first two octets of source_ip (everything before the second dot)
# Example: '10.0.45.23' → '10.0'
# Use SUBSTRING and/or string functions.
# Return only DISTINCT combinations of event_type and ip_prefix.

sql_3_2 = """
-- YOUR QUERY HERE
-- Hint: REGEXP_EXTRACT(source_ip, '^[0-9]+[.][0-9]+') gets the first two octets
-- Or: use SPLIT_PART(source_ip, '.', 1) || '.' || SPLIT_PART(source_ip, '.', 2)
"""

try:
    df = q(sql_3_1)
    check_df(df, {"columns": ["name","department","display_label"]}, "3.1 — correct columns")
    if df is not None:
        sample = df["display_label"].iloc[0]
        check(" — " in sample, True, "3.1 — display_label contains ' — ' separator")
        check(df["display_label"].str.contains("—").all(), True, "3.1 — all rows have separator")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    df = q(sql_3_2)
    check_df(df, {"columns": ["event_type","ip_prefix"]}, "3.2 — correct columns")
    if df is not None:
        check(df["ip_prefix"].str.count(r"\.").eq(1).all(), True,
              "3.2 — ip_prefix has exactly one dot (two octets)")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE — Everything from SQL lessons 01–06
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Build a comprehensive employee security profile.
# Using CTEs:
#
# CTE 1 — employee_base:
#   All active employees with their division (join to departments).
#   Add salary_band (Senior/Mid/Junior) and days_employed.
#
# CTE 2 — event_summary:
#   Per employee: total_events, critical_events, unresolved_events
#
# Final SELECT — join them and return:
#   name, department, division, salary, salary_band, days_employed,
#   total_events, critical_events, unresolved_events
#
# Filters:
#   - Only employees with at least 1 security event
#   - Only Secret or Top Secret clearance
#
# Sort: critical_events DESC, salary DESC

sql_challenge = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_challenge)
    check_df(df, {
        "columns": ["name","department","division","salary","salary_band",
                    "days_employed","total_events","critical_events","unresolved_events"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if df is not None and len(df) > 0:
        check(set(df["salary_band"].unique()).issubset({"Senior","Mid","Junior"}), True,
              "Challenge — salary_band values correct")
        check((df["total_events"] >= 1).all(), True, "Challenge — all have events")
        check(df["critical_events"].is_monotonic_decreasing, True, "Challenge — sorted by critical_events DESC")
        print()
        print(df.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
