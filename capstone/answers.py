"""
CAPSTONE — ANSWER KEY
======================
⚠️  Attempt everything yourself first.
"""

# ─── SECTION A — SQL ──────────────────────────────────────────────────────────

sql_a1 = """
SELECT
    department,
    COUNT(*) AS headcount,
    ROUND(AVG(salary), 0) AS avg_salary,
    SUM(CASE WHEN clearance = 'Top Secret' THEN 1 ELSE 0 END) AS top_secret_count
FROM employees
GROUP BY department
ORDER BY headcount DESC
"""

sql_a2 = """
WITH ranked AS (
    SELECT name, department, salary,
           DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
    FROM employees
)
SELECT name, department, salary, dept_rank
FROM ranked
WHERE dept_rank <= 2
"""

sql_a3 = """
SELECT
    e.name,
    e.department,
    d.division,
    COUNT(se.event_id) AS event_count
FROM employees e
INNER JOIN departments d     ON e.department_id  = d.department_id
LEFT JOIN  security_events se ON e.employee_id   = se.employee_id
GROUP BY e.name, e.department, d.division
ORDER BY event_count DESC
"""

sql_a4 = """
SELECT
    name, department, salary, hire_date,
    SUM(salary) OVER (PARTITION BY department ORDER BY hire_date) AS running_dept_salary
FROM employees
ORDER BY department, hire_date
"""

sql_a5 = """
SELECT
    e.department,
    COUNT(se.event_id) AS total_events,
    SUM(CASE WHEN se.severity = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_events,
    ROUND(SUM(CASE WHEN se.severity = 'CRITICAL' THEN 1 ELSE 0 END) * 100.0 / COUNT(se.event_id), 1) AS critical_pct
FROM employees e
INNER JOIN security_events se ON e.employee_id = se.employee_id
GROUP BY e.department
HAVING ROUND(SUM(CASE WHEN se.severity = 'CRITICAL' THEN 1 ELSE 0 END) * 100.0 / COUNT(se.event_id), 1) > 15
ORDER BY critical_pct DESC
"""

# ─── SECTION B — Python ───────────────────────────────────────────────────────

# B1
unresolved_types = [e["event_type"] for e in events_raw if not e["resolved"]]

# B2
high_risk_by_emp = {}
for e in events_raw:
    if e["severity"] in ("HIGH", "CRITICAL"):
        eid = e["employee_id"]
        high_risk_by_emp[eid] = high_risk_by_emp.get(eid, 0) + 1

# B3
def risk_score(event):
    sev = event["severity"]
    resolved = event["resolved"]
    if sev == "CRITICAL" and not resolved: return 4
    if sev == "HIGH"     and not resolved: return 3
    if sev in ("CRITICAL", "HIGH") and resolved: return 2
    return 1

sorted_events = sorted(events_raw, key=lambda e: risk_score(e), reverse=True)

# B4
data = json.loads(payload)
high_earner_ids = [emp["id"] for emp in data["employees"] if emp["salary"] > 100000]

# B5
critical_only  = list(filter(lambda e: e["severity"] == "CRITICAL", events_raw))
critical_upper = list(map(lambda e: e["event_type"].upper(), critical_only))

# ─── SECTION C — Pandas ───────────────────────────────────────────────────────

def salary_band(s):
    if s >= 130000: return "Senior"
    if s >= 100000: return "Mid"
    return "Junior"

# C1
c1_result = (
    emp_pd
    .query("active == 1 and department in ['Cyber', 'Engineering'] and salary > 100000")
    .assign(salary_band=lambda x: x["salary"].apply(salary_band))
    [["name","department","salary","salary_band"]]
)

# C2
def pct_ts(x):
    return round((x == "Top Secret").sum() / len(x) * 100, 1)

c2_result = (
    emp_pd.groupby("department")
    .agg(
        headcount=("employee_id", "count"),
        avg_salary=("salary", lambda x: round(x.mean(), 0)),
        pct_top_secret=("clearance", pct_ts),
    )
    .reset_index()
)

# C3
emp_enriched = emp_pd.copy()
emp_enriched["dept_avg_salary"] = emp_enriched.groupby("department")["salary"].transform("mean")
emp_enriched["vs_dept_avg"]     = (emp_enriched["salary"] - emp_enriched["dept_avg_salary"]).round(0)
c3_result = (
    emp_enriched
    .nlargest(5, "vs_dept_avg")
    [["name","department","salary","dept_avg_salary","vs_dept_avg"]]
)

# C4
merged = pd.merge(emp_pd[["employee_id","name","department"]], evt_pd[["employee_id","event_id"]], on="employee_id")
c4_result = (
    merged.groupby(["name","department"])
    .agg(event_count=("event_id","count"))
    .reset_index()
    .query("event_count >= 10")
    .sort_values("event_count", ascending=False)
)

# C5
c5_result = (
    evt_pd
    .assign(year=evt_pd["timestamp"].dt.year)
    .groupby(["year","severity"])
    .agg(event_count=("event_id","count"))
    .reset_index()
    .sort_values(["year","event_count"], ascending=[True, False])
)

# ─── SECTION D — Snowflake Reference Answers ─────────────────────────────────

"""
D1. Snowflake's three layers:
    - Storage (S3/Azure/GCS): data stored in columnar, compressed micro-partitions.
      Always available, independent of compute.
    - Compute (Virtual Warehouses): separate clusters that query data. Can be
      started/stopped independently, scaled up/down, and run in parallel.
    - Cloud Services: always-on layer handling authentication, query optimization,
      metadata, and transaction management.

    Separation of compute from storage means: you can suspend compute when idle
    (no CPU cost) while data remains fully available. Multiple warehouses can
    query the same data simultaneously without resource contention.

D2. Time Travel: Snowflake retains change history for 1–90 days (configurable
    per table). YOU can query it using AT/BEFORE syntax and recover dropped
    objects with UNDROP.

    Fail-Safe: An additional 7-day window BEYOND Time Travel. You cannot query
    it yourself — only Snowflake Support can recover data from Fail-Safe.
    It's automatic and non-configurable.

D3.
    SELECT * FROM events AT (OFFSET => -7200);   -- -7200 seconds = 2 hours
    -- or:
    SELECT * FROM events AT (TIMESTAMP => DATEADD('hour', -2, CURRENT_TIMESTAMP));

D4.
    SELECT
        metadata:source::STRING AS source,
        f.value::STRING AS tag
    FROM my_table,
         LATERAL FLATTEN(input => metadata:tags) f;

D5. QUALIFY filters the results of window functions — it runs AFTER the window
    function is evaluated. WHERE filters rows before aggregation; HAVING filters
    groups after aggregation; QUALIFY filters after window functions.

    Example:
      SELECT name, department, salary,
             DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
      FROM employees
      QUALIFY rnk <= 2;

    Without QUALIFY you'd need a subquery/CTE to filter on rnk.
"""
