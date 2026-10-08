# Global Code Smell Tracking

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  

This ledger tracks the introduction, presence, and refactoring remediation of code smells across all developmental versions.

---

## Code Smell Evolution Matrix

| ID | Code Smell | v0.1 | v0.2 | v0.3 | v0.4 | v0.5 | v0.6 | v1.0 |
|----|------------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| **CS01** | Duplicate Auth Logic | Present (10 routes) | Pending | Pending | Pending | Pending | Pending | Pending |
| **CS02** | Long Method | Present (65+ LOC) | Pending | Pending | Pending | Pending | Pending | Pending |
| **CS03** | Large Conditional | Present (nested ifs) | Pending | Pending | Pending | Pending | Pending | Pending |
| **CS04** | Hard-coded Values | Present (literals) | Pending | Pending | Pending | Pending | Pending | Pending |
| **CS05** | Duplicate DB Logic | Present (raw conns) | Pending | Pending | Pending | Pending | Pending | Pending |
| **CS06** | Poor Exception Handling | Present (swallow/leak) | Pending | Pending | Pending | Pending | Pending | Pending |
| **CS07** | Dead Code | Present (legacy fns) | Pending | Pending | Pending | Pending | Pending | Pending |

---

## Measurement Tools
- **Flake8 (PEP 8 / Code Style & Smells):** 82 issues in v0.1
- **Bandit (Quality & Anti-patterns):** B110 (2 instances), B608 (1 instance), B106 (1 instance)
