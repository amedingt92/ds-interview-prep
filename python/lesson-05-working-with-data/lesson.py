"""
Python Lesson 05 — Working with Data
=======================================
Run: python python/lesson-05-working-with-data/lesson.py
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from checker import check, summary
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

# ══════════════════════════════════════════════════════════════════════════════
print("── Section 1: JSON ─────────────────────────────────────────────────────\n")

json_str = '''[
  {"employee_id": 1001, "name": "Alex Chen",   "salary": 140000, "clearance": "Top Secret"},
  {"employee_id": 1002, "name": "Jordan Smith", "salary": 95000,  "clearance": "Secret"},
  {"employee_id": 1003, "name": "Riley Jones",  "salary": 130000, "clearance": "Top Secret"},
  {"employee_id": 1004, "name": "Casey Brown",  "salary": 72000,  "clearance": "Confidential"}
]'''

# ── Exercise 1.1 ──────────────────────────────────────────────────────────────
# Parse json_str into a Python list of dicts.
employees = None  # YOUR CODE HERE

# ── Exercise 1.2 ──────────────────────────────────────────────────────────────
# From employees, build a new list containing only Top Secret employees.
ts_employees = None  # YOUR CODE HERE (list comprehension)

# ── Exercise 1.3 ──────────────────────────────────────────────────────────────
# Convert ts_employees back to a JSON string (pretty-printed, indent=2).
ts_json = None  # YOUR CODE HERE

try:
    check(isinstance(employees, list), True, "1.1 — parsed to list")
    check(len(employees), 4, "1.1 — 4 employees")
    check(employees[0]["name"], "Alex Chen", "1.1 — first employee name")
except Exception as e: print(f"  ❌  1.1 — Error: {e}")

try:
    check(len(ts_employees), 2, "1.2 — 2 Top Secret employees")
    check(all(e["clearance"] == "Top Secret" for e in ts_employees), True, "1.2 — all Top Secret")
except Exception as e: print(f"  ❌  1.2 — Error: {e}")

try:
    parsed_back = json.loads(ts_json)
    check(len(parsed_back), 2, "1.3 — JSON round-trips back to 2 items")
except Exception as e: print(f"  ❌  1.3 — Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 2: File I/O ─────────────────────────────────────────────────\n")

# ── Exercise 2.1 ──────────────────────────────────────────────────────────────
# Read the employees.csv file line by line (no pandas).
# Count how many lines contain the word "Cyber" (including header if present).
cyber_line_count = 0
csv_path = os.path.join(DATA_DIR, "employees.csv")
# YOUR CODE HERE (open file, loop over lines, check if "Cyber" in line)

# ── Exercise 2.2 ──────────────────────────────────────────────────────────────
# Write ts_employees to a temp JSON file, then read it back and verify.
tmp_path = os.path.join(os.path.dirname(__file__), "tmp_output.json")
# Write ts_employees to tmp_path using json.dump
# YOUR CODE HERE

# Read it back
read_back = None
# YOUR CODE HERE (open and json.load)

try:
    check(cyber_line_count > 0, True, "2.1 — found Cyber lines in CSV")
except Exception as e: print(f"  ❌  2.1 — Error: {e}")

try:
    if read_back:
        check(len(read_back), 2, "2.2 — file written and read back correctly")
        check(read_back[0]["name"], "Alex Chen", "2.2 — first employee intact")
except Exception as e: print(f"  ❌  2.2 — Error: {e}")

# Clean up temp file
if os.path.exists(tmp_path):
    os.remove(tmp_path)


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 3: NumPy ────────────────────────────────────────────────────\n")

salaries = np.array([140000, 95000, 115000, 72000, 130000, 125000, 88000, 105000])

# ── Exercise 3.1 ──────────────────────────────────────────────────────────────
# Compute mean, std, min, max of salaries. Round mean and std to 2 decimal places.
sal_mean = None
sal_std  = None
sal_min  = None
sal_max  = None

# ── Exercise 3.2 ──────────────────────────────────────────────────────────────
# Using boolean indexing, get only salaries above the mean.
above_mean = None

# ── Exercise 3.3 ──────────────────────────────────────────────────────────────
# Apply a 10% raise to ALL salaries (broadcasting) and round to nearest int.
raised = None

check(sal_mean, round(float(salaries.mean()), 2), "3.1 — mean correct")
check(sal_min, int(salaries.min()), "3.1 — min = 72000")
check(sal_max, int(salaries.max()), "3.1 — max = 140000")
check(len(above_mean), int((salaries > salaries.mean()).sum()), "3.2 — correct count above mean")
check(all(above_mean > salaries.mean()), True, "3.2 — all values above mean")
check(int(raised[0]), round(140000 * 1.10), "3.3 — 10% raise applied")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Section 4: Error Handling ───────────────────────────────────────────\n")

# ── Exercise 4.1 ──────────────────────────────────────────════════════════════
# Write a function safe_divide(a, b) that returns a/b,
# but returns None (not crash) if b is 0.
def safe_divide(a, b):
    pass  # YOUR CODE HERE

# ── Exercise 4.2 ──────────────────────────────────────────────────────────────
# Write a function parse_salary(value) that tries to convert value to int.
# If it fails (ValueError), return 0.
def parse_salary(value):
    pass  # YOUR CODE HERE

check(safe_divide(10, 2), 5.0, "4.1 — 10/2 = 5.0")
check(safe_divide(10, 0), None, "4.1 — division by zero returns None")
check(parse_salary("95000"), 95000, "4.2 — valid string converts to int")
check(parse_salary("N/A"), 0, "4.2 — invalid string returns 0")


# ══════════════════════════════════════════════════════════════════════════════
print("\n── Mini Challenge ──────────────────────────────────────────────────────\n")

# Read the security_events.csv file using only built-in Python (no pandas/csv module).
# Parse it manually into a list of dicts using the header row as keys.
# Then compute using NumPy:
#   - total event count
#   - count of CRITICAL events
#   - count of resolved events (resolved == '1')
#
# Spiral: file I/O + JSON + NumPy + comprehensions

events_path = os.path.join(DATA_DIR, "security_events.csv")
event_dicts = []
# YOUR CODE HERE — read file, parse header, build list of dicts

total_events    = None
critical_count  = None
resolved_count  = None
# YOUR CODE HERE — use numpy or list comprehensions to compute counts

try:
    check(len(event_dicts), 500, "Challenge — 500 events parsed")
    check(total_events, 500, "Challenge — total_events = 500")
    check(critical_count > 0, True, "Challenge — some CRITICAL events")
    check(resolved_count > 0, True, "Challenge — some resolved events")
    print(f"\n  Total: {total_events} | Critical: {critical_count} | Resolved: {resolved_count}")
except Exception as e: print(f"  ❌  Challenge — Error: {e}")

summary()
