"""
Python Lesson 03 — Lambda, Map, Filter
=========================================
Run: python python/lesson-03-lambda-map-filter/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, summary

employees = [
    {"name": "Alex",   "department": "Cyber",       "salary": 140000, "active": True},
    {"name": "Jordan", "department": "Engineering", "salary": 95000,  "active": True},
    {"name": "Morgan", "department": "Cyber",       "salary": 115000, "active": False},
    {"name": "Casey",  "department": "Logistics",   "salary": 72000,  "active": True},
    {"name": "Riley",  "department": "Cyber",       "salary": 130000, "active": True},
    {"name": "Taylor", "department": "Engineering", "salary": 125000, "active": True},
]

salaries = [140000, 95000, 115000, 72000, 130000, 125000]

events = [
    {"event_type": "login_failure",        "severity": "LOW"},
    {"event_type": "privilege_escalation", "severity": "CRITICAL"},
    {"event_type": "file_access",          "severity": "MEDIUM"},
    {"event_type": "anomalous_traffic",    "severity": "HIGH"},
    {"event_type": "login_success",        "severity": "LOW"},
    {"event_type": "data_export",          "severity": "HIGH"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Lambda + sorted()
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Lambda + sorted() ────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Sort employees by salary descending using sorted() + lambda.
by_salary_desc = None  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Sort employees by department ASC, then salary DESC (within department).
by_dept_then_salary = None  # YOUR CODE HERE

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Sort events by severity in this order: CRITICAL, HIGH, MEDIUM, LOW
# Hint: define a priority dict, use it in the lambda key
severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
by_severity = None  # YOUR CODE HERE

check(by_salary_desc[0]["name"], "Alex", "1.1 — highest salary first (Alex)")
check(by_salary_desc[-1]["name"], "Casey", "1.1 — lowest salary last (Casey)")
check(by_dept_then_salary[0]["department"], "Cyber", "1.2 — Cyber first (alphabetically)")
cyber_rows = [e for e in by_dept_then_salary if e["department"] == "Cyber"]
check(cyber_rows[0]["name"], "Alex", "1.2 — Alex is highest Cyber salary")
check(by_severity[0]["severity"], "CRITICAL", "1.3 — CRITICAL first")
check(by_severity[-1]["severity"], "LOW", "1.3 — LOW last")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — map()
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: map() ────────────────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Apply a 10% raise to every salary using map() + lambda.
# Round to nearest integer.
raised_salaries = None  # YOUR CODE HERE (wrap in list())

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Using map(), extract the "name" field from every employee dict.
emp_names = None  # YOUR CODE HERE

# ── Exercise 2.3 ──────────────────────────────────────────────────────────────
# Using map(), convert every event_type string to UPPERCASE.
upper_events = None  # YOUR CODE HERE

check(raised_salaries[0], 154000, "2.1 — 140000 * 1.1 = 154000")
check(raised_salaries[3], 79200, "2.1 — 72000 * 1.1 = 79200")
check(emp_names, ["Alex","Jordan","Morgan","Casey","Riley","Taylor"], "2.2 — employee names via map")
check(upper_events[0], "LOGIN_FAILURE", "2.3 — uppercase event type")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — filter()
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: filter() ─────────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Use filter() to get only active employees.
active_employees = None  # YOUR CODE HERE (wrap in list())

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Use filter() to get only HIGH or CRITICAL severity events.
high_critical = None  # YOUR CODE HERE

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Use filter() to get employees earning above the average salary.
avg = sum(salaries) / len(salaries)
above_avg = None  # YOUR CODE HERE

check(len(active_employees), 5, "3.1 — 5 active employees")
check(all(e["active"] for e in active_employees), True, "3.1 — all active")
check(len(high_critical), 3, "3.2 — 3 HIGH/CRITICAL events")
check(all(e["severity"] in ("HIGH","CRITICAL") for e in high_critical), True, "3.2 — all HIGH/CRITICAL")
check(all(e["salary"] > avg for e in above_avg), True, "3.3 — all above average salary")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE — Spiral: lambda + map + filter + comprehensions (Lesson 02)
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Using ONLY map(), filter(), and lambda (no comprehensions for this challenge):
# 1. Filter to active employees only
# 2. Apply a 15% raise to their salaries
# 3. Extract just the (name, new_salary) as a list of tuples
# 4. Sort by new_salary descending

step1 = None  # filter — active only
step2 = None  # map — apply 15% raise, round to int, store back in dict
step3 = None  # map — extract (name, new_salary) tuples
step4 = None  # sorted — by new_salary desc

check(len(step1), 5, "Challenge step1 — 5 active employees")
if step2:
    check(list(step2)[0]["salary"], round(employees[0]["salary"] * 1.15),
          "Challenge step2 — salary updated with 15% raise",
          hint="The raised salary should be stored in the dict")
if step4:
    result = list(step4)
    check(result[0][0], "Alex", "Challenge step4 — Alex has highest raised salary")
    check(result[0][1], round(140000 * 1.15), "Challenge step4 — Alex raised salary correct")

summary()
