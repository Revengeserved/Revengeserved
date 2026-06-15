"""Path safety policy for read-only inventory scans.

This module decides whether a path is eligible for read-only inventory. It does
not scan, move, rename, delete, or hash files.
"""

from __future__ import annotations

from pathlib import Path

from .safety import SafetyDecision, allow, deny, unknown_requires_review

PROTECTED_PATH_FRAGMENTS = (
    "/System/",
    "/Library/",
    "/Applications/",
    "/bin/",
    "/sbin/",
    "/usr/",
    "/var/",
    "AppData",
    "Program Files",
    "Windows",
    ".git",
    "node_modules",
    "__pycache__",
)

PACKAGE_SUFFIXES = (
    ".app",
    ".photoslibrary",
    ".musiclibrary",
    ".imovielibrary",
    ".framework",
    ".bundle",
)


def is_inside_root(path: Path, approved_root: Path) -> bool:
    """Return true only when path resolves inside approved_root."""
    try:
        path.resolve().relative_to(approved_root.resolve())
        return True
    except ValueError:
        return False


def evaluate_path(path: str | Path, approved_root: str | Path) -> SafetyDecision:
    """Evaluate whether a path may be inventoried in read-only mode."""
    candidate = Path(path)
    root = Path(approved_root)
    candidate_text = str(candidate)

    if not is_inside_root(candidate, root):
        return deny("path is outside the approved scan root")

    if candidate.is_symlink():
        return unknown_requires_review("symbolic links are not followed by default")

    if any(fragment in candidate_text for fragment in PROTECTED_PATH_FRAGMENTS):
        return deny("path matched protected path fragment")

    if candidate.suffix.lower() in PACKAGE_SUFFIXES:
        return unknown_requires_review("package or bundle requires manual review")

    return allow("path is inside approved root and no protected pattern matched")
