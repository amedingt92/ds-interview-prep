"""
Lesson checker utility — used by every lesson in this repo.
Provides check() for value comparisons and check_df() for DataFrame validation.
"""

_results = []

PASS  = "✅"
FAIL  = "❌"
HINT  = "💡"
SEP   = "─" * 52


def check(actual, expected, label, hint=None):
    """
    Compare actual vs expected and print pass/fail.
    Handles scalars, lists, sets, dicts, and floats.
    """
    try:
        if isinstance(expected, float):
            passed = abs(float(actual) - expected) < 1e-4
        elif isinstance(expected, list):
            passed = list(actual) == list(expected)
        elif isinstance(expected, set):
            passed = set(actual) == set(expected)
        else:
            passed = actual == expected

        if passed:
            print(f"  {PASS}  {label}")
        else:
            print(f"  {FAIL}  {label}")
            print(f"       Expected : {expected}")
            print(f"       Got      : {actual}")
            if hint:
                print(f"       {HINT}  {hint}")

        _results.append((label, passed))

    except Exception as e:
        print(f"  {FAIL}  {label}  [ERROR: {e}]")
        _results.append((label, False))


def check_df(df, checks, label, hint=None):
    """
    Validate a DataFrame against a dict of checks.

    Supported checks:
        rows       : int   — exact row count
        min_rows   : int   — minimum row count
        columns    : list  — all these columns must be present
        no_nulls   : list  — these columns must have no NaN values
    """
    errors = []

    if "rows" in checks:
        if len(df) != checks["rows"]:
            errors.append(f"expected {checks['rows']} rows, got {len(df)}")

    if "min_rows" in checks:
        if len(df) < checks["min_rows"]:
            errors.append(f"expected at least {checks['min_rows']} rows, got {len(df)}")

    if "columns" in checks:
        missing = [c for c in checks["columns"] if c not in df.columns]
        if missing:
            errors.append(f"missing columns: {missing}")

    if "no_nulls" in checks:
        for col in checks["no_nulls"]:
            if col in df.columns and df[col].isna().any():
                errors.append(f"column '{col}' contains NULL/NaN values")

    passed = len(errors) == 0

    if passed:
        print(f"  {PASS}  {label}")
    else:
        print(f"  {FAIL}  {label}")
        for e in errors:
            print(f"       → {e}")
        if hint:
            print(f"       {HINT}  {hint}")

    _results.append((label, passed))


def summary():
    """Print final score for the lesson."""
    total  = len(_results)
    passed = sum(1 for _, p in _results if p)
    pct    = int((passed / total) * 100) if total else 0
    bar    = ("█" * passed) + ("░" * (total - passed))

    print()
    print(SEP)
    print(f"  Score: {passed}/{total}  [{bar}]  {pct}%")
    if pct == 100:
        print("  🎯  Perfect — move on to the next lesson.")
    elif pct >= 70:
        print("  👍  Good — review any ❌ before moving on.")
    else:
        print("  📖  Re-read the README and try again.")
    print(SEP)

    _results.clear()
