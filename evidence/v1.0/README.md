# Master Evidence Checklist – Version 1.0 Final Release

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v1.0 (Final Production Release)  
**Candidate:** Mukilan Vijayakumar  

This master checklist consolidates all physical evidence artifacts across all developmental versions (`v0.1` through `v1.0`) for laboratory examination evaluation.

---

## Master Laboratory Examination Evidence Index

| Version Phase | Evidence ID Range | Primary Verification Targets | Verification Location |
|:---:|:---:|---|---|
| **`v0.1`** | `EV1-01` to `EV1-12` | Working application running; 7 code smells (CS01–07); 5 security weaknesses (SEC01–05); Initial Pytest suite. | [`evidence/v0.1/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v0.1/README.md) |
| **`v0.2`** | `EV2-01` to `EV2-15` | CS01–07 eliminated; decorators added; Flake8 violations reduced from 82 to 0; Bandit B608 fixed; Semgrep SQLi fixed. | [`evidence/v0.2/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v0.2/README.md) |
| **`v0.3`** | `EV3-01` to `EV3-16` | SEC01–05 eliminated; SEC02 IDOR cross-club tamper blocked; bounds validation; audit logs; 18 tests passing. | [`evidence/v0.3/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v0.3/README.md) |
| **`v0.4`** | `EV4-01` to `EV4-14` | Dockerfile (rootless `appuser`, UID 10001); docker-compose.yml; Gunicorn WSGI; dropped capabilities; volume isolation. | [`evidence/v0.4/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v0.4/README.md) |
| **`v0.5`** | `EV5-01` to `EV5-20` | Kubernetes 12 manifests; Pod Security Standards Restricted; zero-trust NetworkPolicy; RBAC; HPA; 24 tests passing. | [`evidence/v0.5/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v0.5/README.md) |
| **`v0.6`** | `EV6-01` to `EV6-13` | GitHub Actions 5-stage pipeline; Hypothesis property fuzzing; 0 crashes across 250+ inputs; 29 tests passing. | [`evidence/v0.6/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v0.6/README.md) |
| **`v1.0`** | `EV10-01` to `EV10-10` | Final Production Release certification; master reports; zero defects; complete Git history and tags. | This Document |

---

## Version 1.0 Final Release Evidence Artifacts

| Item # | Evidence Description | Target File / Command | Verified Status |
|:------:|----------------------|-----------------------|:---------------:|
| **EV10-01** | **Master Production README** | `README.md` | Comprehensive production deployment and security guide |
| **EV10-02** | **Comprehensive Exam Report** | `docs/FINAL_EXAM_REPORT.md` | Full end-semester laboratory examination report |
| **EV10-03** | **End-to-End Traceability** | `docs/traceability.md` | Certified Primary, Secondary, Tertiary, Quaternary, Quinary traces |
| **EV10-04** | **Code Smell Ledger (0 smells)** | `docs/code-smell-tracking.md` | CS01–CS07 certified RESOLVED |
| **EV10-05** | **Security Weakness Ledger (0 flaws)** | `docs/security-tracking.md` | SEC01–SEC05 certified RESOLVED |
| **EV10-06** | **Full Automated Test Suite** | Terminal: `python -m pytest -v` | **29 passed, 0 failed (100% pass rate)** |
| **EV10-07** | **Static Quality Scan (Flake8)** | Terminal: `flake8 run.py app/ tests/` | **0 violations (100% PEP 8 compliant)** |
| **EV10-08** | **Python SAST Scan (Bandit)** | Terminal: `bandit -r app/` | **0 issues identified** |
| **EV10-09** | **Community SAST Scan (Semgrep)** | Terminal: `semgrep scan --config auto app/` | **0 findings (290 rules scanned)** |
| **EV10-10** | **Dependency Scan (pip-audit)** | Terminal: `pip-audit -r requirements.txt` | **No known vulnerabilities found** |
| **EV10-11** | **Final Release Tag Created** | Terminal: `git tag -n` | Displays tag `v1.0` |
| **EV10-12** | **GitHub Remote Synchronization** | GitHub Repository | Verified on `main`, `develop`, and tags `v0.1`–`v1.0` |
