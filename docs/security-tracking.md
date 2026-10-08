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

| Tool | Finding / ID | Severity | First Seen | Fixed In | Verification Status in v0.4 |
|------|--------------|----------|:----------:|:--------:|-----------------------------|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B106 (Hardcoded secret key in app config) | Low | v0.1 | v0.2 | **Verified: 0 findings** |
| **Bandit** | B105 (Test secret key string) | Low | v0.2 | v0.3 | **Verified: 0 findings** |
| **Semgrep** | Raw query concatenation | High | v0.1 | v0.2 | **Verified: 0 findings** (290 rules scanned) |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | v0.3 | **Verified: 0 vulnerabilities** |

---

## Container Security Controls Matrix (v0.4)

| Security Control | Implementation Detail | Target Layer | Verification Method |
|---|---|---|---|
| **Non-Root Execution** | `appuser` (UID 10001, GID 10001) | `Dockerfile` | `USER appuser` directive |
| **Attack Surface Reduction** | `python:3.12-slim-bookworm` | `Dockerfile` | Minimal base image without development toolchains |
| **Layer Hygiene** | `--no-cache-dir` pip flag | `Dockerfile` | Zero persistent wheel or pip cache in container layers |
| **Build Context Filtering** | `.dockerignore` | Build context | Excludes `.git`, `.pytest_cache`, `tests/`, `instance/*.db`, `.env` |
| **Persistent Storage Isolation** | `/app/instance` (0750 permissions) | Docker Volume | Named volume `club_db_data` |
| **Kernel Privilege Hardening** | `no-new-privileges:true`, `cap_drop: ALL` | `docker-compose.yml` | Linux security options |
| **DoS Resource Limits** | `1.0` CPU limit, `512MB` RAM limit | `docker-compose.yml` | Compose deploy resource limits |
| **Automated Health Monitoring** | Native urllib healthcheck | `Dockerfile` & Compose | `HEALTHCHECK` checking `/login` endpoint |
| **Production WSGI Server** | Gunicorn (2 workers, 4 threads) | `Dockerfile` & `requirements.txt` | CMD execution |
