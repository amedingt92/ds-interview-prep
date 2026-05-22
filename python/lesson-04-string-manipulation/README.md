# Python Lesson 04 — String Manipulation

> **Estimated time:** 25–35 minutes  
> **Run exercises:** `python python/lesson-04-string-manipulation/lesson.py`

---

## Core String Methods

```python
s = "  Privilege_Escalation:HIGH  "

s.strip()           # "Privilege_Escalation:HIGH"  (remove whitespace)
s.lower()           # "  privilege_escalation:high  "
s.upper()           # "  PRIVILEGE_ESCALATION:HIGH  "
s.replace("_", " ") # "  Privilege Escalation:HIGH  "
s.split(":")        # ["  Privilege_Escalation", "HIGH  "]
":".join(["a","b"]) # "a:b"
s.startswith("  P") # True
s.endswith("H  ")   # True
"HIGH" in s         # True
```

---

## f-Strings

```python
name = "Alex"
dept = "Cyber"
salary = 140000

label = f"{name} ({dept}) — ${salary:,}"
# "Alex (Cyber) — $140,000"

# With expressions
f"Band: {'Senior' if salary >= 130000 else 'Mid'}"
```

---

## Regex Basics

Import `re` for pattern matching beyond what `LIKE` handles.

```python
import re

text = "Event from 10.0.45.23 at 2024-03-15"

# re.search — find first match anywhere in string
match = re.search(r"\d+\.\d+\.\d+\.\d+", text)
if match:
    print(match.group())   # "10.0.45.23"

# re.findall — find ALL matches, returns list
ips = re.findall(r"\d+\.\d+\.\d+\.\d+", text)

# re.sub — find and replace
clean = re.sub(r"\s+", "_", "login failure")   # "login_failure"

# re.match — match at START of string only
re.match(r"Event", text)   # match
re.match(r"10\.",  text)   # None (doesn't start with "10.")
```

### Common Patterns

| Pattern | Matches |
|---------|---------|
| `\d+` | one or more digits |
| `\w+` | word characters (letters, digits, _) |
| `\s+` | whitespace |
| `.`   | any single character |
| `^`   | start of string |
| `$`   | end of string |
| `[A-Z]` | any uppercase letter |

---

## ✅ You're Ready When You Can Answer

- How do you split a string on a delimiter and rejoin it?
- What is the difference between re.search and re.match?
- How do you extract all IP addresses from a string with regex?
- How do you format a number with commas in an f-string?

---

**Next:** `python python/lesson-04-string-manipulation/lesson.py`
