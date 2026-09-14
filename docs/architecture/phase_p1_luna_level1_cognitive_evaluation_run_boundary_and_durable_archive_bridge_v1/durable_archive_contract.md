# Durable Archive Contract

Implementation: `archive_v1.py`.

Canonical retained-history location:

`evaluation_archive/level1_cognitive_runs/`

This location is distinct from `_eval_out/` and `_tmp_eval_out/`. The latter remain execution/evidence artifact locations and are never promoted automatically.

Archive ownership is `Evaluation Governance`. Records are JSON-serialized `EvaluationRunRecordV1` values with stable identity, version, provenance, source versions, invalidation, trace/profile/gap refs, and boundary flags.

Writes are append-oriented by identity. If the same identity already exists with different content, `ArchiveConflictError` is raised instead of silently overwriting history. Corrections must use a new record identity, supersession, invalidation, or correction refs.

No credentials, unbounded provider payloads, base64 media, or runtime state are stored by this bridge.

