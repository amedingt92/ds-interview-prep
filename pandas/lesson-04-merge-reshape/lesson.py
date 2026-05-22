"""
Pandas Lesson 04 — Merge & Reshape
=====================================
Run: python pandas/lesson-04-merge-reshape/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
emp  = pd.read_csv(f"{DATA}/employees.csv")
dept = pd.read_csv(f"{DATA}/departments.csv")
con  = pd.read_csv(f"{DATA}/contracts.csv")
ec   = pd.read_csv(f"{DATA}/employee_contracts.csv")
evt  = pd.read_csv(f"{DATA}/security_events.csv")


# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: merge() ──────────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Inner join emp and dept on department_id to add the "division" column.
# Keep: name, department, division, salary
emp_with_div = None  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Left join emp to ec on employee_id to find employees with no contract.
# Columns to check: name, department — filter to rows where contract_id is NaN.
no_contract = None  # YOUR CODE HERE

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Three-way merge: emp → ec → con (inner joins) to get
# name, department, contract_name, contract value, contract status.
# Filter to Active contracts only.
emp_contracts = None  # YOUR CODE HERE

try:
    check_df(emp_with_div, {"columns": ["name","department","division","salary"]}, "1.1 — correct columns")
    check(emp_with_div["division"].isna().sum(), 0, "1.1 — no NaN divisions (inner join)")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    check_df(no_contract, {"columns": ["name","department"]}, "1.2 — correct columns")
    check(len(no_contract) >= 0, True, "1.2 — query ran")
    if len(no_contract) > 0:
        ids = no_contract.index.tolist()
        in_ec = emp.loc[emp["name"].isin(no_contract["name"]), "employee_id"]
        check(ec[ec["employee_id"].isin(in_ec)].shape[0], 0,
              "1.2 — anti-join: these employees have no contracts",
              hint="pd.merge(..., how='left') then filter where ec col is NaN")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")

try:
    check_df(emp_contracts, {"columns": ["name","department","contract_name","value","status"]}, "1.3 — correct columns")
    check((emp_contracts["status"] == "Active").all(), True, "1.3 — Active contracts only")
except Exception as e: print(f"  ❌  1.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: concat() ─────────────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Split employees into two DataFrames — active and inactive — then
# stack them back together with concat and reset_index.
# The result should have all 74 rows.
active_df   = emp[emp["active"] == 1].copy()
inactive_df = emp[emp["active"] == 0].copy()

recombined = None  # YOUR CODE HERE

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Create a small "new hires" DataFrame with 2 fake employees and concat
# it onto emp. Result should have 76 rows.
new_hires = pd.DataFrame([
    {"employee_id": 9001, "name": "Sam Lee",    "department": "Cyber",       "salary": 108000, "active": 1, "clearance": "Secret"},
    {"employee_id": 9002, "name": "Dana Park",  "department": "Engineering", "salary":  97000, "active": 1, "clearance": "Confidential"},
])
emp_extended = None  # YOUR CODE HERE

try:
    check(len(recombined), 74, "2.1 — concat gives back 74 rows")
    check(recombined.index.tolist(), list(range(74)), "2.1 — index reset to 0..73",
          hint="Use ignore_index=True")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    check(len(emp_extended), 76, "2.2 — 76 rows after concat")
    check("Sam Lee" in emp_extended["name"].values, True, "2.2 — new hire Sam Lee present")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: pivot_table() ────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Create a pivot table: rows = department, columns = clearance,
# values = count of employees, fill_value = 0.
# Use aggfunc="count" and pivot on "employee_id".
clearance_pivot = None  # YOUR CODE HERE

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Create a pivot table: rows = severity, columns = resolved (0 or 1),
# values = count of events (event_id), fill_value = 0.
resolved_pivot = None  # YOUR CODE HERE

try:
    check(clearance_pivot.shape[0], 6, "3.1 — 6 department rows")
    check(clearance_pivot.values.sum(), 74, "3.1 — total count = 74")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    check(resolved_pivot.shape[0] >= 2, True, "3.2 — at least 2 severity rows")
    check(resolved_pivot.values.sum(), 500, "3.2 — total = 500 events")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: melt() ───────────────────────────────────────────────────\n")

# Wide-format salary data to practice melting
salary_wide = pd.DataFrame({
    "department": ["Cyber", "Engineering", "Logistics"],
    "2022_avg":   [118000, 112000, 68000],
    "2023_avg":   [122000, 115000, 70000],
    "2024_avg":   [126000, 119000, 73000],
})

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Melt salary_wide so that year columns become rows.
# Result columns: department, year, avg_salary
salary_long = None  # YOUR CODE HERE

try:
    check_df(salary_long, {"rows": 9, "columns": ["department","year","avg_salary"]}, "4.1 — 9 rows, correct columns")
    check(set(salary_long["year"].unique()), {"2022_avg","2023_avg","2024_avg"}, "4.1 — year values correct")
except Exception as e: print(f"  ❌  4.1 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Build a full employee + event summary using merge and groupby.
# Steps:
# 1. Merge emp → dept (inner) to get division
# 2. Merge result → evt (left join) to get all employees even if no events
# 3. GroupBy division: headcount (unique emp), total_events, critical_count, avg_salary
# 4. Add pct_critical = critical_count / total_events * 100 (round to 1), NaN → 0
# 5. Sort by pct_critical DESC
#
# Columns: division, headcount, total_events, critical_count, avg_salary, pct_critical

division_profile = None  # YOUR CODE HERE

try:
    check_df(division_profile, {
        "columns": ["division","headcount","total_events","critical_count","avg_salary","pct_critical"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if division_profile is not None:
        check(division_profile["pct_critical"].isna().sum(), 0, "Challenge — no NaN in pct_critical")
        check(division_profile["pct_critical"].is_monotonic_decreasing, True,
              "Challenge — sorted by pct_critical DESC")
        print()
        print(division_profile.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
