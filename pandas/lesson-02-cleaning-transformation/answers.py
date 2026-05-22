"""Pandas Lesson 02 — Cleaning & Transformation — ANSWER KEY"""
import pandas as pd

nan_counts = emp_dirty.isna().sum()

emp_clean = emp_dirty.copy()
emp_clean["clearance"] = emp_clean["clearance"].fillna("Unknown")
emp_clean["salary"]    = emp_clean["salary"].fillna(emp_clean["salary"].median())

emp_no_nan = emp_clean.dropna()

emp_with_band = emp.copy()
emp_with_band["salary_band"] = emp_with_band["salary"].apply(
    lambda s: "Senior" if s >= 130000 else "Mid" if s >= 100000 else "Junior"
)
emp_with_band["display_label"] = emp_with_band.apply(
    lambda row: f"{row['name']} — {row['department']}", axis=1
)

evt_scored = evt.copy()
severity_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
evt_scored["severity_score"] = evt_scored["severity"].map(severity_map)

emp_renamed = emp.rename(columns={"employee_id": "emp_id", "hire_date": "start_date"})
emp_sorted  = emp.sort_values(["department","salary"], ascending=[True, False])
emp_dates   = emp.copy()
emp_dates["hire_date"] = pd.to_datetime(emp_dates["hire_date"])

# Challenge
clearance_score_map = {"Unknown": 0, "None": 0, "Confidential": 1, "Secret": 2, "Top Secret": 3}
result = emp_dirty.copy()
result["clearance"] = result["clearance"].fillna("Unknown")
result["salary"]    = result["salary"].fillna(result["salary"].median())
result["salary_band"]      = result["salary"].apply(lambda s: "Senior" if s >= 130000 else "Mid" if s >= 100000 else "Junior")
result["clearance_score"]  = result["clearance"].map(clearance_score_map).fillna(0).astype(int)
result = result.sort_values(["clearance_score","salary"], ascending=[False, False])
result = result[["name","department","salary","salary_band","clearance","clearance_score"]]
