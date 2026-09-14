# Luna Governance Asset Migration Matrix v1

This matrix is an architecture-placement plan, not a file migration or behavior change.

| current distributed asset | current A3 role | L0/L1 home | future governance handling | current action |
| --- | --- | --- | --- | --- |
| Candidate-only / Fact boundary | protects Translation and Result outputs | L0 Constitution + L1 Input/Output Candidate Governance | contract and admission eligibility rule | reference only |
| Negative Guard 1–5 | prevents Fact, Decision/Action, provenance loss, provider-entity conversion, mutation | L0 principles + L1 Boundary Contract | stable Guard inventory and regression evidence | retain in A3; do not duplicate runtime logic |
| Forbidden-operation flags | makes no-write/no-call claims observable | L1 Protocol Governance + Diagnostics | serialized boundary evidence and drift signal | retain existing flags |
| Runtime flags / `runtime_authorized=false` | blocks Runtime activation and side effects | L1 Permission/Admission + Runtime Boundary + Diagnostics | permission reference and diagnostic state | retain false; no activation |
| Evidence, Context, provenance, source, trace references | traceable candidate input | L1 Protocol Traceability | reference completeness and symmetry validation | retain reference-only mapping |
| Result Contract | candidate output structure | L1 Output Candidate Governance | downstream eligibility contract | retain; no Fact promotion |
| Consumer Governance | read-only consumer restrictions | L1 Permission/Admission + Traceability | governed consumer handoff eligibility | retain; no access grant |
| Learning Candidate Governance | review-bound learning handoff | L1 Permission/Admission + Lifecycle | review/admission candidate only | retain; no Memory/Training write |
| Protocol Admission Mapping | maps A3 to existing L1 route | L1 Protocol Governance + Registry | Registry/Manifest/Protocol Manager reference mapping | retain; no Registry write |
| Validation Closure evidence | fixed-case boundary proof | L1 Diagnostics | audit and regression evidence | retain as baseline evidence |
| Capability identity / owner / lifecycle | future A3 Runtime registration candidate | L1 Capability Registry | existing Registry-owned record and lifecycle | not applied |

## Migration Constraints

No current asset is moved, deleted, or rewritten by this plan. Any future consolidation must preserve contract identifiers, candidate-only semantics, traceability, independent verification, and Reducer mutation authority. Governance consolidation cannot be used to authorize Runtime or real Evidence Binding.

