# System Diagnostics Adjudication Summary v1

## Final decision

**KEEP** System Diagnostics as an independent, narrow maintenance-plane
diagnostic evidence/classification boundary. It observes and classifies state;
it does not decide policy, admission, remediation, semantic consequence, or
execution.

## Canonical flow

```text
Registry / Runtime / Device / Provider / OS / Protocol / Config / Telemetry
        → Probe or passive observation
        → Diagnostic Evidence
        → System Diagnostics
        → Health / Drift / Finding / Snapshot / Conflict
        → Brain, Safety, Permission, Resource, Runtime Admission,
          Provider/Observation/Action Admission, Task, A, Outcome, Maintenance
```

Logical Capability Resolution remains separate from current health. Diagnostics
may say a runtime is unhealthy; Runtime Admission decides whether an executable
candidate exists. A decides cognitive consequence. Maintenance decides repair.

## Sub-boundaries

- Active probe capability: **NARROW / DEFERRED**, bounded and governed.
- Incident aggregation: **KEEP, candidate-only**.
- Root-cause classification: **NARROW, candidate-only**.
- Remediation recommendation: **REASSIGN / DEFERRED** to Maintenance and the
  responsible owner.

## Current status

Documentation-only adjudication complete. Runtime, canonical types, enums,
owners, probes, models, Providers, and verifiers were not changed or run.
