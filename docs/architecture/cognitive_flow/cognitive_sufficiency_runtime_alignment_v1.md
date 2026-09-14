# Cognitive Sufficiency Runtime Alignment v1

Sufficiency is evaluated against a current Cognitive Snapshot/Workspace Candidate and produces candidate feedback for a later tick. It is not a Runtime controller or scheduler.

```text
Current Understanding Candidate -> Sufficiency Evaluation Candidate
  -> next-cognition request candidate -> future Cognitive Tick Candidate
```

The supported outputs are `sufficient`, `insufficient`, `uncertain`, `require_information`, `require_reasoning`, and `defer` candidates. They do not execute observation, retrieval, routing, or a state transition.
