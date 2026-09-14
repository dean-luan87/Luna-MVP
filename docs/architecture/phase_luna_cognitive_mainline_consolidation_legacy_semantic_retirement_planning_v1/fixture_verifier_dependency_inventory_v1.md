# Fixture / Verifier dependency inventory

| Legacy behavior | Current dependency | Replacement dependency | Retirement condition |
|---|---|---|---|
| Dynamic Flow Need/sufficiency/next-step fields | Dynamic Flow fixture A–F, Dynamic Flow Runner/Verifier | A semantic bridge + mechanical command adapter | all callers assert A ownership and only consume Flow as compatibility computation |
| Dynamic Flow stale/invocation filtering | capability and real single-invocation trial fixtures | A Requirement reassessment + Scope/Resolution/Admission | stale Requirement tests migrated |
| Loop local disposition/resume semantics | 42 multi-loop scenarios and lifecycle-closure scenarios | A/Brain semantic refs + Loop mechanical validation | no Loop inference assertions remain |
| Loop closure reason construction | lifecycle closure fixture/Verifier | Brain-governed closure decision supplied to Loop | closure scenarios consume supplied reason |
| Product Loop cognitive states | A Route Product Loop Runner/Verifier and historical planning docs | A Route handoff around Working Envelope/A | Product Loop cognitive path no longer caller |
| Product Loop reobserve/reconsider routes | outcome/observation integration fixtures | A reassessment / Observation admission | semantic recommendations are no longer interpreted by Product Loop |

No deletion is safe at current stage. Verified tests are evidence of compatibility obligations, not proof of target ownership.

