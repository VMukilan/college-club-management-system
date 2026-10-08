# Evidence Checklist – Version 0.6

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.6 (CI/CD Pipeline & Automated Security Fuzz Testing)  

This checklist enumerates all physical evidence artifacts and test verifications required to demonstrate practical completion of Version 0.6 during laboratory examination.

---

## Required Artifacts & Verifications

| Item # | Evidence Description | Target Manifest / File / Command | Verification Method / Status |
|:------:|----------------------|-----------------------------------|------------------------------|
| **EV6-01** | **GitHub Actions CI/CD Pipeline** | `.github/workflows/ci.yml` | 5 automated gates: Lint, SAST/SCA, Test/Fuzz, Container, K8s |
| **EV6-02** | **Property-Based Fuzz Testing** | `tests/test_fuzz.py` | Hypothesis strategies generating arbitrary Unicode, floats, ints, text |
| **EV6-03** | **Adversarial Mutation Fuzzing** | `tests/test_fuzz.py` (`FUZZ_SECURITY_PAYLOADS`) | Injects SQLi, XSS, Path Traversal, Format strings, buffer overflows |
| **EV6-04** | **Fuzz-Driven Vulnerability Fix** | `app/validators.py` | Handled `OverflowError` for float infinity in `validate_integer_id` |
| **EV6-05** | **Zero Crash Verification** | Pytest output | 0 unhandled HTTP 500 errors across all mutation fuzz tests |
| **EV6-06** | **Full Test Suite Output** | Terminal: `python -m pytest -v` | **29 passed, 0 failed** (100% pass rate) |
| **EV6-07** | **Flake8 Quality Scan Output** | Terminal: `flake8 run.py app/ tests/ --statistics` | **0 violations** (100% PEP 8 compliance) |
| **EV6-08** | **Bandit SAST Output** | Terminal: `bandit -r app/` | **0 issues identified** (0 High, 0 Medium, 0 Low) |
| **EV6-09** | **Semgrep Scan Output** | Terminal: `semgrep scan --config auto app/` | **0 findings** (290 rules scanned) |
| **EV6-10** | **pip-audit SCA Output** | Terminal: `pip-audit -r requirements.txt` | **No known vulnerabilities found** |
| **EV6-11** | **Git Commit Log** | Terminal: `git log -1` | Displays commit: `v0.6: Implement CI/CD pipeline and security fuzz testing` |
| **EV6-12** | **Git Tag Created** | Terminal: `git tag -n` | Displays tag `v0.6` |
| **EV6-13** | **GitHub Push Verification** | GitHub web repository | Verified on `main`, `develop`, and `v0.6` tag |
