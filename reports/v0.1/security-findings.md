# Security Analysis & Controlled Weaknesses – Version 0.1

**Tools Run:** Bandit 1.9.4, Semgrep 1.179.0  
**Scan Timestamp:** 2026-10-08  
**Scope:** `app/`  

---

## 1. Automated SAST Findings

### Bandit Scan Summary
- Total Lines of Code: 999
- Total Issues: 4
  - **High:** 0
  - **Medium:** 1
  - **Low:** 3

| Rule ID | Severity | Confidence | Location | Description |
|---------|----------|------------|----------|-------------|
| **B608** | Medium | Medium | `app/services.py:58` | Possible SQL injection vector through string concatenation in `old_fetch_user_by_id`. |
| **B106** | Low | Medium | `app/__init__.py:10` | Hardcoded secret key in `app.config.from_mapping`. |
| **B110** | Low | High | `app/services.py:260` | Silent `try-except-pass` block in `create_event_with_notifications_and_audit`. |
| **B110** | Low | High | `app/services.py:271` | Silent `try-except-pass` block during audit logging in event creation. |

### Semgrep Scan Summary
- Scanned: 6 files, 290 rules executed
- Findings: 1 blocking finding

| Rule | Severity | Location | Details |
|------|----------|----------|---------|
| `sqlalchemy-execute-raw-query` | High/Blocking | `app/services.py:58` | Raw query string concatenation: `SELECT * FROM users WHERE id = " + str(user_id)` |

---

## 2. Controlled Architectural Security Weaknesses

### SEC01 — Non-Centralized Authorization
- **Status in v0.1:** INTENTIONALLY PRESENT
- **Location:** `app/routes.py`, `app/services.py`
- **Vulnerability:** Authorization logic is checked via ad-hoc procedural conditionals inside individual route handlers instead of being enforced consistently by server-side decorators or middleware filters.
- **Risk:** Developers can easily forget to add checks on newly introduced endpoints, leading to authorization bypass.
- **Planned Fix:** Centralized RBAC decorator enforcing role guards in v0.3.

---

### SEC02 — Unauthorized Event Modification (Broken Object Level Authorization / IDOR)
- **Status in v0.1:** INTENTIONALLY PRESENT & VERIFIED VIA AUTOMATED TEST (`test_sec02_unauthorized_cross_club_event_modification_v0_1`)
- **Location:** `app/services.py:277` (`update_event`) and `app/routes.py:228`
- **Vulnerability:** When a coordinator requests an event update via `POST /coordinator/events/edit`, the server confirms the caller has role `coordinator`, but FAILS to verify that the target event belongs to the caller's assigned club (`event.club_id == user.club_id`).
- **Risk:** Any coordinator can tamper with or deface events created by competing clubs across the campus.
- **Planned Fix:** Enforce club ownership verification (`event.club_id == current_user.club_id` or admin override) in v0.3.

---

### SEC03 — Incomplete Input Validation
- **Status in v0.1:** INTENTIONALLY PRESENT
- **Location:** Event creation, announcement publishing, club creation
- **Vulnerability:** Endpoints perform minimal presence checks (`if not title: return False`) without enforcing length limits, regex pattern matching, or strict sanitization against XSS/HTML injections.
- **Risk:** Malicious payloads, UI distortion, or database buffer overflows.
- **Planned Fix:** Dedicated schema validation layer with whitelist rules in v0.3.

---

### SEC04 — Implementation Detail Exposure in Error Handling
- **Status in v0.1:** INTENTIONALLY PRESENT
- **Location:** `app/services.py` (`str(e)` in error returns)
- **Vulnerability:** Unhandled database and system exceptions are returned directly to the user in flash notifications or response messages.
- **Risk:** Information disclosure revealing backend database schema, table names, and stack details.
- **Planned Fix:** Generic user-facing messages coupled with server-side correlation IDs in v0.3.

---

### SEC05 — Inconsistent Audit Logging
- **Status in v0.1:** INTENTIONALLY PRESENT
- **Location:** `AuthenticationService.authenticate()`, `EventService.update_event()`, `routes.admin_assign_coordinator()`
- **Vulnerability:** While successful logins and creations are logged, critical security events such as failed authentication attempts, event modifications, and coordinator reassignments omit audit entries.
- **Risk:** Inability to perform post-incident forensic investigation or detect brute-force attacks.
- **Planned Fix:** Comprehensive, tamper-evident audit logging for all security-sensitive events in v0.3.
