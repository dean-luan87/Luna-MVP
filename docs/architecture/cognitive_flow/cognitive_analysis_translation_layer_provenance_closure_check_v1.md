# A3 Evidence Context Translation Layer Provenance Closure Check v1

## Required Chain

```text
Cognitive Primitive Candidate
        ↓ candidate_id / candidate_status / trace_ref
Translation Candidate Envelope
        ↓ request_ref / negative guards
Translation Request Envelope
        ↓ evidence_refs / context_refs / provenance_refs / source_capability_refs
External Capability Source
```

## Closure Assertions

- `candidate.source_refs` equals the request Evidence references.
- `candidate.context_refs` equals the request Context references.
- `candidate.provenance.source_refs` retains provenance references.
- `candidate.provenance.source_capability_refs` retains source/provider identity as provenance only.
- `candidate.provenance.trace_ref` and `candidate.trace_ref` retain the request trace.
- a candidate ID cannot equal a source-capability reference.

## Failure Conditions

Any missing or replaced source/trace reference, hidden provider identity, context substitution, or conversion of provider identity into an Entity breaks provenance closure and is a blocker. Provenance closure does not resolve Evidence truth or identity.
