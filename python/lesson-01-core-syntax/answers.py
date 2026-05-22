"""Python Lesson 01 — Core Syntax — ANSWER KEY"""

# 1.1
first_event = events[0]
last_event  = events[-1]

# 1.2
middle_three = events[1:4]

# 1.3
has_network_scan = "network_scan" in events

# 1.4
high_risk = []
for event in events:
    if "privilege" in event or "escalation" in event:
        high_risk.append(event)

# 2.1
emp_name   = employee["name"]
emp_salary = employee["salary"]

# 2.2
manager = employee.get("manager", "Unknown")

# 2.3
employee["salary_band"] = "Mid"

# 2.4
emp_keys = list(employee.keys())

# 3.1
unique_clearances = set(all_clearances)

# 3.2
missing_clearances = required - available_on_team

# 3.3
overlap = required & available_on_team

# 4.1
unresolved_high = 0
for event in security_events:
    if event["severity"] in ("HIGH", "CRITICAL") and not event["resolved"]:
        unresolved_high += 1

# 4.2
severity_counts = {}
for event in security_events:
    sev = event["severity"]
    severity_counts[sev] = severity_counts.get(sev, 0) + 1

# 4.3
unresolved_types = []
for event in security_events:
    if not event["resolved"]:
        unresolved_types.append(event["event_type"])

# Challenge
dept_salaries = {}
for emp in employees:
    if emp["active"]:
        dept = emp["department"]
        if dept not in dept_salaries:
            dept_salaries[dept] = []
        dept_salaries[dept].append(emp["salary"])

dept_avg = {}
for dept, salaries in dept_salaries.items():
    dept_avg[dept] = round(sum(salaries) / len(salaries), 0)
