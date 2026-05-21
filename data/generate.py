"""
Seed data generator for ds-interview-prep.
Run once to generate all CSV files used across every lesson.

Usage:
    python data/generate.py
"""

import csv
import random
import datetime
import os

random.seed(2024)
OUT = os.path.dirname(os.path.abspath(__file__))


# ── Helpers ───────────────────────────────────────────────────────────────────

def write_csv(filename, rows, fieldnames=None):
    path = os.path.join(OUT, filename)
    if not rows:
        print(f"  WARNING: no rows for {filename}")
        return
    keys = fieldnames or list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"  {filename:<35} {len(rows)} rows")


def rand_date(start_year=2018, end_year=2024):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + datetime.timedelta(days=random.randint(0, (end - start).days))


def rand_datetime(start_year=2023, end_year=2024):
    d = rand_date(start_year, end_year)
    h = random.randint(0, 23)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return datetime.datetime(d.year, d.month, d.day, h, m, s).isoformat()


# ── Reference data ────────────────────────────────────────────────────────────

DEPARTMENTS = [
    {"department_id": 1, "department_name": "Engineering",   "division": "Technical"},
    {"department_id": 2, "department_name": "Cyber",         "division": "Technical"},
    {"department_id": 3, "department_name": "Intelligence",  "division": "Analytical"},
    {"department_id": 4, "department_name": "Operations",    "division": "Operational"},
    {"department_id": 5, "department_name": "Logistics",     "division": "Operational"},
    {"department_id": 6, "department_name": "Finance",       "division": "Administrative"},
]

DEPT_MAP = {d["department_id"]: d["department_name"] for d in DEPARTMENTS}

ROLES = {
    "Engineering":  ["Systems Engineer", "Software Engineer", "Hardware Analyst", "Integration Engineer"],
    "Cyber":        ["Threat Analyst", "Red Team Operator", "SOC Analyst", "Penetration Tester"],
    "Intelligence": ["Analyst I", "Analyst II", "Senior Analyst", "Lead Analyst"],
    "Operations":   ["Ops Specialist", "Field Coordinator", "Mission Planner", "Program Manager"],
    "Logistics":    ["Coordinator", "Planner", "Supply Specialist", "Logistics Analyst"],
    "Finance":      ["Budget Analyst", "Contracts Specialist", "Financial Analyst", "Auditor"],
}

SALARY_RANGES = {
    "Engineering":  (85000, 145000),
    "Cyber":        (90000, 155000),
    "Intelligence": (70000, 130000),
    "Operations":   (65000, 115000),
    "Logistics":    (55000, 95000),
    "Finance":      (60000, 110000),
}

CLEARANCE_LEVELS = ["None", "Confidential", "Secret", "Top Secret"]
CLEARANCE_WEIGHTS = [0.1, 0.15, 0.45, 0.30]

FIRST_NAMES = [
    "Alex", "Jordan", "Morgan", "Casey", "Riley", "Taylor", "Quinn", "Avery",
    "Parker", "Drew", "Skyler", "Blake", "Cameron", "Reese", "Logan", "Peyton",
    "Harley", "Finley", "Sage", "River", "Dana", "Jamie", "Kendall", "Landen",
    "Micah", "Noel", "Oakley", "Phoenix", "Remy", "Shawn",
]

LAST_NAMES = [
    "Chen", "Martinez", "Johnson", "Williams", "Brown", "Davis", "Miller",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Garcia", "Lee", "Walker", "Hall", "Allen", "Young",
    "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Carter", "Mitchell",
]

CONTRACT_NAMES = [
    "Project Sentinel", "Operation Ironclad", "Initiative Vanguard",
    "Program Nexus", "Contract Apex", "Project Fulcrum", "Operation Keystone",
    "Initiative Rampart", "Program Cipher", "Contract Meridian",
]

EVENT_TYPES = [
    "login_success", "login_failure", "file_access", "privilege_escalation",
    "network_scan", "data_export", "config_change", "service_restart",
    "authentication_bypass", "anomalous_traffic",
]

SEVERITY_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
SEVERITY_WEIGHTS = [0.40, 0.30, 0.20, 0.10]

IP_PREFIXES = ["10.0", "10.1", "172.16", "192.168"]


def rand_ip():
    prefix = random.choice(IP_PREFIXES)
    return f"{prefix}.{random.randint(0,255)}.{random.randint(1,254)}"


# ── employees.csv ─────────────────────────────────────────────────────────────

employees = []
emp_id = 1001
names_used = set()

for dept in DEPARTMENTS:
    dept_name = dept["department_name"]
    lo, hi = SALARY_RANGES[dept_name]
    count = random.randint(8, 14)

    for _ in range(count):
        # Unique name
        for _ in range(100):
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            if name not in names_used:
                names_used.add(name)
                break

        salary = round(random.randint(lo, hi) / 1000) * 1000
        hire_date = rand_date(2016, 2024)
        clearance = random.choices(CLEARANCE_LEVELS, CLEARANCE_WEIGHTS)[0]
        active = random.choices([1, 0], [0.88, 0.12])[0]

        employees.append({
            "employee_id":   emp_id,
            "name":          name,
            "department_id": dept["department_id"],
            "department":    dept_name,
            "role":          random.choice(ROLES[dept_name]),
            "salary":        salary,
            "hire_date":     hire_date.isoformat(),
            "clearance":     clearance,
            "active":        active,
        })
        emp_id += 1

write_csv("employees.csv", employees)


# ── contracts.csv ─────────────────────────────────────────────────────────────

contracts = []
for i, name in enumerate(CONTRACT_NAMES, start=1):
    start = rand_date(2020, 2023)
    duration_days = random.randint(180, 900)
    end = start + datetime.timedelta(days=duration_days)
    value = round(random.randint(500_000, 25_000_000) / 10_000) * 10_000
    dept = random.choice(DEPARTMENTS)
    status = "Active" if end > datetime.date(2024, 6, 1) else "Closed"

    contracts.append({
        "contract_id":     i,
        "contract_name":   name,
        "department_id":   dept["department_id"],
        "department":      dept["department_name"],
        "start_date":      start.isoformat(),
        "end_date":        end.isoformat(),
        "value":           value,
        "status":          status,
    })

write_csv("contracts.csv", contracts)


# ── employee_contracts.csv (junction) ─────────────────────────────────────────

emp_contracts = []
ec_id = 1
for emp in employees:
    # Each employee assigned to 1-3 contracts
    n = random.randint(1, 3)
    chosen = random.sample(contracts, min(n, len(contracts)))
    for c in chosen:
        role_on_contract = random.choice(["Lead", "Contributor", "Reviewer", "Support"])
        emp_contracts.append({
            "assignment_id": ec_id,
            "employee_id":   emp["employee_id"],
            "contract_id":   c["contract_id"],
            "role":          role_on_contract,
            "start_date":    c["start_date"],
        })
        ec_id += 1

write_csv("employee_contracts.csv", emp_contracts)


# ── security_events.csv ───────────────────────────────────────────────────────

events = []
event_id = 5001
active_emps = [e for e in employees if e["active"] == 1]

for _ in range(500):
    emp = random.choice(active_emps)
    event_type = random.choice(EVENT_TYPES)
    severity = random.choices(SEVERITY_LEVELS, SEVERITY_WEIGHTS)[0]
    # High/critical events skew toward certain types
    if severity in ("HIGH", "CRITICAL"):
        event_type = random.choice([
            "privilege_escalation", "authentication_bypass",
            "anomalous_traffic", "data_export", "login_failure"
        ])

    events.append({
        "event_id":    event_id,
        "employee_id": emp["employee_id"],
        "event_type":  event_type,
        "severity":    severity,
        "source_ip":   rand_ip(),
        "dest_ip":     rand_ip(),
        "timestamp":   rand_datetime(2023, 2024),
        "resolved":    random.choices([1, 0], [0.70, 0.30])[0],
    })
    event_id += 1

write_csv("security_events.csv", events)


# ── departments.csv ───────────────────────────────────────────────────────────

write_csv("departments.csv", DEPARTMENTS)


print(f"\nAll seed data written to: {OUT}")
print("Tables: employees, contracts, employee_contracts, security_events, departments")
