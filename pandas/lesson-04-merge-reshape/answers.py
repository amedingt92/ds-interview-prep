"""Pandas Lesson 04 — Merge & Reshape — ANSWER KEY"""
import pandas as pd

# 1.1
emp_with_div = (
    pd.merge(emp, dept[["department_id","division"]], on="department_id", how="inner")
    [["name","department","division","salary"]]
)

# 1.2
left = pd.merge(emp[["employee_id","name","department"]], ec[["employee_id","contract_id"]], on="employee_id", how="left")
no_contract = left[left["contract_id"].isna()][["name","department"]]

# 1.3
step1 = pd.merge(emp[["employee_id","name","department"]], ec[["employee_id","contract_id"]], on="employee_id")
step2 = pd.merge(step1, con[["contract_id","contract_name","value","status"]], on="contract_id")
emp_contracts = step2[step2["status"] == "Active"][["name","department","contract_name","value","status"]]

# 2.1
recombined = pd.concat([active_df, inactive_df], ignore_index=True)

# 2.2
emp_extended = pd.concat([emp, new_hires], ignore_index=True)

# 3.1
clearance_pivot = pd.pivot_table(
    emp, values="employee_id", index="department",
    columns="clearance", aggfunc="count", fill_value=0
)

# 3.2
resolved_pivot = pd.pivot_table(
    evt, values="event_id", index="severity",
    columns="resolved", aggfunc="count", fill_value=0
)

# 4.1
salary_long = pd.melt(
    salary_wide,
    id_vars=["department"],
    value_vars=["2022_avg","2023_avg","2024_avg"],
    var_name="year",
    value_name="avg_salary",
)

# Challenge
m1 = pd.merge(emp, dept[["department_id","division"]], on="department_id", how="inner")
m2 = pd.merge(m1, evt, on="employee_id", how="left")
division_profile = (
    m2.groupby("division")
    .agg(
        headcount=("employee_id_x", "nunique"),
        total_events=("event_id", "count"),
        critical_count=("severity", lambda x: (x == "CRITICAL").sum()),
        avg_salary=("salary", lambda x: round(x.mean(), 0)),
    )
    .reset_index()
)
division_profile["pct_critical"] = (
    (division_profile["critical_count"] / division_profile["total_events"] * 100)
    .round(1)
    .fillna(0)
)
division_profile = division_profile.sort_values("pct_critical", ascending=False)
