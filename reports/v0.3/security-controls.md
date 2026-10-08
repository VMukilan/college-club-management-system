# Version 0.3 Security Controls Report

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Version:** `v0.3`  
**Date:** 2026-10-08  

---

## 1. Executive Summary
Version 0.3 delivers the secure implementation phase of the College Club Management System. All five controlled security weaknesses (SEC01–SEC05) identified in earlier releases have been remediated and verified with automated test suites and SAST/SCA tooling.

---

## 2. Implemented Security Controls

### Control 1: Object-Level Access Control (SEC02 Enforcement)
- **Problem Statement:** In `v0.1` and `v0.2`, `EventService.update_event()` validated only the caller's role (`coordinator`), allowing any coordinator to modify any event across club boundaries by supplying arbitrary `event_id` values (Insecure Direct Object Reference).
- **Remediation:** Enforced club ownership checking:
  ```python
  if user_role == Role.COORDINATOR:
      if event["club_id"] != user_club_id:
          self.audit_repo.log(
              user_id,
              AuditAction.AUTHZ_FAILURE,
              f"Cross-club modification DENIED on event #{valid_event_id}..."
          )
          return False, "Access Denied: You are not authorized to modify events for another club."
  ```
- **Verification:** Automated tests verify that Coordinator A modifying Club A event succeeds, whereas Coordinator A modifying Club B event is rejected and logged as `AUTHZ_FAILURE`.

### Control 2: Comprehensive Input and Bounds Validation (SEC03 Enforcement)
- **Problem Statement:** Input strings were accepted without bounds checking, creating vulnerability to malformed data and UI rendering defects.
- **Remediation:** Implemented `app/validators.py`:
  - Enforced string lengths (e.g., event titles 3–100 chars, descriptions 5–1000 chars, locations 2–100 chars).
  - Enforced date format validation (`YYYY-MM-DD`).
  - Enforced strict integer ID validation.
- **Verification:** `test_input_validation_bounds` asserts rejection of oversized and undersized payloads with clear validation errors.

### Control 3: Stored XSS Mitigation via DOM Event Binding
- **Problem Statement:** Inline HTML event handlers (`onclick="populateEditModal('...')"` in `templates/coordinator.html`) evaluated attributes in JavaScript context, creating potential Stored XSS if unescaped quotes or payloads were present.
- **Remediation:** Refactored to HTML5 `data-*` attributes (`data-event-id`, `data-title`, etc.) and event listeners (`addEventListener('click', ...)`), ensuring the browser parser never executes user data as code.

### Control 4: Session Hardening & Account Status Verification (SEC01)
- **Problem Statement:** Default session cookies lacked explicit HTTP-only and SameSite flags.
- **Remediation:** Enforced `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`, and 30-minute session lifetime. Enforced `is_active` account verification during authentication.

### Control 5: Security Auditing and Non-Repudiation (SEC05 Enforcement)
- **Problem Statement:** Failed logins, unauthorized access attempts, and event modifications were not logged in the audit trail.
- **Remediation:** Integrated `AuditRepository.log()` across:
  - Authentication rejections (`LOGIN_FAILED`)
  - Authorization failures and tampering attempts (`AUTHZ_FAILURE`)
  - Event modifications (`EVENT_MODIFIED`)
  - Event registrations (`EVENT_REGISTERED`)
- **Verification:** Automated tests verify database entries in `audit_logs` table upon failed login and tamper attempts.

### Control 6: Dependency Vulnerability Remediation (SCA)
- **Problem Statement:** `pip-audit` detected `CVE-2026-102598` in `Werkzeug==3.1.8`.
- **Remediation:** Upgraded to `Werkzeug==3.1.9` in `requirements.txt`. Subsequent `pip-audit` scan reported 0 vulnerabilities.

---

## 3. Security Scan Summary

| Scanner | Target | Issues Detected | Remediated Status |
|---------|--------|:---------------:|:-----------------:|
| **Bandit SAST** | `app/` | 0 | **Clean (0 issues)** |
| **Semgrep SAST** | `app/` (290 rules) | 0 | **Clean (0 findings)** |
| **pip-audit SCA** | `requirements.txt` | 0 | **Clean (0 vulnerabilities)** |
| **Flake8 Quality** | `app/`, `tests/` | 0 | **Clean (0 violations)** |
