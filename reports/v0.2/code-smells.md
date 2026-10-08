# Code Smell Refactoring Report – Version 0.2

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.2  
**Objective:** Elimination and remediation of controlled code smells (CS01–CS07).  

---

## 1. Refactoring Summary

| ID | Code Smell | Status in v0.1 | Status in v0.2 | Remediation Implemented |
|:---:|------------|:--------------:|:--------------:|--------------------------|
| **CS01** | Duplicate Auth Logic | Present (10 routes) | **RESOLVED** | Created centralized `@roles_accepted` decorator in `app/auth_decorators.py` |
| **CS02** | Long Method | Present (>65 lines) | **RESOLVED** | Decomposed `create_event_with_notifications_and_audit` into 3 single-responsibility helpers |
| **CS03** | Large Conditional | Present (40-line if/elif) | **RESOLVED** | Replaced with declarative `ROLE_PERMISSIONS` matrix in `AuthorizationService` |
| **CS04** | Hard-coded Values | Present (scattered strings) | **RESOLVED** | Centralized in `app/constants.py` (`Role`, `AuditAction`) & `app/config.py` |
| **CS05** | Duplicate DB Logic | Present (raw connections) | **RESOLVED** | Added `count()` methods to `ClubRepository` & `EventRepository`, removed raw SQL in routes |
| **CS06** | Poor Exception Handling | Present (bare pass / leak) | **RESOLVED** | Implemented standard Python `logging`, domain exceptions in `app/exceptions.py`, removed bare `pass` |
| **CS07** | Dead / Unused Code | Present (legacy functions) | **RESOLVED** | Deleted `legacy_calculate_club_score()` and `old_fetch_user_by_id()` |

---

## 2. Detailed Remediation Evidence

### CS01 — Centralized Authentication & Role Checking
- **Before (v0.1):** Every route repeated boilerplate session inspection:
  ```python
  if 'user_id' not in session or session.get('role') != 'admin':
      flash("Unauthorized: Administrator access only.", "danger")
      return redirect(url_for('routes.login'))
  ```
- **After (v0.2):** Clean declarative decorator applied to endpoints:
  ```python
  @bp.route("/admin")
  @roles_accepted(Role.ADMIN)
  def admin_dashboard():
      ...
  ```

### CS02 — Long Method Decomposition
- **Before (v0.1):** `create_event_with_notifications_and_audit()` was 68 lines handling input validation, database insertion, notification formatting, notification insertion, audit logging, and exception swallowing.
- **After (v0.2):** Broken down into modular methods:
  - `_validate_event_payload()`: Handles presence verification.
  - `_publish_event_announcement()`: Dispatches announcement notifications.
  - `_log_event_creation()`: Handles audit logging.
  - `create_event_with_notifications_and_audit()`: Orchestrates the workflow in under 25 lines.

### CS03 — Declarative Role-Permission Mapping
- **Before (v0.1):** Deeply nested procedural conditionals checking each action string manually across 40 lines.
- **After (v0.2):** Clean dictionary lookup:
  ```python
  ROLE_PERMISSIONS = {
      Role.ADMIN: {"admin_dashboard": ["view"], "events": ["create", "edit", "view"], ...},
      Role.COORDINATOR: {"events": ["create", "edit", "view"], "members": ["view", "manage"], ...},
      Role.STUDENT: {"events": ["view", "register"], "clubs": ["view", "join"], ...}
  }
  ```

### CS05 — Centralized Database Access via Repository Pattern
- **Before (v0.1):** `routes.get_quick_stats()` opened its own raw `sqlite3.connect()` connection and executed direct SQL queries.
- **After (v0.2):** Removed raw database connections from presentation layer. Implemented `ClubRepository.count()` and `EventRepository.count()`, invoked via repository instances.

### CS07 — Dead Code Removal
- **Before (v0.1):** Unused functions `legacy_calculate_club_score()` and `old_fetch_user_by_id()` existed in `app/services.py`, the latter introducing a raw SQL string concatenation vulnerability.
- **After (v0.2):** Both functions completely deleted.
