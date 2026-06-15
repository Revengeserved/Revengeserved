"""Report redaction helpers.

Reports must not expose secrets or recovery material. This module stores labels
and placeholders, not raw sensitive values.
"""

from __future__ import annotations

REDACTED = "REDACTED"
SENSITIVE_LABELS = {
    "seed_phrase",
    "private_key",
    "password",
    "recovery_code",
    "ssn",
    "bank_account",
    "medical_identifier",
    "legal_case_identifier",
}


def redact_value(value: str | None) -> str:
    """Return a safe placeholder instead of the provided value."""
    if value is None:
        return REDACTED
    return REDACTED


def evidence_flag(label: str, description: str) -> dict[str, str | bool]:
    """Build a safe evidence flag without raw sensitive content."""
    normalized = label.strip().lower()
    return {
        "sensitive": normalized in SENSITIVE_LABELS,
        "label": normalized,
        "description": description,
        "raw_value": REDACTED,
    }
