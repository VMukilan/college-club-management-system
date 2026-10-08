# Evidence Checklist – Version 0.4

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.4 (Docker Containerization & Orchestration)  

This checklist enumerates all physical evidence artifacts and configuration verifications required to demonstrate practical completion of Version 0.4 during laboratory examination.

---

## Required Artifacts & Verifications

| Item # | Evidence Description | Target Screen / Command / File | Verification Method / Status |
|:------:|----------------------|--------------------------------|------------------------------|
| **EV4-01** | **Hardened Dockerfile** | `Dockerfile` | Non-root `appuser` (UID 10001), slim base, urllib healthcheck, Gunicorn CMD |
| **EV4-02** | **Docker Ignore Specification** | `.dockerignore` | Excludes `.git`, `.pytest_cache`, `tests/`, `instance/*.db`, `.env` |
| **EV4-03** | **Docker Compose Orchestration** | `docker-compose.yml` | Resource limits (1.0 CPU, 512MB RAM), `no-new-privileges`, `cap_drop: ALL`, persistent volume |
| **EV4-04** | **Environment Configuration Template** | `.env.example` | Production secret key and port configuration template |
| **EV4-05** | **Production WSGI Dependency** | `requirements.txt` | Includes `gunicorn==26.2.0` |
| **EV4-06** | **Container Entrypoint Support** | `run.py` | Environment variable port/host parsing |
| **EV4-07** | **Pytest Test Suite Output** | Terminal: `python -m pytest -v` | **18 passed, 0 failed** (100% pass rate) |
| **EV4-08** | **Flake8 Quality Scan Output** | Terminal: `flake8 run.py app/ tests/ --statistics` | **0 violations** (100% PEP 8 compliance) |
| **EV4-09** | **Bandit SAST Output** | Terminal: `bandit -r app/` | **0 issues identified** (0 High, 0 Medium, 0 Low) |
| **EV4-10** | **Semgrep Scan Output** | Terminal: `semgrep scan --config auto app/` | **0 findings** (290 rules scanned) |
| **EV4-11** | **pip-audit SCA Output** | Terminal: `pip-audit -r requirements.txt` | **No known vulnerabilities found** |
| **EV4-12** | **Git Commit Log** | Terminal: `git log -1` | Displays commit: `v0.4: Implement secure Docker containerization and compose orchestration` |
| **EV4-13** | **Git Tag Created** | Terminal: `git tag -n` | Displays tag `v0.4` |
| **EV4-14** | **GitHub Push Verification** | GitHub web repository | Verified on `main`, `develop`, and `v0.4` tag |
