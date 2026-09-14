# Implementation Readiness Matrix v1

| Surface | Readiness | Reason |
|---|---|---|
| Capability↔Model binding | NEEDS_SCHEMA / NEEDS_OWNER_REVIEW | owner selected; binding record must be consolidated |
| Model↔Provider binding | NEEDS_SCHEMA / NEEDS_OWNER_REVIEW | provider-facing lifecycle selected; mapping contract absent |
| Source-state handoff | NEEDS_SCHEMA | common candidate-only handoff and Field/World routing required |
| Outcome→Brain input/output | NEEDS_EXISTING_TYPE_EXTENSION | existing Outcome/Brain refs need explicit separation |
| Version/invalidation refs | NEEDS_EXISTING_TYPE_EXTENSION | distributed lifecycle fields need compatible common profile |
| Edge observability | CONTRACT_READY_FOR_IMPLEMENTATION | semantic record frozen; local adapters still needed |
| Brain→Envelope | NEEDS_ADAPTER_ONLY | existing binding concepts and refs exist |
| Envelope→Outline/Snapshot | NEEDS_ADAPTER_ONLY | existing sibling products; handoff alignment incomplete |
| A→Attention/Capability | NEEDS_ADAPTER_ONLY | canonical requirements exist; runtime handoff absent |
| Capability→Runtime | NEEDS_ADAPTER_ONLY | existing candidate chain; no runtime |
| Observation→Provider | CONTRACT_READY_FOR_IMPLEMENTATION | existing request/admission family |
| Provider Result→Evidence | NEEDS_ADAPTER_ONLY | existing Gateway/evidence family |
| Decision→Task→Action | NEEDS_ADAPTER_ONLY | existing canonical boundaries; migration remains |
| Action Result→Outcome | NEEDS_EXISTING_TYPE_EXTENSION | result/evaluation refs need closure |
| Outcome→Brain | NEEDS_SCHEMA | explicit adjudication input/output contract required |
| Memory/Experience | DEFERRED | minimal candidate-only boundary by design |

## Readiness meaning

Readiness here means contract work can proceed. It does not mean runtime execution is available or safe.

