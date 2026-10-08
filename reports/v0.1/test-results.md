# Test Results – Version 0.1

**Date:** 2026-10-08  
**Framework:** pytest 9.1.1  
**Python Version:** 3.12.5  
**Execution Command:** `python -m pytest -v`

---

## 1. Executive Summary

| Metric | Result |
|--------|--------|
| **Total Tests** | 12 |
| **Passed Tests** | 12 |
| **Failed Tests** | 0 |
| **Errors** | 0 |
| **Pass Rate** | 100% |
| **Execution Duration** | 18.61s |

---

## 2. Detailed Test Cases

| # | Test Identifier | Purpose | Outcome | Notes |
|---|-----------------|---------|---------|-------|
| 1 | `test_student_login` | Verify student authentication and dashboard redirection | **PASSED** | Validates session setup for role `student` |
| 2 | `test_coordinator_login` | Verify coordinator authentication and dashboard redirection | **PASSED** | Validates session setup for role `coordinator` |
| 3 | `test_admin_login` | Verify administrator authentication and dashboard redirection | **PASSED** | Validates session setup for role `admin` |
| 4 | `test_view_clubs` | Verify student can browse all registered campus clubs | **PASSED** | Renders 3 seeded clubs |
| 5 | `test_join_club` | Verify student joining a campus club | **PASSED** | Creates record in `MEMBERSHIP` table |
| 6 | `test_view_events` | Verify student viewing upcoming events | **PASSED** | Displays scheduled events |
| 7 | `test_event_registration` | Verify student registering for a club event | **PASSED** | Creates record in `EVENT_REGISTRATION` |
| 8 | `test_event_creation` | Verify coordinator creating an event | **PASSED** | Creates record in `EVENT`, triggers announcement |
| 9 | `test_announcement_creation` | Verify coordinator publishing campus announcement | **PASSED** | Creates record in `ANNOUNCEMENT` |
| 10 | `test_invalid_login` | Verify rejection of invalid credentials | **PASSED** | Shows proper user feedback |
| 11 | `test_unauthenticated_access_redirect` | Verify unauthenticated access protection | **PASSED** | Redirects anonymous requests to `/login` |
| 12 | `test_sec02_unauthorized_cross_club_event_modification_v0_1` | Verify presence of controlled weakness SEC02 in v0.1 | **PASSED** | Documents missing club-level authorization in v0.1 |
