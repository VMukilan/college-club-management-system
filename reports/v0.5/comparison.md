# Evolutionary Comparison: v0.1 through v0.5

**Course:** 24CYS401 – Secure Software Engineering  
**Project:** College Club Management System  
**Comparison:** Progression across `v0.1` (Baseline), `v0.2` (Refactored), `v0.3` (Secured), `v0.4` (Containerized), and `v0.5` (Kubernetes Orchestrated)  
**Date:** 2026-10-08  

---

## 1. Quantitative Metric Progression

| Metric | v0.1 | v0.2 | v0.3 | v0.4 | v0.5 | Cumulative Delta |
|--------|:----:|:----:|:----:|:----:|:----:|:----------------:|
| **Active Code Smells** | 7 | 0 | 0 | 0 | **0** | **-7 (-100%)** |
| **Flake8 Violations** | 82 | 0 | 0 | 0 | **0** | **-82 (-100%)** |
| **Bandit SAST Issues** | 4 | 1 | 0 | 0 | **0** | **-4 (-100%)** |
| **Semgrep SAST Issues** | 1 | 0 | 0 | 0 | **0** | **-1 (-100%)** |
| **pip-audit Vulnerabilities** | 1 | 1 | 0 | 0 | **0** | **-1 (-100%)** |
| **Automated Tests** | 12 | 12 | 18 | 18 | **24** | **+12 (+100%)** |
| **Test Pass Rate** | 100% | 100% | 100% | 100% | **100% (24/24)** | **Maintained** |
| **Active Security Weaknesses** | 5 | 5 | 0 | 0 | **0** | **-5 (-100%)** |
| **Infrastructure Paradigm** | Host | Host | Host | Docker Compose | **Kubernetes Cluster** | **Cloud Native** |
| **High Availability & Autoscaling** | None | None | None | None | **2 Replicas + HPA** | **Enterprise Resilience** |

---

## 2. Infrastructure & Orchestration Evolution Matrix

| Feature | v0.1 / v0.2 / v0.3 | v0.4 (Docker) | v0.5 (Kubernetes) |
|---|---|---|---|
| **Deployment Target** | Bare OS / Host | Single Host Docker Engine | Kubernetes Cluster |
| **Service High Availability** | 1 process | 1 container | Multi-replica (2 pods) with RollingUpdate |
| **Auto-Healing & Probes** | Manual | Single container healthcheck | Automated Liveness & Readiness Probes with kubelet restart |
| **Dynamic Autoscaling** | None | None | HorizontalPodAutoscaler (CPU threshold 75%) |
| **Cluster Security Policy** | Host OS file permissions | Docker `cap_drop: ALL` | Pod Security Standards **Restricted Profile** |
| **Network Security** | Unrestricted localhost | Bridge network | Zero-Trust **NetworkPolicy** (Ingress + Egress filtering) |
| **Identity & Access** | Host user | `USER appuser` | Dedicated `ServiceAccount` + RBAC `Role` & `RoleBinding` |
| **Secrets Management** | Flat config / env file | Compose `.env` | Native Kubernetes `Secret` + `ConfigMap` segregation |
| **Ingress & TLS** | Direct port bind | Direct port mapping | Reverse Proxy `Ingress` with TLS termination |

---

## 3. Summary
Version 0.5 expands the application architecture into a hardened Kubernetes orchestration platform, enforcing cluster-level defense-in-depth, declarative least-privilege security policies, and high-availability self-healing capabilities.
