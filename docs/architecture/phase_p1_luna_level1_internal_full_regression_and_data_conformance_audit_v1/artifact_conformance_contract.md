# Artifact Conformance Contract

Transient `_eval_out` files are execution outputs and may be replaced by a
new run. Durable archive files are immutable historical records keyed by
execution identity. The audit keeps these roots separate.

It checks readable JSON, phase and case shape, internal references, archive
path/identity correspondence, White-box links, Plane A/B/G links, provenance,
availability objects, and execution-instance consistency. Absolute filesystem
paths are not accepted as canonical identity references.

Archive cross-reference checks are applicable only when the component manifest
declares `archive_required=true`. Runtime-only components such as the A-Route
replay runtime receive an explicit `NOT_APPLICABLE` result and are validated
against their runtime proof and transitions instead. The historical
`CROSS-RUN-None` finding was caused by this applicability omission and is
retained as a resolved audit-infrastructure finding.

The same applicability rule applies to phase presence: durable declarations
use their own schema/identity contract, while phase-scoped execution outputs
may require `phase`. The Dataset Registry declaration therefore reports
`phase_present=NOT_APPLICABLE`; it is not repaired by adding fabricated phase
metadata.
