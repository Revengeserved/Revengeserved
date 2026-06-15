"""SQLite inventory database schema.

The database stores observations about files. It must not store file contents.
Original storage locations remain the source of truth.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,
    source_account TEXT,
    source_path TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    extension TEXT,
    mime_type TEXT,
    file_size_bytes INTEGER,
    created_time TEXT,
    modified_time TEXT,
    observed_time TEXT NOT NULL,
    last_seen_time TEXT NOT NULL,
    source_file_id TEXT,
    parent_path TEXT,
    is_folder INTEGER DEFAULT 0,
    is_package INTEGER DEFAULT 0,
    is_deleted_at_source INTEGER DEFAULT 0,
    scan_batch_id INTEGER
);

CREATE TABLE IF NOT EXISTS file_hashes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    hash_type TEXT NOT NULL,
    hash_value TEXT,
    hash_time TEXT,
    hash_status TEXT NOT NULL,
    hash_error TEXT,
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS classifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    classification_type TEXT NOT NULL,
    category TEXT,
    subcategory TEXT,
    confidence_score INTEGER NOT NULL,
    evidence TEXT NOT NULL,
    classifier_version TEXT NOT NULL,
    classified_time TEXT NOT NULL,
    review_required INTEGER DEFAULT 0,
    protected_status TEXT NOT NULL,
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS duplicate_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_hash TEXT,
    hash_type TEXT,
    duplicate_type TEXT NOT NULL,
    created_time TEXT NOT NULL,
    confidence_score INTEGER NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS duplicate_group_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duplicate_group_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    member_role TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    reason TEXT,
    FOREIGN KEY(duplicate_group_id) REFERENCES duplicate_groups(id),
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS scan_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_time TEXT NOT NULL,
    completed_time TEXT,
    source_type TEXT NOT NULL,
    source_account TEXT,
    scan_root TEXT,
    scan_mode TEXT NOT NULL,
    status TEXT NOT NULL,
    files_seen INTEGER DEFAULT 0,
    files_added INTEGER DEFAULT 0,
    files_updated INTEGER DEFAULT 0,
    files_excluded INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    operator_notes TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_time TEXT NOT NULL,
    event_type TEXT NOT NULL,
    actor TEXT NOT NULL,
    source_type TEXT,
    file_id INTEGER,
    scan_batch_id INTEGER,
    action TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    reason TEXT,
    confidence_score INTEGER,
    tool_or_module TEXT,
    FOREIGN KEY(file_id) REFERENCES files(id),
    FOREIGN KEY(scan_batch_id) REFERENCES scan_batches(id)
);

CREATE TABLE IF NOT EXISTS review_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_time TEXT NOT NULL,
    status TEXT NOT NULL,
    assigned_to TEXT,
    decision TEXT,
    decision_time TEXT,
    decision_notes TEXT,
    FOREIGN KEY(file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS config_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_batch_id INTEGER NOT NULL,
    config_type TEXT NOT NULL,
    config_json TEXT NOT NULL,
    created_time TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    FOREIGN KEY(scan_batch_id) REFERENCES scan_batches(id)
);

CREATE INDEX IF NOT EXISTS idx_files_source_path
ON files(source_type, source_path);

CREATE INDEX IF NOT EXISTS idx_files_source_file_id
ON files(source_type, source_file_id);

CREATE INDEX IF NOT EXISTS idx_file_hashes_hash
ON file_hashes(hash_type, hash_value);

CREATE INDEX IF NOT EXISTS idx_classifications_file
ON classifications(file_id);

CREATE INDEX IF NOT EXISTS idx_review_queue_status
ON review_queue(status, priority);

CREATE INDEX IF NOT EXISTS idx_audit_log_file
ON audit_log(file_id);

CREATE INDEX IF NOT EXISTS idx_scan_batches_status
ON scan_batches(status);
"""


def initialize_database(db_path: str | Path) -> None:
    """Create the SQLite inventory schema if needed."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.executescript(SCHEMA_SQL)
        connection.commit()
