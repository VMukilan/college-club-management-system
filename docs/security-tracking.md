# Global Security Issue Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks controlled security weaknesses introduced across versions and their eventual remediation and verification.

---

## Security Weaknesses Tracking Matrix

| ID | Security Issue | Introduced | Fixed | Fixed Version | Verification Method |
|----|----------------|:----------:|:-----:|:-------------:|---------------------|
| **SEC01** | Missing centralized authorization | v0.1 | Partial (Decorators added) | Planned v0.3 | Route security checks & RBAC enforcement |
| **SEC02** | Unauthorized event modification (IDOR) | v0.1 | No (Maintained in v0.2) | Planned v0.3 | `test_sec02_unauthorized_cross_club_event_modification` |
| **SEC03** | Weak input validation | v0.1 | No | Planned v0.3 | Input boundary testing & fuzz validation |
| **SEC04** | Weak error handling (info disclosure) | v0.1 | Partial (No `str(e)` in responses) | Planned v0.3 | Safe error message inspection & logger verification |
| **SEC05** | Missing audit logging | v0.1 | No | Planned v0.3 | Audit log coverage across all operations |

---

## Automated Tool Findings Tracking (SAST & SCA)

| Tool | Finding / ID | Severity | First Seen | Fixed In | Verification Status |
|------|--------------|----------|:----------:|:--------:|---------------------|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | **v0.2** | Verified: 0 Medium issues |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | **v0.2** | Verified: Logging implemented |
| **Bandit** | B106 (Hardcoded secret key in app config) | Low | v0.1 | **v0.2** | Verified: Moved to Config class |
| **Semgrep** | Raw query concatenation | High | v0.1 | **v0.2** | Verified: 0 findings reported |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | Planned v0.3/v0.4 | Dependency upgrade scheduled |
