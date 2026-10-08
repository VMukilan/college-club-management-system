# Global Security Issue Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks controlled security weaknesses introduced across versions, their remediation, and their automated verification.

---

## Security Weaknesses Tracking Matrix

| ID | Security Issue | Introduced | Fixed | Fixed Version | Verification Method |
|----|----------------|:----------:|:-----:|:-------------:|---------------------|
| **SEC01** | Missing centralized authorization | v0.1 | **YES** | **v0.3** | `@login_required`, `@roles_accepted(*roles)`, user status check, and session security |
| **SEC02** | Unauthorized event modification (IDOR) | v0.1 | **YES** | **v0.3** | `EventService.update_event()` object-level ownership check + automated tests 12–15 |
| **SEC03** | Weak input validation & Stored XSS | v0.1 | **YES** | **v0.3** | `app/validators.py` type/length bounds + unobtrusive event handlers (`data-*`) |
| **SEC04** | Weak error handling (information disclosure) | v0.1 | **YES** | **v0.3** | Generic client messages, Python `logging`, no sensitive disclosure in responses/logs |
| **SEC05** | Missing audit logging | v0.1 | **YES** | **v0.3** | `AuditRepository` logging on failed logins, password rejections, event edits, and authorization failures |

---

## Automated Tool Findings Tracking (SAST & SCA)

| Tool | Finding / ID | Severity | First Seen | Fixed In | Verification Status in v0.5 |
|------|--------------|----------|:----------:|:--------:|-----------------------------|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B106 (Hardcoded secret key in app config) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B105 (Test secret key string) | Low | v0.2 | v0.3 | **Verified: 0 findings** |
| **Semgrep** | Raw query concatenation | High | v0.1 | v0.2 | **Verified: 0 findings** (290 rules scanned) |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | v0.3 | **Verified: 0 vulnerabilities** |

---

## Kubernetes Orchestration Security Controls Matrix (v0.5)

| Security Control | Implementation Detail | Target Resource | Verification Method |
|---|---|---|---|
| **Restricted Pod Security** | `pod-security.kubernetes.io/enforce: restricted` | `k8s/namespace.yaml` | `test_k8s_namespace_restricted_pod_security` |
| **Non-Root Execution** | `runAsNonRoot: true`, `runAsUser: 10001` | `k8s/deployment.yaml` | `test_k8s_deployment_security_context` |
| **Capability Stripping** | `drop: ["ALL"]`, `allowPrivilegeEscalation: false` | `k8s/deployment.yaml` | `test_k8s_deployment_security_context` |
| **Runtime Seccomp Profile** | `seccompProfile: {type: RuntimeDefault}` | `k8s/deployment.yaml` | `test_k8s_deployment_security_context` |
| **Token Theft Mitigation** | `automountServiceAccountToken: false` | `k8s/serviceaccount.yaml` | `test_k8s_serviceaccount_token_automount_disabled` |
| **Least-Privilege RBAC** | Namespace-scoped `Role` & `RoleBinding` | `k8s/rbac.yaml` | Manifest validation |
| **Zero-Trust NetworkPolicy** | Ingress from ingress controller; egress DNS-only | `k8s/networkpolicy.yaml` | `test_k8s_networkpolicy_rules` |
| **Resource Quotas & Limits** | Requests: 100m/128Mi; Limits: 500m/512Mi | `k8s/deployment.yaml` | `test_k8s_deployment_resources_and_probes` |
| **Health Probes (Self-Healing)**| Liveness and Readiness probes checking `/login` | `k8s/deployment.yaml` | `test_k8s_deployment_resources_and_probes` |
| **Horizontal Autoscaling** | HPA min 2, max 5, target CPU 75% | `k8s/hpa.yaml` | Manifest validation |
