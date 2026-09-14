# Execution result to Field chain

The previous phase ends at `PerceptionEvidenceV1`. This phase begins there and
uses the existing contracts:

```text
ProviderInvocationResult
  → RuntimeObservationEnvelope
  → Observation Gateway admission
  → PerceptionEvidenceV1
  → FieldEventCandidateV1
  → Field Event Admission
  → admitted reducer input
  → Field State Reducer candidate
  → FieldStateV1 / CurrentWorldCandidateV1 read representations
```

`FieldEventCandidateV1` is formed only when the caller supplies a field and
context reference and the Evidence shape is complete. The adapter copies the
opaque payload reference; it never maps provider/capability names to a world
meaning.

An admitted event is reducer-eligible, not a fact. A reducer candidate is not
a persisted state. A Current World candidate is a cognition-cycle
representation, not an additional state store.
