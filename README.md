# College Club Management System

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** `v0.1` (Initial Prototype with Controlled Code Smells and Weaknesses)

---

## 1. Project Overview

The **College Club Management System** is a role-based web application tailored for managing campus student clubs, membership rosters, event scheduling, event registrations, and campus-wide announcements.

### Roles & Responsibilities

1. **Student**
   - Authenticate (Login/Logout)
   - Browse campus clubs
   - Join clubs
   - View scheduled club events
   - Register for events
   - View official club announcements

2. **Club Coordinator**
   - Authenticate (Login/Logout)
   - Create club events
   - Modify events belonging to their assigned club
   - Publish official club announcements
   - View roster of registered club members

3. **Administrator**
   - Authenticate (Login/Logout)
   - Register and manage campus clubs
   - View and assign coordinators to clubs
   - Inspect system audit trail logs (`AUDIT_LOG`)

---

## 2. Seed Credentials for Demonstration

| Role | Username | Password | Notes |
|------|----------|----------|-------|
| Administrator | `admin` | `AdminPass123` | Full administrative oversight |
| Coordinator (Robotics) | `coord_robotics` | `CoordPass123` | Assigned to Robotics Club (ID: 1) |
| Coordinator (Coding) | `coord_coding` | `CoordPass123` | Assigned to Coding Club (ID: 2) |
| Student | `student_alice` | `StudentPass123` | Alice Smith |
| Student | `student_bob` | `StudentPass123` | Bob Johnson |

---

## 3. Technology Stack

- **Backend:** Python 3.12, Flask 3.1
- **Database:** SQLite 3 (Database entities: `USER`, `CLUB`, `MEMBERSHIP`, `EVENT`, `EVENT_REGISTRATION`, `ANNOUNCEMENT`, `AUDIT_LOG`)
- **Frontend:** Semantic HTML5, Vanilla CSS3 (Custom Design System), Vanilla JavaScript
- **Testing:** pytest
- **Security & Quality Tooling:** Bandit, flake8, pip-audit
- **CI/CD:** GitHub Actions

---

## 4. Layered Architecture

```
Presentation Layer (Jinja2 Templates + Flask Routes)
         ↓
Application / Service Layer (Auth, Club, Event, Membership, Registration, Announcement, Audit)
         ↓
Data Access Layer (Repository Pattern)
         ↓
Database Layer (SQLite)
```

---

## 5. Version Lifecycle Notice

This repository follows a strict multi-version evolutionary lifecycle for Secure Software Engineering:
- **v0.1:** Initial working application with controlled code smells and security weaknesses.
- **v0.2:** Refactoring and code-smell reduction.
- **v0.3:** Hardened authentication, centralized RBAC, input validation, and audit logging.
- **v0.4:** Docker containerization and vulnerability mitigation.
- **v0.5:** Kubernetes orchestration and security contexts.
- **v0.6:** DevSecOps CI/CD pipeline, SAST/SCA scanning, fuzz testing.
- **v1.0:** Final hardened release.
