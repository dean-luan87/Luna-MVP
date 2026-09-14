# Cognitive Constraint Model Definition v1

## Candidate schema

`CognitiveConstraintCandidateV1` is a traceable, non-authoritative future candidate with:

| Field | Meaning |
| --- | --- |
| `context_reference` | Current Cognitive Context reference |
| `survival_pressure_reference` | Candidate survival pressure reference |
| `goal_reference` | Goal/task reference |
| `risk_candidate_reference` | Risk candidate; not a Fact |
| `information_gap_reference` | Explicit unresolved information |
| `information_value_reference` | Candidate value of reducing the gap |
| `exploration_cost` | Candidate cost of continued exploration |
| `reasoning_cost` | Candidate cost of continued cognition |
| `time_constraint` | Available time/window reference |
| `resource_constraint` | Candidate energy, compute, and attention limitation |
| `experience_reference` | Historical pattern candidate reference |
| `constraint_type` | Exploration, information, reasoning, action, or resource constraint |
| `constraint_reason` | Traceable explanation of the candidate limit |
| `provenance` / `trace_ref` | Source lineage and trace closure |

It is candidate-only, non-Fact, non-State, non-Decision, non-Action, non-Permission, and non-Memory. It must not contain an action command, a permission grant, a State-write target, a Fact id, or a Decision id.

## Constraint meanings

- **Exploration Constraint**: retain, narrow, defer, or abandon exploration consideration.
- **Information Constraint**: accept unknown when acquisition cost exceeds relevant value.
- **Reasoning Constraint**: preserve, suspend, or reduce a reasoning branch candidate.
- **Action Constraint**: express behavior-space limits, never control action.
- **Resource Constraint**: represent time, energy, compute, or attention limits.
