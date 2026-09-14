# Failure-State Mapping

No new canonical enum is introduced. The following mapping reuses existing
resolution, model admission, Provider, and Observation vocabulary.

| Conceptual failure | Existing status/error family | Boundary |
|---|---|---|
| Capability not resolved | `UNAVAILABLE_CANDIDATE` | Logical Resolution |
| Model not available | `ADMISSION_BLOCKED_ASSET_MISSING`, `MODEL_NOT_AVAILABLE` | Model/Provider |
| Model not admitted | `ADMISSION_BLOCKED_*`, `PROVIDER_NOT_ADMITTED` | Runtime/Provider Admission |
| Dependency unhealthy/unresolved | `ADMISSION_BLOCKED_DEPENDENCY`, `PYTHON_DEPENDENCY_*` | Diagnostics → Admission |
| Integrity failed | `CHECKSUM_MISMATCH`, `ADMISSION_BLOCKED_CHECKSUM` | Integrity → Admission |
| Resource unavailable | `DEGRADED_CANDIDATE` or existing resource admission rejection | Scope/Admission |
| Permission denied | Existing permission admission rejection | Permission/Capability Admission |
| Provider not ready | `ADMISSION_BLOCKED_PROVIDER`, `PROVIDER_NOT_ADMITTED` | Provider Admission |
| Provider invocation failed | `PROVIDER_INVOCATION_FAILED` | Provider execution |
| Evidence invalid | `EVIDENCE_MAPPING_FAILED` or Observation Gateway rejection state | Evidence Gateway |
| Candidate stale/expired | Existing expiry/revocation/supersession refs and Observation states | Admission/evidence boundary |

Unknowns remain explicit. A missing evidence ref never becomes an implicit
`ADMISSION_READY_CANDIDATE`.

