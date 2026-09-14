# Cross-Domain Version / Invalidation Contract v1

## Version reference

No global state version is created. A reusable version reference contains:

`source_owner`, `source_ref`, `source_version`, `issued_or_observed_at`, `validity_status`, `superseded_by_ref`, `invalidation_ref`, `provenance_ref`, `trace_ref`.

It applies to Envelope, Semantic Outline, Cognitive Snapshot, Field, Context, Current World, Intent, Role, Task, Capability/Model/Provider bindings, Evidence, Decision, Action, Outcome and Diagnostics.

## Invalidation record

An invalidation record identifies what became stale/invalid, why, source change, old/new versions if known, affected contract/ref, detector, authority owner, semantic consequence owner, whether re-admission or refresh is required, and trace/provenance.

## Boundary

Invalidation is classification and binding control, not A Reconsideration. A decides local cognitive consequence. Brain decides global consequence. Source owners retain source mutation authority. Loop records the lineage.

## Stale behavior

Consumers must reject, mark stale, degrade, or request a governed new candidate according to the consuming contract. A stale PASS cannot remain indefinitely executable. Historical traces retain the original version and are not rewritten.

