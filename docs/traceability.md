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

---

## 3. Tertiary Trace: Container Security & Isolation Controls (v0.4)

| Phase Stage | Detail / Mapping |
|-------------|------------------|
| **Security Requirement** | Container processes must execute with least privilege, drop all kernel capabilities, prevent privilege escalation, and constrain resource consumption. |
| **Use Case** | UC-10: Deploy and Run Application in Production Container |
| **DFD Process** | Process 8.1: Container Process Spawning & Request Handling |
| **Architecture Component** | `Dockerfile` + `docker-compose.yml` + Gunicorn WSGI Server |
| **Threat (STRIDE)** | **Elevation of Privilege** (Container escape, root escalation) & **Denial of Service** (Resource exhaustion) |
| **Vulnerability** | Running as root inside container, unbounded memory/CPU, excessive Linux capabilities |
| **Attack Tree** | Root: Break out of container to host → Node: Exploit kernel bug as root → Prerequisite: Container running as root (UID 0) |
| **User Story** | *As a DevOps/SecOps Engineer, I want the container to execute as an unprivileged user with dropped capabilities so that a web compromise cannot compromise the host node.* |
| **Implementation** | `USER appuser` (UID 10001), `no-new-privileges:true`, `cap_drop: ALL`, CPU limit 1.0, RAM limit 512MB. |
| **Automated Test** | Healthcheck assertion + Configuration validation. |
| **CI/CD Check** | Dockerfile linting and container security scanning. |
| **Deployment Control** | Non-root runtime enforcement and container cgroup limits. |

---

## 4. Quaternary Trace: Kubernetes Cluster Security & Zero-Trust Orchestration (v0.5)

| Phase Stage | Detail / Mapping |
|-------------|------------------|
| **Security Requirement** | Workloads must run within a hardened Kubernetes namespace enforcing Pod Security Standards Restricted, least privilege RBAC, and zero-trust network isolation. |
| **Use Case** | UC-11: Deploy and Orchestrate Scalable Application in Kubernetes Cluster |
| **DFD Process** | Process 9.1: Ingress Routing, Service Load Balancing & Pod Execution |
| **Architecture Component** | `k8s/` (Namespace, Deployment, Service, Ingress, NetworkPolicy, RBAC, PVC, HPA) |
| **Threat (STRIDE)** | **Information Disclosure** (Token theft), **Elevation of Privilege** (Root escalation), **Denial of Service** (Unmanaged crashes) |
| **Vulnerability** | Privileged container admission, unconfined system calls, permissive network egress, unmanaged secrets |
| **Attack Tree** | Root: Cluster Lateral Movement → Node: Steal default service account token → Node: Pivot across namespaces |
| **User Story** | *As a Cluster Administrator, I want workloads restricted by admission controllers and network policies so that a pod compromise remains strictly contained.* |
| **Implementation** | `pod-security.kubernetes.io/enforce: restricted`, `automountServiceAccountToken: false`, `NetworkPolicy` DNS egress whitelist, Liveness/Readiness probes. |
| **Automated Test** | Automated test suite in `tests/test_k8s.py` verifying YAML structure and security attributes. |
| **CI/CD Check** | Automated Pytest and manifest validation in CI pipeline. |
| **Deployment Control** | Kubernetes Admission Controller, CNI network policy filtering, PersistentVolume isolation. |


