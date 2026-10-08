# College Club Management System

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** `v1.0` (Final Production Release)  
**Author / Candidate:** Mukilan Vijayakumar  
**Repository:** [https://github.com/VMukilan/college-club-management-system.git](https://github.com/VMukilan/college-club-management-system.git)  

---

## 1. Executive Summary

The **College Club Management System** is a production-grade, secure, role-based web application developed for managing student clubs, membership enrollments, event lifecycles, and announcements. 

Engineered through a strict phased evolutionary lifecycle (`v0.1` $\rightarrow$ `v1.0`), the system demonstrates the end-to-end transformation of an intentionally vulnerable baseline prototype into a hardened, containerized, cluster-orchestrated, and continuously verified cloud-native application.

---

## 2. Evolutionary Lifecycle Roadmap

```
 v0.1: Baseline Prototype (7 Code Smells CS01-07, 5 Security Flaws SEC01-05)
   │
   ▼
 v0.2: Architectural Refactoring (Eliminated all 7 code smells, 0 Flake8 violations)
   │
   ▼
 v0.3: Security Hardening (Resolved SEC01-05, IDOR fix, input validation, audit trail)
   │
   ▼
 v0.4: Docker Containerization (Non-root appuser, slim base, Gunicorn WSGI, Compose)
   │
   ▼
 v0.5: Kubernetes Orchestration (Restricted Pod Security, NetworkPolicy, RBAC, HPA)
   │
   ▼
 v0.6: CI/CD & Security Fuzz Testing (GitHub Actions 5 gates, Hypothesis fuzz testing)
   │
   ▼
 v1.0: Final Production Release (Full audit certification, 29/29 tests passed, zero defects)
```

| Phase | Milestone Description | Key Technical Achievement |
|---|---|---|
| **`v0.1`** | Initial Baseline Prototype | Functional 3-role portal with controlled vulnerabilities for educational demonstration. |
| **`v0.2`** | Code Smell Reduction | Eliminated CS01–CS07; Flake8 violations reduced from 82 to 0; eliminated dead code SQLi. |
| **`v0.3`** | Secure Implementation | Remediated SEC01–SEC05; enforced object-level authorization (IDOR fix), centralized validators, and audit logging. |
| **`v0.4`** | Docker Containerization | Hardened rootless container (`appuser`, UID 10001), dropped capabilities, Gunicorn WSGI, resource limits. |
| **`v0.5`** | Kubernetes Orchestration | Pod Security Standards Restricted profile, least-privilege RBAC, zero-trust NetworkPolicy, HPA autoscaling. |
| **`v0.6`** | CI/CD & Fuzz Testing | 5-stage GitHub Actions pipeline, Hypothesis property-based fuzz testing, zero unhandled 500 errors. |
| **`v1.0`** | Final Production Release | Complete laboratory exam certification, 100% test pass rate across 29 automated tests. |

---

## 3. System Architecture & Design

### Layered Architecture
```
┌─────────────────────────────────────────────────────────────┐
│ Presentation Layer (HTML5, Vanilla CSS3, JavaScript DOM)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Web Routing & Controller Layer (Flask Blueprints, Decorators)│
│  - @login_required, @roles_accepted(*roles)                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Application Service Layer (Business Logic & AuthZ)           │
│  - AuthenticationService, ClubService, EventService         │
│  - MembershipService, RegistrationService, AuditService      │
│  - Centralized Input & Bounds Validation (app/validators.py)│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Data Access Layer (Repository Pattern)                      │
│  - UserRepository, ClubRepository, EventRepository          │
│  - MembershipRepository, RegistrationRepository, AuditRepo   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Database Layer (SQLite 3 with Parametrized SQL Queries)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Security Controls Summary

| Threat / Control Area | Implemented Security Mechanism | Verification Standard |
|---|---|---|
| **Broken Object Level Authorization (SEC02)** | Strict ownership check in `EventService.update_event()` ensures coordinators can only edit their own club's events. | Critical Security Tests 12–15 (`tests/test_app.py`) |
| **Centralized Authentication & Session Security (SEC01)** | `HttpOnly`, `SameSite=Lax`, 30-minute session lifetime, account `is_active` validation. | Route decorators & login test suite |
| **Input Validation & Stored XSS (SEC03)** | Strict whitelist and bounds validation in `app/validators.py`; HTML5 `data-*` attributes and DOM event listeners. | Bounds tests & Hypothesis fuzz tests |
| **Information Disclosure (SEC04)** | Sanitized user-facing error feedback; structured internal logging without sensitive token leaks. | Exception handlers & SAST scans |
| **Security Audit Logging (SEC05)** | Immutable audit records for logins, failed logins, authorization rejections (`AUTHZ_FAILURE`), and updates. | Automated database audit tests |
| **Container & Process Isolation** | Unprivileged execution as `appuser` (UID 10001); dropped Linux capabilities (`cap_drop: ALL`). | `Dockerfile` & `docker-compose.yml` |
| **Cluster Security & Zero-Trust** | Kubernetes Pod Security Standards Restricted profile; NetworkPolicy ingress and DNS-only egress. | `tests/test_k8s.py` test suite |
| **Crash Resistance** | Property-based fuzz testing via Hypothesis (250+ iterations); handled `OverflowError` for float infinities. | `tests/test_fuzz.py` test suite |

---

## 5. Seed Credentials for Demonstration

| Role | Username | Password | Assigned Club / Scope |
|---|---|---|---|
| **Administrator** | `admin` | `AdminPass123` | Campus-Wide Administrative Oversight |
| **Coordinator** | `coord_robotics` | `CoordPass123` | Robotics Club (Club ID: 1) |
| **Coordinator** | `coord_coding` | `CoordPass123` | Coding Club (Club ID: 2) |
| **Student** | `student_alice` | `StudentPass123` | Student Portal |
| **Student** | `student_bob` | `StudentPass123` | Student Portal |

---

## 6. Deployment & Running Instructions

### Option A: Local Python Environment
```bash
# 1. Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
python run.py
# Application accessible at http://127.0.0.1:5000/login
```

### Option B: Docker Compose Containerization
```bash
# Build and run with Docker Compose
docker compose up --build -d

# Check container status and health
docker compose ps
docker compose logs -f

# Stop container
docker compose down
```

### Option C: Kubernetes Cluster Deployment
```bash
# Deploy complete cluster suite via Kustomize
kubectl apply -k k8s/

# Verify pods running in restricted namespace
kubectl get pods -n college-club
kubectl get services,ingress,networkpolicies -n college-club
```

---

## 7. Testing, Security & Quality Verification

Run all test suites and security scans locally:

```bash
# 1. Run complete automated test suite (29 tests)
python -m pytest -v

# 2. Run code style & quality check (0 violations required)
python -m flake8 run.py app/ tests/ --statistics

# 3. Run Bandit SAST security scan (0 issues required)
python -m bandit -r app/

# 4. Run Semgrep SAST scan (0 findings required)
semgrep scan --config auto app/

# 5. Run pip-audit dependency vulnerability scan (0 CVEs required)
python -m pip_audit -r requirements.txt
```

---

## 8. Verification Results (v1.0 Production Release)

- **Pytest:** **29 passed, 0 failed (100% pass rate)**
- **Flake8:** **0 violations (100% PEP 8 compliant)**
- **Bandit SAST:** **0 issues identified**
- **Semgrep SAST:** **0 findings (290 rules scanned)**
- **pip-audit SCA:** **No known vulnerabilities found**
- **Security Fuzzing:** **0 unhandled 500 errors across 250+ generated inputs**
- **Kubernetes Security:** **100% compliant with Pod Security Standards Restricted**

---

## 9. Examination & Documentation Index

- [`docs/FINAL_EXAM_REPORT.md`](file:///d:/projects/College%20club%20Management%20system/docs/FINAL_EXAM_REPORT.md) – Comprehensive Laboratory Examination Report.
- [`docs/traceability.md`](file:///d:/projects/College%20club%20Management%20system/docs/traceability.md) – End-to-End Requirements Traceability Matrix.
- [`docs/code-smell-tracking.md`](file:///d:/projects/College%20club%20Management%20system/docs/code-smell-tracking.md) – Global Code Smell Evolution Matrix.
- [`docs/security-tracking.md`](file:///d:/projects/College%20club%20Management%20system/docs/security-tracking.md) – Global Security Weaknesses Tracking Matrix.
- [`evidence/v1.0/README.md`](file:///d:/projects/College%20club%20Management%20system/evidence/v1.0/README.md) – Master Laboratory Examination Evidence Checklist.
- Version-specific release notes: [`v0.1.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v0.1.md), [`v0.2.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v0.2.md), [`v0.3.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v0.3.md), [`v0.4.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v0.4.md), [`v0.5.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v0.5.md), [`v0.6.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v0.6.md), [`v1.0.md`](file:///d:/projects/College%20club%20Management%20system/docs/versions/v1.0.md).
