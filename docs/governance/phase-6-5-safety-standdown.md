# Phase 6.5 Safety Stand-Down

Status: Approved for safety-file implementation
Phase: 6.5

## Purpose

This stand-down exists before Phase 7 because Phase 7 introduces the first scanner behavior. Even read-only scanning can expose private paths, trigger cloud downloads, or mishandle protected files if the controls are weak.

## Current Connector Status

- GitHub is connected.
- Codex is not connected in this chat.
- Real iPhone, iCloud, Google Drive, Dropbox, and OneDrive file sources are not connected for scanning.
- Phase 6.5 must not require real personal files.

## Safety Rules

1. The first scanner must be metadata-only.
2. File modification is disabled.
3. File deletion is disabled.
4. File renaming is disabled.
5. File moving is disabled.
6. Unknown protected status is treated as protected until manual review.
7. Live cloud sync roots are not allowed for the first scan.
8. Symbolic links are not followed by default.
9. Packages and bundles require manual review.
10. Reports must redact sensitive values.
11. Real scan outputs must not be committed to GitHub.
12. Local databases must not be committed to GitHub.
13. Real scan path configs must not be committed to GitHub.
14. Duplicate detection must not rely on filenames.
15. Exact duplicates require SHA-256 content hashing after hashing is approved.

## Phase 7 Renaming

Phase 7 should be named:

`Phase 7 — Metadata-only dry-run scan of test fixtures`

Phase 7 must use fake test fixtures only, not real personal data.

## Approval Gate Before Phase 7

Before Phase 7 starts, confirm:

- `.gitignore` blocks local databases, reports, logs, real exports, and local path configs.
- Path policy refuses paths outside approved roots.
- Symlinks are blocked or queued for manual review.
- Redaction exists before report generation.
- No rename, move, delete, or cloud-write functionality exists.
