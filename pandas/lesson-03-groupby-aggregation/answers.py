"""Pandas Lesson 03 — GroupBy & Aggregation — ANSWER KEY"""
import pandas as pd

# 1.1
dept_avg = (
    emp.groupby("department")
    .agg(avg_salary=("salary", lambda x: round(x.mean(), 0)))
    .reset_index()
)

# 1.2
sev_counts = (
    evt.groupby("severity")
    .agg(event_count=("event_id", "count"))
    .reset_index()
    .sort_values("event_count", ascending=False)
)

# 2.1
dept_summary = (
    emp.groupby("department")
    .agg(
        headcount=("employee_id", "count"),
        avg_salary=("salary", lambda x: round(x.mean(), 0)),
        min_salary=("salary", "min"),
        max_salary=("salary", "max"),
    )
    .reset_index()
)

# 2.2
sev_summary = (
    evt.groupby("severity")
    .agg(
        event_count=("event_id", "count"),
        unique_employees=("employee_id", "nunique"),
        resolved_count=("resolved", "sum"),
    )
    .reset_index()
)

# 3.1
emp_enriched = emp.copy()
emp_enriched["dept_avg_salary"] = emp_enriched.groupby("department")["salary"].transform("mean")
emp_enriched["vs_dept_avg"]     = (emp_enriched["salary"] - emp_enriched["dept_avg_salary"]).round(0)

# 3.2
emp_enriched["dept_rank"] = (
    emp_enriched.groupby("department")["salary"]
    .transform(lambda x: x.rank(method="dense", ascending=False))
)

# 4.1
dept_clearance = (
    emp.groupby(["department", "clearance"])
    .agg(
        count=("employee_id", "count"),
        avg_salary=("salary", lambda x: round(x.mean(), 0)),
    )
    .reset_index()
    .sort_values(["department", "count"], ascending=[True, False])
)

# Challenge
merged = emp.merge(evt, on="employee_id", how="inner")
threat_profile = (
    merged.groupby("department")
    .agg(
        headcount=("employee_id", "nunique"),
        total_events=("event_id", "count"),
        critical_events=("severity", lambda x: (x == "CRITICAL").sum()),
        avg_salary=("salary", lambda x: round(x.mean(), 0)),
    )
    .reset_index()
)
threat_profile["threat_score"] = (
    (threat_profile["critical_events"] / threat_profile["total_events"] * 100).round(1)
)
threat_profile = threat_profile.sort_values("threat_score", ascending=False)
