# Controlled Code Smells Analysis – Version 0.1

**Project:** College Club Management System  
**Version:** v0.1  
**Total Smells Identified:** 7  

---

## Code Smells Inventory

### CS01 — Duplicated Authentication / Authorization Logic
- **File:** `app/routes.py` & `app/services.py`
- **Function / Class:** `student_dashboard()`, `student_join_club()`, `coordinator_dashboard()`, `coordinator_create_event()`, `admin_dashboard()`, etc.
- **Description:** Route handlers repeatedly duplicate manual session inspection (`if 'user_id' not in session or session.get('role') != ...`).
- **Impact:** High maintenance overhead, error-prone authorization checks, risk of routes accidentally omitting checks.
- **Planned Remediation (v0.2):** Implement centralized route decorators (`@login_required`, `@roles_accepted('admin')`).

---

### CS02 — Long Method
- **File:** `app/services.py`
- **Function / Class:** `EventService.create_event_with_notifications_and_audit()`
- **Description:** A monolithic method (>65 lines) handling parameter extraction, formatting, event table insertion, automated announcement formatting, announcement insertion, audit logging, and exception swallowing.
- **Impact:** Violates Single Responsibility Principle (SRP), high cyclomatic complexity, difficult to unit-test components independently.
- **Planned Remediation (v0.2):** Decompose into smaller single-responsibility methods (`_validate_event_input`, `_notify_members`, `_record_audit`).

---

### CS03 — Large Conditional / Excessive Role Checking
- **File:** `app/services.py`
- **Function / Class:** `AuthorizationService.check_access()`
- **Description:** Deeply nested `if role == 'admin': ... elif role == 'coordinator': ... elif role == 'student': ...` checking each permission string procedurally.
- **Impact:** High cyclomatic complexity, difficult to extend with new roles or permissions, violates Open/Closed Principle.
- **Planned Remediation (v0.2):** Refactor into a declarative role-permission matrix or dictionary lookup map.

---

### CS04 — Hard-coded Configuration & Role Values
- **File:** `app/__init__.py`, `app/routes.py`, `app/services.py`
- **Function / Class:** Global constants, session lookups, table status
- **Description:** Literal strings like `'admin'`, `'coordinator'`, `'student'`, `'ACTIVE'`, `'REGISTERED'`, along with hard-coded dev secret keys and database paths.
- **Impact:** Typo risks, poor maintainability, inability to configure environments through variables.
- **Planned Remediation (v0.2):** Introduce an `Enum` or `constants.py` module and a structured `Config` class loaded via environment variables.

---

### CS05 — Duplicated Database Access Logic
- **File:** `app/routes.py` & `app/services.py`
- **Function / Class:** `routes.get_quick_stats()`, `services.old_fetch_user_by_id()`
- **Description:** Raw `sqlite3.connect()` calls and cursor operations scattered directly inside routes and services, completely bypassing the repository pattern.
- **Impact:** Inconsistent connection pooling, transaction handling discrepancies, leakage of data layer details into presentation layer.
- **Planned Remediation (v0.2):** Consolidate all database operations inside the Repository Layer (`app/repositories.py`).

---

### CS06 — Poor Exception Handling
- **File:** `app/services.py`
- **Function / Class:** `EventService.create_event_with_notifications_and_audit()`, `ClubService.create_club()`
- **Description:** Catching broad `Exception` and either silently swallowing with `pass` or returning raw error strings without structured logging.
- **Impact:** Diagnostic blindness during silent failures, unpredictable execution states, coupled with implementation detail exposure (SEC04).
- **Planned Remediation (v0.2):** Introduce custom domain exceptions (`EntityNotFoundError`, `AuthorizationError`), proper Python `logging`, and explicit exception chaining.

---

### CS07 — Unused / Dead Code
- **File:** `app/services.py`
- **Function / Class:** `legacy_calculate_club_score()`, `old_fetch_user_by_id()`
- **Description:** Leftover prototype functions that are defined but never referenced or invoked by any application workflow or test.
- **Impact:** Bloated codebase, cognitive clutter for developers, and security risk (Bandit flagged SQL injection B608 inside the dead code `old_fetch_user_by_id`).
- **Planned Remediation (v0.2):** Deprecate and delete dead code routines and unused imports.
