# Integration Contract

The adapter accepts a Task result only when Task Manager reports admission and
the controlled Task state is `admitted`, `planned`, or `ready`. It carries the
selected Decision, Decision trace, final cognition, Sufficiency, Stop, Task
state, and Task trace as references.

The existing `ActionGovernanceInputV1` is then used unchanged. Action
Governance produces the Action Candidate, trace, readiness, state transition,
and candidate-only Runtime Executor handoff. The integration calls no runtime
executor.

Action-boundary admission means the existing Action candidate/readiness and
static boundary validators succeed. It does not mean Action execution.
