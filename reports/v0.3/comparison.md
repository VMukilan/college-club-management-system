# Evolution Comparison: v0.1 vs v0.2 vs v0.3

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Comparison:** `v0.1` (Baseline) vs `v0.2` (Refactored) vs `v0.3` (Secured)  
**Date:** 2026-10-08  

---

## 1. Quantitative Metric Evolution

| Metric | v0.1 (Baseline) | v0.2 (Refactored) | v0.3 (Secured) | Total Evolution Delta |
|--------|:---------------:|:-----------------:|:--------------:|:---------------------:|
| **Active Code Smells** | 7 | 0 | **0** | **-7 (-100%)** |
| **Flake8 Violations** | 82 | 0 | **0** | **-82 (-100%)** |
| **Bandit Findings** | 4 | 1 | **0** | **-4 (-100%)** |
| **Semgrep Findings** | 1 | 0 | **0** | **-1 (-100%)** |
| **pip-audit CVEs** | 1 | 1 | **0** | **-1 (-100%)** |
| **Total Automated Vulnerabilities** | 6 | 2 | **0** | **-6 (-100%)** |
| **Total Automated Tests** | 12 | 12 | **18** | **+6 (+50%)** |
| **Test Pass Rate** | 100% (12/12) | 100% (12/12) | **100% (18/18)** | **Maintained 100%** |
| **Active Security Weaknesses** | 5 (SEC01–05) | 5 (Maintained) | **0 (All Fixed)** | **-5 (-100%)** |

---

## 2. Security Weakness Status Matrix

| Issue ID | Description | v0.1 Status | v0.2 Status | v0.3 Status | Remediation in v0.3 |
|:---:|-------------|:---:|:---:|:---:|-------------------|
| **SEC01** | Missing Centralized Auth & Session Security | Present | Partially Refactored | **RESOLVED** | `@login_required`, `@roles_accepted`, `is_active` check, HttpOnly/SameSite cookies |
| **SEC02** | Cross-Club Event Modification (IDOR) | Present | Maintained (Demonstrable) | **RESOLVED** | Object-level club ownership verification in `EventService.update_event()` |
| **SEC03** | Weak Input Validation & Stored XSS | Present | Maintained | **RESOLVED** | Type/length/bounds validation in `app/validators.py` + DOM data binding |
| **SEC04** | Information Disclosure in Errors | Present | Partially Refactored | **RESOLVED** | Generic user feedback; structured internal logging without sensitive data leaks |
| **SEC05** | Missing Audit Logging | Present | Maintained | **RESOLVED** | Immutable audit logs on failed logins, tampering rejections, event changes |

---

## 3. Side-by-Side Code Comparison: SEC02 Fix

### v0.1 & v0.2 (Vulnerable Code):
```python
def update_event(self, event_id, title, description, event_date, location, user_role):
    # Only checked whether the user was a coordinator
    if user_role not in [Role.COORDINATOR, Role.ADMIN]:
        return False, "Access Denied"
    
    # Missing object ownership check: any coordinator could edit any event!
    self.event_repo.update(event_id, title, description, event_date, location)
    return True, "Event updated successfully"
```

### v0.3 (Secure Hardened Code):
```python
def update_event(self, event_id, title, description, event_date, location,
                 user_id, user_role, user_club_id=None):
    if user_role not in [Role.COORDINATOR, Role.ADMIN]:
        self.audit_repo.log(user_id, AuditAction.AUTHZ_FAILURE, ...)
        return False, "Access Denied: Only coordinators or administrators can modify events."

    valid_event_id = validate_integer_id(event_id, "Event ID")
    event = self.event_repo.get_by_id(valid_event_id)
    if not event:
        return False, "Event not found"

    # SEC02 Object-Level Authorization Check
    if user_role == Role.COORDINATOR:
        if event["club_id"] != user_club_id:
            logger.warning("SEC02 PREVENTED: Coordinator %s denied modifying Event %s",
                           user_id, valid_event_id)
            self.audit_repo.log(user_id, AuditAction.AUTHZ_FAILURE, ...)
            return False, "Access Denied: You are not authorized to modify events for another club."

    # SEC03 Input Validation
    val_title = validate_string(title, 3, 100, "Event title")
    val_desc = validate_string(description, 5, 1000, "Event description")
    val_date = validate_date_string(event_date, "Event date")
    val_loc = validate_string(location, 2, 100, "Location")

    self.event_repo.update(valid_event_id, val_title, val_desc, val_date, val_loc)
    self.audit_repo.log(user_id, AuditAction.EVENT_MODIFIED, ...)
    return True, "Event updated successfully"
```

---

## 4. Conclusion
Version 0.3 completes the application hardening milestone. Code smells remain at 0, static analysis and SCA findings are completely eliminated (0 findings across Bandit, Semgrep, and pip-audit), and all security controls are verified with 18 automated tests.
