# Observation / Provider Failure Semantics v1

| Failure | Owner |
|---|---|
| OBSERVATION_REQUEST_INVALID / OBSERVATION_BLOCKED | Observation/FPO and supplied Brain policy |
| CAPABILITY_UNAVAILABLE | Capability/Runtime Admission |
| PROVIDER_NOT_ADMITTED / PROVIDER_UNAVAILABLE | Provider Governance |
| PROVIDER_INVOCATION_FAILED / TIMEOUT / CANCELLED | Provider/Runtime Executor |
| RESULT_MALFORMED / EVIDENCE_MAPPING_FAILED | evidence adapter/FPO/Gateway |
| EVIDENCE_REJECTED / STALE / DUPLICATE | Gateway/Evidence admission |
| SOURCE_VERSION_MISMATCH | source/version admission boundary |

Failures return candidate/status refs. No semantic recovery or fabricated
Evidence is produced.
