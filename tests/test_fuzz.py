"""
Automated Security Fuzz Testing Suite (v0.6)
Implements property-based fuzzing and mutation-based vulnerability probing
against validators, service layers, and web route handlers.
"""

from hypothesis import given, settings, strategies as st
from app.validators import (
    validate_string,
    validate_integer_id,
    validate_date_string
)
from app.exceptions import ValidationError

# Curated mutation payloads covering common attack vectors
FUZZ_SECURITY_PAYLOADS = [
    # SQL Injection mutations
    "' OR '1'='1",
    "1; DROP TABLE users; --",
    "admin'--",
    "' UNION SELECT null, null, null --",
    "1' ORDER BY 1--+",
    # Cross-Site Scripting (XSS) mutations
    "<script>alert('XSS')</script>",
    "'\"><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "javascript:/*--></title></script><svg/onload=alert(1)>",
    # Path Traversal mutations
    "../../../../../../etc/passwd",
    "..\\..\\..\\..\\windows\\system32\\config\\sam",
    # Format strings & Template Injections
    "%s%s%s%s%s%n",
    "{{7*7}}",
    "${7*7}",
    "#{7*7}",
    # Extreme Bounds & Null Bytes
    "\x00\x00\x00",
    "A" * 10000,
    "   ",
    "\r\n\t",
    "🎉🔥💻🔒🛡️🚀",
]


@given(st.text())
@settings(max_examples=100)
def test_fuzz_validate_string_arbitrary_text(val):
    """
    Property-based fuzz test: validate_string should never raise unhandled
    exceptions regardless of arbitrary input.
    """
    try:
        result = validate_string(val, min_length=3, max_length=100,
                                 field_name="Fuzz Field")
        assert isinstance(result, str)
        assert 3 <= len(result) <= 100
    except ValidationError:
        pass


@given(st.one_of(st.integers(), st.floats(), st.text(), st.none()))
@settings(max_examples=100)
def test_fuzz_validate_integer_id_types(val):
    """
    Property-based fuzz test: validate_integer_id handles varied types
    and gracefully returns positive integer or raises ValidationError.
    """
    try:
        result = validate_integer_id(val, "Fuzz ID")
        assert isinstance(result, int)
        assert result > 0
    except ValidationError:
        pass


@given(st.text())
@settings(max_examples=50)
def test_fuzz_validate_date_string_arbitrary(val):
    """
    Property-based fuzz test: validate_date_string strictly enforces
    ISO 8601 YYYY-MM-DD or raises ValidationError.
    """
    try:
        result = validate_date_string(val, "Fuzz Date")
        assert isinstance(result, str)
        assert len(result) == 10
    except ValidationError:
        pass


def test_fuzz_event_creation_mutation_payloads(client):
    """
    Fuzz test: Inject malicious SQL, XSS, format strings, and buffer overflows
    into event creation route. Server MUST NOT crash with 500.
    """
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })

    for payload in FUZZ_SECURITY_PAYLOADS:
        response = client.post("/coordinator/events/create", data={
            "title": payload[:100],
            "event_date": "2026-12-15",
            "location": payload[:50] or "Room 101",
            "description": payload
        }, follow_redirects=True)
        # Server must gracefully handle request with 200 (redirect followed)
        # and never crash with 500 Internal Server Error
        assert response.status_code == 200, (
            f"Server failed with status {response.status_code} "
            f"on payload: {payload[:30]!r}"
        )


def test_fuzz_event_modification_mutation_payloads(client):
    """
    Fuzz test: Inject adversarial payloads into event modification endpoint.
    Verifies input validation and object-level authorization repel attacks.
    """
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })

    for payload in FUZZ_SECURITY_PAYLOADS:
        response = client.post("/coordinator/events/edit", data={
            "event_id": payload,
            "title": payload[:100],
            "event_date": payload[:10],
            "location": payload[:50],
            "description": payload
        }, follow_redirects=True)
        assert response.status_code in [200, 400, 403], (
            f"Server crashed with status {response.status_code} "
            f"on payload: {payload[:30]!r}"
        )
