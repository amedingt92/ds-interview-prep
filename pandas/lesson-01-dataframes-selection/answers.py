"""Pandas Lesson 01 — DataFrames & Selection — ANSWER KEY"""

unique_dept_count     = emp["department"].nunique()
most_common_clearance = emp["clearance"].value_counts().index[0]
name_dept_sal         = emp[["name","department","salary"]]
clearance_values      = emp["clearance"].unique().tolist()
first_salary_iloc     = emp.iloc[0, emp.columns.get_loc("salary")]
first_name_loc        = emp.loc[0, "name"]
first_3x3             = emp.iloc[0:3, 0:3]
cyber_df              = emp[emp["department"] == "Cyber"]
active_high_earners   = emp[(emp["active"] == 1) & (emp["salary"] >= 100000)]
ts_tech               = emp[emp["department"].isin(["Cyber","Engineering"]) & (emp["clearance"] == "Top Secret")]
analysts              = emp[emp["role"].str.contains("Analyst")]

# Challenge
high_critical_events = evt[evt["severity"].isin(["HIGH","CRITICAL"])]
trimmed              = high_critical_events[["event_id","employee_id","event_type","severity","resolved"]]
unresolved_count     = int((trimmed["resolved"] == 0).sum())
