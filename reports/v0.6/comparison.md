# Evolutionary Comparison: v0.1 through v0.6

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Comparison:** Progression across `v0.1` (Baseline), `v0.2` (Refactored), `v0.3` (Secured), `v0.4` (Containerized), `v0.5` (Kubernetes), and `v0.6` (CI/CD & Fuzz Testing)  
**Date:** 2026-10-08  

---

## 1. Quantitative Metric Progression

| Metric | v0.1 | v0.2 | v0.3 | v0.4 | v0.5 | v0.6 | Total Evolution Delta |
|--------|:----:|:----:|:----:|:----:|:----:|:----:|:---------------------:|
| **Active Code Smells** | 7 | 0 | 0 | 0 | 0 | **0** | **-7 (-100%)** |
| **Flake8 Violations** | 82 | 0 | 0 | 0 | 0 | **0** | **-82 (-100%)** |
| **Bandit SAST Issues** | 4 | 1 | 0 | 0 | 0 | **0** | **-4 (-100%)** |
| **Semgrep SAST Issues** | 1 | 0 | 0 | 0 | 0 | **0** | **-1 (-100%)** |
| **pip-audit Vulnerabilities** | 1 | 1 | 0 | 0 | 0 | **0** | **-1 (-100%)** |
| **Automated Tests** | 12 | 12 | 18 | 18 | 24 | **29** | **+17 (+142%)** |
| **Test Pass Rate** | 100% | 100% | 100% | 100% | 100% | **100% (29/29)** | **Maintained** |
| **Fuzz Testing Coverage** | None | None | None | None | None | **250+ Mutated Inputs** | **NEW** |
| **CI/CD Security Gates** | None | None | None | None | None | **5 Multi-Stage Gates** | **NEW** |
| **Active Security Weaknesses** | 5 | 5 | 0 | 0 | 0 | **0** | **-5 (-100%)** |

---

## 2. Testing Evolution Across Development Phases

| Version | Testing Focus | Tooling / Implementation | Total Tests | Pass Rate |
|---|---|---|:---:|:---:|
| **v0.1** | Baseline functional smoke tests | Pytest basic client | 12 | 100% |
| **v0.2** | Regression testing after refactoring | Pytest with repository fixtures | 12 | 100% |
| **v0.3** | Critical Security Scenarios (SEC02 IDOR, SEC05 Audit) | Pytest cross-club authorization tests | 18 | 100% |
| **v0.4** | Container entrypoint and runtime testing | Pytest + environment variable tests | 18 | 100% |
| **v0.5** | Kubernetes manifest security policy compliance | Pytest + PyYAML Pod Security tests | 24 | 100% |
| **v0.6** | Automated Property Fuzzing & Mutation Testing | Pytest + Hypothesis + Adversarial Payloads | **29** | **100%** |

---

## 3. Summary
Version 0.6 achieves automated testing maturity. With property-based fuzzing hardening the validation layer against unexpected crashes and GitHub Actions enforcing five distinct automated security gates, the application is robust, self-verifying, and ready for final release.
