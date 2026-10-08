# Version 0.6 Automated Security Fuzz Testing Report

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Version:** `v0.6` (CI/CD & Security Fuzz Testing)  
**Date:** 2026-10-08  

---

## 1. Executive Summary
Version 0.6 introduces automated security fuzz testing to evaluate the system's crash resistance, boundary validation, and resilience against malformed inputs and adversarial attack payloads. Using Hypothesis property-based testing and mutation-based vulnerability injection, the validation and routing layers were subjected to hundreds of synthetic inputs. Zero unhandled server crashes (HTTP 500) or database corruption occurred.

---

## 2. Fuzz Testing Methodology

### 2.1 Dual-Pronged Fuzzing Approach
1. **Property-Based Generative Fuzzing (Hypothesis):** Generates arbitrary permutations of Unicode strings, special symbols, control characters, null bytes, floats, extreme integers, and null types to test invariant properties of input sanitizers.
2. **Adversarial Mutation Fuzzing:** Injects curated security attack vectors (SQLi, XSS, Path Traversal, Format Strings, Buffer Overflows) directly into authenticated Flask web routes.

### 2.2 Fuzz Test Suite (`tests/test_fuzz.py`)

| Test Function | Target Component | Methodology | Invariant Asserted |
|---|---|---|---|
| `test_fuzz_validate_string_arbitrary_text` | `validate_string()` | 100 random text inputs | Always returns sanitized string within bounds or raises `ValidationError`. Never raises unexpected exceptions. |
| `test_fuzz_validate_integer_id_types` | `validate_integer_id()` | 100 mixed types (int, float, text, none) | Returns positive integer or raises `ValidationError`. Handles overflow and non-numerics cleanly. |
| `test_fuzz_validate_date_string_arbitrary` | `validate_date_string()` | 50 arbitrary text patterns | Strictly enforces ISO 8601 (`YYYY-MM-DD`) or raises `ValidationError`. |
| `test_fuzz_event_creation_mutation_payloads` | `/coordinator/events/create` | Curated SQLi, XSS, format string mutations | Server never returns HTTP 500; gracefully returns HTTP 200/redirect. |
| `test_fuzz_event_modification_mutation_payloads` | `/coordinator/events/edit` | Cross-club & adversarial payloads | Server returns HTTP 200, 400, or 403; denies tampering and maintains state. |

---

## 3. Discovered Vulnerability & Fuzz-Driven Hardening

### Finding: Unhandled `OverflowError` on Float Infinity
- **Root Cause:** During fuzzing of `validate_integer_id(val)` with `st.floats()`, Hypothesis generated `val = float('inf')`. Python's `int(float('inf'))` raises `OverflowError: cannot convert float infinity to integer`.
- **Pre-fuzzing Handler:** Caught only `(ValueError, TypeError)`.
- **Fuzz-Driven Fix:** Updated `app/validators.py`:
  ```python
  try:
      num = int(value)
  except (ValueError, TypeError, OverflowError):
      raise ValidationError(f"{field_name} must be a valid integer.")
  ```
- **Outcome:** The validator is now immune to float infinity injection and extreme float exponents.

---

## 4. Adversarial Payload Mutation Matrix

| Attack Category | Sample Payloads Tested | Server Response | Application Outcome |
|---|---|:---:|---|
| **SQL Injection** | `' OR '1'='1`, `1; DROP TABLE users; --`, `' UNION SELECT ...` | 200 / Flash Error | Parametrized query preserved; 0 SQL errors |
| **Cross-Site Scripting** | `<script>alert('XSS')</script>`, `<svg/onload=alert(1)>` | 200 / Rendered Safe | Jinja2 autoescaping + DOM data binding neutralized execution |
| **Path Traversal** | `../../../../../../etc/passwd`, `..\..\windows\system32\config\sam` | 200 / Validation Error | Rejected or treated as literal text; 0 path access |
| **Format Strings** | `%s%s%s%s%s%n`, `{{7*7}}`, `${7*7}` | 200 / Validation Error | Handled as raw text; 0 evaluation |
| **Extreme Lengths** | String of 10,000 `"A"` characters | 200 / Flash Error | Rejected by `validate_string()` length bounds |
| **Control Characters** | `\x00\x00\x00` (Null bytes), non-printable ASCII | 200 / Flash Error | Rejected by control character validator |

---

## 5. Fuzzing Test Results Summary
- Total Fuzz Test Cases Executed: **5 fuzz suites** (incorporating 250+ Hypothesis generated inputs and 19 mutation payloads).
- Unhandled HTTP 500 Internal Errors: **0 (Zero)**
- Data Corruption Incidents: **0 (Zero)**
- Overall Test Suite Pass Rate: **29 passed, 0 failed (100%)**
