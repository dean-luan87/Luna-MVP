# Cognitive Brain Architecture v1

## Phase boundary

This phase defines Luna Brain as the cognitive processing center that
interprets a Global Cognitive State, evaluates situations and options, checks
Intent alignment, analyzes conflicts, and produces a Decision Candidate.

Brain is not a Large Language Model, Memory, Planner, Action Executor, or
Prediction Engine. It is a governed cognitive evaluation layer:

```text
Global Cognitive State
        ↓
      Brain
        ↓
Decision Candidate
        ↓
Decision Boundary
        ↓
Action Boundary
```

Brain does not replace Reality, Field, Self, Goal, Memory, Attention, or
Capability owners. It consumes their state references and emits candidates
back to the existing decision and action boundaries.

## Core responsibilities

### State Interpretation

Brain interprets the current Global Cognitive State and produces a Current
Cognitive Interpretation Candidate. It describes the current Field, Self,
Intent, Task, Risk, Unknown, Hypothesis, Belief, and Expectation context; it
does not mutate any source state.

### Situation Evaluation

Brain evaluates the current Situation and emits a Situation Evaluation
Candidate. It does not replace or rewrite Situation Understanding.

### Intent Alignment

Brain checks whether candidate interpretations and options align with the
active Intent, Goal, Task, Drive, and Value constraints. Misalignment is a
candidate finding, not an automatic rejection or Decision.

### Option Evaluation

Brain consumes Option Candidates together with Global Cognitive State and
produces trade-off, risk, confidence, constraint, and unknown assessments.
Option Evaluation is not Action generation.

### Conflict Evaluation

Brain can evaluate simultaneous Intent Conflict, Goal Conflict, Role
Conflict, Value Conflict, Field Conflict, and Resource Conflict. Conflicts
remain explicitly represented and may require clarification, more Evidence,
or a deferred Decision Candidate.

### Decision Candidate Generation

Brain produces a Decision Candidate, never an Action Command. The candidate
contains its context, options, constraints, risks, Unknowns, confidence,
value considerations, and provenance for Brain Review and the existing
Decision Boundary.

## Brain Context Package

Brain receives a Brain Context Package composed from:

```text
Global Cognitive State
        + Relevant Evidence
        + Hypothesis Candidates
        + Expectation Feedback
        + Option Candidates
        + Constraint Candidates
        ↓
Brain Context Package
```

Brain does not directly access Camera, Model, Hardware, Database, or Provider.
Those remain behind Capability, Evidence, Reality, and Governance contracts.
Brain receives Evidence and state references, not raw devices or ungoverned
model output.

## Cognitive processing flow

```text
State Understanding
        ↓
Situation Evaluation
        ↓
Intent Alignment
        ↓
Option Evaluation
        ↓
Conflict Analysis
        ↓
Decision Candidate
        ↓
Decision Trace
```

Each stage produces a candidate with confidence, Unknown, Risk, Constraint,
and Provenance. A missing input remains Unknown; Brain does not fabricate a
complete state.

## Interfaces

### Attention

Attention does not belong to Brain. Brain may produce an Attention
Requirement or Need More Evidence candidate. Attention retains resource
allocation, arbitration, and observation authority:

```text
Brain
  ↓ Need More Evidence
Observation Requirement
  ↓
Attention
  ↓
Evidence Update
```

### Hypothesis and Expectation

Brain evaluates Hypothesis Candidates and uses Expectation Feedback. It does
not create facts, automatically solidify Beliefs, or rewrite Expectation.
Current Evidence and Feedback remain authoritative.

### Value and Drive

Value supplies constraints; Brain does not create Value. Drive supplies
motivation influence; Brain does not create Drive. The relation is:

```text
Value → Constraint → Brain Evaluation
Drive → Influence → Brain Evaluation
```

### Learning and Memory

Learning supplies Experience Candidate, Strategy Candidate, and Pattern
Candidate. Memory supplies relevant historical context. Neither owns Brain,
changes its parameters, or directly makes a Decision.

## Decision Trace

Every Decision Candidate carries a Decision Trace containing:

- the Global Cognitive State Snapshot and relevant Evidence;
- Intent, Goal, Task, Field, Role, Relationship, and Self context;
- Option candidates and trade-offs;
- Value constraints and Drive influence;
- Hypothesis, Belief, Expectation Feedback, Unknown, Risk, and Conflict;
- confidence, selected rationale candidate, rejected alternatives, and
  Provenance.

Decision Trace is an explanation record, not a command and not a new source
of Reality.

## Lifecycle and governance

```text
Created
   ↓
Context Loaded
   ↓
Evaluation
   ↓
Candidate Generated
   ↓
Reviewed
   ↓
Completed
   ↓
Archived
```

Lifecycle transitions are candidate-based and provenance-preserving. Brain
Governance checks the package, authority boundaries, Value constraints, risk,
Unknown, conflict, and Decision Candidate schema. Brain cannot bypass
Constitution or Governance.

## B Route placeholder and explicit non-goals

Future B Route may consume a Global Cognitive State Snapshot for Alternative
Evaluation. This phase defines an interface placeholder only; it does not
implement B Simulation Runtime or mutate live state.

This phase does not implement LLM integration, automatic reasoning Runtime,
Action execution, automatic planning, Prediction, World Model, automatic
learning, model training, hardware calls, or Action Runtime.

Contract keywords: not Memory; not Planner; not an Action Executor; not a Prediction Engine; Current Cognitive Interpretation Candidate; Situation Evaluation Candidate; Role Conflict; Attention Requirement; Attention retains resource allocation; Drive supplies motivation influence; Pattern Candidate; Alternative Evaluation; automatic learning.
