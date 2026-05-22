"""
Pandas Lesson 05 — Datetime & Advanced Pandas
================================================
Run: python pandas/lesson-05-datetime-advanced/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
emp = pd.read_csv(f"{DATA}/employees.csv")
evt = pd.read_csv(f"{DATA}/security_events.csv")

# Convert datetime columns upfront
emp["hire_date"]  = pd.to_datetime(emp["hire_date"])
evt["timestamp"]  = pd.to_datetime(evt["timestamp"])


# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: .dt Accessor ─────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Add columns hire_year, hire_month, hire_quarter to emp.
emp_dt = emp.copy()
emp_dt["hire_year"]    = None  # YOUR CODE HERE
emp_dt["hire_month"]   = None  # YOUR CODE HERE
emp_dt["hire_quarter"] = None  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Compute days_employed = days from hire_date to today for each employee.
# Add as a column, rounded to 0 decimal places (integer).
emp_dt["days_employed"] = None  # YOUR CODE HERE

try:
    check(emp_dt["hire_year"].between(2010, 2030).all(), True, "1.1 — hire_year in reasonable range")
    check(emp_dt["hire_month"].between(1, 12).all(), True, "1.1 — hire_month 1–12")
    check(emp_dt["hire_quarter"].between(1, 4).all(), True, "1.1 — hire_quarter 1–4")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    check((emp_dt["days_employed"] > 0).all(), True, "1.2 — all days_employed > 0")
    check(emp_dt["days_employed"].dtype.kind in ("i","f"), True, "1.2 — numeric dtype")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: Datetime Filtering ───────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Filter emp to employees hired on or after 2020-01-01.
recent_hires = None  # YOUR CODE HERE

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Count security events per year (use evt["timestamp"].dt.year).
# Columns: year, event_count. Sort by year ASC.
events_by_year = None  # YOUR CODE HERE

try:
    check((emp[emp["hire_date"] >= "2020-01-01"].shape[0]), len(recent_hires),
          "2.1 — correct count of post-2020 hires")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    check_df(events_by_year, {"columns": ["year","event_count"]}, "2.2 — correct columns")
    check(int(events_by_year["event_count"].sum()), 500, "2.2 — total = 500")
    check(events_by_year["year"].is_monotonic_increasing, True, "2.2 — sorted by year ASC")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: resample() ───────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Using resample(), count how many security events occurred per month.
# Set timestamp as index first. Result: Series or DataFrame with monthly counts.
# Columns when reset: timestamp (or period), event_count
evt_indexed = evt.set_index("timestamp")
monthly_counts = None  # YOUR CODE HERE — resample("ME") or ("M") then count

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Using resample("YE") (or "Y"), compute the mean salary of employees hired each year.
# Set hire_date as index on emp_dt.
emp_indexed = emp_dt.set_index("hire_date")
annual_avg_salary = None  # YOUR CODE HERE

try:
    if monthly_counts is not None:
        mc = monthly_counts.reset_index() if hasattr(monthly_counts, "reset_index") else monthly_counts
        check(int(mc.iloc[:, 1].sum() if mc.shape[1] > 1 else mc.sum()), 500,
              "3.1 — monthly counts sum to 500")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    if annual_avg_salary is not None:
        check(len(annual_avg_salary) >= 1, True, "3.2 — at least one annual period")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: Method Chaining & query() ────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Using query(), filter emp to active employees in Cyber or Engineering
# with salary > 100000.
high_tech = None  # YOUR CODE HERE

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# Write a method chain (no intermediate variables) that:
# 1. Filters emp to active == 1
# 2. Assigns a salary_band column (Senior/Mid/Junior)
# 3. Groups by department and salary_band
# 4. Counts employees (headcount)
# 5. Resets index and sorts by department, headcount DESC
band_counts = None  # YOUR CODE HERE — one chain

def salary_band(s):
    if s >= 130000: return "Senior"
    if s >= 100000: return "Mid"
    return "Junior"

try:
    check(set(high_tech["department"].unique()).issubset({"Cyber","Engineering"}), True,
          "4.1 — only Cyber/Engineering")
    check((high_tech["active"] == 1).all(), True, "4.1 — all active")
    check((high_tech["salary"] > 100000).all(), True, "4.1 — salary > 100000")
except Exception as e: print(f"  ❌  4.1 — Error: {e}")

try:
    check_df(band_counts, {"columns": ["department","salary_band","headcount"]}, "4.2 — correct columns")
    check(int(band_counts["headcount"].sum()), emp[emp["active"]==1].shape[0],
          "4.2 — headcounts sum to active employee count")
except Exception as e: print(f"  ❌  4.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────════════════════════════════════\n")

# Build a time-based security event report using method chaining.
# Starting from evt (timestamp already converted above):
# 1. Add event_year and event_month columns (.dt accessor)
# 2. Filter to CRITICAL and HIGH severity only
# 3. Group by event_year, severity — count events and count distinct employees
# 4. Reset index, sort by event_year ASC then event count DESC
# 5. Rename count column to event_count
#
# Columns: event_year, severity, event_count, unique_employees

time_report = None  # YOUR CODE HERE — method chain preferred

try:
    check_df(time_report, {
        "columns": ["event_year","severity","event_count","unique_employees"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if time_report is not None:
        check(set(time_report["severity"].unique()).issubset({"HIGH","CRITICAL"}), True,
              "Challenge — only HIGH and CRITICAL")
        check(time_report["event_year"].is_monotonic_increasing, True,
              "Challenge — sorted by year ASC")
        print()
        print(time_report.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
