# Version 0.1 vs Version 0.2 Comparison

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Comparison:** `v0.1` (Initial Prototype) vs `v0.2` (Refactored Release)  

---

## 1. Quantitative Metric Comparison

| Metric | v0.1 | v0.2 | Change | Notes / Evidence |
|--------|:----:|:----:|:------:|------------------|
| **Active Code Smells** | 7 | 0 | **-7 (-100%)** | CS01–CS07 refactored |
| **Flake8 Quality Violations** | 82 | 0 | **-82 (-100%)** | Full PEP 8 compliance |
| **Critical Issues (SAST)** | 0 | 0 | 0 | No critical flaws |
| **High Issues (SAST / Semgrep)** | 1 | 0 | **-1 (-100%)** | Semgrep blocking SQL string concatenation eliminated |
| **Medium Issues (Bandit)** | 1 | 0 | **-1 (-100%)** | Bandit B608 (SQL injection in dead code) eliminated |
| **Low Issues (Bandit)** | 3 | 1 | **-2 (-67%)** | B110 try-except-pass (2 instances) removed |
| **Total Automated SAST Findings** | 5 | 1 | **-4 (-80%)** | Significant code-level risk reduction |
| **Total Tests** | 12 | 12 | 0 | Test suite stability maintained |
| **Passed Tests** | 12 | 12 | 0 | 100% pass rate preserved |
| **Failed Tests** | 0 | 0 | 0 | Zero regressions introduced |
| **Lines of Code (LOC)** | 999 | 1,321 | +322 | Increased due to modularity, decorators, and constants |

---

## 2. Before / After Code Examples

### Example 1: Route Authentication & Role Checking (CS01)

#### Before (v0.1) — `app/routes.py`:
```python
# v0.1: Procedural boilerplate repeated on every route handler
@bp.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Unauthorized: Administrator access only.", "danger")
        return redirect(url_for('routes.login'))

    clubs = club_service.get_all_clubs()
    coordinators = user_repo.get_coordinators()
    audit_logs = audit_service.get_audit_trail(session.get('role'))
    total_clubs, total_events = get_quick_stats() # CS05: Raw DB connection helper
    return render_template('admin.html', ...)
```

#### After (v0.2) — `app/routes.py`:
```python
# v0.2: Declarative centralized decorator and repository metrics
@bp.route("/admin")
@roles_accepted(Role.ADMIN)
def admin_dashboard():
    clubs = club_service.get_all_clubs()
    coordinators = user_repo.get_coordinators()
    audit_logs = audit_service.get_audit_trail(session.get("role"))

    # Consolidated via Repository Pattern (CS05)
    total_clubs = club_repo.count()
    total_events = event_repo.count()
    return render_template("admin.html", ...)
```

---

### Example 2: Long Method Decomposition (CS02)

#### Before (v0.1) — `app/services.py`:
```python
# v0.1: Monolithic 68-line method handling validation, formatting,
# database operations, announcement generation, and audit logging
def create_event_with_notifications_and_audit(self, club_id, title, description, event_date, location, user_id):
    if not club_id or not title or not description or not event_date or not location:
        return False, "Fields required"
    formatted_title = title.strip()
    formatted_desc = description.strip()
    formatted_loc = location.strip()
    try:
        event_id = self.event_repo.create(...)
    except Exception as e:
        return False, f"Database failure: {str(e)}" # SEC04: Leaking details
    try:
        self.announcement_repo.create(...)
    except Exception:
        pass # CS06: Silent swallowing
    try:
        self.audit_repo.log(...)
    except Exception:
        pass # CS06: Silent swallowing
    return True, event_id
```

#### After (v0.2) — `app/services.py`:
```python
# v0.2: Clean, modular single-responsibility helper methods
def _validate_event_payload(self, club_id, title, description, event_date, location):
    if not club_id: return False, "Club ID is required"
    if not title: return False, "Event title is required"
    if not description: return False, "Event description is required"
    if not event_date: return False, "Event date is required"
    if not location: return False, "Location is required"
    return True, None

def _publish_event_announcement(self, club_id, title, event_date, location, user_id):
    try:
        self.announcement_repo.create(...)
    except Exception as err:
        logger.warning("Could not publish automatic event announcement: %s", err)

def _log_event_creation(self, user_id, title, event_id, club_id):
    try:
        self.audit_repo.log(user_id, AuditAction.EVENT_CREATED, ...)
    except Exception as err:
        logger.warning("Audit logging for event creation failed: %s", err)

def create_event_with_notifications_and_audit(self, club_id, title, description, event_date, location, user_id):
    is_valid, msg = self._validate_event_payload(club_id, title, description, event_date, location)
    if not is_valid:
        return False, msg
    ...
    self._publish_event_announcement(club_id, fmt_title, event_date, fmt_loc, user_id)
    self._log_event_creation(user_id, fmt_title, event_id, club_id)
    return True, event_id
```

---

### Example 3: Dead Code Elimination (CS07 & Bandit B608)

#### Before (v0.1) — `app/services.py`:
```python
# v0.1: Dead code introducing SQL Injection vulnerability
def old_fetch_user_by_id(user_id):
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = " + str(user_id)) # Bandit B608 / Semgrep
    row = cur.fetchone()
    conn.close()
    return row
```

#### After (v0.2):
```python
# Function completely eliminated from the codebase.
# UserRepository.get_by_id(user_id) handles parameterization safely.
```
