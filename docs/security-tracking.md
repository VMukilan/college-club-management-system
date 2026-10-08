# Global Security Issue Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks controlled security weaknesses introduced across versions, their remediation, and their automated verification up to the Final Production Release (`v1.0`).

---

## Security Weaknesses Tracking Matrix

| ID | Security Issue | Introduced | Fixed | Fixed Version | Verification Method | Status in v1.0 |
|:---:|----------------|:----------:|:-----:|:-------------:|---------------------|:--------------:|
| **SEC01** | Missing centralized authorization | v0.1 | **YES** | **v0.3** | `@login_required`, `@roles_accepted(*roles)`, user status check, and session security | **RESOLVED** |
| **SEC02** | Unauthorized event modification (IDOR) | v0.1 | **YES** | **v0.3** | `EventService.update_event()` object-level ownership check + automated tests 12–15 | **RESOLVED** |
| **SEC03** | Weak input validation & Stored XSS | v0.1 | **YES** | **v0.3** | `app/validators.py` type/length bounds + unobtrusive event handlers (`data-*`) | **RESOLVED** |
| **SEC04** | Weak error handling (information disclosure) | v0.1 | **YES** | **v0.3** | Generic client messages, Python `logging`, no sensitive disclosure in responses/logs | **RESOLVED** |
| **SEC05** | Missing audit logging | v0.1 | **YES** | **v0.3** | `AuditRepository` logging on failed logins, password rejections, event edits, and authorization failures | **RESOLVED** |

---

## Automated Tool Findings Tracking (SAST & SCA)

| Tool | Finding / ID | Severity | First Seen | Fixed In | Verification Status in v1.0 |
|------|--------------|----------|:----------:|:--------:|:---------------------------:|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B106 (Hardcoded secret key in app config) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B105 (Test secret key string) | Low | v0.2 | v0.3 | **Verified: 0 findings** |
| **Semgrep** | Raw query concatenation | High | v0.1 | v0.2 | **Verified: 0 findings** (290 rules scanned) |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | v0.3 | **Verified: 0 vulnerabilities** |

---

## Final Security Assurance Verification (v1.0)

| Layer | Security Controls Enforced | Verification Status |
|---|---|:---:|
| **Application Layer** | Centralized RBAC, Session Hardening (HttpOnly, SameSite, 30m timeout), Object Authorization (IDOR elimination) | **PASSED** |
| **Data Layer** | Parametrized SQLite queries, strict bounds validation (`app/validators.py`), persistent volume storage | **PASSED** |
| **Audit Layer** | Immutable audit trail for authentication, authorization rejections, event modifications, registrations | **PASSED** |
| **Container Layer** | Non-root execution (`appuser`, UID 10001), minimal slim base image, dropped capabilities, no-cache build | **PASSED** |
| **Cluster Layer** | Pod Security Standards Restricted, least-privilege RBAC, zero-trust NetworkPolicy, autoscaling | **PASSED** |
| **Pipeline Layer** | GitHub Actions 5-stage automated security gates, property-based fuzz testing (250+ iterations) | **PASSED** |
