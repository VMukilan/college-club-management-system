# Security Findings Analysis – Version 0.2

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.2  
**Tools Executed:** Bandit 1.9.4, Semgrep 1.179.0, pip-audit 2.10.1  

---

## 1. Automated SAST & SCA Scan Results

### Bandit SAST Results (`bandit -r app/`)
- Total lines scanned: 1321
- **High Severity:** 0
- **Medium Severity:** 0 *(Down from 1 in v0.1! B608 SQL injection eliminated)*
- **Low Severity:** 1 *(Down from 3 in v0.1! B110 try-except-pass eliminated)*
  - `B105`: Hardcoded test secret in `TestingConfig.SECRET_KEY` ([app/config.py](file:///d:/projects/College%20club%20Management%20system/app/config.py#L30))

### Semgrep SAST Results (`semgrep scan --config auto app/`)
- Target files scanned: 10
- Rules evaluated: 290
- **Total Findings:** **0** *(Down from 1 blocking issue in v0.1!)*
- Result: Raw query string concatenation finding in `app/services.py` completely eliminated through removal of dead code routine.

### Dependency Vulnerability Results (`pip-audit -r requirements.txt`)
- Total packages: 6
- Vulnerabilities: 1 known CVE (`werkzeug==3.1.8`, `CVE-2026-102598`)
- Scheduled for version upgrade in v0.3 / v0.4 container build.

---

## 2. Controlled Architectural Security Weaknesses Status

| ID | Weakness | Status in v0.2 | Notes / Planned v0.3 Remediation |
|:---:|----------|:--------------:|-----------------------------------|
| **SEC01** | Missing Centralized Authorization | In Progress | Centralized decorators introduced in `app/auth_decorators.py`; full declarative RBAC server-side guard in v0.3 |
| **SEC02** | Unauthorized Event Modification (IDOR) | **INTENTIONALLY MAINTAINED** | Preserved in v0.2 as required so the security fix can be implemented and contrasted in v0.3 |
| **SEC03** | Incomplete Input Validation | Pending | Schema validation layer planned for v0.3 |
| **SEC04** | Error Information Disclosure | **IMPROVED** | Raw `str(e)` strings replaced with user-safe flash alerts; backend logs structured errors |
| **SEC05** | Inconsistent Audit Logging | Pending | Audit coverage expansion scheduled for v0.3 |
