# Evolutionary Comparison: v0.1 vs v0.2 vs v0.3 vs v0.4

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Comparison:** Progression across `v0.1` (Baseline), `v0.2` (Refactored), `v0.3` (Secured), and `v0.4` (Containerized)  
**Date:** 2026-10-08  

---

## 1. Quantitative Metric Progression

| Metric | v0.1 (Baseline) | v0.2 (Refactored) | v0.3 (Secured) | v0.4 (Containerized) | Total Delta |
|--------|:---------------:|:-----------------:|:--------------:|:--------------------:|:-----------:|
| **Active Code Smells** | 7 | 0 | 0 | **0** | **-7 (-100%)** |
| **Flake8 Violations** | 82 | 0 | 0 | **0** | **-82 (-100%)** |
| **Bandit SAST Issues** | 4 | 1 | 0 | **0** | **-4 (-100%)** |
| **Semgrep SAST Issues** | 1 | 0 | 0 | **0** | **-1 (-100%)** |
| **pip-audit Vulnerabilities** | 1 | 1 | 0 | **0** | **-1 (-100%)** |
| **Automated Tests** | 12 | 12 | 18 | **18** | **+6 (+50%)** |
| **Test Pass Rate** | 100% | 100% | 100% | **100% (18/18)** | **Maintained** |
| **Active Security Weaknesses** | 5 (SEC01–05) | 5 | 0 | **0** | **-5 (-100%)** |
| **Containerization Standard** | None (Host only) | None | None | **Production Slim Non-Root** | **NEW** |
| **WSGI Server** | Werkzeug Dev | Werkzeug Dev | Werkzeug Dev | **Gunicorn 26.2.0** | **Production Grade** |

---

## 2. Infrastructure & Deployment Evolution

| Architectural Dimension | v0.1 / v0.2 (Initial Prototype) | v0.3 (Secure Codebase) | v0.4 (Containerized Release) |
|---|---|---|---|
| **Runtime Environment** | Host OS direct execution | Host OS direct execution | Containerized Docker environment |
| **Process Identity** | Current user (potentially root/admin) | Current user | Dedicated unprivileged user (`appuser`, UID 10001) |
| **Base OS Footprint** | Full host system | Full host system | Minimal Debian Slim (`python:3.12-slim-bookworm`) |
| **Kernel Capabilities** | Unrestricted host privileges | Unrestricted host privileges | All capabilities dropped (`cap_drop: ALL`) |
| **Privilege Escalation** | Dependent on OS settings | Dependent on OS settings | Explicitly blocked (`no-new-privileges:true`) |
| **Resource Isolation** | Unbounded | Unbounded | CPU limit (1.0) & Memory limit (512MB) |
| **Health Monitoring** | Manual | Manual | Automated container `HEALTHCHECK` |
| **Data Persistence** | Local directory | Local directory | Dedicated Docker volume (`club_db_data`) |
| **Local Orchestration** | None (Manual python script) | None | Declarative `docker-compose.yml` |

---

## 3. Summary
Version 0.4 elevates the secure codebase of `v0.3` into an isolated, reproducible, production-ready container environment without degrading code quality or introducing security vulnerabilities.
