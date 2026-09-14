# Cognitive Runtime Life Process Architecture v1

## Position

Cognitive Runtime is the lifecycle plane that keeps the frozen Cognitive Core
continuously alive. It manages time, wake-up, process states, workspace
refresh, resource allocation, maintenance, and escalation. It is not Brain and
does not own Goal, Reasoning, Decision, or Action. Workspace refresh is a governed runtime responsibility.

```text
External Change → Tick → Wake-up Evaluation → Process Scheduling
      → Field / Workspace / Attention Refresh
      → Brain Invocation Boundary when required
      → State Synchronization → Next Tick
```

## Runtime components

- Lifecycle Manager: owns process lifecycle candidates.
- Tick Manager: defines logical Cognitive Tick and cadence classes.
- Wake-up Manager: evaluates Reality Change, Field Change, Attention Trigger, Reflex Signal, and Task Deadline.
- Process Scheduler: coordinates Survival, Foreground, Background, and Maintenance processes.
- Workspace Manager: refreshes Primary and Background Workspaces without becoming Brain.
- Attention Scheduler: requests resource allocation from Attention Governance.
- Memory Maintenance: proposes retrieval/consolidation candidates; it does not rewrite Memory.
- Learning Scheduler: schedules candidate evaluation; it does not execute automatic learning.
- Reflex Monitor: listens for safety signals and emits Reflex Candidates.
- Brain Invocation Boundary: escalates complex, conflicting, or uncertain states.

## Tick and cadence

Cognitive Tick is a logical state-advance unit, not a wall-clock promise. High Frequency, Normal Cadence, and Low Frequency are explicit cadence classes. Safety
and Reflex monitors may use high-frequency candidates; Attention and Field
refresh may use normal cadence; Memory Maintenance and Learning evaluation may
use low-frequency cadence. Cadence is a governance candidate, not a runtime
implementation.

## Wake-up and process lifecycle

Wake-up sources are Reality Change, Field Change, Attention Trigger, Reflex
Signal, and Task Deadline. Processes move through
`Created → Activated → Running → Background → Suspended → Completed → Archived`.
The Scheduler does not choose Goals or resolve value conflicts.

## Resource and state governance

Runtime receives resource constraints for compute, energy, memory, time, and
sensor availability. It emits Allocation Candidates and Degradation
Candidates; Attention and Governance own resource policy. State Synchronization
preserves Field, Self, Workspace, Task, Attention, Memory, Learning, Reflex,
and Emotion Context boundaries.

## Brain invocation boundary

Routine, low-risk maintenance may remain on process paths. Unknown, conflict,
high-risk, or high-cost situations produce Brain Invocation Candidate. Runtime
provides a governed state package; Brain retains Goal, Value, Reasoning, and
final Decision authority. Runtime never says what Luna should choose.

## Failure escalation

Failure flows through `Failure → Diagnostics → Fallback Candidate → Escalation`.
Capability failure, stale state, resource denial, malformed context, and
process starvation are diagnostic candidates, not automatic Actions.

## Explicit non-goals

This phase does not implement a real Scheduler, No real Scheduler, Runtime loop, automatic Learning execution, model call,
Hardware Runtime, Action Runtime, B Simulation, or automatic Learning
execution. It defines the lifecycle blueprint only.
