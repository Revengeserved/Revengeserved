"""Metadata extraction structures.

Phase 6 defines the shape of metadata records only. Phase 7 will add the first
read-only local export extraction implementation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FileMetadata:
    """Observed metadata for a single file instance."""

    source_type: str
    source_account: str | None
    source_path: str
    original_filename: str
    extension: str | None
    mime_type: str | None
    file_size_bytes: int | None
    created_time: str | None
    modified_time: str | None
    parent_path: str | None
    is_folder: bool = False
    is_package: bool = False
    source_file_id: str | None = None
