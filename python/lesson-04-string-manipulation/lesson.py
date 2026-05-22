"""
Python Lesson 04 — String Manipulation
=========================================
Run: python python/lesson-04-string-manipulation/lesson.py
"""

import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, summary

raw_events = [
    "  login_failure:LOW:10.0.1.5  ",
    "privilege_escalation:CRITICAL:172.16.3.44",
    "  file_access:MEDIUM:192.168.0.12  ",
    "anomalous_traffic:HIGH:10.1.255.3",
    "login_success:LOW:10.0.1.5",
    "data_export:HIGH:172.16.8.99  ",
]

log_line = "2024-03-15T14:32:01 | employee_id=1042 | event=privilege_escalation | severity=CRITICAL | src_ip=10.0.45.23 | dest_ip=192.168.1.100"


# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: String Methods ───────────────────────────────────────────\n")

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Parse raw_events into a list of dicts with keys: event_type, severity, ip
# Steps: strip whitespace, then split on ":"
parsed = []
# YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# From parsed, build a formatted string for each event:
# "EVENT_TYPE (severity) from IP"  — event_type in uppercase
# Example: "LOGIN_FAILURE (LOW) from 10.0.1.5"
formatted = []
# YOUR CODE HERE (list comprehension + f-string)

try:
    check(len(parsed), 6, "1.1 — 6 parsed events")
    check(parsed[0]["event_type"], "login_failure", "1.1 — event_type stripped and parsed")
    check(parsed[0]["severity"], "LOW", "1.1 — severity correct")
    check(parsed[0]["ip"], "10.0.1.5", "1.1 — ip correct")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    check(formatted[0], "LOGIN_FAILURE (LOW) from 10.0.1.5", "1.2 — formatted string correct")
    check(all("from" in f for f in formatted), True, "1.2 — all entries have 'from'")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: f-Strings ────────────────────────────────────────────────\n")

employees = [
    {"name": "Alex Chen", "salary": 140000, "department": "Cyber"},
    {"name": "Casey Brown", "salary": 72000, "department": "Logistics"},
]

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# For each employee build a label: "Name — Department — $SALARY"
# with salary formatted with commas. Example: "Alex Chen — Cyber — $140,000"
labels = None  # YOUR CODE HERE

check(labels[0], "Alex Chen — Cyber — $140,000", "2.1 — formatted label with commas")
check(labels[1], "Casey Brown — Logistics — $72,000", "2.1 — second label")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: Regex ────────────────────────────────────────────────────\n")

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Extract the employee_id value from log_line using re.search.
emp_id = None  # YOUR CODE HERE — should be the string "1042"

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Extract BOTH IP addresses from log_line using re.findall.
ips = None  # YOUR CODE HERE — should be a list of 2 IP strings

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Replace all underscores in log_line with spaces using re.sub.
cleaned = None  # YOUR CODE HERE

check(emp_id, "1042", "3.1 — employee_id extracted")
check(sorted(ips), sorted(["10.0.45.23","192.168.1.100"]), "3.2 — both IPs extracted")
check("privilege escalation" in cleaned, True, "3.3 — underscores replaced with spaces")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Parse all raw_events into structured dicts (reuse parsed from 1.1),
# then filter to HIGH/CRITICAL events and build a report string per event:
# "ALERT: EVENT_TYPE from IP_PREFIX.x.x (SEVERITY)"
# where IP_PREFIX is just the first two octets of the IP.
# Example: "ALERT: PRIVILEGE_ESCALATION from 172.16.x.x (CRITICAL)"

alerts = []
# YOUR CODE HERE

check(len(alerts) > 0, True, "Challenge — at least one alert generated")
if alerts:
    check(all(a.startswith("ALERT:") for a in alerts), True, "Challenge — all start with ALERT:")
    check(all("x.x" in a for a in alerts), True, "Challenge — all have IP_PREFIX.x.x format")
    check(all("CRITICAL" in a or "HIGH" in a for a in alerts), True, "Challenge — only HIGH/CRITICAL")
    for a in alerts:
        print(" ", a)

summary()
