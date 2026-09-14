# Recommended Route

## Decision gate

**Selected: ROUTE D.**

Current Capability Resolution conflates logical readiness with the ability to
produce an executable handoff candidate. The code and contracts already have
most of the required owners; the missing architectural seam is the explicit
split between logical resolution and Runtime Admission.

This does **not** imply a new Runtime Admission Manager. The target is a
composed responsibility:

```text
Capability Admission Governance
  coordinates
    Capability Registry / Scope / Resolution
    Model Manager / Model Governance
    System Diagnostics / Runtime Health evidence
    Provider Governance / Provider admission
    Observation Gateway / FPO execution boundary
```

## Existing failure/result vocabulary

Use existing namespaces where possible:

- logical resolution: `READY_CANDIDATE`, `UNAVAILABLE_CANDIDATE`,
  `DEGRADED_CANDIDATE`;
- model technical admission: `ADMISSION_READY_CANDIDATE`,
  `ADMISSION_BLOCKED_ASSET_MISSING`, `ADMISSION_BLOCKED_CHECKSUM`,
  `ADMISSION_BLOCKED_DEPENDENCY`, `ADMISSION_BLOCKED_CONTRACT`;
- Provider result: `PROVIDER_NOT_ADMITTED`, `MODEL_NOT_AVAILABLE`,
  `PROVIDER_INVOCATION_FAILED`, `EVIDENCE_MAPPING_FAILED`;
- observation/gateway: existing admission states such as `REJECTED`,
  `REVOKED`, `EXPIRED`, `SUPERSEDED`.

Conceptual mappings for review, without adding enums:

| Requested meaning | Existing nearest status |
|---|---|
| CAPABILITY_NOT_RESOLVED | `UNAVAILABLE_CANDIDATE` |
| MODEL_NOT_AVAILABLE | `MODEL_NOT_AVAILABLE` or asset-missing admission status |
| MODEL_NOT_ADMITTED | `ADMISSION_BLOCKED_*` / `PROVIDER_NOT_ADMITTED` |
| DEPENDENCY_UNHEALTHY | `ADMISSION_BLOCKED_DEPENDENCY` |
| ASSET_INTEGRITY_FAILED | `ADMISSION_BLOCKED_CHECKSUM` / `CHECKSUM_MISMATCH` |
| RESOURCE_NOT_AVAILABLE | `DEGRADED_CANDIDATE` or existing resource rejection |
| PERMISSION_DENIED | existing permission/resource rejection candidate |
| PROVIDER_NOT_READY | `PROVIDER_NOT_ADMITTED` |
| PROVIDER_INVOCATION_FAILED | existing Provider error code |
| EVIDENCE_INVALID | `EVIDENCE_MAPPING_FAILED` or Observation Gateway rejection |

## Recommended next phase

Contract-only first: define the logical-resolution output versus executable
admission input/output using existing refs and statuses. Then build a narrow
candidate adapter that consumes Model/Diagnostics/Integrity/Provider evidence,
without creating a new owner or changing Provider behavior. Only after that
should the real-approved checkpoint be considered for canonical admission
consumption.

