# Evidence Checklist – Version 0.2

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.2 (Refactoring & Code Smell Reduction)  

This checklist enumerates all physical evidence artifacts and screenshots required to demonstrate practical completion of Version 0.2 during laboratory examination.

---

## Required Screenshots & Artifacts

| Item # | Evidence Description | Target Screen / Command / File | Status / Verification Method |
|:------:|----------------------|--------------------------------|------------------------------|
| **EV2-01** | **Application Running** | Browser at `http://127.0.0.1:5000/login` | Application operational with refactored architecture |
| **EV2-02** | **Centralized Auth Decorators (CS01)** | `app/auth_decorators.py` & `app/routes.py` | Shows `@roles_accepted` applied to routes |
| **EV2-03** | **Long Method Decomposition (CS02)** | `app/services.py` | Shows modular helper methods for event creation |
| **EV2-04** | **Declarative Role Mapping (CS03)** | `app/services.py` (`ROLE_PERMISSIONS`) | Clean dictionary lookup replacing 40-line `if/elif` |
| **EV2-05** | **Centralized Constants & Config (CS04)** | `app/constants.py` & `app/config.py` | `Role` constants and structured `Config` class |
| **EV2-06** | **Repository Metrics Centralization (CS05)** | `app/repositories.py` & `app/routes.py` | `ClubRepository.count()` replacing raw SQL connections |
| **EV2-07** | **Exception Handling & Logging (CS06)** | `app/exceptions.py` & `app/services.py` | Domain exceptions and structured logger usage |
| **EV2-08** | **Dead Code Removal (CS07)** | `app/services.py` | Unused legacy functions deleted |
| **EV2-09** | **Flake8 Quality Scan Output** | Terminal: `flake8 app/ --statistics` | **0 violations** (100% PEP 8 compliance) |
| **EV2-10** | **Bandit SAST Output** | Terminal: `bandit -r app/` | **0 Medium issues** (B608 eliminated), only 1 Low |
| **EV2-11** | **Semgrep Scan Output** | Terminal: `semgrep scan --config auto app/` | **0 findings** (blocking query issue eliminated) |
| **EV2-12** | **Pytest Test Suite Output** | Terminal: `python -m pytest -v` | **12 passed** (100% pass rate preserved) |
| **EV2-13** | **Git Commit Log** | Terminal: `git log -1` | Displays commit: `v0.2: Refactor code smells and improve maintainability` |
| **EV2-14** | **Git Tag Created** | Terminal: `git tag -n` | Displays tag `v0.2` |
| **EV2-15** | **GitHub Push Verification** | GitHub web repository | Verified on `main`, `develop`, and `v0.2` tag |
