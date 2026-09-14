# Existing FPO / Gateway compatibility

## `ObservationRequestCandidateV1`

This is an existing FPO active-observation candidate. It carries a
task/provider-facing observation goal, target region, capability kinds,
evidence expectation, budget, and temporal validity. It is a pre-runtime
candidate, not the current cognitive `PerceptionRoutingCandidateV1` and not a
runtime ingress request.

The current routing candidate does not contain enough information to populate
task, provider, model, budget, or runtime-session semantics. It is therefore
not converted directly into `ObservationRequestCandidateV1` in this phase.

## `ObservationIngressRequestV1`

This is the Observation Gateway ingress contract. It requires ingress/provider
and source metadata and can carry a reference-only runtime observation
envelope. The Gateway produces `ObservationGatewayRuntimeAdmissionV1` in its
live-mode path. It is a runtime-facing downstream contract, not a candidate
projection target for this phase.

## Active Observation Control

The existing FPO integration already expresses the controlled observation
decisions `STOP`, `CONTINUE`, `REDIRECT`, `SWITCH_PROVIDER`, `ADD_CAPABILITY`,
`RECONSIDER`, `DEFER`, and `FAIL`. It also explicitly guards that Gateway
admission is not continuation authorization. This phase reuses that owner and
does not reproduce the control engine.

## Compatibility direction

The implemented seam is:

```text
PerceptionRoutingCandidateV1
  → PerceptionRoutingAdmissionCompatibilityCandidateV1
  → [future FPO admission / Gateway request adapter]
```

No FPO runtime call, Gateway submission, Provider binding, Model binding, or
runtime admission decision is created here. A future adapter may add the
downstream fields only after their owning governance boundaries supply them.
