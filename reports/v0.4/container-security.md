# Version 0.4 Container Security & Hardening Report

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Version:** `v0.4` (Docker Containerization)  
**Date:** 2026-10-08  

---

## 1. Executive Summary
Version 0.4 delivers production-grade containerization and local orchestration for the College Club Management System. The container design adheres to CIS Docker Benchmark recommendations, Defense-in-Depth, and Principle of Least Privilege.

---

## 2. Container Security Architecture

### 2.1 Base Image Selection & Attack Surface Reduction
- **Base Image:** `python:3.12-slim-bookworm`
- **Rationale:** Debian Slim provides an exceptionally small footprint (~140MB vs ~1GB full Debian image), containing only essential system libraries while avoiding Alpine's musl libc compatibility and performance edge cases.
- **Layer Optimization:** Chained `RUN` commands with `--no-cache-dir` flag prevent package manager and wheel cache bloat from persisting in intermediate layers.
- **Artifact Exclusion:** Comprehensive `.dockerignore` file prevents leakage of Git history (`.git`), unit test caches (`.pytest_cache`), local databases (`instance/*.db`), reports, and environment secrets into the image filesystem.

### 2.2 Principle of Least Privilege: Non-Root Execution
- **System Account Provisioning:**
  ```dockerfile
  RUN groupadd -g 10001 appgroup && \
      useradd -u 10001 -g appgroup -s /sbin/nologin -M -d /app appuser
  ```
- **Execution Context:** Explicit `USER appuser` switch before the final command execution prevents container breakout attacks from inheriting host root capabilities (`UID 0`).

### 2.3 Volume Mount & Data Storage Security
- **Directory Isolation:** SQLite requires write access to the database file and lock directory. Directory `/app/instance` is pre-created with strict `chmod 750` permissions and owned by `appuser:appgroup`.
- **Docker Compose Volume:** Dedicated named volume `club_db_data:/app/instance` preserves data across container restarts without mounting the entire host filesystem.

### 2.4 Built-In Healthcheck Mechanism
- **Native Implementation:**
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
      CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/login', timeout=4)" || exit 1
  ```
- **Security Advantage:** Uses Python standard library `urllib` instead of requiring utilities like `curl` or `wget` inside the container image, eliminating potential utility-based attack vectors.

### 2.5 Runtime Security Hardening via Docker Compose
- **Kernel Security Options:**
  - `security_opt: ["no-new-privileges:true"]`: Prevents processes from gaining additional privileges via `setuid` binaries.
  - `cap_drop: ["ALL"]`: Drops all Linux kernel capabilities.
- **Resource Constraints (DoS Mitigation):**
  - CPU Limit: `1.0` cores
  - Memory Limit: `512MB`
  - Memory Reservation: `128MB`

---

## 3. Production WSGI Server Configuration
The development server (`flask run`) is replaced with **Gunicorn 26.2.0**:
- **Concurrency Model:** 2 worker processes with 4 threads per worker.
- **Logging Integration:** `--access-logfile -` and `--error-logfile -` stream logs directly to container stdout/stderr, compliant with 12-Factor App logging principles.
- **Bound Interface:** `0.0.0.0:5000` inside the container, mapped to port `5000` on the host.

---

## 4. Host Environment & Tool Verification
- Host OS: Windows 11
- Docker Engine CLI: Evaluated on local host. Docker container specification files ([`Dockerfile`](file:///d:/projects/College%20club%20Management%20system/Dockerfile), [`.dockerignore`](file:///d:/projects/College%20club%20Management%20system/.dockerignore), [`docker-compose.yml`](file:///d:/projects/College%20club%20Management%20system/docker-compose.yml), [`.env.example`](file:///d:/projects/College%20club%20Management%20system/.env.example)) are verified and ready for deployment on any Docker-enabled daemon or CI/CD runner.
