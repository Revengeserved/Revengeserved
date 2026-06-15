"""Safety constants and approval gates for the file organization system.

Phase 6.5 policy:
- Unknown status is treated as protected.
- The first scanner must be metadata-only and dry-run oriented.
- File modification features are intentionally not implemented here.
"""

from __future__ import annotations

from dataclasses import dataclass


UNKNOWN_PROTECTED_STATUS = "unknown"
PROTECTED_STATUS = "protected"
USER_CONTENT_STATUS = "user_content"
MANUAL_REVIEW_STATUS = "manual_review_required"

SAFE_INITIAL_SCAN_MODE = "metadata_only"
HASH_SCAN_MODE = "hash_enabled"


@dataclass(frozen=True)
class SafetyDecision:
    """Result of a safety check."""

    allowed: bool
    reason: str
    protected_status: str
    review_required: bool


def deny(reason: str, protected_status: str = PROTECTED_STATUS) -> SafetyDecision:
    """Return a blocking decision."""
    return SafetyDecision(
        allowed=False,
        reason=reason,
        protected_status=protected_status,
        review_required=True,
    )


def allow(reason: str) -> SafetyDecision:
    """Return an allow decision for read-only inventory operations."""
    return SafetyDecision(
        allowed=True,
        reason=reason,
        protected_status=USER_CONTENT_STATUS,
        review_required=False,
    )


def unknown_requires_review(reason: str) -> SafetyDecision:
    """Treat uncertainty as protected until manual review."""
    return SafetyDecision(
        allowed=False,
        reason=reason,
        protected_status=UNKNOWN_PROTECTED_STATUS,
        review_required=True,
    )
