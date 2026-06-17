"""Report redaction helpers.

Reports must not expose secrets or recovery material. This module stores labels
and placeholders, not raw sensitive values.
"""

from __future__ import annotations

REDACTED = "REDACTED"
SAFE_DESCRIPTION_MAX_LEN = 160
SENSITIVE_LABELS = {
    "seed_phrase",
    "private_key",
    "password",
    "recovery_code",
    "ssn",
    "bank_account",
    "medical_identifier",
    "legal_case_identifier",
    "credential_material",
    "private_note",
}


def redact_value(value: str | None) -> str:
    """Return a safe placeholder instead of the provided value."""
    return REDACTED


def sanitize_description(label: str, description: str) -> str:
    """Prevent report descriptions from leaking sensitive text."""
    normalized = label.strip().lower()
    cleaned = " ".join(description.split())
    if normalized in SENSITIVE_LABELS:
        return "Sensitive evidence detected"
    return cleaned[:SAFE_DESCRIPTION_MAX_LEN]


def evidence_flag(label: str, description: str) -> dict[str, str | bool]:
    """Build a safe evidence flag without raw sensitive content."""
    normalized = label.strip().lower()
    return {
        "sensitive": normalized in SENSITIVE_LABELS,
        "label": normalized,
        "description": sanitize_description(normalized, description),
        "raw_value": REDACTED,
    }
