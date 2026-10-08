# Version 0.5 Kubernetes Security & Hardening Report

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Version:** `v0.5` (Kubernetes Deployment & Hardened Orchestration)  
**Date:** 2026-10-08  

---

## 1. Executive Summary
Version 0.5 establishes enterprise-grade Kubernetes orchestration for the College Club Management System. The cluster manifests adhere strictly to Kubernetes Pod Security Standards (Restricted Profile), CIS Kubernetes Benchmark recommendations, and Zero-Trust network architecture.

---

## 2. Kubernetes Security Architecture & Hardening Controls

### 2.1 Namespace Isolation & Pod Security Standards (Restricted Profile)
- **Manifest:** `k8s/namespace.yaml`
- **Security Labels:**
  ```yaml
  pod-security.kubernetes.io/enforce: restricted
  pod-security.kubernetes.io/enforce-version: latest
  pod-security.kubernetes.io/audit: restricted
  pod-security.kubernetes.io/warn: restricted
  ```
- **Policy Enforcement:** Rejects any workload attempting to run as root (`UID 0`), requiring privilege escalation, or utilizing host namespaces.

### 2.2 Pod & Container SecurityContext Hardening
- **Manifest:** `k8s/deployment.yaml`
- **Pod-Level SecurityContext:**
  - `runAsNonRoot: true`: Enforces unprivileged execution.
  - `runAsUser: 10001`: Dedicated non-root UID (`appuser`).
  - `runAsGroup: 10001`: Dedicated GID (`appgroup`).
  - `fsGroup: 10001`: Ensures mounted volumes inherit appropriate group ownership.
  - `seccompProfile: { type: RuntimeDefault }`: Constrains system calls to the default seccomp profile.
- **Container-Level SecurityContext:**
  - `allowPrivilegeEscalation: false`: Blocks setuid binaries and subprocess privilege escalation.
  - `capabilities: { drop: ["ALL"] }`: Strips all Linux kernel capabilities from the process table.

### 2.3 Principle of Least Privilege: RBAC & ServiceAccount Hardening
- **Manifests:** `k8s/serviceaccount.yaml`, `k8s/rbac.yaml`
- **Token Protection:** `automountServiceAccountToken: false` on `ServiceAccount: college-club-sa`. Prevents Kubernetes API tokens from being mounted inside pods, eliminating credential theft vectors.
- **Role Scoping:** `Role: college-club-role` grants minimal read-only access strictly within the `college-club` namespace, bound via `RoleBinding: college-club-rolebinding`.

### 2.4 Configuration & Secret Segregation
- **ConfigMap (`k8s/configmap.yaml`):** Stores non-sensitive parameters (`FLASK_ENV`, `DATABASE_NAME`, `PORT`).
- **Secret (`k8s/secret.yaml`):** Isolates session cryptographic keys (`SECRET_KEY`), mounted as environment variables via `secretRef`.

### 2.5 Persistent Storage & High Availability
- **Storage (`k8s/pvc.yaml`):** 1Gi PersistentVolumeClaim mounted to `/app/instance` ensures persistent SQLite data retention across pod restarts and rolling updates.
- **High Availability (`k8s/deployment.yaml`):** 2 replicas configured with zero-downtime `RollingUpdate` strategy (`maxSurge: 1`, `maxUnavailable: 0`).
- **Elasticity (`k8s/hpa.yaml`):** HorizontalPodAutoscaler scales pods dynamically from 2 to 5 replicas when average CPU utilization exceeds 75%.

### 2.6 Zero-Trust Network Isolation (NetworkPolicy)
- **Manifest:** `k8s/networkpolicy.yaml`
- **Ingress Filtering:** Allows incoming TCP traffic on port 5000 only from the Ingress Controller namespace (`ingress-nginx`).
- **Egress Filtering:** Blocks all arbitrary outbound connections, permitting outbound traffic exclusively for cluster DNS resolution (port 53 UDP/TCP).

---

## 3. Automated Validation & Test Suite
Automated compliance tests in `tests/test_k8s.py` verify that:
1. All 12 Kubernetes manifests parse cleanly without YAML syntax errors.
2. The namespace enforces `pod-security.kubernetes.io/enforce: restricted`.
3. The deployment strictly enforces `runAsNonRoot: true`, `runAsUser: 10001`, `drop: ["ALL"]`, and `allowPrivilegeEscalation: false`.
4. Probes (liveness, readiness) and resource boundaries (limits, requests) are defined.
5. ServiceAccount disables automatic API token mounting.
6. NetworkPolicy restricts ingress and egress traffic.

All 24 automated tests passed with a 100% success rate.
