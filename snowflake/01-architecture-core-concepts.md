# Snowflake 01 — Architecture & Core Concepts

> **Format:** Reference + self-check  
> No interactive exercises — read, understand, test yourself at the bottom.

---

## What Is Snowflake?

Snowflake is a cloud data warehouse. Unlike traditional databases that run on one server, Snowflake separates compute from storage — you pay for storage always and compute only when you're running queries.

---

## The Three-Layer Architecture

```
┌─────────────────────────────────────┐
│         Cloud Services Layer        │  ← Authentication, query optimization,
│     (metadata, security, query      │    metadata management
│      planning — always on)          │
└─────────────────────────────────────┘
          ↕ talks to both layers
┌─────────────────────────────────────┐
│         Compute Layer               │  ← Virtual Warehouses — this is where
│     (Virtual Warehouses)            │    SQL actually runs
│     XS / S / M / L / XL / ...      │
└─────────────────────────────────────┘
          ↕ reads from / writes to
┌─────────────────────────────────────┐
│         Storage Layer               │  ← Columnar storage, auto-compressed,
│     (S3 / Azure Blob / GCS)         │    always available even when compute
│     — always available              │    is suspended
└─────────────────────────────────────┘
```

---

## Virtual Warehouses

A Virtual Warehouse is a cluster of compute resources. You can have multiple running simultaneously without interfering with each other — data scientists on one warehouse, ETL on another.

```sql
-- Create a warehouse
CREATE WAREHOUSE my_wh
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 300          -- suspend after 5 minutes idle
  AUTO_RESUME = TRUE;         -- auto-start on next query

-- Resume / suspend manually
ALTER WAREHOUSE my_wh RESUME;
ALTER WAREHOUSE my_wh SUSPEND;

-- Use a warehouse
USE WAREHOUSE my_wh;
```

**Warehouse sizes:** X-Small → Small → Medium → Large → X-Large → 2X-Large → ...  
Each step up roughly doubles compute (and cost).

---

## Database, Schema, Table Hierarchy

```
Organization
  └── Account
        └── Database (logical container)
              └── Schema (namespace for objects)
                    ├── Tables
                    ├── Views
                    ├── Stages
                    └── Functions
```

```sql
CREATE DATABASE company_db;
CREATE SCHEMA company_db.analytics;
CREATE TABLE company_db.analytics.employees (...);

-- Or set context and use shorthand
USE DATABASE company_db;
USE SCHEMA analytics;
SELECT * FROM employees;
```

---

## Micro-Partitions

Snowflake automatically divides every table into micro-partitions — small chunks of compressed, columnar data (typically 50–500 MB uncompressed). You never define them; Snowflake manages them automatically.

**Why it matters:**
- Queries that filter on partition columns skip entire micro-partitions (partition pruning = fast queries)
- You can inspect pruning with `EXPLAIN` or query profile

---

## Clustering Keys

On very large tables, you can declare a clustering key to sort the data in a way that improves pruning for common query patterns.

```sql
ALTER TABLE large_events CLUSTER BY (event_date, department);
```

> For the assessment: know that clustering helps query performance by improving micro-partition pruning. You don't need to know the implementation details.

---

## Caching

Snowflake has three cache layers (fastest to slowest):

1. **Result cache** — if the exact same query ran recently and the data hasn't changed, Snowflake returns the cached result instantly with zero compute cost
2. **Local disk cache** (SSD) — compressed data cached on the warehouse node from recent scans
3. **Remote storage** — reading from S3/Azure/GCS — slowest, always available

---

## Key Snowflake-Specific Features

| Feature | What it is |
|---------|-----------|
| Time Travel | Query historical data up to 90 days back |
| Zero-Copy Cloning | Clone a table/schema/database instantly without copying data |
| Fail-Safe | 7-day data recovery window beyond Time Travel (Snowflake manages) |
| Streams | Change data capture — track INSERT/UPDATE/DELETE changes to a table |
| Tasks | Scheduled SQL execution (like cron for SQL) |
| Data Sharing | Share live data with other Snowflake accounts without copying |

---

## Self-Check ✅

Try to answer these without looking:

1. What does it mean that Snowflake separates compute from storage?
2. If you suspend a Virtual Warehouse, can you still query the data?
3. What is a micro-partition and why does it matter for performance?
4. What is the result cache and when does it kick in?
5. What are three Snowflake-specific features you wouldn't find in a standard SQL database?

---

**Next:** `snowflake/02-snowflake-sql-differences.md`
