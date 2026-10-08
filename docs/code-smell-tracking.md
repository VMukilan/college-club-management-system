# Global Code Smell Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks the introduction, presence, and refactoring remediation of code smells across all developmental versions.

---

## Code Smell Evolution Matrix

| ID | Code Smell | v0.1 | v0.2 | v0.3 | v0.4 | v0.5 | v0.6 | v1.0 |
|----|------------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| **CS01** | Duplicate Auth Logic | Present (10 routes) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |
| **CS02** | Long Method | Present (65+ LOC) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |
| **CS03** | Large Conditional | Present (nested ifs) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |
| **CS04** | Hard-coded Values | Present (literals) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |
| **CS05** | Duplicate DB Logic | Present (raw conns) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |
| **CS06** | Poor Exception Handling | Present (swallow/leak) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |
| **CS07** | Dead Code | Present (legacy fns) | **RESOLVED** | Pending | Pending | Pending | Pending | Pending |

---

## Measurement Tools
- **Flake8 (PEP 8 / Code Style & Smells):** 82 issues in v0.1 $\rightarrow$ **0 issues in v0.2** (-100%)
- **Bandit (Quality & Anti-patterns):** 4 issues in v0.1 $\rightarrow$ **1 issue in v0.2** (-75%, Medium issues eliminated)
- **Semgrep (Code Rules):** 1 blocking issue in v0.1 $\rightarrow$ **0 issues in v0.2** (-100%)
