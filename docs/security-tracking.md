# Global Security Issue Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks controlled security weaknesses introduced across versions and their eventual remediation and verification.

---

## Security Weaknesses Tracking Matrix

| ID | Security Issue | Introduced | Fixed | Fixed Version | Verification Method |
|----|----------------|:----------:|:-----:|:-------------:|---------------------|
| **SEC01** | Missing centralized authorization | v0.1 | No | Planned v0.3 | Automated route security checks / 403 response verification |
| **SEC02** | Unauthorized event modification (IDOR) | v0.1 | No | Planned v0.3 | `test_sec02_unauthorized_cross_club_event_modification` (fails in v0.1, must pass in v0.3) |
| **SEC03** | Weak input validation | v0.1 | No | Planned v0.3 | Boundary testing & fuzz tests on string parameters |
| **SEC04** | Weak error handling (info disclosure) | v0.1 | No | Planned v0.3 | Error response inspection verifying lack of stack/SQL traces |
| **SEC05** | Missing audit logging | v0.1 | No | Planned v0.3 | Database verification of `AUDIT_LOG` table entries on failures & edits |

---

## Automated Tool Findings Tracking (SAST & SCA)

| Tool | Finding / ID | Severity | First Seen | Remediation Plan |
|------|--------------|----------|:----------:|------------------|
| **Bandit** | B608 (SQL injection in dead code) | Medium | v0.1 | Remove dead function in v0.2 |
| **Bandit** | B106 (Hardcoded secret key) | Low | v0.1 | Move to environment configuration in v0.2 |
| **Bandit** | B110 (Try, Except, Pass x 2) | Low | v0.1 | Implement structured logging in v0.2 |
| **pip-audit** | CVE-2026-102598 (`werkzeug==3.1.8`) | Moderate | v0.1 | Upgrade dependency version in v0.3/v0.4 |
| **Semgrep** | Raw query concatenation | High | v0.1 | Replace with parameterized query / remove in v0.2 |
