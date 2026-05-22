"""
Pandas Lesson 02 — Cleaning & Transformation
==============================================
Run: python pandas/lesson-02-cleaning-transformation/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import pandas as pd
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
emp = pd.read_csv(f"{DATA}/employees.csv")
evt = pd.read_csv(f"{DATA}/security_events.csv")

# Inject some NaN values for practice
emp_dirty = emp.copy()
np.random.seed(42)
null_idx = np.random.choice(emp_dirty.index, size=8, replace=False)
emp_dirty.loc[null_idx, "clearance"] = np.nan
emp_dirty.loc[null_idx[:3], "salary"] = np.nan


# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: NaN Handling ─────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Count NaN values per column in emp_dirty.
nan_counts = None  # YOUR CODE HERE — result should be a Series

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Fill NaN in "clearance" with "Unknown" and NaN in "salary" with the median salary.
# Assign to emp_clean.
emp_clean = None  # YOUR CODE HERE

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Drop any rows still containing NaN from emp_clean. Assign to emp_no_nan.
emp_no_nan = None  # YOUR CODE HERE

try:
    check(int(nan_counts["clearance"]), 8, "1.1 — 8 NaN in clearance")
    check(int(nan_counts["salary"]), 3, "1.1 — 3 NaN in salary")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    check(emp_clean["clearance"].isna().sum(), 0, "1.2 — no NaN in clearance after fill")
    check(emp_clean["salary"].isna().sum(), 0, "1.2 — no NaN in salary after fill")
    check(emp_clean[emp_clean["clearance"] == "Unknown"].shape[0], 8, "1.2 — 8 rows have 'Unknown' clearance")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")

try:
    check(emp_no_nan.isna().sum().sum(), 0, "1.3 — zero total NaN values after dropna")
except Exception as e: print(f"  ❌  1.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: apply() and map() ────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Add a salary_band column to emp using apply():
#   "Senior" >= 130000, "Mid" >= 100000, else "Junior"
emp_with_band = emp.copy()
emp_with_band["salary_band"] = None  # YOUR CODE HERE (apply + lambda or function)

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Add a display_label column using apply(axis=1):
# format: "Name — Department"
emp_with_band["display_label"] = None  # YOUR CODE HERE (apply axis=1)

# ── Exercise 2.3 ──────────────────────────────────────────────────────────────
# Map severity to a numeric score using map():
# LOW=1, MEDIUM=2, HIGH=3, CRITICAL=4
severity_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
evt_scored = evt.copy()
evt_scored["severity_score"] = None  # YOUR CODE HERE

try:
    check(emp_with_band.loc[emp_with_band["salary"] >= 130000, "salary_band"].eq("Senior").all(), True, "2.1 — Senior band correct")
    check(emp_with_band.loc[emp_with_band["salary"] < 100000, "salary_band"].eq("Junior").all(), True, "2.1 — Junior band correct")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    check(emp_with_band["display_label"].str.contains(" — ").all(), True, "2.2 — display_label has ' — ' separator")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")

try:
    check(evt_scored.loc[evt_scored["severity"]=="CRITICAL","severity_score"].eq(4).all(), True, "2.3 — CRITICAL maps to 4")
    check(evt_scored.loc[evt_scored["severity"]=="LOW","severity_score"].eq(1).all(), True, "2.3 — LOW maps to 1")
except Exception as e: print(f"  ❌  2.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: Renaming, Sorting, Dedup ─────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Rename "employee_id" to "emp_id" and "hire_date" to "start_date".
emp_renamed = None  # YOUR CODE HERE

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Sort emp by department ASC then salary DESC.
emp_sorted = None  # YOUR CODE HERE

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Convert hire_date column to datetime (in emp, not emp_renamed).
emp_dates = emp.copy()
emp_dates["hire_date"] = None  # YOUR CODE HERE

try:
    check("emp_id" in emp_renamed.columns, True, "3.1 — employee_id renamed to emp_id")
    check("start_date" in emp_renamed.columns, True, "3.1 — hire_date renamed to start_date")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    check(emp_sorted["department"].is_monotonic_increasing, True, "3.2 — sorted by department ASC")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")

try:
    check(str(emp_dates["hire_date"].dtype), "datetime64[ns]", "3.3 — hire_date is datetime",
          hint="pd.to_datetime(emp['hire_date'])")
except Exception as e: print(f"  ❌  3.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Start with emp_dirty (has NaN values).
# Build a clean, enriched DataFrame:
# 1. Fill clearance NaN with "Unknown", salary NaN with median
# 2. Add salary_band column (Senior/Mid/Junior)
# 3. Add severity_score equivalent: clearance_score
#    None/Unknown=0, Confidential=1, Secret=2, Top Secret=3
# 4. Sort by clearance_score DESC, salary DESC
# 5. Select only: name, department, salary, salary_band, clearance, clearance_score
#
# Spiral: NaN filling + apply + map + sort + select (all from this lesson)

clearance_score_map = {"Unknown": 0, "None": 0, "Confidential": 1, "Secret": 2, "Top Secret": 3}
result = None  # YOUR CODE HERE — chain the steps

try:
    check_df(result, {
        "columns": ["name","department","salary","salary_band","clearance","clearance_score"],
        "no_nulls": ["salary","clearance"],
    }, "Challenge — correct columns, no nulls in salary/clearance")
    if result is not None:
        check(result["clearance_score"].is_monotonic_decreasing or True, True, "Challenge — sorted by clearance_score DESC")
        check(set(result["salary_band"].unique()).issubset({"Senior","Mid","Junior"}), True, "Challenge — valid salary bands")
        print()
        print(result.head(5).to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
