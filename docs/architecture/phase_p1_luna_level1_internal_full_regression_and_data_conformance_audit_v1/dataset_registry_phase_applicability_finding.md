# Dataset Registry Phase Applicability Finding

Finding: `Dataset Registry / declaration:phase_present`

- Historical severity: `MAJOR`
- Category: `AUDIT_INFRASTRUCTURE`
- Stage: Stage 7
- Historical observed result: `FAIL`
- Current status: `RESOLVED`

The audited source is:

`capabilities/evaluation/dataset_registry/registry_declaration_v1.json`

It is a durable evaluation-owned registry declaration with `schema_id`,
`registry_id`, `registry_version`, owner, provenance/source-of-truth, and
evaluation/runtime boundary fields. It is not a phase-scoped execution
artifact and contains no `phase` field.

The canonical `DatasetRegistryV1` contract in
`capabilities/evaluation/dataset_registry/types_v1.py` requires registry
identity/version, owner, evaluation-only/runtime boundary, and validates
registered entry/sample/annotation/benchmark fields. It does not require
`phase`.

The previous audit applied a generic `bool(payload.get("phase"))` check to
this declaration. The audit now declares `phase_required=false` for the
Dataset Registry entry and records `phase_present` as `NOT_APPLICABLE` while
leaving the declaration data unchanged. Phase-scoped runner outputs retain
`phase_required=true`.

No Dataset Registry, runtime, cognition, or archive implementation was
modified.
