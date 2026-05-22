"""Python Lesson 02 — Functions & Comprehensions — ANSWER KEY"""

def get_salary_band(salary):
    if salary >= 130000:
        return "Senior"
    elif salary >= 100000:
        return "Mid"
    else:
        return "Junior"

def summarize_events(*events):
    counts = {}
    for event in events:
        sev = event["severity"]
        counts[sev] = counts.get(sev, 0) + 1
    return counts

# 2.1
all_names = [e["name"] for e in employees]

# 2.2
active_names = [e["name"] for e in employees if e["active"]]

# 2.3
high_salaries = [e["salary"] for e in employees if e["active"] and e["salary"] > 100000]

# 2.4
name_bands = [(e["name"], get_salary_band(e["salary"])) for e in employees]

# 3.1
salary_lookup = {e["name"]: e["salary"] for e in employees}

# 3.2
ts_lookup = {e["name"]: e["clearance"] for e in employees if e["clearance"] == "Top Secret"}

# Challenge
def dept_report(employees):
    active = [e for e in employees if e["active"]]
    depts = {}
    for emp in active:
        dept = emp["department"]
        if dept not in depts:
            depts[dept] = []
        depts[dept].append(emp)
    report = {}
    for dept, emps in depts.items():
        salaries = [e["salary"] for e in emps]
        top = max(emps, key=lambda e: e["salary"])
        report[dept] = {
            "count": len(emps),
            "avg_salary": round(sum(salaries) / len(salaries), 0),
            "top_earner": top["name"],
        }
    return report

high_event_types = set([e["event_type"] for e in security_events if e["severity"] in ("HIGH","CRITICAL")])
