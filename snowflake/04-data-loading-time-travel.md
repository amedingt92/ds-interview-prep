# Snowflake 04 — Data Loading & Time Travel

> **Format:** Reference + self-check  
> These topics are "bonus" for the assessment but real Snowflake work requires them.

---

## Stages — Where Files Live Before Loading

A Stage is a named storage location (internal to Snowflake or external like S3) that holds files you want to load or export.

```sql
-- Internal stage (Snowflake manages the storage)
CREATE STAGE my_internal_stage;

-- External stage pointing to S3
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID='...' AWS_SECRET_KEY='...');

-- List files in a stage
LIST @my_stage;

-- Upload a file to internal stage (from SnowSQL CLI)
PUT file:///local/path/employees.csv @my_internal_stage;
```

---

## File Formats

Before loading, define how files are formatted.

```sql
CREATE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

CREATE FILE FORMAT my_json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE;   -- unwrap top-level array
```

---

## COPY INTO — Bulk Loading from Stage

```sql
-- Load CSV from stage into table
COPY INTO employees
FROM @my_stage/employees.csv
FILE_FORMAT = (FORMAT_NAME = 'my_csv_format');

-- Load all CSV files matching a pattern
COPY INTO employees
FROM @my_stage
PATTERN = '.*employees.*\.csv'
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

-- Validate without loading (ON_ERROR = 'CONTINUE' skips bad rows)
COPY INTO employees
FROM @my_stage
FILE_FORMAT = (TYPE = 'CSV')
ON_ERROR = 'CONTINUE';
```

---

## COPY INTO — Unloading (Export)

```sql
COPY INTO @my_stage/output/employees.csv
FROM employees
FILE_FORMAT = (TYPE = 'CSV' COMPRESSION = 'NONE')
SINGLE = TRUE;    -- one file instead of many parts
```

---

## Time Travel — Querying Historical Data

Snowflake retains a history of every change. You can query data as it was at any past point (up to 90 days for Enterprise, 1 day for Standard).

```sql
-- Query data as it was 1 hour ago
SELECT * FROM employees AT (OFFSET => -3600);

-- Query data at a specific timestamp
SELECT * FROM employees AT (TIMESTAMP => '2024-03-01 09:00:00'::TIMESTAMP);

-- Query data just before a specific transaction
SELECT * FROM employees BEFORE (STATEMENT => '<query_id>');
```

### Recovering Dropped Objects

```sql
-- Accidentally dropped a table
DROP TABLE employees;

-- Restore it (within the Time Travel retention window)
UNDROP TABLE employees;

-- Also works for schemas and databases
UNDROP SCHEMA analytics;
UNDROP DATABASE company_db;
```

### Cloning from a Point in Time

```sql
-- Clone a table to how it looked yesterday
CREATE TABLE employees_backup
    CLONE employees AT (OFFSET => -86400);   -- 86400 seconds = 1 day
```

---

## Fail-Safe

Beyond the Time Travel window, Snowflake keeps another 7-day Fail-Safe period. This is for disaster recovery only — you can't query it yourself. You have to contact Snowflake Support. It's automatic and non-configurable.

```
Time ─────────────────────────────────────────────────────►

  Data change   │← Time Travel (0–90 days, you control) →│← Fail-Safe (7 days, Snowflake only) →│
```

---

## Zero-Copy Cloning

Cloning in Snowflake doesn't copy any data — it creates a new metadata pointer to the same micro-partitions. Storage only increases when the clone diverges from the original.

```sql
-- Clone a full schema for a dev environment — instant, no storage cost until you change data
CREATE SCHEMA dev_analytics CLONE prod_analytics;

-- Clone a table
CREATE TABLE employees_test CLONE employees;
```

---

## Data Retention Period

```sql
-- Set Time Travel retention when creating a table
CREATE TABLE important_events (
    ...
) DATA_RETENTION_TIME_IN_DAYS = 90;

-- Change it after creation
ALTER TABLE important_events SET DATA_RETENTION_TIME_IN_DAYS = 7;
```

---

## Self-Check ✅

1. What is a Stage in Snowflake and what is it used for?
2. What SQL command loads files from a stage into a table?
3. How do you query what a table looked like 2 hours ago?
4. What does UNDROP TABLE do and when does it stop working?
5. What is the difference between Time Travel and Fail-Safe?
6. What does zero-copy cloning mean — why is it "zero-copy"?

---

**You've finished the Snowflake reference section.**  
**Next:** `capstone/README.md`
