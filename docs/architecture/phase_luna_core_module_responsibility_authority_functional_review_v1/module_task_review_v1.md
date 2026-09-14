# M08 Task / Task Manager — Module Review

## Identity and purpose

Canonical name: Task Manager / Task lifecycle boundary. Evidence: `capabilities/midplatform/core/task_manager/`, especially lifecycle, dependency, result aggregator, module API, and capability router. If removed, Luna loses behavior constraints, completion conditions, dependency/readiness organization, interruption/recovery, and execution-result aggregation.

## Functions and authority

`CORE`: Task lifecycle, dependency/readiness, completion/failure organization, behavior constraints. `SUPPORTING`: capability/requirement routing and result aggregation. `COMPATIBILITY_ONLY`: older Task Manager skeletons. Task may provide a target, behavior constraint, completion condition, dependency, permission/resource constraint. It has no authority to create A Current Need, select Provider/model, judge Scope, control cognitive Loop, alter Concern, or adopt B.

Responsibility is task organization and completion reporting. A owns cognitive interpretation; Capability Governance owns technical resolution; Loop persists supplied mechanics.

## Inputs, outputs, state, lifecycle

Inputs: Goal/Intent linkage, behavior/completion constraints, dependencies, resource/permission refs. Outputs: Task refs, readiness/completion/results, and technical requirement-support refs. Task state is Task-owned lifecycle state, not cognitive semantic state. Lifecycle: create → ready/block → execute organization → interrupt/recover → complete/fail/archive.

## Communication and negative boundaries

Allowed: Task→A as constraint/ref; Task→Capability bridge as requirement support; Task→execution organization; Loop may store Task refs. Forbidden: Task→Need, Task→Provider, Task→Observation direct admission, Task→Loop cognition, Task→Concern mutation. Capability router is a possible technical-routing overlap, not cognitive authority.

## Walkthroughs

1. Normal: Task supplies completion condition; A forms Need independently; Task reports execution completion.
2. Blocked dependency: Task marks readiness blocked; A/Brain decide cognitive response; Loop records only supplied state.
3. Task condition changes: new Task version reaches envelope; A judges semantic impact and may replan; no automatic Need mutation.

## Overlap, gaps, evolution, disposition

Overlap: `TERMINOLOGY_OVERLAP` Task Requirement vs Cognitive Requirement; `IMPLEMENTATION_OVERLAP` capability router vs Capability Governance. Gap: adapter contract separating task technical routing from cognitive Need. It may evolve as execution organization, never a cognition/Capability owner. **Disposition: NARROW**.

**Ledger summary:** authority = task lifecycle/constraints; responsibility = task readiness/completion; state = task lifecycle; receiver = A/Capability/execution; confidence = high.
