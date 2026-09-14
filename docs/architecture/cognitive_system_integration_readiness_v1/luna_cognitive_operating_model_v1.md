# Luna Cognitive Operating Model v1

## Purpose and boundary

This is a planning-only integration blueprint. It describes how the already
governed cognitive modules can form a continuous life flow. It does not
implement Runtime, Scheduler, Model, Hardware, or Action execution.

The Cognitive Constitution remains the highest constraint. Brain owns Goal,
Intent, and final Judgment. Runtime owns cycle progression, wake-up, state
synchronization, and resource boundaries; Runtime is not a cognitive subject.

## Global Cognitive Loop

```text
External World
    ↓
Reality Update
    ↓
Field Update
    ↓
Attention Allocation
    ↓
Situation Update
    ↓
Goal / Task Check
    ↓
Decision Candidate
    ↓
Action Boundary
    ↓
Outcome
    ↓
Experience
    ↓
Future Adaptation
```

Every transition remains a candidate or governed state update. External
changes enter through Evidence and the Reality Reducer; no Provider, Model,
Field, Runtime, or Action path may directly mutate Reality, Goal, Decision,
Identity, or Authority.

## Module responsibilities

- Reality Workspace maintains facts, provenance, temporal validity, conflict,
  and Unknown. It does not interpret goals or make decisions.
- Cognitive Field organizes relevant Reality, Self, Goal, Rule, Social, and
  Emotion placeholders into a bounded context. It does not plan or act.
- Attention is the global resource bus for Reality Observation, Field Update,
  Task, Brain Escalation, and Capability Usage. It allocates candidates but
  does not own Goal or Decision.
- Situation combines Field, Self Capability, Self State, Goal, constraints,
  risk, and Unknown into a Situation Candidate.
- Goal and Task continuity tracks long-lived intent, progress, pending
  information, and lifecycle without becoming a Brain.
- A Route generates Options, Evaluation Candidates, and Decision Candidates.
- Brain reviews Goal, trade-offs, Authority, Unknown, and Decision Candidate;
  Brain retains final cognitive judgment.
- Action Boundary converts an accepted Decision into an Action Request. It is
  not Action Runtime and cannot execute or write Reality.
- Outcome and Experience use Outcome Evidence and Cause Attribution to create
  future adaptation candidates. Experience cannot directly rewrite Reality,
  Goal, Identity, or Attention policy.
- Capability Governance maps a Need to Capability, then to Model/Hardware
  implementation options, and returns Evidence through the Evidence Gateway.
- Governance intercepts Protocol, Authority, Admission, Resource, Runtime,
  and Diagnostics boundaries before activation candidates.

## Continuous process model

Each Cognitive Process has the lifecycle:

```text
Created → Activated → Running → Background → Suspended → Completed → Archived
```

The lifecycle is a governance model, not a Scheduler implementation. Foreground,
Background, Survival, and Maintenance processes can be represented, but no
automatic execution is introduced in this phase. A process may be resumed only
through a governed candidate carrying Field, Goal, Task, resource, authority,
and provenance references.

## Attention bus integration

The Attention Global Bus receives candidates from Reality Observation, Field
Update, Task progress, Brain Escalation, Self State, and Capability Usage. It
records source, information value, uncertainty, risk, resource cost, context,
and lifecycle. Arbitration may produce an Attention Allocation Candidate,
Observation Requirement, or Brain Escalation Candidate. It may not directly
change Goal, Decision, Reality, Identity, or Action.

## Capability execution flow

```text
Need
  ↓
Capability
  ↓
Model / Hardware
  ↓
Evidence
```

Attention and Capability Governance select a Capability Requirement. Model
Manager and Hardware Registry expose implementation options and constraints.
Provider output is Raw Evidence Candidate only. Evidence Gateway validation,
Reality Update Candidate, and Reducer processing are mandatory. Human Input is
also an Evidence source; Models are not the only source.

## Governance interception points

Every lifecycle transition and capability flow is intercepted by:

1. Protocol compatibility and version governance;
2. Authority and permission governance;
3. Registry identity and binding governance;
4. Admission and boundary governance;
5. Resource and Attention budget governance;
6. Runtime lifecycle and state synchronization governance;
7. Diagnostics, failure classification, and change governance.

Diagnostics emits a Diagnostic Candidate, not an Action. A failure may create a
Fallback Candidate, Capability Degradation Candidate, or Brain Escalation
Candidate, while preserving Unknown and provenance.

## Long-running blueprint

The planning scenarios cover 24 hours, 7 days, and 30 days. Stable Identity,
Constitution, and core Capability remain continuous. Field, Attention, Task,
Self State, and Experience Candidates may change. Reality is never replaced by
Experience; Unknown does not disappear merely because time passed.

## Explicit non-goals

No real Model, Camera, OCR, SLAM, Hardware Runtime, Action Runtime, Emotion
Runtime, Social Runtime, or B Runtime is included. No Scheduler implementation,
automatic execution, automatic model switching, automatic learning, Role
Runtime, or network/device side effect is included.

Exact exclusions: Model Manager remains an implementation governance layer. No
Camera, No OCR, No SLAM, No Hardware Runtime, No Action Runtime, No Emotion
Runtime, No Social Runtime, No B Runtime, No automatic execution, No automatic
model switching, and No automatic learning are included.

No Camera. No Emotion Runtime. No automatic model switching.
