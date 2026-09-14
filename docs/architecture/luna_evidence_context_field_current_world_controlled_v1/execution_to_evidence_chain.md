# Execution-to-evidence boundary used by this phase

This phase starts after the previous controlled chain has produced an admitted
`PerceptionEvidenceV1`. The upstream chain remains:

```text
Execution Instance → Provider Session → Invocation Result
  → RuntimeObservationEnvelopeV1
  → ObservationGatewayRuntimeAdmissionV1
  → PerceptionEvidenceV1
```

The current phase does not call the Provider, Runtime, or Gateway again. It
consumes the existing Evidence contract and begins the separate Field path:

```text
PerceptionEvidenceV1 → FieldEventCandidateV1
  → Field Event Admission → Field State Reducer candidate
```

This preserves the boundary that Gateway admission is ingress qualification,
not Truth admission, and that Evidence is a basis for a Field Event candidate,
not an admitted event or Field State by itself.
