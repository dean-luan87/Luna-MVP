# Reality Outcome Trace Contract v1

## Trace purpose

Outcome Trace captures what a future controlled scenario represents as having
occurred after an execution boundary. It prevents “success/failure only”
records from hiding cost, change, uncertainty, or user constraints.

```text
Outcome Reference
├── Goal Result
├── Risk Change
├── Resource Cost
├── Environment Change
├── User Feedback
├── Unexpected Event
└── Unknown / Missing Observation
```

Each field retains provenance, temporal scope, confidence/uncertainty, and
trace linkage to Decision/Expected Outcome references. Outcome Trace is not
Evaluation, Value Feedback, truth, or a direct update command.
