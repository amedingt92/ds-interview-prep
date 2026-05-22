# Python Lesson 05 — Working with Data

> **Estimated time:** 30–40 minutes  
> **Run exercises:** `python python/lesson-05-working-with-data/lesson.py`

---

## File I/O

```python
# Reading a file
with open("data.txt", "r") as f:
    content = f.read()         # entire file as one string
    lines = f.readlines()      # list of lines

# Writing a file
with open("output.txt", "w") as f:
    f.write("Hello\n")

# Appending
with open("log.txt", "a") as f:
    f.write("new line\n")
```

> Always use `with` — it closes the file automatically even if an error occurs.

---

## JSON

```python
import json

# Parse JSON string → Python dict/list
data = json.loads('{"name": "Alex", "salary": 140000}')
data["name"]   # "Alex"

# Read JSON file
with open("data.json") as f:
    data = json.load(f)

# Python dict → JSON string
json.dumps({"name": "Alex"}, indent=2)

# Write JSON file
with open("out.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## NumPy Basics

```python
import numpy as np

arr = np.array([95000, 115000, 130000, 72000, 140000])

arr.mean()    # 110400.0
arr.std()     # 24...
arr.min()     # 72000
arr.max()     # 140000
arr.sum()     # 552000

# Boolean indexing
arr[arr > 100000]         # array([115000, 130000, 140000])

# Math operations (broadcasting)
arr * 1.10                # apply 10% raise to all
arr - arr.mean()          # deviation from mean
```

---

## Error Handling

```python
try:
    result = int("not_a_number")
except ValueError as e:
    print(f"Conversion failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Always runs")

# Raising errors
def get_salary(emp):
    if "salary" not in emp:
        raise KeyError("Employee missing salary field")
    return emp["salary"]
```

---

## ✅ You're Ready When You Can Answer

- What is the difference between json.load() and json.loads()?
- Why use `with open(...)` instead of just `open(...)`?
- How do you select only array elements above a threshold in NumPy?
- What is the difference between except ValueError and except Exception?

---

**Next:** `python python/lesson-05-working-with-data/lesson.py`
