# Evidence Checklist – Version 0.1

**Course:** 24CYS401 – Secure Software Engineering  
**Version:** v0.1  

This checklist enumerates all physical evidence artifacts and screenshots required to demonstrate practical completion of Version 0.1 during laboratory examination.

---

## Required Screenshots & Artifacts

| Item # | Evidence Description | Target Screen / Command / File | Status / Verification Method |
|:------:|----------------------|--------------------------------|------------------------------|
| **EV-01** | **Application Running** | Browser at `http://127.0.0.1:5000/login` | Application loads successfully |
| **EV-02** | **Student Login** | Login using `student_alice` / `StudentPass123` | Redirects to Student Portal (`/student`) |
| **EV-03** | **Coordinator Login** | Login using `coord_robotics` / `CoordPass123` | Redirects to Coordinator Portal (`/coordinator`) |
| **EV-04** | **Administrator Login** | Login using `admin` / `AdminPass123` | Redirects to Administrator Control Center (`/admin`) |
| **EV-05** | **Student Functionality** | View Clubs, Join Club, View Events, Register for Event | Cards and tables update in Student Portal |
| **EV-06** | **Coordinator Functionality** | Create Event form, Roster of Club Members, Broadcast Announcement | Event appears in event table and announcement roster |
| **EV-07** | **Admin Functionality** | Create Club, Assign Coordinator, View System Audit Trail | Renders registered clubs and active audit entries |
| **EV-08** | **Git Repository Initialized** | Terminal: `git status` | Clean working tree on branch `main` |
| **EV-09** | **Git Commit Log** | Terminal: `git log -1` | Displays commit message: `v0.1: Initial College Club Management System` |
| **EV-10** | **Git Tag Created** | Terminal: `git tag -n` | Displays tag `v0.1` |
| **EV-11** | **GitHub Repository / Remote** | GitHub Web UI or `git remote -v` | Repository created and remote connected |
| **EV-12** | **GitHub Actions Pipeline** | GitHub Actions Tab: `.github/workflows/ci.yml` | Workflow triggered on push / tag |
| **EV-13** | **Code Quality Scan Output** | Terminal: `flake8 app/ --statistics` | Shows 82 quality issues identified |
| **EV-14** | **Code Smells (CS01 - CS07)** | `app/services.py`, `app/routes.py` lines | Code smells highlighted in IDE |
| **EV-15** | **Security Scan (Bandit)** | Terminal: `bandit -r app/` | Displays 4 issues (1 Medium, 3 Low) |
| **EV-16** | **Dependency Scan (pip-audit)** | Terminal: `pip-audit -r requirements.txt` | Displays 1 CVE for `werkzeug==3.1.8` |
| **EV-17** | **Static Scan (Semgrep)** | Terminal: `semgrep scan --config auto app/` | Displays 1 query concatenation issue |
| **EV-18** | **Pytest Test Results** | Terminal: `python -m pytest -v` | Displays 12 passed tests (100% pass rate) |

---

## Instructions for Capturing Evidence
1. Run the local Flask server using:
   ```bash
   python run.py
   ```
2. Open your web browser and navigate through EV-01 to EV-07 using the quick credentials helper buttons.
3. Take terminal screenshots of `python -m pytest -v`, `flake8 app/ --statistics`, `bandit -r app/`, and `git log -1`.
4. Store exported screenshot files (`.png` / `.jpg`) in this `evidence/v0.1/` directory.
