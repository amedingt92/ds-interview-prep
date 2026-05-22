"""Python Lesson 05 — Working with Data — ANSWER KEY"""
import json, os
import numpy as np

# 1.1
employees = json.loads(json_str)

# 1.2
ts_employees = [e for e in employees if e["clearance"] == "Top Secret"]

# 1.3
ts_json = json.dumps(ts_employees, indent=2)

# 2.1
cyber_line_count = 0
with open(csv_path) as f:
    for line in f:
        if "Cyber" in line:
            cyber_line_count += 1

# 2.2
with open(tmp_path, "w") as f:
    json.dump(ts_employees, f, indent=2)

with open(tmp_path) as f:
    read_back = json.load(f)

# 3.1
sal_mean = round(float(salaries.mean()), 2)
sal_std  = round(float(salaries.std()), 2)
sal_min  = int(salaries.min())
sal_max  = int(salaries.max())

# 3.2
above_mean = salaries[salaries > salaries.mean()]

# 3.3
raised = np.round(salaries * 1.10).astype(int)

# 4.1
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

# 4.2
def parse_salary(value):
    try:
        return int(value)
    except ValueError:
        return 0

# Challenge
event_dicts = []
with open(events_path) as f:
    lines = f.readlines()
    header = lines[0].strip().split(",")
    for line in lines[1:]:
        values = line.strip().split(",")
        event_dicts.append(dict(zip(header, values)))

total_events   = len(event_dicts)
critical_count = sum(1 for e in event_dicts if e.get("severity") == "CRITICAL")
resolved_count = sum(1 for e in event_dicts if e.get("resolved") == "1")
