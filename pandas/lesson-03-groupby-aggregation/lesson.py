"""
Pandas Lesson 03 — GroupBy & Aggregation
==========================================
Run: python pandas/lesson-03-groupby-aggregation/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, check_df, summary
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
emp = pd.read_csv(f"{DATA}/employees.csv")
evt = pd.read_csv(f"{DATA}/security_events.csv")


# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Basic groupby ────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Group employees by department and compute mean salary.
# Result: DataFrame with columns department, avg_salary (rounded to 0).
dept_avg = None  # YOUR CODE HERE — use .agg() with named aggregation + reset_index()

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Count security events by severity.
# Result: DataFrame with columns severity, event_count, sorted by event_count DESC.
sev_counts = None  # YOUR CODE HERE

try:
    check_df(dept_avg, {"rows": 6, "columns": ["department","avg_salary"]}, "1.1 — 6 depts, correct columns")
    check(dept_avg["avg_salary"].dtype.kind in ("f","i"), True, "1.1 — avg_salary is numeric")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    check_df(sev_counts, {"columns": ["severity","event_count"]}, "1.2 — correct columns")
    check(int(sev_counts["event_count"].sum()), 500, "1.2 — total = 500")
    check(sev_counts["event_count"].is_monotonic_decreasing, True, "1.2 — sorted DESC")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: Named Aggregation ────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Per department, compute: headcount, avg_salary (round to 0), min_salary, max_salary.
# Columns: department, headcount, avg_salary, min_salary, max_salary
dept_summary = None  # YOUR CODE HERE

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Per severity level in security_events, compute:
#   event_count, unique_employees (nunique on employee_id), resolved_count (sum of resolved)
# Columns: severity, event_count, unique_employees, resolved_count
sev_summary = None  # YOUR CODE HERE

try:
    check_df(dept_summary, {"rows": 6, "columns": ["department","headcount","avg_salary","min_salary","max_salary"]},
             "2.1 — 6 rows, correct columns")
    check(int(dept_summary["headcount"].sum()), 74, "2.1 — headcounts sum to 74")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    check_df(sev_summary, {"columns": ["severity","event_count","unique_employees","resolved_count"]},
             "2.2 — correct columns")
    check(int(sev_summary["event_count"].sum()), 500, "2.2 — total events = 500")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: transform() vs agg() ────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Add a column dept_avg_salary to emp using transform().
# Then add vs_dept_avg = salary - dept_avg_salary (rounded to 0).
emp_enriched = emp.copy()
emp_enriched["dept_avg_salary"] = None  # YOUR CODE HERE — transform
emp_enriched["vs_dept_avg"]     = None  # YOUR CODE HERE — salary minus dept_avg_salary

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Add a column dept_rank to emp using transform + rank.
# Rank salary within each department, highest salary = rank 1.
# Use method='dense' and ascending=False.
emp_enriched["dept_rank"] = None  # YOUR CODE HERE

try:
    check(len(emp_enriched), 74, "3.1 — still 74 rows after transform")
    check("dept_avg_salary" in emp_enriched.columns, True, "3.1 — dept_avg_salary column exists")
    # Same dept should have same avg
    cyber_avgs = emp_enriched[emp_enriched["department"]=="Cyber"]["dept_avg_salary"].unique()
    check(len(cyber_avgs), 1, "3.1 — all Cyber rows share same dept_avg_salary")
except Exception as e: print(f"  ❌  3.1 — Error: {e}")

try:
    check(emp_enriched["dept_rank"].min(), 1.0, "3.2 — min rank = 1")
    check("dept_rank" in emp_enriched.columns, True, "3.2 — dept_rank column exists")
except Exception as e: print(f"  ❌  3.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: Multi-key GroupBy ────────────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Group by department AND clearance, count employees and compute avg salary.
# Columns: department, clearance, count, avg_salary
# Sort by department, then count DESC.
dept_clearance = None  # YOUR CODE HERE

try:
    check_df(dept_clearance, {"columns": ["department","clearance","count","avg_salary"]},
             "4.1 — correct columns")
    check(int(dept_clearance["count"].sum()), 74, "4.1 — counts sum to 74")
except Exception as e: print(f"  ❌  4.1 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────════════════════════\n")

# Build a department security threat profile.
# Merge emp and evt on employee_id, then groupby department:
#   department, headcount (unique employees), total_events,
#   critical_events (sum where severity==CRITICAL), avg_salary
#
# Add a threat_score column = critical_events / total_events * 100 (rounded to 1)
# Sort by threat_score DESC.
#
# Spiral: merge (preview Lesson 04) + groupby + agg + apply

merged = emp.merge(evt, on="employee_id", how="inner")
threat_profile = None  # YOUR CODE HERE — groupby + agg on merged
# Add threat_score after groupby

try:
    check_df(threat_profile, {
        "columns": ["department","headcount","total_events","critical_events","avg_salary","threat_score"],
        "min_rows": 1,
    }, "Challenge — correct columns")
    if threat_profile is not None:
        check(threat_profile["threat_score"].is_monotonic_decreasing, True,
              "Challenge — sorted by threat_score DESC")
        check((threat_profile["threat_score"] >= 0).all() and (threat_profile["threat_score"] <= 100).all(),
              True, "Challenge — threat_score is between 0 and 100")
        print()
        print(threat_profile.to_string(index=False))
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
