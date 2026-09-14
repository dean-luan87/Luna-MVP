# Cognitive Snapshot Transition Model v1

`Cognitive Snapshot` is a temporary cognitive observation window containing Context, active Schema, Workspace, Goal, Attention, Unknowns, Hypothesis, and Simulation references. It is not Reality State, System State, Memory State, or a persistent runtime state store.

```text
Current Cognitive Snapshot + New Candidate
  -> Transition Candidate
  -> Next Cognitive Snapshot Candidate
  -> New Cognitive Tick Candidate
```

A transition records `previous_snapshot_ref`, `current_snapshot_ref`, reason, confidence candidate, retention references, activation references, and provenance. The next snapshot remains a candidate; it is not a state mutation.
