"""Pandas Lesson 05 — Datetime & Advanced Pandas — ANSWER KEY"""
import pandas as pd

# 1.1
emp_dt = emp.copy()
emp_dt["hire_year"]    = emp_dt["hire_date"].dt.year
emp_dt["hire_month"]   = emp_dt["hire_date"].dt.month
emp_dt["hire_quarter"] = emp_dt["hire_date"].dt.quarter

# 1.2
emp_dt["days_employed"] = (pd.Timestamp("today") - emp_dt["hire_date"]).dt.days

# 2.1
recent_hires = emp[emp["hire_date"] >= "2020-01-01"]

# 2.2
events_by_year = (
    evt.assign(year=evt["timestamp"].dt.year)
    .groupby("year")
    .agg(event_count=("event_id", "count"))
    .reset_index()
    .sort_values("year")
)

# 3.1
evt_indexed = evt.set_index("timestamp")
monthly_counts = evt_indexed["event_id"].resample("ME").count().reset_index()
monthly_counts.columns = ["timestamp", "event_count"]

# 3.2
emp_indexed = emp_dt.set_index("hire_date")
annual_avg_salary = emp_indexed["salary"].resample("YE").mean()

# 4.1
high_tech = emp.query("active == 1 and department in ['Cyber', 'Engineering'] and salary > 100000")

# 4.2
def salary_band(s):
    if s >= 130000: return "Senior"
    if s >= 100000: return "Mid"
    return "Junior"

band_counts = (
    emp
    .query("active == 1")
    .assign(salary_band=lambda x: x["salary"].apply(salary_band))
    .groupby(["department", "salary_band"])
    .agg(headcount=("employee_id", "count"))
    .reset_index()
    .sort_values(["department", "headcount"], ascending=[True, False])
)

# Challenge
time_report = (
    evt
    .assign(
        event_year=evt["timestamp"].dt.year,
        event_month=evt["timestamp"].dt.month,
    )
    .query("severity in ['CRITICAL', 'HIGH']")
    .groupby(["event_year", "severity"])
    .agg(
        event_count=("event_id", "count"),
        unique_employees=("employee_id", "nunique"),
    )
    .reset_index()
    .sort_values(["event_year", "event_count"], ascending=[True, False])
)
