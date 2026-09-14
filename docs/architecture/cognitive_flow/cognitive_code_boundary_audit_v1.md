# Cognitive Code Boundary Audit v1

## V0 findings

Static inspection found no code path matching:

- infinite `while True` agent loop;
- direct `.execute()` or `.update_state()` module call;
- memory-write API;
- `self.state` persistent mutation pattern;
- real model, network, OCR, camera, or device-library integration;
- direct imports between planned runtime subsystems.

## Confirmed protections

- `Candidate` is frozen and recursively freezes mapping/list/set payload values.
- `CognitiveSignal` is frozen and carries only context-bound signal metadata.
- `CognitiveSnapshot.with_candidate()` returns a replacement view rather than mutating a snapshot.
- `CandidateOnlyEmitter` rejects `state_mutation_requested=True` and names Reducer as the sole State Mutation Authority.
- controlled execution and state transition modules declare synthetic-only boundaries.

## Boundary risks recorded

1. `Candidate.candidate_type` and `Candidate.payload` are intentionally generic; the contract does not yet mechanically reject authority-shaped candidate types or payload keys.
2. `CognitiveSignal.payload` is also generic and does not yet enforce an evidence/context/goal/attention/feedback/interrupt envelope.
3. Current static protections are appropriate for a skeleton baseline but need dedicated admission validation before broader subsystem implementation.

These are refactoring candidates, not authorization to change current contracts in this review phase.

