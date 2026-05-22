"""
Pandas Lesson 01 — DataFrames & Selection
==========================================
Run: python pandas/lesson-01-dataframes-selection/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
emp = pd.read_csv(f"{DATA}/employees.csv")
evt = pd.read_csv(f"{DATA}/security_events.csv")

print("\n── employees preview ───────────────────────────────────────────────────")
print(emp.head(3).to_string(index=False))
print(f"\nShape: {emp.shape}  |  Columns: {list(emp.columns)}\n")


# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Exploration ──────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# How many unique departments are in the employees DataFrame?
unique_dept_count = None  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# What is the most common clearance level? (use value_counts, get index 0)
most_common_clearance = None  # YOUR CODE HERE

check(unique_dept_count, emp["department"].nunique(), "1.1 — unique department count")
check(most_common_clearance, emp["clearance"].value_counts().index[0], "1.2 — most common clearance")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: Column Selection ─────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Select only name, department, salary columns. Assign to name_dept_sal.
name_dept_sal = None  # YOUR CODE HERE

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Get all unique values in the "clearance" column as a Python list.
clearance_values = None  # YOUR CODE HERE

check_df(name_dept_sal, {"columns": ["name","department","salary"], "rows": 74}, "2.1 — correct columns and row count")
check(isinstance(clearance_values, list), True, "2.2 — clearance_values is a list")
check(len(clearance_values), emp["clearance"].nunique(), "2.2 — correct unique count")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: .loc and .iloc ────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Using .iloc, get the salary of the first row (position 0).
first_salary_iloc = None  # YOUR CODE HERE

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Using .loc, get the name of the row with index label 0.
first_name_loc = None  # YOUR CODE HERE

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Using .iloc, get the first 3 rows and first 3 columns.
first_3x3 = None  # YOUR CODE HERE

check(first_salary_iloc, emp.iloc[0, emp.columns.get_loc("salary")], "3.1 — first salary via iloc")
check(first_name_loc, emp.loc[0, "name"], "3.2 — first name via loc")
check_df(first_3x3, {"rows": 3}, "3.3 — 3 rows via iloc")
check(first_3x3.shape[1], 3, "3.3 — 3 columns via iloc")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: Boolean Masks ─────────────────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Filter to only Cyber department employees.
cyber_df = None  # YOUR CODE HERE

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# Filter to active employees (active == 1) earning >= 100000.
active_high_earners = None  # YOUR CODE HERE

# ── Exercise 4.3 ──────────────────────────────────────────────────────────────
# Filter to employees in Cyber OR Engineering with Top Secret clearance.
ts_tech = None  # YOUR CODE HERE

# ── Exercise 4.4 ──────────────────────────────────────────────────────────────
# Filter to employees whose role contains "Analyst".
analysts = None  # YOUR CODE HERE

check_df(cyber_df, {"columns": ["employee_id","name"]}, "4.1 — Cyber filter keeps correct columns")
check((cyber_df["department"] == "Cyber").all(), True, "4.1 — only Cyber rows")
check((active_high_earners["active"] == 1).all() and (active_high_earners["salary"] >= 100000).all(),
      True, "4.2 — active AND salary >= 100000")
check(set(ts_tech["department"].unique()).issubset({"Cyber","Engineering"}), True, "4.3 — Cyber/Engineering only")
check((ts_tech["clearance"] == "Top Secret").all(), True, "4.3 — all Top Secret")
check(analysts["role"].str.contains("Analyst").all(), True, "4.4 — all roles contain Analyst")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# From the security_events DataFrame:
# 1. Filter to HIGH and CRITICAL severity events (use .isin())
# 2. From that result, get only the columns: event_id, employee_id, event_type, severity, resolved
# 3. Find how many are UNRESOLVED (resolved == 0)
# Spiral: selection + filtering (this lesson) + value counting (Lesson 02 preview)

high_critical_events = None  # step 1
trimmed              = None  # step 2
unresolved_count     = None  # step 3

try:
    check_df(high_critical_events, {"columns": ["event_id","employee_id","event_type","severity","resolved","source_ip","dest_ip","timestamp"]}, "Challenge step 1 — filtered to HIGH/CRITICAL")
    check(set(high_critical_events["severity"].unique()).issubset({"HIGH","CRITICAL"}), True, "Challenge — only HIGH/CRITICAL")
    check_df(trimmed, {"columns": ["event_id","employee_id","event_type","severity","resolved"]}, "Challenge step 2 — trimmed columns")
    check(unresolved_count > 0, True, "Challenge step 3 — some unresolved events")
    print(f"\n  HIGH/CRITICAL events: {len(high_critical_events)} | Unresolved: {unresolved_count}")
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
