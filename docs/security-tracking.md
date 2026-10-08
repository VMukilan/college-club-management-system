# Global Security Issue Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks controlled security weaknesses introduced across versions, their remediation, and their automated verification.

---

## Security Weaknesses Tracking Matrix

| ID | Security Issue | Introduced | Fixed | Fixed Version | Verification Method |
|----|----------------|:----------:|:-----:|:-------------:|---------------------|
| **SEC01** | Missing centralized authorization | v0.1 | **YES** | **v0.3** | `@login_required`, `@roles_accepted(*roles)`, user status check, and session security |
| **SEC02** | Unauthorized event modification (IDOR) | v0.1 | **YES** | **v0.3** | `EventService.update_event()` object-level ownership check + automated tests 12–15 |
| **SEC03** | Weak input validation & Stored XSS | v0.1 | **YES** | **v0.3** | `app/validators.py` type/length bounds + unobtrusive event handlers (`data-*`) |
| **SEC04** | Weak error handling (information disclosure) | v0.1 | **YES** | **v0.3** | Generic client messages, Python `logging`, no sensitive disclosure in responses/logs |
| **SEC05** | Missing audit logging | v0.1 | **YES** | **v0.3** | `AuditRepository` logging on failed logins, password rejections, event edits, and authorization failures |

---

## Automated Tool Findings Tracking (SAST & SCA)

| Tool | Finding / ID | Severity | First Seen | Fixed In | Verification Status in v0.6 |
|------|--------------|----------|:----------:|:--------:|-----------------------------|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B106 (Hardcoded secret key in app config) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B105 (Test secret key string) | Low | v0.2 | v0.3 | **Verified: 0 findings** |
| **Semgrep** | Raw query concatenation | High | v0.1 | v0.2 | **Verified: 0 findings** (290 rules scanned) |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | v0.3 | **Verified: 0 vulnerabilities** |

---

## CI/CD & Fuzz Testing Security Gates Matrix (v0.6)

| Pipeline Gate | Tool / Strategy | Execution Scope | Enforcement Threshold |
|---|---|---|---|
| **Quality Gate** | Flake8 7.4.1 | Code style & PEP 8 compliance | 0 violations (Zero tolerance) |
| **SAST Gate 1** | Bandit 1.9.4 | Python Abstract Syntax Tree security rules | 0 High, 0 Medium findings |
| **SAST Gate 2** | Semgrep 1.179.0 | 290 Community security rules | 0 findings |
| **SCA Gate** | pip-audit 2.10.1 | Dependency vulnerabilities via OSV | 0 known vulnerabilities |
| **Dynamic Test Gate** | Pytest 9.1.1 | 29 automated tests (Functional, Security, K8s) | 100% pass rate |
| **Fuzz Testing Gate** | Hypothesis 6.168.5 | 250+ generated inputs & 19 exploit mutations | 0 unhandled HTTP 500 errors |
| **Container Gate** | Docker Buildx | Container image buildability | Build success without layer cache failure |
| **K8s Security Gate** | Pytest + PyYAML | Manifest syntax and Pod Security Standards | 100% compliance with Restricted PSS |
