"""Python Lesson 03 — Lambda, Map, Filter — ANSWER KEY"""

by_salary_desc      = sorted(employees, key=lambda e: e["salary"], reverse=True)
by_dept_then_salary = sorted(employees, key=lambda e: (e["department"], -e["salary"]))
severity_order      = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
by_severity         = sorted(events, key=lambda e: severity_order[e["severity"]])
raised_salaries     = list(map(lambda s: round(s * 1.10), salaries))
emp_names           = list(map(lambda e: e["name"], employees))
upper_events        = list(map(lambda e: e["event_type"].upper(), events))
active_employees    = list(filter(lambda e: e["active"], employees))
high_critical       = list(filter(lambda e: e["severity"] in ("HIGH","CRITICAL"), events))
avg                 = sum(salaries) / len(salaries)
above_avg           = list(filter(lambda e: e["salary"] > avg, employees))

# Challenge
step1 = list(filter(lambda e: e["active"], employees))
step2 = list(map(lambda e: {**e, "salary": round(e["salary"] * 1.15)}, step1))
step3 = list(map(lambda e: (e["name"], e["salary"]), step2))
step4 = sorted(step3, key=lambda t: t[1], reverse=True)
