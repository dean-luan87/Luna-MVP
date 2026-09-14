# Ownership and Order

| Concern | Existing owner | Finding |
|---|---|---|
| Active-observation semantic control | FPO / Active Observation Control | Owns STOP, CONTINUE, REDIRECT, SWITCH_PROVIDER, ADD_CAPABILITY, RECONSIDER, DEFER and FAIL. |
| Runtime ingress and admission proof | Observation Gateway Governance | Owns `ObservationGatewayRuntimeAdmissionV1`. |
| Capability inventory and slot lifecycle | Capability Registry / Universal Capability Slot | Owns availability, reservation and activation. |
| Provider / Model binding | Provider Governance / Model Manager | Downstream of the current compatibility candidate. |

There is no standalone Routing Admission Governance owner.

The Gateway proof requires a supplied `RuntimeObservationEnvelopeV1` in
`LIVE_RUNTIME`, including provider/capability identity, execution instance,
observation result and provenance. `source_model_ref` is optional in that
envelope, but no model binding may be fabricated by this phase.

The resulting order is:

```text
Perception Routing Candidate
→ FPO Admission Compatibility Candidate
→ Provider/Model Governance and runtime target preparation
→ Observation Gateway Runtime Admission
→ Observation Execution
```

Only the order decision is evaluated here.

