# Evidence Checklist – Version 0.3

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.3 (Secure Implementation & Hardening)  

This checklist enumerates all physical evidence artifacts and test verifications required to demonstrate practical completion of Version 0.3 during laboratory examination.

---

## Required Screenshots & Artifacts

| Item # | Evidence Description | Target Screen / Command / File | Status / Verification Method |
|:------:|----------------------|--------------------------------|------------------------------|
| **EV3-01** | **Application Running** | Browser at `http://127.0.0.1:5000/login` | Application operational with hardened security controls |
| **EV3-02** | **Critical Security Scenario 1 (ALLOW)** | Coordinator modifying own club event | Modal saves successfully; flash notification displayed; `EVENT_MODIFIED` audit log created |
| **EV3-03** | **Critical Security Scenario 2 (DENY)** | Coordinator modifying other club event | POST blocked; flash message: "Access Denied: You are not authorized to modify events for another club."; `AUTHZ_FAILURE` audit log created |
| **EV3-04** | **Critical Security Scenario 3 (DENY)** | Student attempting event edit POST | Denied by role decorator; redirect to login or error |
| **EV3-05** | **Critical Security Scenario 4 (ALLOW)** | Administrator modifying event | Successfully saves; `EVENT_MODIFIED` audit log created |
| **EV3-06** | **SEC03 Input Validation** | `app/validators.py` | Enforces type, length bounds, date formatting; bounds test passes |
| **EV3-07** | **SEC03 Stored XSS Neutralization** | `templates/coordinator.html` | Inline `onclick` replaced with HTML5 `data-*` attributes & event listeners |
| **EV3-08** | **SEC05 Audit Trail Coverage** | Terminal / DB `audit_logs` | Logs generated for `LOGIN_FAILED`, `AUTHZ_FAILURE`, `EVENT_MODIFIED`, `EVENT_REGISTERED` |
| **EV3-09** | **Flake8 Quality Scan Output** | Terminal: `flake8 app/ tests/ --statistics` | **0 violations** (100% PEP 8 compliant) |
| **EV3-10** | **Bandit SAST Output** | Terminal: `bandit -r app/` | **0 issues identified** (0 High, 0 Medium, 0 Low) |
| **EV3-11** | **Semgrep Scan Output** | Terminal: `semgrep scan --config auto app/` | **0 findings** (290 rules scanned) |
| **EV3-12** | **pip-audit SCA Output** | Terminal: `pip-audit -r requirements.txt` | **No known vulnerabilities found** (`Werkzeug==3.1.9`) |
| **EV3-13** | **Pytest Test Suite Output** | Terminal: `python -m pytest -v` | **18 passed, 0 failed** (100% pass rate) |
| **EV3-14** | **Git Commit Log** | Terminal: `git log -1` | Displays commit: `v0.3: Implement authentication RBAC and security controls` |
| **EV3-15** | **Git Tag Created** | Terminal: `git tag -n` | Displays tag `v0.3` |
| **EV3-16** | **GitHub Push Verification** | GitHub web repository | Verified on `main`, `develop`, and `v0.3` tag |
