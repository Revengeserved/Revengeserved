# Filename Preservation, Duplicate Detection, and Future Renaming Rule

Status: Approved
Phase: 6.5 Safety Stand-Down

## Rule

The system must preserve all original filenames, original paths, timestamps, metadata, and source locations during inventory, classification, duplicate detection, and review.

The system must not rename files during initial inventory or duplicate detection.

Duplicate detection must not rely on filename matching. Files with different names may be exact duplicates, and files with the same name may be different files.

Exact duplicate detection shall be based on SHA-256 content hashing when hashing is approved and available.

Metadata-only scans may identify possible duplicates using filename, size, date, extension, or path evidence, but these are not proof of duplication.

The system may later generate proposed cleaned filenames after inventory, classification, duplicate grouping, and review are complete.

Proposed filenames must be stored separately from original filenames and must include the reason, confidence score, collision status, and approval status.

No rename may be applied automatically.

Renaming may only occur after manual user approval and only after the original filename and source path have been permanently preserved in the inventory and audit log.

Original filenames remain part of the permanent record even if a later approved rename occurs.

## Implementation Notes

A later phase should add a `filename_recommendations` table or equivalent structure with at least:

- file_id
- original_filename
- proposed_filename
- reason
- confidence_score
- collision_status
- approval_status
- approved_by
- approved_time
- applied_time

No rename operation should exist in the first scanner implementation.
