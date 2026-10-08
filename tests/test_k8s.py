"""
Kubernetes Manifest Security & Compliance Tests (v0.5)
Verifies that all Kubernetes manifests comply with Pod Security Standards
(Restricted Profile), Principle of Least Privilege, and resource bounds.
"""

import glob
import os
import yaml


def _load_manifests():
    k8s_dir = os.path.join(os.path.dirname(__file__), "..", "k8s")
    files = glob.glob(os.path.join(k8s_dir, "*.yaml"))
    docs = []
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            for doc in yaml.safe_load_all(f):
                if doc:
                    docs.append(doc)
    return docs


def test_k8s_manifests_load_cleanly():
    """Verify that all k8s YAML manifests parse without syntax errors."""
    docs = _load_manifests()
    assert len(docs) >= 11
    kinds = {d.get("kind") for d in docs}
    assert "Deployment" in kinds
    assert "Service" in kinds
    assert "Namespace" in kinds
    assert "NetworkPolicy" in kinds
    assert "ConfigMap" in kinds
    assert "Secret" in kinds


def test_k8s_namespace_restricted_pod_security():
    """Verify that namespace enforces Pod Security Standards Restricted."""
    docs = _load_manifests()
    ns = next(d for d in docs if d.get("kind") == "Namespace")
    labels = ns.get("metadata", {}).get("labels", {})
    assert labels.get("pod-security.kubernetes.io/enforce") == "restricted"
    assert labels.get("pod-security.kubernetes.io/audit") == "restricted"


def test_k8s_deployment_security_context():
    """Verify non-root, seccomp, dropped capabilities, and no escalation."""
    docs = _load_manifests()
    deployment = next(d for d in docs if d.get("kind") == "Deployment")
    pod_spec = deployment["spec"]["template"]["spec"]

    # Pod level security context
    pod_sec = pod_spec.get("securityContext", {})
    assert pod_sec.get("runAsNonRoot") is True
    assert pod_sec.get("runAsUser") == 10001
    assert pod_sec.get("seccompProfile", {}).get("type") == "RuntimeDefault"

    # Container level security context
    container = pod_spec["containers"][0]
    c_sec = container.get("securityContext", {})
    assert c_sec.get("allowPrivilegeEscalation") is False
    assert "ALL" in c_sec.get("capabilities", {}).get("drop", [])


def test_k8s_deployment_resources_and_probes():
    """Verify that containers define resource bounds and health probes."""
    docs = _load_manifests()
    deployment = next(d for d in docs if d.get("kind") == "Deployment")
    container = deployment["spec"]["template"]["spec"]["containers"][0]

    # Resource limits and requests
    resources = container.get("resources", {})
    assert "limits" in resources
    assert "requests" in resources
    assert resources["limits"]["memory"] == "512Mi"
    assert resources["requests"]["memory"] == "128Mi"

    # Health probes
    assert "livenessProbe" in container
    assert "readinessProbe" in container


def test_k8s_serviceaccount_token_automount_disabled():
    """Verify automountServiceAccountToken is False for least privilege."""
    docs = _load_manifests()
    sa = next(d for d in docs if d.get("kind") == "ServiceAccount")
    assert sa.get("automountServiceAccountToken") is False


def test_k8s_networkpolicy_rules():
    """Verify NetworkPolicy isolates ingress and restricts egress."""
    docs = _load_manifests()
    netpol = next(d for d in docs if d.get("kind") == "NetworkPolicy")
    spec = netpol.get("spec", {})
    assert "Ingress" in spec.get("policyTypes", [])
    assert "Egress" in spec.get("policyTypes", [])
    assert len(spec.get("ingress", [])) > 0
    assert len(spec.get("egress", [])) > 0
