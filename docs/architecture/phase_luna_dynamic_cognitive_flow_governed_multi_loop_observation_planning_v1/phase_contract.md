# Phase-Luna-Cognitive-Loop-Architecture-Alignment-And-Implementation-Contract-v1-001

Status: architecture baseline aligned; candidate-only controlled implementation
present, user-terminal verification pending.

This phase aligns the existing multi-loop planning with the clarified Brain /
Cognitive Loop architecture. It defines when a local cognitive concern may be
materialized as a Loop, how the Loop remains subordinate to Brain governance,
how continuity is assessed on resume, and how a `REQUEST_MORE_EVIDENCE`
disposition becomes a next observation candidate. It does not execute a
provider, start a camera, schedule work, mutate a Task, change an Intent, or
create a second YOLO invocation.

## Architectural baseline

Brain is the cognitive subject. A Cognitive Loop is a subordinate persistent
process for one local cognitive concern; it is not a second Brain or a second
cognitive governance layer.

Not every cognitive operation becomes a Loop. Brain / Cognitive Flow may keep
an immediate concern local when it has no persistent state, cross-time
continuity, waiting, pause/resume, re-observation, reconsideration, hypothesis
maintenance, or capability-use requirement.

When Brain materializes a concern as a Loop, Brain retains global governance
and must not independently solve the same local concern in parallel. The Loop
owns only its local cognitive process state and references to authoritative
owners.

## Contract objective

The phase adds a generic loop identity and lifecycle envelope around the
existing Cognitive Flow owner. It preserves the existing path:

`Cognitive State`
`-> Current Minimum Need`
`-> Capability Requirement`
`-> Scope / Resolution / Permission / Resource admission`
`-> Observation Candidate`
`-> Evidence / Outcome`
`-> new Cognitive State version`
`-> Sufficiency / Reconsideration`

The final arrow produces a candidate only. A later runtime phase may decide
whether any provider invocation is authorized.

Loop completion produces a Cognitive Outcome Candidate. Brain performs outcome
assimilation. Completion does not directly create World Truth, Decision,
Action, Memory, Experience, or Intent mutation.

## Canonical ownership decision

The generic Cognitive Loop identity, lifecycle envelope, state transition
candidate, and loop-local provenance index belong to **Cognitive Flow
Governance**. This is an extension of the existing Cognitive Flow owner, not a
new Loop Manager, Loop Brain, Loop Planner, or second governance layer.

The loop is not a Task, Intent, Plan, execution queue, Observation owner,
resource allocator, Safety authority, Self, Role, Emotion, Memory, Experience,
Action, World Truth authority, or Provider identity owner.

Authoritative data remains in its canonical owner. Loop-local state is limited
to current disposition, local Need selection, hypothesis/expectation lineage,
pending candidates, state-version lineage, pause/wait reason, and local trace
references. All other inputs are read-only references.

## Lifecycle contract

The contract vocabulary is:

`ACTIVE`, `PAUSED`, `WAITING`, `DEFERRED`, `STOPPED`, `COMPLETED`.

Existing vocabulary is reused where it is exact:

- `PAUSED` reuses `SuspendCandidateV1` and the existing Cognitive Flow cycle
  state `SUSPENDED`.
- `COMPLETED` reuses `CYCLE_STATES.COMPLETED` and is emitted only when the
  loop's own goal reaches a terminal completion disposition, including
  `STOP_SUFFICIENT`.
- `DEFERRED` reuses Dynamic Cognitive Flow's `DEFER` next-step disposition and
  the existing `DEFERRED_ASYNC_REFERENCE` relationship.
- `WAITING` is a lifecycle interpretation of a governed hold with no current
  executable next step. It may reference Task readiness `HOLD` or
  `REQUIRES_OBSERVATION`, but it does not change Task state.
- `STOPPED` is an intentional terminal stop candidate distinct from failure;
  it is not an automatic alias for Task cancellation or failure.
- `ACTIVE` is the loop-level label for a currently admitted cognitive
  transition candidate; it does not authorize execution.

No new enum, scheduler state machine, or runtime lifecycle implementation is
created in this phase.

## Required negative guards

- `Cognitive Loop != Task`
- `Cognitive Loop != Intent`
- `Cognitive Loop != Plan`
- `Cognitive Loop != execution queue`
- loop lifecycle transitions do not invoke providers
- loop pause does not release or delete capability history
- loop resume does not reuse a stale Requirement
- a loop cannot bypass Scope, Truth, Action, Safety, Permission, or Resource
  governance
- a loop cannot mutate Context, Field, Current World, Attention, Hypothesis,
  Intent, Task, Memory, Learning, or SRSK state
- an unmaterialized candidate is not a capability failure
- one loop's failure, pause, wait, or stop does not terminate another loop
- Brain remains the sole authority for Loop materialization, priority, and
  outcome assimilation
- materializing a Loop prevents Brain from independently solving that same
  local concern in parallel
- Loop completion is a Cognitive Outcome Candidate, not automatic Experience
  or Memory mutation

## Deferred implementation

The current controlled implementation adds only candidate-only types, fixtures,
Runner, and Verifier under the existing Cognitive Flow integration tree. Real
multi-provider execution, autonomous scheduling, optimal resource allocation,
utility scoring, capability acquisition, Learning, Memory/Experience mutation,
semantic folding/expansion, and Action execution remain deferred.

## Lifecycle closure extension

The lifecycle closure bridge keeps a Loop-local state `OPEN` through closure
assessment. Only a Brain/Cognitive Flow governed closure decision can create
an accepted lifecycle closure, freeze final-state references, dispose
outstanding Requirements/Observation Candidates, and emit the existing
Loop Closure Record plus Cognitive Outcome Candidate. The Brain assimilation
candidate and Loop Package are bounded reference handoffs; they do not create
Truth, Decision, Action, Task, Intent, Memory, Experience, Learning, or a child
Loop.

The focused closure fixture contains 28 `LC-*` scenarios. Its phase-specific
Runner and Verifier are documented for user-terminal execution only.
