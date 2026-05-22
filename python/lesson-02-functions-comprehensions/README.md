# Python Lesson 02 — Functions & Comprehensions

> **Estimated time:** 35–45 minutes  
> **Run exercises:** `python python/lesson-02-functions-comprehensions/lesson.py`

---

## Defining Functions

```python
def greet(name, greeting="Hello"):   # greeting has a default value
    return f"{greeting}, {name}!"

greet("Alex")              # "Hello, Alex!"
greet("Alex", "Hi")        # "Hi, Alex!"
```

### *args and **kwargs

```python
def total(*args):           # *args = variable number of positional args
    return sum(args)

total(1, 2, 3)              # 6

def display(**kwargs):      # **kwargs = variable number of keyword args
    for k, v in kwargs.items():
        print(f"{k}: {v}")

display(name="Alex", dept="Cyber")
```

---

## List Comprehensions

A concise way to build lists. Replaces most simple for-loops.

```python
# For loop version
squares = []
for x in range(5):
    squares.append(x ** 2)

# Comprehension version — same result
squares = [x ** 2 for x in range(5)]
# [0, 1, 4, 9, 16]
```

### With a filter condition

```python
# Only even numbers
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Filter list of dicts
high_severity = [e for e in events if e["severity"] in ("HIGH", "CRITICAL")]
```

### Transforming values

```python
# Extract one field from a list of dicts
names = [e["name"] for e in employees]

# Transform and filter
high_salaries = [e["salary"] * 1.1 for e in employees if e["salary"] > 100000]
```

---

## Dict Comprehensions

```python
# {key: value for item in iterable}
salary_map = {e["name"]: e["salary"] for e in employees}
# {"Alex": 140000, "Jordan": 95000, ...}

# With filter
senior_map = {e["name"]: e["salary"] for e in employees if e["salary"] >= 130000}
```

---

## Nested Comprehensions

```python
# Flatten a list of lists
nested = [[1,2,3],[4,5,6],[7,8,9]]
flat = [x for sublist in nested for x in sublist]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## ✅ You're Ready When You Can Answer

- What does `*args` collect in a function call?
- What is the comprehension syntax for filtering a list?
- How do you extract one field from every dict in a list using a comprehension?
- How is `[x*2 for x in nums if x > 5]` different from a regular for loop?
- How do you build a dict comprehension?

---

**Next:** `python python/lesson-02-functions-comprehensions/lesson.py`
