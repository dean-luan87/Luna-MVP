# Cognitive Intent Architecture v1

## Phase boundary

This phase defines the Intent Layer as a governed expression of what the
subject is trying to accomplish in a context. It does not implement
autonomous will, automatic goal generation, personality-driven intent,
Emotion Decision, or Action.

The Intent Layer sits between motivation and continuity:

```text
Drive / Value
    ↓
Intent
    ↓
Goal
    ↓
Task
    ↓
Action Boundary
```

The cognitive interpretation path is:

```text
Situation
    ↓
Intent
    ↓
Goal
    ↓
Task
    ↓
Action Boundary
```

Intent is not a command and is not a decision. It is an Intent Candidate
whose source, context, confidence, constraints, unknowns, and provenance are
explicit. The Brain retains interpretation, goal authority, value review, and
final Decision authority.

## Intent definition

An Intent Candidate expresses a desired direction or purpose without
committing the system to a Goal, Task, Decision, or Action. An Intent
Expression is the normalized statement of that candidate. Intent Context
binds the expression to the current Field, Role, Relationship, Self state,
Situation, and time window.

For example, “go to the hospital” may express navigation, accompanying a
family member, attending an appointment, or seeking emergency help. The
surface instruction is evidence for an Intent Candidate, not an automatic
interpretation or automatic goal.

## Intent sources

The source registry admits five bounded source classes:

```text
Intent Source
├── User Intent
├── Self Intent
├── Survival Intent
├── Task Intent
└── Field Requirement
```

- **User Intent** is a user-provided or user-confirmed purpose candidate.
- **Self Intent** is a self-continuity or capability-preservation candidate;
  it is not autonomous will.
- **Survival Intent** is a Constitution/Reflex-derived safety purpose
  candidate and must remain inside safety governance.
- **Task Intent** is a purpose inherited from an existing Goal/Task process;
  it cannot create a task by itself.
- **Field Requirement** is a context-derived requirement candidate, such as
  finding an exit or reducing uncertainty in an unfamiliar field.

Source precedence is not a fixed decision order. Conflicting sources produce
an Intent Conflict Candidate for Brain review and preserve all provenance.

## Field and subject binding

Intent is always context-bound. The same Goal can express different Intent
Candidates in different fields, roles, relationships, or self states. A
visitor, clinician, and patient can share a hospital Field while having
different Intent Context packages.

The binding package contains:

- Field reference and Field state;
- active Role and Relationship context;
- Self Identity reference, Capability state, and Self State;
- Situation reference, Goal/Task references, and time validity;
- Drive influence and Value constraints;
- Attention relevance, risk, unknowns, and provenance.

The Intent Layer references an existing Field, Role, Relationship, Goal, and
Task. It does not create or mutate them. Reality remains authoritative over
Intent interpretation, and Unknown is preserved when intent cannot be
resolved.

## Interfaces

Intent produces governed candidates for downstream systems:

```text
Intent Candidate
    ├── Attention influence candidate
    ├── Option relevance candidate
    ├── Goal alignment candidate
    └── Brain review package
```

Intent influences Attention, Option, and Decision Candidate context, but it
does not allocate Attention, generate an Option, make a Decision, or execute
an Action. Existing Goal and Task contracts remain the owners of continuity;
this phase only supplies an intent reference and alignment candidate.

The Brain receives the Intent Brain Interface package and may accept,
modify, reject, request clarification, request more information, or defer an
Intent Candidate. The Brain retains final Decision authority. A Capability or
Provider cannot create an Intent, Goal, or Action through this interface.

## Conflict and uncertainty

When multiple Intent Candidates are simultaneously applicable, the system
creates an Intent Conflict Candidate containing the candidates, contexts,
constraints, risk, unknowns, and provenance. Conflict is not silently
resolved. Brain review is required for material conflicts, and a request for
more information is a valid outcome.

Intent confidence is not Reality confidence. A high-confidence intent still
requires current Reality, Field, and Situation validation. Historical Memory,
Emotion Context, and Learning may contribute candidates or metadata but may
not override Reality or silently change intent authority.

## Lifecycle and governance

An Intent Candidate follows:

```text
Created → Qualified → ContextBound → Presented → Reviewed →
Accepted | Modified | Rejected | Deferred | Expired | Archived
```

Every transition is provenance-preserving and candidate-based. Governance
checks source permission, Field binding, Goal/Task compatibility, Value and
Drive constraints, risk, unknowns, and expiry. An accepted Intent does not
automatically generate a Goal; Brain or an explicitly authorized upstream
owner must perform Goal admission.

## Explicit non-goals

This phase has no automatic goal generation, no autonomous will, no
personality-driven intent, no Emotion Decision, no Action, no Action Runtime,
no model invocation, no hardware invocation, no B Route Runtime, and no
simulation execution. The future B Route may consume an Intent Snapshot and
vary an Intent Candidate as a placeholder only; it must not mutate Reality or
the live Intent state.

Contract keyword statements: Intent Expression; does not make a Decision;
Simulation Runtime is not implemented; Provenance is mandatory metadata.
