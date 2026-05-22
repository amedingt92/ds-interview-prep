"""
Python Lesson 01 — Core Syntax & Data Types
=============================================
Read README.md first, then complete each exercise.
Run: python python/lesson-01-core-syntax/lesson.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, summary


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Lists
# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: Lists ────────────────────────────────────────────────────\n")

events = ["login_failure", "file_access", "privilege_escalation", "network_scan", "data_export"]

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Get the first and last element of the events list.
first_event = None  # YOUR CODE HERE
last_event  = None  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# Slice the list to get only the middle three events (index 1, 2, 3).
middle_three = None  # YOUR CODE HERE

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Check whether "network_scan" is in the events list. Result should be True/False.
has_network_scan = None  # YOUR CODE HERE

# ── Exercise 1.4 ──────────────────────────────────────────────────────────────
# Using a loop, build a new list called high_risk that contains only events
# from the events list that contain the word "privilege" or "escalation".
high_risk = []
# YOUR CODE HERE (loop + if + append)

check(first_event, "login_failure", "1.1 — first element")
check(last_event, "data_export", "1.1 — last element", hint="Use index -1")
check(middle_three, ["file_access","privilege_escalation","network_scan"], "1.2 — middle three slice", hint="events[1:4]")
check(has_network_scan, True, "1.3 — 'network_scan' in events")
check(high_risk, ["privilege_escalation"], "1.4 — high_risk list", hint="Check if 'privilege' in event or 'escalation' in event")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Dictionaries
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: Dictionaries ─────────────────────────────────────────────\n")

employee = {
    "name":       "Alex Chen",
    "department": "Cyber",
    "salary":     120000,
    "clearance":  "Top Secret",
    "active":     True,
}

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Get the employee's name and salary from the dict.
emp_name   = None  # YOUR CODE HERE
emp_salary = None  # YOUR CODE HERE

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Safely get the "manager" key. If it doesn't exist, return "Unknown".
manager = None  # YOUR CODE HERE (use .get())

# ── Exercise 2.3 ──────────────────────────────────────────────────────────────
# Add a new key "salary_band" with value "Senior" (since salary >= 130000 is
# Senior, 100000-129999 is Mid, else Junior — this employee earns 120000).
# YOUR CODE HERE

# ── Exercise 2.4 ──────────────────────────────────────────────────────────────
# Build a list of all KEYS in the employee dict.
emp_keys = None  # YOUR CODE HERE

check(emp_name, "Alex Chen", "2.1 — employee name")
check(emp_salary, 120000, "2.1 — employee salary")
check(manager, "Unknown", "2.2 — missing key returns default", hint="employee.get('manager', 'Unknown')")
check(employee.get("salary_band"), "Mid", "2.3 — salary_band added correctly",
      hint="120000 is between 100000 and 129999 → 'Mid'")
check(isinstance(emp_keys, list), True, "2.4 — emp_keys is a list", hint="list(employee.keys())")
check("name" in emp_keys, True, "2.4 — 'name' is in emp_keys")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Sets
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: Sets ─────────────────────────────────────────────────────\n")

all_clearances    = ["Secret", "Top Secret", "Secret", "Confidential", "Top Secret", "None", "Secret"]
required          = {"Secret", "Top Secret"}
available_on_team = {"Top Secret", "Confidential", "None"}

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Convert all_clearances to a set to get unique values.
unique_clearances = None  # YOUR CODE HERE

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Find clearances that are REQUIRED but NOT available on the team (set difference).
missing_clearances = None  # YOUR CODE HERE

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Find clearances that exist in BOTH required and available_on_team (intersection).
overlap = None  # YOUR CODE HERE

check(unique_clearances, {"Secret","Top Secret","Confidential","None"}, "3.1 — unique clearances set")
check(missing_clearances, {"Secret"}, "3.2 — missing clearances", hint="required - available_on_team")
check(overlap, {"Top Secret"}, "3.3 — overlap", hint="required & available_on_team")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Conditionals and Loops
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: Conditionals and Loops ───────────────────────────────────\n")

security_events = [
    {"event_type": "login_failure",       "severity": "LOW",      "resolved": False},
    {"event_type": "privilege_escalation","severity": "CRITICAL",  "resolved": False},
    {"event_type": "file_access",         "severity": "MEDIUM",   "resolved": True},
    {"event_type": "anomalous_traffic",   "severity": "HIGH",     "resolved": False},
    {"event_type": "login_success",       "severity": "LOW",      "resolved": True},
]

# ── Exercise 4.1 ──────────────────────────────────────────────────────────────
# Using a loop, count how many events have severity "HIGH" or "CRITICAL"
# AND are NOT resolved.
unresolved_high = 0
# YOUR CODE HERE

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# Build a dict that maps each severity level to a count of how many
# events have that severity.
# Expected: {"LOW": 2, "CRITICAL": 1, "MEDIUM": 1, "HIGH": 1}
severity_counts = {}
# YOUR CODE HERE

# ── Exercise 4.3 ──────────────────────────────────────────────────────────────
# Build a list of event_type strings for all UNRESOLVED events only.
unresolved_types = []
# YOUR CODE HERE

check(unresolved_high, 2, "4.1 — 2 unresolved HIGH/CRITICAL events")
check(severity_counts, {"LOW":2,"CRITICAL":1,"MEDIUM":1,"HIGH":1}, "4.2 — severity counts dict")
check(sorted(unresolved_types), sorted(["login_failure","privilege_escalation","anomalous_traffic"]),
      "4.3 — unresolved event types")


# ══════════════════════════════════════════════════════════════════════════════
# MINI CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

employees = [
    {"name": "Alex",   "department": "Cyber",       "salary": 140000, "active": True},
    {"name": "Jordan", "department": "Engineering", "salary": 95000,  "active": True},
    {"name": "Morgan", "department": "Cyber",       "salary": 115000, "active": False},
    {"name": "Casey",  "department": "Logistics",   "salary": 72000,  "active": True},
    {"name": "Riley",  "department": "Cyber",       "salary": 130000, "active": True},
    {"name": "Taylor", "department": "Engineering", "salary": 125000, "active": True},
]

# Using loops and conditionals (no list comprehensions yet — that's next lesson):
#
# 1. Build dept_salaries: a dict mapping department → list of salaries
#    for ACTIVE employees only.
#    Expected: {"Cyber": [140000, 130000], "Engineering": [95000, 125000], "Logistics": [72000]}
#
# 2. Build dept_avg: a dict mapping department → average salary (rounded to 0 decimal)
#    from dept_salaries.
#    Expected: {"Cyber": 135000.0, "Engineering": 110000.0, "Logistics": 72000.0}

dept_salaries = {}
# YOUR CODE HERE

dept_avg = {}
# YOUR CODE HERE

check(dept_salaries.get("Cyber"), [140000, 130000], "Challenge — Cyber salaries (active only)")
check(dept_salaries.get("Engineering"), [95000, 125000], "Challenge — Engineering salaries")
check(dept_salaries.get("Logistics"), [72000], "Challenge — Logistics salaries")
check(dept_avg.get("Cyber"), 135000.0, "Challenge — Cyber avg salary")
check(dept_avg.get("Engineering"), 110000.0, "Challenge — Engineering avg salary")

summary()
