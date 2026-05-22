# Python Lesson 01 — Core Syntax & Data Types

> **Estimated time:** 30–40 minutes  
> **Run exercises:** `python python/lesson-01-core-syntax/lesson.py`

---

## Variables and Basic Types

```python
name    = "Alex"          # str
salary  = 95000           # int
rate    = 0.0625          # float
active  = True            # bool
nothing = None            # NoneType
```

---

## Conditionals

```python
if salary > 130000:
    band = "Senior"
elif salary >= 100000:
    band = "Mid"
else:
    band = "Junior"
```

---

## Lists

Ordered, mutable, allows duplicates.

```python
severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

severities[0]        # "LOW"  (first item)
severities[-1]       # "CRITICAL" (last item)
severities[1:3]      # ["MEDIUM", "HIGH"] (slice, end is exclusive)

severities.append("UNKNOWN")    # add to end
severities.remove("UNKNOWN")    # remove by value
len(severities)                 # 4
"HIGH" in severities            # True
```

---

## Dictionaries

Key-value pairs, unordered (Python 3.7+ maintains insertion order), mutable.

```python
employee = {
    "name":       "Alex Chen",
    "department": "Cyber",
    "salary":     120000,
    "active":     True,
}

employee["name"]                    # "Alex Chen"
employee.get("clearance", "None")   # "None" (safe — no KeyError)
employee["salary"] = 125000         # update
employee["clearance"] = "Secret"    # add new key
"department" in employee            # True (checks keys)

employee.keys()    # dict_keys([...])
employee.values()  # dict_values([...])
employee.items()   # dict_items([('name', 'Alex Chen'), ...])
```

---

## Sets

Unordered, unique values only. Great for deduplication and membership testing.

```python
clearances = {"Secret", "Top Secret", "Secret", "Confidential"}
# → {"Secret", "Top Secret", "Confidential"}  (duplicate removed)

"Secret" in clearances    # True (fast lookup)
clearances.add("None")
clearances.discard("None")

# Set operations
a = {"Secret", "Top Secret"}
b = {"Top Secret", "Confidential"}
a & b   # intersection: {"Top Secret"}
a | b   # union:        {"Secret", "Top Secret", "Confidential"}
a - b   # difference:   {"Secret"}
```

---

## Tuples

Ordered, **immutable** (can't change after creation). Use for fixed data.

```python
coords = (37.7749, -122.4194)
coords[0]    # 37.7749
# coords[0] = 1.0  ← TypeError — tuples are immutable

# Unpacking
lat, lon = coords
```

---

## Loops

```python
# For loop over list
for severity in ["LOW", "MEDIUM", "HIGH"]:
    print(severity)

# For loop with range
for i in range(5):         # 0, 1, 2, 3, 4
    print(i)

# Enumerate — get index and value together
for i, item in enumerate(["a", "b", "c"]):
    print(i, item)         # 0 a, 1 b, 2 c

# Loop over dict items
for key, value in employee.items():
    print(f"{key}: {value}")

# While loop
count = 0
while count < 3:
    count += 1
```

---

## When to Use Each Data Structure

| Structure | Use when... |
|-----------|-------------|
| `list` | ordered collection, duplicates OK, need to iterate |
| `dict` | key-value lookup, named fields |
| `set` | unique values, fast membership test, deduplication |
| `tuple` | fixed data that shouldn't change (coordinates, DB rows) |

---

## ✅ You're Ready When You Can Answer

- What is the difference between a list and a tuple?
- How do you safely access a dict key that might not exist?
- What does a set do with duplicates?
- What does `list[-1]` return?
- How do you loop over both keys and values of a dictionary?

---

**Next:** `python python/lesson-01-core-syntax/lesson.py`
