# Decision / Action Runtime Gap v1

The repository contains controlled Decision and Action Governance engines,
immutable candidate types, static registries, ownership guards, lifecycle
candidate states and candidate-only handoffs. Decision outputs explicitly avoid
Action trigger and Task creation. Action outputs explicitly avoid runtime
execution, scheduler execution and device control. Outcome Evaluation returns
candidate-only comparison/evaluation and learning/observation handoffs.

Gaps are `RUNTIME_GAP` (authoritative commitment and real side-effect runtime),
`CONTRACT_GAP` (candidate versus committed Decision vocabulary),
`ADAPTER_GAP` (Decision→Task/direct Action, Action→Capability/Runtime/Provider,
and Result→Field/Outcome seams), and `LEGACY_OVERLAP` (navigation, speech,
A Route and Task routers). This is not permission to change runtime.
