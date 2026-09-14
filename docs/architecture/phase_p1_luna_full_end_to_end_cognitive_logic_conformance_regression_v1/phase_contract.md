# Phase contract

This is a controlled, candidate-only regression. It reuses the canonical
Observation Gateway, A-Route, Cognitive State Formation, Decision, Task, and
Action Governance paths. It does not add an owner or alter runtime semantics.

The result has independent fields:

```text
operational_result: PASS | FAIL
cognitive_logic_result: PASS | FAIL
final_decision: GO only when both are PASS, otherwise NOT_GO
```

No `NOT_INDEPENDENTLY_EXERCISED` value is used for this phase. If a required
philosophical relationship cannot be observed, the result is `FAIL` with a
`COGNITIVE_LOGIC_CAPABILITY_GAP`.

