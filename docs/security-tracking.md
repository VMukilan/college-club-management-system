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

| Tool | Finding / ID | Severity | First Seen | Fixed In | Verification Status in v0.3 |
|------|--------------|----------|:----------:|:--------:|-----------------------------|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B106 (Hardcoded secret key in app config) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B105 (Test secret key string) | Low | v0.2 | v0.3 | **Verified: 0 findings** (`# nosec B105` with env fallback) |
| **Semgrep** | Raw query concatenation | High | v0.1 | v0.2 | **Verified: 0 findings** (290 rules scanned) |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | v0.3 | **Verified: 0 vulnerabilities** (Upgraded to `werkzeug==3.1.9`) |

---

## Critical Security Scenario Test Coverage (v0.3)

| Scenario | Actor | Target Event | Expected Outcome | Audit Action | Pytest Test |
|----------|-------|--------------|:----------------:|:------------:|-------------|
| **1** | Coordinator (Club 1) | Club 1 Event | **ALLOW** | `EVENT_MODIFIED` | `test_sec02_own_club_event_modification_allowed` |
| **2** | Coordinator (Club 1) | Club 2 Event | **DENY** | `AUTHZ_FAILURE` | `test_sec02_cross_club_event_modification_denied` |
| **3** | Student | Club 1 Event | **DENY** | `AUTHZ_FAILURE` | `test_student_event_modification_denied` |
| **4** | Administrator | Club 2 Event | **ALLOW** | `EVENT_MODIFIED` | `test_admin_event_modification_allowed` |
