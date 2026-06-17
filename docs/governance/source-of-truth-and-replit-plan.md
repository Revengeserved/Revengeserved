# Source of Truth and Replit Execution Plan

Status: Approved
Phase: 6.5 Safety Stand-Down

## Source of Truth

The source-of-truth repository for this project is:

`Revengeserved/file-org-recovery`

This is the repository that should be imported into Replit for future test execution.

The public profile repository `Revengeserved/Revengeserved` is not the project source of truth and should not be used for Phase 7 scanner work.

## Execution Environment

Codex is no longer required for the next phase.

Replit may be used as the runtime/testing environment for early test-fixture work because it can run in a browser and is easier to access from iPhone or a public computer.

## Replit Safety Boundary

Replit is a testing lab, not a private file vault.

Allowed in Replit:

- fake test fixtures
- metadata-only dry-run scanner tests
- SQLite test database generated from fake fixtures
- import/runtime checks
- path policy checks
- redaction checks

Not allowed in Replit during Phase 7:

- real iPhone data
- real iCloud data
- real Google Drive data
- real Dropbox data
- real OneDrive data
- wallet files
- legal files
- medical files
- private documents
- real local exports
- live cloud sync roots

## Phase 7 Gate

Phase 7 may only start after Phase 6.5 audit review passes.

Phase 7 must remain:

`Metadata-only dry-run scan of test fixtures`

No real personal files may be scanned in Phase 7.
