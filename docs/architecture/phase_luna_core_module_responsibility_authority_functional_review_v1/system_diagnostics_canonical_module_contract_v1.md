# System Diagnostics Canonical Module Contract v1

## Canonical purpose

System Diagnostics observes, validates, classifies, versions, and reports
system/runtime health facts and diagnostic evidence for downstream governance,
admission, maintenance, and operator visibility. It does not own semantic,
policy, admission, remediation, or execution decisions.

## Independent boundary

Disposition: **KEEP, narrowly bounded**. Diagnostics is an independent
maintenance-plane evidence boundary because dependency, device, runtime,
provider, resource, protocol, and configuration observations are reused by
multiple consumers. Brain remains the global governance owner; Diagnostics is
not a Brain subroutine and no Health Manager is created by this adjudication.

## Authority

Diagnostics may authoritatively classify the result of an identified probe or
passive telemetry source within its declared scope, with observed time,
source/version, provenance, and freshness. It may publish `unknown`, `stale`,
and `unavailable` rather than fabricate a pass.

## Outputs and stop line

Outputs are diagnostic evidence, health/drift findings, versioned snapshots,
conflict records, and candidate incident/root-cause/remediation references.
Runtime Admission decides executable consequences; Provider/Action/Observation
Admission enforces execution boundaries; Maintenance owners perform repair.
Diagnostics never invokes a Provider, grants Permission, changes Safety policy,
allocates Resource, rewrites protocols/configuration, or mutates world state.

## Current status

Existing assets are distributed across maintenance, model, provider, field,
task, protocol, and watchdog namespaces. They provide useful candidate-only
diagnostics but do not yet form one complete cross-domain contract.

## Known gaps

OWNER_GAP for a single canonical cross-domain contract; CONTRACT_GAP for
freshness, source version, conflict, and diagnostic fact semantics;
ADAPTER_GAP between local diagnostics and Runtime/Provider Admission;
LEGACY_OVERLAP in watchdog/maintenance aggregators; RUNTIME_GAP for a future
live diagnostic service, intentionally deferred.
