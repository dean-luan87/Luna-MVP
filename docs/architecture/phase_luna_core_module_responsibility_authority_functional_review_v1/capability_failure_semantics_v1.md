# Capability Failure Semantics v1

Existing/local vocabulary maps as follows:

| Failure | Owner |
|---|---|
| `UNAVAILABLE_CANDIDATE` | Capability logical resolution |
| `DEGRADED_CANDIDATE` | Capability/Runtime Admission governance |
| `ADMISSION_BLOCKED_ASSET_MISSING` / `MODEL_NOT_AVAILABLE` | Model Manager/Runtime Admission |
| `ADMISSION_BLOCKED_CHECKSUM` | Integrity/Model Manager evidence consumed by Runtime Admission |
| `ADMISSION_BLOCKED_DEPENDENCY` | Diagnostics evidence consumed by Runtime Admission |
| `ADMISSION_BLOCKED_CONTRACT` | Capability/Provider contract boundary |
| `PROVIDER_NOT_ADMITTED` | Provider Governance |
| `PROVIDER_INVOCATION_FAILED` | Provider Governance |
| `EVIDENCE_MAPPING_FAILED` | Observation/Gateway/evidence mapping |

No new canonical enum is proposed. Logical scope failures must not be reported
as runtime readiness failures, and Provider failures must not be reported as
Capability identity failures.
