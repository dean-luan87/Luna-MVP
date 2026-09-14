# Reality State Runtime Concept v1

## State representation

Reality State contains only structured current-world descriptors:

- Entity;
- Event;
- Relation;
- State;
- Location;
- Change;
- validity, timestamp, provenance, confidence, and Unknown.

Example: a river region, water present, depth candidate 60 cm, flow Unknown,
weather rain-after candidate. The state does not infer that a small horse can
cross or that a route should be selected.

## Continuous update concept

```text
Evidence Candidate
      ↓
Reality Candidate
      ↓
Reality Reducer
      ↓
Current Reality State
```

The concept supports persistent state and incremental change. It does not create
a Prediction Layer, Outcome Prediction, Decision Loop, Planning, Reasoning, or
Action. This is not a Prediction Layer.

## Boundary

Reality State is not Situation. It is not a Goal, Decision, Evaluation, or
Experience. A Route consumes it and forms a Situation Candidate; Brain retains
final judgment.
