# Version 0.6 CI/CD Pipeline & Automated Security Gates Report

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Version:** `v0.6` (CI/CD Pipeline & Automated Quality Gates)  
**Date:** 2026-10-08  

---

## 1. Executive Summary
Version 0.6 implements an enterprise-grade Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub Actions ([`.github/workflows/ci.yml`](file:///d:/projects/College%20club%20Management%20system/.github/workflows/ci.yml)). The pipeline establishes five automated quality and security gates, enforcing "Shift-Left" security verification on every code commit and pull request.

---

## 2. CI/CD Architecture & Pipeline Topology

The pipeline executes five coordinated jobs across build runners:

```
                  ┌──────────────────────┐
                  │ Push / Pull Request  │
                  │   (main & develop)   │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌────────────────────────┐       ┌────────────────────────┐
│  Job: lint-and-quality │       │   Job: security-scans  │
│  - Flake8 (0 issues)   │       │  - Bandit SAST         │
│                        │       │  - Semgrep SAST        │
│                        │       │  - pip-audit SCA       │
└───────────┬────────────┘       └────────────┬───────────┘
            │                                 │
            └────────────────┬────────────────┘
                             │ (Both Must Pass)
                             ▼
                ┌────────────────────────┐
                │  Job: test-and-fuzz    │
                │  - Functional Tests    │
                │  - Critical Scenarios  │
                │  - Hypothesis Fuzzing  │
                │  - Coverage Reporting  │
                └────────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌────────────────────────┐       ┌────────────────────────┐
│Job: container-verificat│       │Job: k8s-manifest-valid │
│- Docker build          │       │- PyYAML manifest check │
│- Image validation      │       │- Pod Security checks   │
└────────────────────────┘       └────────────────────────┘
```

---

## 3. Automated Security Gates & Thresholds

### Gate 1: Code Quality & Style Gate (`lint-and-quality`)
- **Tool:** Flake8 7.4.1
- **Target:** `run.py`, `app/`, `tests/`
- **Threshold:** Strict zero tolerance (0 violations allowed). Pipeline fails immediately upon any PEP 8 style violation, unused import, or whitespace irregularity.

### Gate 2: Security SAST & SCA Gate (`security-scans`)
- **SAST Tool 1:** Bandit 1.9.4 (`bandit -r app/ -ll`)
  - Target: Python Abstract Syntax Tree vulnerability patterns.
  - Threshold: 0 High and 0 Medium issues.
- **SAST Tool 2:** Semgrep 1.179.0 (`semgrep scan --config auto app/ --error`)
  - Target: 290 Community Security rules (SQL injection, session leakage, unvalidated redirects).
  - Threshold: 0 findings.
- **SCA Tool:** pip-audit 2.10.1 (`pip-audit -r requirements.txt`)
  - Target: Open Source Vulnerability (OSV) and PyPI advisory databases.
  - Threshold: 0 known vulnerabilities.

### Gate 3: Dynamic Verification & Fuzz Gate (`test-and-fuzz`)
- **Tool:** Pytest 9.1.1 + Hypothesis 6.168.5 + pytest-cov
- **Scope:** 29 automated tests encompassing:
  - 11 Core Functional tests (login, club enrollment, event management)
  - 4 Critical Security Scenarios (SEC02 object authorization, cross-club tamper rejection)
  - 3 Audit & Bounds validation tests (SEC03, SEC05)
  - 5 Property-based fuzzing and mutation injection tests
  - 6 Kubernetes manifest security compliance tests
- **Threshold:** 100% test pass rate required.

### Gate 4: Container Build Verification (`container-verification`)
- **Tool:** Docker Buildx
- **Action:** Builds container image using `Dockerfile` to guarantee build reproducibility, layer hygiene, and non-root user setup prior to deployment.

### Gate 5: Kubernetes Manifest Security Gate (`k8s-manifest-validation`)
- **Tool:** Pytest + PyYAML
- **Action:** Validates all 12 Kubernetes YAML manifests, enforcing Pod Security Standards Restricted profile compliance.

---

## 4. Shift-Left Security Benefits
1. **Immediate Feedback:** Developers receive automated security scan feedback within minutes of pushing a branch.
2. **Zero Regression Guarantee:** Broken object authorization (SEC02) or unhandled exceptions (fuzzing) immediately block pull requests from merging.
3. **Reproducibility:** Eliminates "works on my machine" defects by validating builds in clean ephemeral runners.
