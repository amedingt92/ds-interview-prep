# Python Lesson 03 — Lambda, Map, Filter

> **Estimated time:** 25–35 minutes  
> **Run exercises:** `python python/lesson-03-lambda-map-filter/lesson.py`

---

## Lambda Functions

A lambda is an anonymous (unnamed) one-line function.

```python
# Regular function
def double(x):
    return x * 2

# Lambda equivalent
double = lambda x: x * 2
double(5)   # 10
```

Lambdas are most useful as arguments to other functions — not as standalone definitions.

---

## sorted() with key=

The most common lambda use case in data work:

```python
employees = [
    {"name": "Alex",   "salary": 140000},
    {"name": "Jordan", "salary": 95000},
    {"name": "Riley",  "salary": 130000},
]

# Sort by salary ascending
sorted(employees, key=lambda e: e["salary"])

# Sort by salary descending
sorted(employees, key=lambda e: e["salary"], reverse=True)

# Sort by multiple fields: department then salary
sorted(employees, key=lambda e: (e["department"], -e["salary"]))
```

---

## map()

Applies a function to every element of an iterable. Returns a lazy iterator — wrap in `list()`.

```python
salaries = [95000, 115000, 130000, 72000]

# Apply 10% raise
raised = list(map(lambda s: round(s * 1.10), salaries))

# Using a named function
def apply_raise(s):
    return round(s * 1.10)

raised = list(map(apply_raise, salaries))
```

> 💡 In practice, list comprehensions are often cleaner than `map()`.  
> Know both — tests ask for both.

```python
# map() version
list(map(lambda s: s * 1.1, salaries))

# Comprehension equivalent
[s * 1.1 for s in salaries]
```

---

## filter()

Keeps only elements where the function returns True. Also lazy — wrap in `list()`.

```python
events = ["login_failure", "file_access", "privilege_escalation", "login_success"]

logins = list(filter(lambda e: "login" in e, events))
# ["login_failure", "login_success"]

# Comprehension equivalent
logins = [e for e in events if "login" in e]
```

---

## When to Use Each

| Tool | Use when... |
|------|-------------|
| `lambda` | Short one-liner passed as argument to sorted/map/filter |
| `map()` | Transforming every element — asked on tests |
| `filter()` | Filtering by condition — asked on tests |
| Comprehension | Almost anything else — more readable |

---

## ✅ You're Ready When You Can Answer

- What is the syntax for a lambda that adds two numbers?
- How do you sort a list of dicts by a specific key descending?
- What does map() return and why do you need list() around it?
- What is the comprehension equivalent of filter()?
- How do you sort by multiple keys with a lambda?

---

**Next:** `python python/lesson-03-lambda-map-filter/lesson.py`
