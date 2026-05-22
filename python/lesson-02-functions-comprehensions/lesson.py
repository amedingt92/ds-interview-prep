"""
Python Lesson 02 — Functions & Comprehensions
===============================================
Run: python python/lesson-02-functions-comprehensions/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, summary

employees = [
    {"name": "Alex",   "department": "Cyber",       "salary": 140000, "active": True,  "clearance": "Top Secret"},
    {"name": "Jordan", "department": "Engineering", "salary": 95000,  "active": True,  "clearance": "Secret"},
    {"name": "Morgan", "department": "Cyber",       "salary": 115000, "active": False, "clearance": "Top Secret"},
    {"name": "Casey",  "department": "Logistics",   "salary": 72000,  "active": True,  "clearance": "Confidential"},
    {"name": "Riley",  "department": "Cyber",       "salary": 130000, "active": True,  "clearance": "Secret"},
    {"name": "Taylor", "department": "Engineering", "salary": 125000, "active": True,  "clearance": "Top Secret"},
    {"name": "Quinn",  "department": "Intelligence","salary": 88000,  "active": True,  "clearance": "Secret"},
    {"name": "Avery",  "department": "Operations",  "salary": 105000, "active": True,  "clearance": "Confidential"},
]

security_events = [
    {"employee": "Alex",   "event_type": "privilege_escalation", "severity": "CRITICAL"},
    {"employee": "Jordan", "event_type": "login_failure",         "severity": "LOW"},
    {"employee": "Alex",   "event_type": "data_export",           "severity": "HIGH"},
    {"employee": "Riley",  "event_type": "network_scan",          "severity": "MEDIUM"},
    {"employee": "Morgan", "event_type": "anomalous_traffic",     "severity": "HIGH"},
    {"employee": "Casey",  "event_type": "login_success",         "severity": "LOW"},
    {"employee": "Taylor", "event_type": "config_change",         "severity": "MEDIUM"},
    {"employee": "Quinn",  "event_type": "privilege_escalation",  "severity": "HIGH"},
]


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Functions
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Functions ────────────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Write a function get_salary_band(salary) that returns:
#   "Senior" if salary >= 130000
#   "Mid"    if salary >= 100000
#   "Junior" otherwise

def get_salary_band(salary):
    pass  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Write a function summarize_events(*events) that accepts any number of
# event dicts and returns a dict: {severity: count}

def summarize_events(*events):
    pass  # YOUR CODE HERE

check(get_salary_band(140000), "Senior", "1.1 — 140000 = Senior")
check(get_salary_band(115000), "Mid",    "1.1 — 115000 = Mid")
check(get_salary_band(72000),  "Junior", "1.1 — 72000 = Junior")

result = summarize_events(*security_events)
check(result.get("CRITICAL"), 1, "1.2 — 1 CRITICAL event")
check(result.get("HIGH"),     3, "1.2 — 3 HIGH events")
check(result.get("LOW"),      2, "1.2 — 2 LOW events")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — List Comprehensions
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: List Comprehensions ──────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Extract all employee names using a list comprehension.
all_names = None  # YOUR CODE HERE

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Get names of ACTIVE employees only (list comprehension with filter).
active_names = None  # YOUR CODE HERE

# ── Exercise 2.3 ──────────────────────────────────────────────────────────────
# Get salaries of active employees earning over 100000 (list comprehension).
high_salaries = None  # YOUR CODE HERE

# ── Exercise 2.4 ──────────────────────────────────────────────────────────────
# Build a list of (name, salary_band) tuples for all employees.
# Use get_salary_band() from Section 1.
name_bands = None  # YOUR CODE HERE

check(all_names, ["Alex","Jordan","Morgan","Casey","Riley","Taylor","Quinn","Avery"], "2.1 — all names")
check(active_names, ["Alex","Jordan","Casey","Riley","Taylor","Quinn","Avery"], "2.2 — active names only")
check(sorted(high_salaries), sorted([140000,130000,125000,105000]), "2.3 — active salaries > 100k")
check(("Alex","Senior") in name_bands, True, "2.4 — Alex is Senior")
check(("Casey","Junior") in name_bands, True, "2.4 — Casey is Junior")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Dict Comprehensions
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: Dict Comprehensions ──────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Build a dict mapping name → salary for all employees.
salary_lookup = None  # YOUR CODE HERE

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Build a dict mapping name → clearance for Top Secret employees only.
ts_lookup = None  # YOUR CODE HERE

check(salary_lookup.get("Alex"), 140000, "3.1 — Alex salary lookup")
check(salary_lookup.get("Casey"), 72000, "3.1 — Casey salary lookup")
check(set(ts_lookup.keys()), {"Alex","Morgan","Taylor"}, "3.2 — only Top Secret employees")
check(ts_lookup.get("Jordan"), None, "3.2 — Jordan not in ts_lookup (Secret, not Top Secret)")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# 1. Write a function dept_report(employees) that returns a dict:
#    {department: {"count": N, "avg_salary": X, "top_earner": "Name"}}
#    Only include ACTIVE employees.
#
# 2. Using a list comprehension, extract all CRITICAL or HIGH severity
#    event_types from security_events (deduplicate using set()).

def dept_report(employees):
    pass  # YOUR CODE HERE

high_event_types = None  # YOUR CODE HERE (list comprehension + set)

report = dept_report(employees)
check(report["Cyber"]["count"], 2, "Challenge — Cyber active count = 2 (Morgan inactive)")
check(report["Cyber"]["top_earner"], "Alex", "Challenge — Cyber top earner = Alex")
check(report["Engineering"]["avg_salary"], 110000.0, "Challenge — Engineering avg salary")
check(isinstance(high_event_types, set), True, "Challenge — high_event_types is a set")
check("privilege_escalation" in high_event_types, True, "Challenge — privilege_escalation in high events")

summary()
