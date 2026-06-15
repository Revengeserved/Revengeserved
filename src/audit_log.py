"""Append-only audit logging helpers.

The audit log is an evidence ledger. Normal application logic must append
corrections instead of editing or deleting old audit events.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    """Structured audit event used before database persistence exists."""

    event_type: str
    actor: str
    action: str
    reason: str
    tool_or_module: str
    event_time: str
    file_id: int | None = None
    scan_batch_id: int | None = None
    confidence_score: int | None = None


def utc_now_iso() -> str:
    """Return the current UTC timestamp as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def build_event(
    *,
    event_type: str,
    actor: str,
    action: str,
    reason: str,
    tool_or_module: str,
    file_id: int | None = None,
    scan_batch_id: int | None = None,
    confidence_score: int | None = None,
) -> AuditEvent:
    """Build an immutable audit event.

    Persistence is intentionally deferred until inventory_db is initialized.
    """
    return AuditEvent(
        event_type=event_type,
        actor=actor,
        action=action,
        reason=reason,
        tool_or_module=tool_or_module,
        event_time=utc_now_iso(),
        file_id=file_id,
        scan_batch_id=scan_batch_id,
        confidence_score=confidence_score,
    )
