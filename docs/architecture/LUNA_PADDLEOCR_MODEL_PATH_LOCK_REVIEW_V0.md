# LUNA — PaddleOCR Model Path Lock Review v0

## Phase

- **Phase-ModelOCR-006C**

## Review scope

- runtime det/rec/cls paths
- runtime model source classification (`pinned_manifest | paddlex_cache | auto_resolved | unknown`)
- runtime hash evidence and manifest alignment evidence
- lock status (`locked | fallback_cache | unknown | mismatch`) with reasons
