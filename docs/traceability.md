# Security Requirements Traceability Matrix

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

Traceability provides end-to-end alignment from high-level security objectives down to deployment runtime controls.

```
Security Requirement
        ↓
    Use Case
        ↓
   DFD Process
        ↓
Architecture Component
        ↓
      Threat
        ↓
  Vulnerability
        ↓
   Attack Tree
        ↓
   User Story
        ↓
 Implementation
        ↓
      Test
        ↓
   CI/CD Check
        ↓
Deployment Control
```

---

## 1. Primary Trace: Prevention of Unauthorized Event Modification (SEC02)

| Phase Stage | Detail / Mapping |
|-------------|------------------|
| **Security Requirement** | Only authorized club coordinators may modify events belonging strictly to their assigned club. Cross-club event tampering must be denied. |
| **Use Case** | UC-04: Modify Club Event |
| **DFD Process** | Process 4.2: Update Event Details (Data Flow: Coordinator Credentials + Event ID + Update Payload) |
| **Architecture Component** | `EventService` + `AuthorizationService` + `EventRepository` |
| **Threat (STRIDE)** | **Elevation of Privilege** (Coordinator acting outside authorized scope) & **Tampering** (Altering another club's event information) |
| **Vulnerability** | Missing club-level authorization check (Broken Object Level Authorization / Insecure Direct Object Reference) |
| **Attack Tree** | Root: Deface Competitor Event → Node: Intercept Edit Request → Node: Substitute `event_id` of target club → Outcome: Success if server lacks object ownership check |
| **User Story** | *As a Club Coordinator, I want to edit details of only my club's events so that other clubs cannot alter our schedule or venues.* |
| **Implementation (v0.1)** | Controlled weakness in `EventService.update_event()`: only checks `user_role == 'coordinator'`, omits `event.club_id == user.club_id`. (Remediated in v0.3). |
| **Automated Test** | `tests/test_app.py::test_sec02_unauthorized_cross_club_event_modification_v0_1` (Demonstrates vulnerability in v0.1; will assert 403 Forbidden in v0.3). |
| **CI/CD Check** | GitHub Actions Workflow (`.github/workflows/ci.yml`): automated pytest test execution on every commit. |
| **Deployment Control** | Container non-root execution + Kubernetes network isolation + Server-side session integrity. |

---

## 2. Secondary Trace: Audit Logging of Security-Sensitive Operations (SEC05)

| Phase Stage | Detail / Mapping |
|-------------|------------------|
| **Security Requirement** | All security-sensitive actions (failed logins, event updates, administrative assignments) must be recorded in an immutable audit log. |
| **Use Case** | UC-09: Inspect System Audit Trail |
| **DFD Process** | Process 7.1: Write Security Audit Event to Data Store |
| **Architecture Component** | `AuditService` + `AuditRepository` → `AUDIT_LOG` table |
| **Threat (STRIDE)** | **Repudiation** (Actor denies modifying event or attempting unauthorized access) |
| **Vulnerability** | Incomplete audit trail (unmonitored actions in v0.1) |
| **Attack Tree** | Root: Escape Accountability → Node: Perform Action Without Audit Trail |
| **User Story** | *As a System Administrator, I want a complete audit trail so that all security events are traceable to a specific timestamp and user.* |
| **Implementation** | `AuditRepository.log()` writing user, action, and details. Full coverage enforced in v0.3. |
| **Automated Test** | Pytest validation inspecting database rows in `audit_logs` table. |
| **CI/CD Check** | Pytest automated test run in CI pipeline. |
| **Deployment Control** | Secure persistent storage volume with restricted write privileges. |
