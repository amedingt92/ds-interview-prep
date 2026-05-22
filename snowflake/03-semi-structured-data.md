# Snowflake 03 — Semi-Structured Data

> **Format:** Reference + self-check  
> Snowflake's VARIANT type and JSON handling are common on data assessments.

---

## The VARIANT Type

Snowflake can store JSON, Avro, Parquet, and XML natively using the `VARIANT` type. A VARIANT column can hold any valid JSON value — object, array, string, number, or null.

```sql
CREATE TABLE events (
    event_id   INT,
    event_data VARIANT     -- can hold any JSON
);

-- Inserting JSON
INSERT INTO events
SELECT 1, PARSE_JSON('{"type": "login", "severity": "HIGH", "ip": "10.0.1.5"}');
```

---

## Accessing JSON Fields — Colon Notation

Use `:` to traverse JSON keys. Use `::type` to cast the result.

```sql
-- Dot and colon notation
event_data:type                    -- returns VARIANT
event_data:type::STRING            -- cast to string
event_data:severity::STRING        -- "HIGH"
event_data:metadata:source::STRING -- nested: metadata.source

-- Array indexing
event_data:tags[0]::STRING         -- first element of a JSON array
event_data:tags[1]::INT            -- second element cast to int
```

```sql
-- Full example
SELECT
    event_id,
    event_data:type::STRING      AS event_type,
    event_data:severity::STRING  AS severity,
    event_data:ip::STRING        AS source_ip
FROM events;
```

---

## GET() and GET_PATH()

Alternative to colon notation when the key name is dynamic or contains special characters.

```sql
GET(event_data, 'type')::STRING
GET_PATH(event_data, 'metadata.source')::STRING
```

---

## FLATTEN() and LATERAL FLATTEN

When a VARIANT column contains a JSON array, use `FLATTEN` to explode it into rows.

```sql
-- If event_data looks like:
-- {"employee_id": 1001, "tags": ["phishing", "brute-force", "insider"]}

SELECT
    e.event_id,
    f.value::STRING AS tag
FROM events e,
     LATERAL FLATTEN(input => e.event_data:tags) f;

-- Result:
-- event_id | tag
-- 1        | phishing
-- 1        | brute-force
-- 1        | insider
```

### What LATERAL FLATTEN produces

`FLATTEN` returns these columns you can reference:
- `f.value` — the individual array element
- `f.index` — 0-based position in the array
- `f.key` — key name if the input is an object (not array)
- `f.path` — dot-path to the element

---

## PARSE_JSON() and TO_VARIANT()

```sql
-- Convert a string to VARIANT
PARSE_JSON('{"key": "value"}')

-- Convert a SQL value to VARIANT
TO_VARIANT(42)
TO_VARIANT('hello')
```

---

## Checking for Keys

```sql
-- Check if a key exists
event_data:tags IS NOT NULL

-- Type check
TYPEOF(event_data:severity)   -- returns 'VARCHAR', 'INTEGER', 'ARRAY', etc.
IS_ARRAY(event_data:tags)     -- returns TRUE/FALSE
IS_OBJECT(event_data)         -- returns TRUE/FALSE
```

---

## Loading Semi-Structured Data

```sql
-- Create a stage pointing to an S3 bucket
CREATE STAGE my_stage URL = 's3://my-bucket/events/';

-- Load JSON files from stage into a VARIANT column
COPY INTO events
FROM @my_stage
FILE_FORMAT = (TYPE = 'JSON');
```

---

## Practical Pattern: Normalize a VARIANT table

```sql
-- Flatten event_data into proper columns
SELECT
    event_id,
    event_data:employee_id::INT     AS employee_id,
    event_data:event_type::STRING   AS event_type,
    event_data:severity::STRING     AS severity,
    event_data:timestamp::TIMESTAMP AS event_time,
    f.value::STRING                 AS tag
FROM raw_events,
     LATERAL FLATTEN(input => event_data:tags) f;
```

---

## Self-Check ✅

1. What SQL type does Snowflake use to store JSON? What types of values can it hold?
2. How do you access a nested JSON field `metadata.source` in colon notation?
3. What does `LATERAL FLATTEN` do and when do you need it?
4. What does `f.value` refer to in a FLATTEN query?
5. How do you cast a VARIANT value to a string?

---

**Next:** `snowflake/04-data-loading-time-travel.md`
