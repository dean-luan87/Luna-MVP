# Ownership audit

| Boundary | Owner | Responsibility in this phase | Not owned here |
|---|---|---|---|
| Runtime execution grant | Permission / Admission Manager | permission and pre-execution authorization decision | allocation or execution |
| Provider eligibility / binding domain | Provider Governance | provider candidate eligibility and future binding | runtime grant |
| Runtime allocation and execution identity | Runtime Executor | allocation realization, instance lifecycle, start/stop/failure | deciding semantic need or grant |
| Resource feasibility / allocation policy | Resource Governance / Runtime boundary | satisfiability and later allocation | cognitive reinterpretation |
| Safety / constitutional veto | Safety Governance / Protocol Manager | block a prohibited execution path | provider selection |
| Active observation semantics | FPO | continue, stop, redirect, evidence sufficiency | provider binding and resource allocation |
| Runtime observation ingress | Observation Gateway Governance | admit an already formed runtime observation envelope | pre-execution grant |

The existing Permission / Admission Manager already classifies
`runtime_access_admission` and evaluates evidence, provenance, authority,
risk, conflict, revocation, and expiry. Its existing decision builder remains
a candidate-only assessment. The new typed grant decision is a narrow
extension under that same owner; it does not create a second permission or
admission system.

The Gateway's `ObservationGatewayRuntimeAdmissionV1` consumes a concrete
runtime observation identity and result/evidence references. It is therefore
ingress proof after runtime observation formation, not this phase's
pre-execution authorization.
