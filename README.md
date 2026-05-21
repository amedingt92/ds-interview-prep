# Data Science Interview Prep

Structured practice for a timed data science assessment covering **SQL**, **Python**, **Pandas**, and **Snowflake**.

Each lesson is self-contained: read the concept doc, run the exercises, get instant pass/fail feedback, check the answer key only after you've tried.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ds-interview-prep
cd ds-interview-prep

# 2. Create and activate a virtual environment
python3 -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the shared dataset (run once)
python data/generate.py

# 5. Start with Lesson 1
python sql/lesson-01-select-filtering/lesson.py
```

> **Python version:** 3.10, 3.11, 3.12, or 3.13 recommended.  
> 3.14+ should work but is very new — if a package fails to install, this is likely why.

---

## How Each Lesson Works

```
lesson-XX-topic/
├── README.md     ← Read this first. Concepts, diagrams, examples.
├── lesson.py     ← Run this. Fill in queries/code, get ✅ / ❌ feedback.
└── answers.py    ← Open only after attempting everything yourself.
```

**The loop:**
1. Read `README.md` until you can answer the "You're Ready When..." questions
2. Open `lesson.py` and fill in each `# YOUR QUERY / CODE HERE` section
3. Run the lesson: `python path/to/lesson.py`
4. Fix any ❌ — re-run until all green
5. Review `answers.py` for any you couldn't crack, then move on

---

## Curriculum

### SQL — Interactive Lessons

| # | Topic | Concepts |
|---|-------|----------|
| [01](sql/lesson-01-select-filtering/) | SELECT & Filtering | SELECT, WHERE, AND/OR/NOT, IN, BETWEEN, LIKE, IS NULL, DISTINCT, ORDER BY, LIMIT |
| 02 | Aggregation | GROUP BY, HAVING, COUNT / SUM / AVG / MIN / MAX, COUNT(DISTINCT), NULLs in aggregates |
| 03 | JOINs | INNER, LEFT, RIGHT, FULL OUTER, self-join, anti-join, NULL behavior |
| 04 | CTEs & Subqueries | WITH clause, correlated vs uncorrelated subqueries, when to use each |
| 05 | Window Functions | ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD, SUM/AVG OVER, PARTITION BY, QUALIFY |
| 06 | Advanced SQL | CASE WHEN, date functions, string functions, query optimization basics |

### Python — Interactive Lessons

| # | Topic | Concepts |
|---|-------|----------|
| 01 | Core Syntax & Data Types | Variables, if/else, loops, lists, dicts, sets, tuples |
| 02 | Functions & Comprehensions | def, return, list/dict comprehensions, nested comprehensions |
| 03 | Lambda, Map, Filter | Anonymous functions, map(), filter(), sorted() with key= |
| 04 | String Manipulation | split/join/strip/replace, f-strings, regex basics |
| 05 | Working with Data | File I/O, JSON, NumPy basics, error handling |

### Pandas — Interactive Lessons

| # | Topic | Concepts |
|---|-------|----------|
| 01 | DataFrames & Selection | read_csv, shape/dtypes, .loc vs .iloc, boolean masks |
| 02 | Cleaning & Transformation | fillna/dropna, astype, rename, apply/map, value_counts |
| 03 | GroupBy & Aggregation | groupby().agg(), transform() vs agg(), named aggregation |
| 04 | Merge & Reshape | merge(), concat(), pivot_table(), melt() |
| 05 | Datetime & Advanced | pd.to_datetime, .dt accessor, resample(), method chaining |

### Snowflake — Reference Docs (read + self-check, no local execution needed)

| # | Topic |
|---|-------|
| 01 | Architecture & Core Concepts |
| 02 | Snowflake SQL Differences |
| 03 | Semi-Structured Data (VARIANT, FLATTEN) |
| 04 | Data Loading & Time Travel |

---

## Recommended Study Order

```
Day 1  →  SQL 01 + SQL 02
Day 2  →  SQL 03 + SQL 04
Day 3  →  Python 01 + Python 02 + Python 03
Day 4  →  SQL 05 + SQL 06
Day 5  →  Pandas 01 + Pandas 02 + Pandas 03
Day 6  →  Pandas 04 + Pandas 05 + Python 04 + Python 05
Day 7  →  Snowflake 01–04 (reference docs) + Capstone project
```

---

## The Dataset

All lessons use the same five tables so you never need to re-learn a schema:

| Table | Description |
|-------|-------------|
| `employees` | 74 employees across 6 departments with salary, clearance, hire date |
| `departments` | 6 departments with division groupings |
| `contracts` | 10 contracts with value, status, and date ranges |
| `employee_contracts` | Junction table — which employees work on which contracts |
| `security_events` | 500 security log events with severity, IP addresses, timestamps |

---

## Spiral Learning

Every lesson after the first includes a **Spiral Callbacks** section — exercises that
deliberately reapply earlier concepts alongside the new ones. Nothing gets left behind.

---

## Progress Tracker

- [ ] SQL 01 — SELECT & Filtering
- [ ] SQL 02 — Aggregation
- [ ] SQL 03 — JOINs
- [ ] SQL 04 — CTEs & Subqueries
- [ ] SQL 05 — Window Functions
- [ ] SQL 06 — Advanced SQL
- [ ] Python 01 — Core Syntax & Data Types
- [ ] Python 02 — Functions & Comprehensions
- [ ] Python 03 — Lambda, Map, Filter
- [ ] Python 04 — String Manipulation
- [ ] Python 05 — Working with Data
- [ ] Pandas 01 — DataFrames & Selection
- [ ] Pandas 02 — Cleaning & Transformation
- [ ] Pandas 03 — GroupBy & Aggregation
- [ ] Pandas 04 — Merge & Reshape
- [ ] Pandas 05 — Datetime & Advanced
- [ ] Snowflake 01 — Architecture & Core Concepts
- [ ] Snowflake 02 — Snowflake SQL Differences
- [ ] Snowflake 03 — Semi-Structured Data
- [ ] Snowflake 04 — Data Loading & Time Travel
- [ ] Capstone Project
