"""
CAPSTONE — End-to-End Assessment Simulation
=============================================
Target time: 60 minutes
No hints. Debug your own answers.
Run: python capstone/capstone.py
"""

import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
from checker import check, check_df, summary
import duckdb
import pandas as pd
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
con = duckdb.connect()
con.execute(f"CREATE TABLE employees          AS SELECT * FROM read_csv_auto('{DATA}/employees.csv')")
con.execute(f"CREATE TABLE departments        AS SELECT * FROM read_csv_auto('{DATA}/departments.csv')")
con.execute(f"CREATE TABLE contracts          AS SELECT * FROM read_csv_auto('{DATA}/contracts.csv')")
con.execute(f"CREATE TABLE employee_contracts AS SELECT * FROM read_csv_auto('{DATA}/employee_contracts.csv')")
con.execute(f"CREATE TABLE security_events    AS SELECT * FROM read_csv_auto('{DATA}/security_events.csv')")

emp = pd.read_csv(f"{DATA}/employees.csv")
evt = pd.read_csv(f"{DATA}/security_events.csv")
dept = pd.read_csv(f"{DATA}/departments.csv")

def q(sql):
    sql = sql.strip()
    if not sql or sql.startswith("--"): return None
    return con.execute(sql).df()

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║         DS INTERVIEW PREP — CAPSTONE ASSESSMENT SIMULATION                 ║
║                                                                              ║
║  20 questions  |  Target: 60 minutes  |  Passing: 15/20 (75%)              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION A — SQL (5 questions)
# ══════════════════════════════════════════════════════════════════════════════
print("═" * 78)
print("  SECTION A — SQL")
print("═" * 78 + "\n")

# ── A1 ────────────────────────────────────────────────────────────────────────
# For each department, return: department, headcount, avg_salary (rounded to 0),
# and the number of employees with Top Secret clearance.
# Sort by headcount descending.
# Columns: department, headcount, avg_salary, top_secret_count

sql_a1 = """
-- YOUR QUERY HERE
"""

# ── A2 ────────────────────────────────────────────────────────────────────────
# Using a CTE, find the top 2 highest-paid employees in each department.
# Columns: name, department, salary, dept_rank
# dept_rank must be 1 or 2 (use DENSE_RANK).

sql_a2 = """
-- YOUR QUERY HERE
"""

# ── A3 ────────────────────────────────────────────────────────────────────────
# Return all employees with their division (from departments table)
# and count of security events they've generated.
# Include employees with zero events (LEFT JOIN).
# Columns: name, department, division, event_count
# Sort by event_count DESC.

sql_a3 = """
-- YOUR QUERY HERE
"""

# ── A4 ────────────────────────────────────────────────────────────────────────
# For each employee, return their salary and the running total of salary
# within their department, ordered by hire_date ascending.
# Columns: name, department, salary, hire_date, running_dept_salary

sql_a4 = """
-- YOUR QUERY HERE
"""

# ── A5 ────────────────────────────────────────────────────────────────────────
# Find departments where the percentage of CRITICAL security events
# (out of all events for employees in that department) is above 15%.
# Columns: department, total_events, critical_events, critical_pct
# critical_pct = ROUND(critical_events * 100.0 / total_events, 1)
# Sort by critical_pct DESC.

sql_a5 = """
-- YOUR QUERY HERE
"""

print("── A1: Department summary with Top Secret count ────────────────────────\n")
try:
    df = q(sql_a1)
    check_df(df, {"rows": 6, "columns": ["department","headcount","avg_salary","top_secret_count"]}, "A1 columns + row count")
    if df is not None:
        check(int(df["headcount"].sum()), 74, "A1 headcounts sum to 74")
        check(df["headcount"].is_monotonic_decreasing, True, "A1 sorted by headcount DESC")
except Exception as e: print(f"  ❌  A1 — Error: {e}")

print("\n── A2: Top 2 per department ────────────────────────────────────────────\n")
try:
    df = q(sql_a2)
    check_df(df, {"columns": ["name","department","salary","dept_rank"]}, "A2 columns")
    if df is not None:
        check(df["dept_rank"].max(), 2, "A2 max rank = 2")
        check(df["dept_rank"].min(), 1, "A2 min rank = 1")
except Exception as e: print(f"  ❌  A2 — Error: {e}")

print("\n── A3: Employees with division and event count ─────────────────────────\n")
try:
    df = q(sql_a3)
    check_df(df, {"columns": ["name","department","division","event_count"]}, "A3 columns")
    if df is not None:
        check(len(df), 74, "A3 all 74 employees returned (LEFT JOIN)")
        check(df["event_count"].is_monotonic_decreasing, True, "A3 sorted by event_count DESC")
except Exception as e: print(f"  ❌  A3 — Error: {e}")

print("\n── A4: Running total salary by department ──────────────────────────────\n")
try:
    df = q(sql_a4)
    check_df(df, {"columns": ["name","department","salary","hire_date","running_dept_salary"]}, "A4 columns")
    if df is not None:
        check(len(df), 74, "A4 all 74 rows")
except Exception as e: print(f"  ❌  A4 — Error: {e}")

print("\n── A5: Departments with >15% critical events ───────────────────────────\n")
try:
    df = q(sql_a5)
    check_df(df, {"columns": ["department","total_events","critical_events","critical_pct"]}, "A5 columns")
    if df is not None:
        check((df["critical_pct"] > 15).all(), True, "A5 all depts above 15%")
        check(df["critical_pct"].is_monotonic_decreasing, True, "A5 sorted DESC")
except Exception as e: print(f"  ❌  A5 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION B — Python (5 questions)
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 78)
print("  SECTION B — Python")
print("═" * 78 + "\n")

events_raw = [
    {"employee_id": 1001, "event_type": "login_failure",        "severity": "LOW",      "resolved": False},
    {"employee_id": 1002, "event_type": "privilege_escalation", "severity": "CRITICAL",  "resolved": False},
    {"employee_id": 1001, "event_type": "data_export",          "severity": "HIGH",     "resolved": True},
    {"employee_id": 1003, "event_type": "network_scan",         "severity": "MEDIUM",   "resolved": False},
    {"employee_id": 1002, "event_type": "anomalous_traffic",    "severity": "HIGH",     "resolved": False},
    {"employee_id": 1001, "event_type": "login_success",        "severity": "LOW",      "resolved": True},
    {"employee_id": 1003, "event_type": "config_change",        "severity": "MEDIUM",   "resolved": True},
    {"employee_id": 1002, "event_type": "privilege_escalation", "severity": "CRITICAL",  "resolved": False},
]

# ── B1 ────────────────────────────────────────────────────────────────────────
# Using a list comprehension, extract the event_type for every UNRESOLVED event.
unresolved_types = None  # YOUR CODE HERE

# ── B2 ────────────────────────────────────────────────────────────────────────
# Build a dict mapping employee_id → count of CRITICAL or HIGH events
# for that employee. Include only employees with at least 1 such event.
high_risk_by_emp = {}  # YOUR CODE HERE

# ── B3 ────────────────────────────────────────────────────────────────────────
# Write a function risk_score(event) that returns:
#   4 if severity == "CRITICAL" and not resolved
#   3 if severity == "HIGH" and not resolved
#   2 if severity in ("CRITICAL","HIGH") and resolved
#   1 otherwise
# Then sort events_raw by risk_score descending using sorted() + lambda.
def risk_score(event):
    pass  # YOUR CODE HERE

sorted_events = None  # YOUR CODE HERE — sorted(events_raw, ...)

# ── B4 ────────────────────────────────────────────────────────────────────────
# Parse this JSON string and return the list of employee IDs whose salary
# is above 100000 as a list of ints.
payload = '{"employees": [{"id": 1001, "salary": 140000}, {"id": 1002, "salary": 85000}, {"id": 1003, "salary": 125000}, {"id": 1004, "salary": 72000}]}'
high_earner_ids = None  # YOUR CODE HERE

# ── B5 ────────────────────────────────────────────────────────────────────────
# Using only map() and filter() (no comprehensions):
# From events_raw, get a list of event_type strings (uppercased)
# for CRITICAL severity events only.
critical_upper = None  # YOUR CODE HERE

print("── B1: Unresolved event types ──────────────────────────────────────────\n")
check(sorted(unresolved_types), sorted(["login_failure","privilege_escalation","network_scan","anomalous_traffic","privilege_escalation"]),
      "B1 — unresolved event types (list comprehension)")

print("\n── B2: High risk counts per employee ───────────────────────────────────\n")
check(high_risk_by_emp.get(1002), 3, "B2 — employee 1002 has 3 high/critical events")
check(high_risk_by_emp.get(1001), 1, "B2 — employee 1001 has 1 high/critical event")
check(1004 not in high_risk_by_emp, True, "B2 — employee 1004 not in dict (no events)")

print("\n── B3: risk_score function + sorted ────────────────────────────────────\n")
check(risk_score({"severity": "CRITICAL", "resolved": False}), 4, "B3 — CRITICAL unresolved = 4")
check(risk_score({"severity": "LOW",      "resolved": False}), 1, "B3 — LOW = 1")
if sorted_events:
    check(sorted_events[0]["severity"], "CRITICAL", "B3 — first sorted event is CRITICAL")
    check(sorted_events[0]["resolved"], False, "B3 — first event is unresolved")

print("\n── B4: JSON parsing ────────────────────────────────────────────────────\n")
check(sorted(high_earner_ids), [1001, 1003], "B4 — IDs above 100000")

print("\n── B5: map + filter ────────────────────────────────────────────────────\n")
if critical_upper:
    check(sorted(critical_upper), sorted(["PRIVILEGE_ESCALATION","PRIVILEGE_ESCALATION"]),
          "B5 — CRITICAL events uppercased")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION C — Pandas (5 questions)
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 78)
print("  SECTION C — Pandas")
print("═" * 78 + "\n")

emp_pd  = emp.copy()
evt_pd  = evt.copy()
dept_pd = dept.copy()
evt_pd["timestamp"] = pd.to_datetime(evt_pd["timestamp"])

# ── C1 ────────────────────────────────────────────────────────────────────────
# Filter to active employees in Cyber or Engineering earning above 100000.
# Add a salary_band column. Return only: name, department, salary, salary_band.
c1_result = None  # YOUR CODE HERE

# ── C2 ────────────────────────────────────────────────────────────────────────
# Group employees by department. Compute: headcount, avg_salary (round 0),
# pct_top_secret (% of dept with Top Secret clearance, round to 1).
# Columns: department, headcount, avg_salary, pct_top_secret
c2_result = None  # YOUR CODE HERE

# ── C3 ────────────────────────────────────────────────────────────────────────
# Add a dept_avg_salary column to emp_pd using transform().
# Then return the 5 employees with the largest positive vs_dept_avg (salary - dept_avg).
# Columns: name, department, salary, dept_avg_salary, vs_dept_avg
c3_result = None  # YOUR CODE HERE

# ── C4 ────────────────────────────────────────────────────────────────────────
# Merge emp_pd and evt_pd on employee_id (inner join).
# Count events per employee. Return employees with >= 10 events.
# Columns: name, department, event_count. Sort by event_count DESC.
c4_result = None  # YOUR CODE HERE

# ── C5 ────────────────────────────────────────────────────────────────────────
# From evt_pd, count security events by year and severity.
# Columns: year, severity, event_count. Sort by year ASC then event_count DESC.
c5_result = None  # YOUR CODE HERE

print("── C1: Filter + salary_band ────────────────────────────────────────────\n")
try:
    check_df(c1_result, {"columns": ["name","department","salary","salary_band"]}, "C1 columns")
    if c1_result is not None:
        check(set(c1_result["department"].unique()).issubset({"Cyber","Engineering"}), True, "C1 dept filter")
        check((c1_result["salary"] > 100000).all(), True, "C1 salary > 100000")
        check(set(c1_result["salary_band"].unique()).issubset({"Senior","Mid"}), True, "C1 salary_band values")
except Exception as e: print(f"  ❌  C1 — Error: {e}")

print("\n── C2: GroupBy with pct_top_secret ─────────────────────────────────────\n")
try:
    check_df(c2_result, {"rows": 6, "columns": ["department","headcount","avg_salary","pct_top_secret"]}, "C2 columns + 6 rows")
    if c2_result is not None:
        check(int(c2_result["headcount"].sum()), 74, "C2 headcounts sum to 74")
        check((c2_result["pct_top_secret"] >= 0).all() and (c2_result["pct_top_secret"] <= 100).all(),
              True, "C2 pct_top_secret in 0–100")
except Exception as e: print(f"  ❌  C2 — Error: {e}")

print("\n── C3: transform + top 5 vs dept avg ───────────────────────────────────\n")
try:
    check_df(c3_result, {"rows": 5, "columns": ["name","department","salary","dept_avg_salary","vs_dept_avg"]}, "C3 columns + 5 rows")
    if c3_result is not None:
        check(c3_result["vs_dept_avg"].is_monotonic_decreasing, True, "C3 sorted by vs_dept_avg DESC")
        check((c3_result["vs_dept_avg"] > 0).all(), True, "C3 all vs_dept_avg positive")
except Exception as e: print(f"  ❌  C3 — Error: {e}")

print("\n── C4: Merge + event count >= 10 ───────────────────────────────────────\n")
try:
    check_df(c4_result, {"columns": ["name","department","event_count"]}, "C4 columns")
    if c4_result is not None:
        check((c4_result["event_count"] >= 10).all(), True, "C4 all event_count >= 10")
        check(c4_result["event_count"].is_monotonic_decreasing, True, "C4 sorted DESC")
except Exception as e: print(f"  ❌  C4 — Error: {e}")

print("\n── C5: Events by year and severity ─────────────────────────────────────\n")
try:
    check_df(c5_result, {"columns": ["year","severity","event_count"]}, "C5 columns")
    if c5_result is not None:
        check(int(c5_result["event_count"].sum()), 500, "C5 total = 500")
        check(c5_result["year"].is_monotonic_increasing, True, "C5 sorted by year ASC")
except Exception as e: print(f"  ❌  C5 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION D — Snowflake Concepts (self-graded)
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 78)
print("  SECTION D — Snowflake Concepts (self-graded)")
print("═" * 78)
print("""
Write your answers below, then compare to the answer key in capstone/answers.py.
Grade yourself 1 point per correct answer (5 possible).

D1. Explain the three-layer architecture of Snowflake. What does separating
    compute from storage enable that traditional databases can't do?

D2. What is the difference between Time Travel and Fail-Safe in Snowflake?
    Who controls each?

D3. Write the Snowflake SQL syntax to query a table called "events" as it
    existed 2 hours ago.

D4. You have a VARIANT column called "metadata" storing JSON like:
      {"source": "endpoint", "tags": ["brute-force", "insider"]}
    Write Snowflake SQL to extract the "source" value and explode the
    "tags" array into individual rows.

D5. What does QUALIFY do and how is it different from WHERE and HAVING?
    Give a brief example.
""")

d1_answer = """
YOUR ANSWER HERE
"""
d2_answer = """
YOUR ANSWER HERE
"""
d3_answer = """
YOUR ANSWER HERE
"""
d4_answer = """
YOUR ANSWER HERE
"""
d5_answer = """
YOUR ANSWER HERE
"""

# Self-grade: check capstone/answers.py for reference answers
print("  → Compare your answers to capstone/answers.py  (Section D)\n")


# ══════════════════════════════════════════════════════════════════════════════
summary()
print("""
─────────────────────────────────────────────────────────────────────────────
  Add your self-graded Section D score (0–5) to the total above.
  Target: 15+ out of 20 (75%) → ready for the assessment.
─────────────────────────────────────────────────────────────────────────────
""")
