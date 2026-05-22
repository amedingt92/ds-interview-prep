"""
SQL Lesson 03 — JOINs
=======================
Read README.md first, then work through each exercise.
Run: python sql/lesson-03-joins/lesson.py
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

print("\n── Schema reminder ─────────────────────────────────────────────────────")
print("  employees:          employee_id, name, department_id, department, role, salary, hire_date, clearance, active")
print("  departments:        department_id, department_name, division")
print("  contracts:          contract_id, contract_name, department_id, start_date, end_date, value, status")
print("  employee_contracts: assignment_id, employee_id, contract_id, role, start_date")
print("  security_events:    event_id, employee_id, event_type, severity, source_ip, dest_ip, timestamp, resolved")
print("────────────────────────────────────────────────────────────────────────\n")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — INNER JOIN
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: INNER JOIN ───────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Join employees to departments to get the division for each employee.
# Columns: name, department, division, salary
# Sort by division, then name.

sql_1_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Join security_events to employees to get the employee name and department
# for each security event.
# Columns: event_id, event_type, severity, name, department
# Only include HIGH and CRITICAL severity events.
# Sort by severity, then event_id.

sql_1_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_1_1)
    check_df(df, {"columns": ["name","department","division","salary"]}, "1.1 — correct columns")
    if df is not None:
        check("division" in df.columns and df["division"].notna().all(), True,
              "1.1 — division column present and no NULLs (inner join)")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    df = q(sql_1_2)
    check_df(df, {"columns": ["event_id","event_type","severity","name","department"]}, "1.2 — correct columns")
    if df is not None:
        check(set(df["severity"].unique()).issubset({"HIGH","CRITICAL"}), True,
              "1.2 — only HIGH and CRITICAL events")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — LEFT JOIN
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: LEFT JOIN ────────────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Return ALL employees along with their contract role if they have one.
# If an employee has no contract, still include them with NULL for contract columns.
# Columns: name, department, contract_name, contract_role
# (contract_name comes from contracts, contract_role from employee_contracts.role)
# Sort by name.

sql_2_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Anti-join: find employees who are NOT assigned to any contract.
# Columns: employee_id, name, department
# Sort by department, name.

sql_2_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_2_1)
    check_df(df, {"columns": ["name","department","contract_name","contract_role"]}, "2.1 — correct columns")
    if df is not None:
        # Should have more rows than just employees (employees can appear multiple times for multiple contracts)
        check(len(df) >= 74, True, "2.1 — at least 74 rows (LEFT JOIN keeps all employees)",
              hint="LEFT JOIN employee_contracts ... LEFT JOIN contracts ...")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    df = q(sql_2_2)
    check_df(df, {"columns": ["employee_id","name","department"]}, "2.2 — correct columns")
    if df is not None:
        check(len(df) >= 0, True, "2.2 — query ran successfully")
        # Verify these employees truly have no contracts
        if len(df) > 0:
            ids = tuple(df["employee_id"].tolist())
            if len(ids) == 1:
                ids = f"({ids[0]})"
            result = q(f"SELECT COUNT(*) AS n FROM employee_contracts WHERE employee_id IN {ids}")
            check(int(result.iloc[0,0]), 0, "2.2 — returned employees have no contracts (anti-join)",
                  hint="LEFT JOIN ... WHERE ec.employee_id IS NULL")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Multi-Table JOINs
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: Multi-Table JOINs ────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Join employees → employee_contracts → contracts to get:
#   name, department, contract_name, contract value, contract status
# Only include Active contracts.
# Sort by contract value descending.

sql_3_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# For each division (from departments), count:
#   - how many employees are in that division
#   - the average salary for that division
#   - how many CRITICAL security events employees in that division have generated
#
# Columns: division, employee_count, avg_salary, critical_event_count
# Sort by critical_event_count descending.
#
# Hint: you'll need employees → departments for division,
#       and employees → security_events for events.

sql_3_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_3_1)
    check_df(df, {"columns": ["name","department","contract_name","value","status"]}, "3.1 — correct columns")
    if df is not None:
        check((df["status"] == "Active").all(), True, "3.1 — only Active contracts")
        check(df["value"].is_monotonic_decreasing, True, "3.1 — sorted by value DESC")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    df = q(sql_3_2)
    check_df(df, {"columns": ["division","employee_count","avg_salary","critical_event_count"]}, "3.2 — correct columns")
    if df is not None:
        check(df["critical_event_count"].is_monotonic_decreasing, True, "3.2 — sorted by critical_event_count DESC")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — JOIN + Aggregation (Spiral: Lesson 02)
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: JOIN + Aggregation ───────────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# For each contract, count how many employees are assigned to it.
# Columns: contract_name, status, assigned_count
# Only show contracts with at least 5 employees assigned.
# Sort by assigned_count descending.

sql_4_1 = """
-- YOUR QUERY HERE
"""

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# For each employee, count their total security events and how many were CRITICAL.
# Only include employees with at least 1 CRITICAL event.
# Columns: name, department, total_events, critical_events
# Sort by critical_events descending, then name.

sql_4_2 = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_4_1)
    check_df(df, {"columns": ["contract_name","status","assigned_count"]}, "4.1 — correct columns")
    if df is not None:
        check((df["assigned_count"] >= 5).all(), True, "4.1 — all counts >= 5",
              hint="HAVING COUNT(*) >= 5")
        check(df["assigned_count"].is_monotonic_decreasing, True, "4.1 — sorted DESC")
except Exception as e: print(f"  ❌  4.1 — Error: {e}")

try:
    df = q(sql_4_2)
    check_df(df, {"columns": ["name","department","total_events","critical_events"]}, "4.2 — correct columns")
    if df is not None:
        check((df["critical_events"] >= 1).all(), True, "4.2 — all have at least 1 critical event")
        check(df["critical_events"].is_monotonic_decreasing, True, "4.2 — sorted by critical_events DESC")
except Exception as e: print(f"  ❌  4.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Build a threat summary report.
# For each department, return:
#   department, division, headcount, total_events, high_critical_events,
#   unresolved_events, avg_salary
#
# - division comes from the departments table
# - total_events = all security events for employees in that department
# - high_critical_events = events with severity IN ('HIGH','CRITICAL')
# - unresolved_events = events where resolved = 0
# - avg_salary rounded to 0 decimal places
#
# Only include departments with at least 1 HIGH or CRITICAL event.
# Sort by high_critical_events descending.
#
# Spiral callbacks: JOIN (this lesson) + GROUP BY + HAVING + COUNT (Lesson 02)

sql_challenge = """
-- YOUR QUERY HERE
"""

try:
    df = q(sql_challenge)
    check_df(df, {
        "columns": ["department","division","headcount","total_events",
                    "high_critical_events","unresolved_events","avg_salary"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if df is not None and len(df) > 0:
        check((df["high_critical_events"] >= 1).all(), True, "Challenge — all depts have HIGH/CRITICAL events")
        check(df["high_critical_events"].is_monotonic_decreasing, True, "Challenge — sorted DESC")
        check((df["unresolved_events"] <= df["total_events"]).all(), True,
              "Challenge — unresolved <= total")
        print()
        print(df.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
