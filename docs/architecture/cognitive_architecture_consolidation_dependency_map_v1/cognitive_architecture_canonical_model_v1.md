# Cognitive Architecture Consolidation and Dependency Map v1

## Phase boundary

This phase consolidates the already-defined Luna Cognitive Architecture into
one canonical model. It adds no cognitive capability and does not implement a
runtime. The canonical model is an architectural reference for dependencies,
information flow, state ownership, and forbidden paths.

The execution mode is **Planning Only**. V0 static checks are Agent-allowed;
V2 final verification is User Terminal Only; V3 audit and final decision are
ChatGPT-only. The Agent stop point is
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.

## Canonical cognitive domains

```text
Constitution
  ↓
Governance Plane
  ├── Protocol Governance
  ├── Registry / Admission Governance
  ├── Authority Governance
  ├── Diagnostics Governance
  └── Resource / Runtime Governance
  ↓
Cognitive Core
  ├── Reality / Evidence
  ├── Field Network
  │   ├── Physical Field
  │   └── Social / Role / Relationship Context
  ├── Self (Identity / Capability / State)
  ├── Attention
  ├── Workspace
  ├── Drive / Value
  ├── Situation / Hypothesis / Belief / Expectation
  ├── Intent / Goal / Task
  ├── Memory / Experience / Learning
  ├── Reflex
  ├── Emotion Context Boundary
  └── Brain
  ↓
Decision Candidate → Decision Commitment → Action Request Candidate
  ↓
Action Boundary (execution authority remains outside this phase)
  ↓
Outcome / Evidence Feedback
  ↓
Experience / Learning Candidates
```

## Canonical dependency direction

The primary dependency direction is:

```text
Reality / Evidence
  → Field and Self State
  → Situation Context
  → Hypothesis / Belief / Expectation Candidates
  → Global Cognitive State / Workspace
  → Brain Evaluation
  → Intent / Goal / Task Context
  → Decision Candidate
  → Decision Commitment
  → Action Request Candidate
  → Action Boundary
  → Outcome Evidence
  → Experience / Learning Candidates
```

Dependencies are classified as `Required Dependency`, `Optional Dependency`,
`Candidate Dependency`, or `Future Interface`. A candidate dependency never
silently becomes an authoritative write.

## Information-flow rules

Allowed examples include Evidence → Field update candidate, Field → Situation
context, Memory → Brain relevant retrieval, Learning → Memory candidate,
Brain → Decision Commitment candidate, and Decision Commitment → Action
Boundary action-request candidate.

The following paths are prohibited:

```text
Learning → Reality write
Emotion Context → Decision override
Capability / Provider → Goal creation
Provider → Brain direct access
Model → Decision
Hardware → Goal or Value mutation
Action Boundary → Reality direct write
```

Canonical edge labels: `Reality / Evidence → Field`, `Global Cognitive State → Brain`,
`Brain → Decision Candidate → Decision Commitment`,
`Decision Commitment → Action Request Candidate → Action Boundary`, and
`Outcome Evidence → Experience → Learning Candidates`.

Reality is updated only through the Evidence / Reality Update Pipeline and its
Reducer boundary. Current Evidence has priority over stale Memory, Belief,
Expectation, or Experience. Unknown and provenance are preserved throughout.

## Authority and state ownership

The ownership matrices are normative:

- Reality: Evidence / Reality Update Pipeline owns update candidates and the
  Reducer owns accepted state transitions.
- Field: Field System owns Field State; Role and Relationship are context
  projections bound to a Field, not Identity mutations.
- Attention: Attention System owns allocation, competition, arbitration,
  persistence, and release.
- Goal and Intent: Goal / Intent contracts with Brain Review retain authority;
  Task maintains continuity but cannot invent authority.
- Decision: Brain owns final Decision judgment; Decision Commitment only
  qualifies a candidate for preparation.
- Action: Action Boundary owns permission, authorization, risk, and external
  execution isolation.
- Experience and Learning: Experience System owns records; Learning produces
  candidates and cannot automatically rewrite Reality, Identity, Goal, Value,
  or Strategy.

Every state map records `Owner`, `Writer`, and `Reader`. A Reader has no write
authority merely by receiving a state package.

## Canonical cognitive loop

```text
Observe
  ↓
Represent
  ↓
Understand
  ↓
Hypothesize
  ↓
Evaluate
  ↓
Commit
  ↓
Prepare Action
  ↓
Feedback
  ↓
Learn
  ↓
Adapt
```

`Commit` means Decision Commitment candidate review only. `Prepare Action`
means an Action Request Candidate may be handed to Action Boundary. Neither
step executes external behavior in this phase.

## Boundary audit and migration posture

Core, Governance, Capability, Runtime, and future Simulation concerns remain
separate. Capability can provide state and evidence candidates but cannot
produce cognition, create Goal, or access Brain directly. Model, Provider, and
Hardware integration remain future interfaces and are not activated here.

This consolidation does not rename or delete previously passed assets. The
migration map records canonical aliases, ownership corrections, and future
compatibility work as candidates only. No automatic migration, runtime
rewrite, Action execution, model call, hardware call, B Simulation, or
automatic Learning is performed.

## Required negative guards

No new module creation beyond this consolidation phase; no Runtime
implementation; no Model Manager or Provider integration; no Hardware
integration; no Action execution; no automatic Learning; no B Simulation; no
Emotion Runtime; no authority inversion; no direct Reality mutation; no
`Provider → Brain Direct Access`; no `Capability → Goal Creation`; no
`Learning → Reality`; no `Emotion → Decision Override`.

Contract keywords: no Runtime implementation; no Hardware integration; no
Emotion Runtime.
Exact guard: no Emotion Runtime.
