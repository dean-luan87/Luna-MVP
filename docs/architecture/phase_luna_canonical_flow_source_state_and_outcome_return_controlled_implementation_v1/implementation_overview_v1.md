# Implementation Overview v1

## Location

`capabilities/midplatform/core/cognitive_flow/integration/canonical_source_state_outcome_return_controlled/`

## Reuse-first decisions

The package reuses the existing `CurrentWorldCandidateV1`, Observation Gateway evidence/provenance conventions, outcome candidate refs, runtime result references, and cognitive-flow trace vocabulary. Local dataclasses are integration candidates, not replacement canonical owner types.

## Components

- `types_v1.py`: local candidate, guard, failure, and observability records;
- `adapters_v1.py`: source-state and Outcome→Brain candidate adapters;
- `fixtures_v1.py`: 30 synthetic scenarios;
- `runner_v1.py`: controlled synthetic execution only;
- `verifier_v1.py`: report verifier, not executed in this phase.

## Status

Implemented as a narrow candidate-only seam. No runtime or source owner was invoked.

