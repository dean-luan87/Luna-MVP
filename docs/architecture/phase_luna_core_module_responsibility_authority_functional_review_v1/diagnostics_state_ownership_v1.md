# Diagnostics State Ownership v1

| State | Classification | Owner/meaning |
|---|---|---|
| Probe definition | AUTHORITATIVE | Diagnostics contract for source/scope; source mechanism may be external. |
| Probe execution result/raw telemetry | EXTERNAL / REFERENCE_ONLY | Producing runtime/device/OS/provider source. |
| Diagnostic evidence | AUTHORITATIVE within source contract | Diagnostics lineage and validity. |
| Health status/finding | AUTHORITATIVE_DIAGNOSTIC_FACT | Diagnostics classification, bounded and versioned. |
| Snapshot/trend | LOCAL_DERIVED | Diagnostics aggregation with source refs. |
| Incident candidate | CANDIDATE | Diagnostic correlation only. |
| Drift finding | AUTHORITATIVE_DIAGNOSTIC_FACT | Comparison result; source owner retains reference truth. |
| Root-cause candidate | CANDIDATE | Evidence-linked hypothesis, not Truth. |
| Remediation candidate | CANDIDATE | Handoff only; Maintenance owns execution. |
| Source version/trace | REFERENCE_ONLY | Originating owner plus Diagnostics lineage. |

No item in this table is an Executable Capability Candidate, Permission Grant,
Safety Policy, Resource allocation, Action, or World Truth.
