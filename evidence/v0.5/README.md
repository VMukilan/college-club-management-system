# Evidence Checklist – Version 0.5

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.5 (Kubernetes Deployment & Hardened Orchestration)  

This checklist enumerates all physical evidence artifacts and configuration verifications required to demonstrate practical completion of Version 0.5 during laboratory examination.

---

## Required Artifacts & Verifications

| Item # | Evidence Description | Target Manifest / File / Command | Verification Method / Status |
|:------:|----------------------|-----------------------------------|------------------------------|
| **EV5-01** | **Restricted Namespace** | `k8s/namespace.yaml` | `pod-security.kubernetes.io/enforce: restricted` label verified |
| **EV5-02** | **Hardened ServiceAccount** | `k8s/serviceaccount.yaml` | `automountServiceAccountToken: false` verified |
| **EV5-03** | **Least Privilege RBAC** | `k8s/rbac.yaml` | Scoped Role and RoleBinding for `college-club` namespace |
| **EV5-04** | **ConfigMap & Secret** | `k8s/configmap.yaml`, `k8s/secret.yaml` | Decoupled runtime config and base64-encoded secret keys |
| **EV5-05** | **Storage Persistence** | `k8s/pvc.yaml` | PersistentVolumeClaim mounted to `/app/instance` |
| **EV5-06** | **Hardened Deployment** | `k8s/deployment.yaml` | `runAsNonRoot: true`, `runAsUser: 10001`, `drop: ["ALL"]`, probes defined |
| **EV5-07** | **Service Manifest** | `k8s/service.yaml` | Stable ClusterIP routing port 80 to container port 5000 |
| **EV5-08** | **Ingress & TLS Configuration** | `k8s/ingress.yaml` | TLS termination and security header annotations |
| **EV5-09** | **Zero-Trust NetworkPolicy** | `k8s/networkpolicy.yaml` | Restricts ingress to ingress-nginx and egress strictly to DNS port 53 |
| **EV5-10** | **Autoscaling (HPA)** | `k8s/hpa.yaml` | Dynamic CPU-based scaling (2 to 5 replicas) |
| **EV5-11** | **Kustomize Bundle** | `k8s/kustomization.yaml` | Consolidates all manifests for `kubectl apply -k` deployment |
| **EV5-12** | **K8s Security Test Suite** | `tests/test_k8s.py` | 6 automated tests validating YAML syntax and security policies |
| **EV5-13** | **Full Test Suite Output** | Terminal: `python -m pytest -v` | **24 passed, 0 failed** (100% pass rate) |
| **EV5-14** | **Flake8 Quality Scan Output** | Terminal: `flake8 run.py app/ tests/ --statistics` | **0 violations** (100% PEP 8 compliance) |
| **EV5-15** | **Bandit SAST Output** | Terminal: `bandit -r app/` | **0 issues identified** (0 High, 0 Medium, 0 Low) |
| **EV5-16** | **Semgrep Scan Output** | Terminal: `semgrep scan --config auto app/` | **0 findings** (290 rules scanned) |
| **EV5-17** | **pip-audit SCA Output** | Terminal: `pip-audit -r requirements.txt` | **No known vulnerabilities found** |
| **EV5-18** | **Git Commit Log** | Terminal: `git log -1` | Displays commit: `v0.5: Implement Kubernetes deployment manifests and cluster security policies` |
| **EV5-19** | **Git Tag Created** | Terminal: `git tag -n` | Displays tag `v0.5` |
| **EV5-20** | **GitHub Push Verification** | GitHub web repository | Verified on `main`, `develop`, and `v0.5` tag |
