# A-Route Attention Context Model v1

## Purpose

Attention Context Candidate expresses why a world, self, goal, temporal, or
future social-reference item may deserve bounded cognitive consideration. It
does not judge Reality, prove importance, or direct an Action.

```text
Attention Context Candidate
├── Target Candidate
├── Relevance Candidate
├── Risk Candidate
├── Goal Alignment Candidate
├── Temporal Change Candidate
├── Uncertainty Candidate
├── Resource Cost Candidate
├── Confidence Candidate
└── trace_ref
```

| Field | Meaning | Boundary |
|---|---|---|
| Target Candidate | possible object, relation, self condition, or information gap | not a fact or exclusive world object |
| Relevance Candidate | possible significance for the current subject | not value truth |
| Risk Candidate | bounded possible adverse relevance | not a danger verdict |
| Goal Alignment Candidate | possible relation to Goal Context | does not create or modify Goal |
| Temporal Change Candidate | change relevance from Temporal Understanding | not a future prediction |
| Uncertainty Candidate | why more understanding may be useful | not proof that an unseen object exists |
| Resource Cost Candidate | estimated cognitive/capability burden | not actual allocation |
| Confidence Candidate | support quality for this candidate | not factual confidence |

## Core rules

- `Attention Selection != Reality Judgment`.
- An unselected item does not become absent, irrelevant, false, or safe.
- Attention Context Candidate is candidate-only and cannot directly modify
  Reality, World State, Self Model, Situation, Decision, Action, Provider plan,
  Attention Runtime, or Reducer State.

