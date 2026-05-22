"""Python Lesson 04 — String Manipulation — ANSWER KEY"""
import re

# 1.1
parsed = []
for raw in raw_events:
    parts = raw.strip().split(":")
    parsed.append({"event_type": parts[0], "severity": parts[1], "ip": parts[2]})

# 1.2
formatted = [f"{e['event_type'].upper()} ({e['severity']}) from {e['ip']}" for e in parsed]

# 2.1
labels = [f"{e['name']} — {e['department']} — ${e['salary']:,}" for e in employees]

# 3.1
m = re.search(r"employee_id=(\d+)", log_line)
emp_id = m.group(1) if m else None

# 3.2
ips = re.findall(r"\d+\.\d+\.\d+\.\d+", log_line)

# 3.3
cleaned = re.sub(r"_", " ", log_line)

# Challenge
alerts = []
for e in parsed:
    if e["severity"] in ("HIGH", "CRITICAL"):
        octets = e["ip"].split(".")
        prefix = ".".join(octets[:2])
        alerts.append(f"ALERT: {e['event_type'].upper()} from {prefix}.x.x ({e['severity']})")
