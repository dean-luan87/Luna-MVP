# Governance boundary

The phase reuses existing Field Perception Orchestrator and Self State
boundaries. It does not add Plane G governance. All outputs are candidate-only.

Forbidden in this layer:

- provider/model invocation or runtime execution;
- Self-owned observation decisions;
- Field mutation or Field/World Truth declaration;
- Decision, Task, Action, Runtime Executor, device control, or navigation;
- scenario/cycle-driven semantic branching;
- numeric geometry or fabricated motion evidence.

The existing Re-observation path remains the owner of Re-observation. This
phase supplies the missing upstream check:

`Re-observation Request → Necessity → Conditions → Relative State → Feasibility → Window → Eligibility`.

