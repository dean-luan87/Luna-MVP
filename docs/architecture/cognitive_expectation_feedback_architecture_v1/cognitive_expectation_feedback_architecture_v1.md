# Cognitive Expectation and Feedback Architecture v1

## Phase boundary

This phase defines how Luna forms an Expectation Candidate from its current
understanding and compares that expectation with later Reality Feedback.
Expectation is a context-bound observation standard, not a future prediction.

The cognitive path is:

```text
Reality
    ↓
Evidence
    ↓
Hypothesis
    ↓
Belief Candidate
    ↓
Expectation
    ↓
Reality Feedback
    ↓
Experience
    ↓
Learning
    ↓
Future Understanding
```

The complete feedback loop is:

```text
Reality
    ↓
Understanding
    ↓
Expectation
    ↓
Observation
    ↓
Feedback
    ↓
Adaptation Candidate
```

## Expectation definition

Expectation is a current cognitive state’s conditional statement about what
Evidence should be observable if the current Hypothesis, Belief, Field Rule,
or Task interpretation is adequate. It constrains what to verify; it does
not assert that a future event will occur.

Prediction is a future-event estimate. Expectation is not Prediction, and
this phase does not implement a Prediction Runtime, future prediction model,
World Model, or time-series prediction.

For example, if a corridor is hypothesized to be an exit, the Expectation
Candidate may specify exit signage, a gate, or people moving outward as
expected Evidence. Absence of those signals produces Feedback; it does not
automatically prove a different world state.

## Expectation Candidate schema

Every Expectation Candidate contains:

```text
expectation_id
source_hypothesis
source_belief
related_field
related_situation
expected_state
expected_evidence
time_context
confidence
validation_condition
feedback_status
lifecycle_state
```

It also preserves source type, Field and Situation context, Task reference,
supporting Evidence, Unknown, Risk, Difference, and Provenance.

## Expectation sources

Four source classes are supported:

1. **Hypothesis Driven** — expected Evidence that would support or weaken a
   Hypothesis.
2. **Belief Driven** — a context-bound expectation derived from a validated
   pattern, still revocable by current Reality.
3. **Field Rule Driven** — expected observations implied by a current Field
   Rule, such as airport signage or security flow.
4. **Task Driven** — expected state changes required to evaluate progress in
   an existing Task, such as route direction or distance change.

No source creates a Decision or mutates Reality. A Belief-driven expectation
cannot override current Evidence, and a Task-driven expectation cannot alter
Task ownership.

## Hypothesis and Expectation boundary

Hypothesis explains current uncertainty. Expectation specifies what should be
observable if that explanation remains useful. The relation is:

```text
Hypothesis: the closed road may be under construction
Expectation: if so, barriers, notices, or a detour should be observable
```

Hypothesis and Expectation remain separate records with separate confidence,
validation, contradiction, and lifecycle state. Expectation does not become a
Hypothesis, Belief, or Reality automatically.

## Field and Situation binding

Expectation is always bound to Field Context, Situation, Belief or
Hypothesis source, and Time. The same sound or state can yield different
expectations in a hospital and a home. Cross-Field transfer is a candidate
requiring revalidation; it is never silent.

## Feedback and Difference

The feedback loop is:

```text
Expectation
    ↓
Reality Observation
    ↓
Compare
    ↓
Feedback Candidate
    ↓
Update Candidate
```

Feedback status is one of `Confirmed`, `Partially Confirmed`, `Contradicted`,
`Unknown`, or `Expired`. Expectation Difference records the expected state,
observed Reality, comparison basis, magnitude or category of difference,
Unknown, and Provenance. Expectation Difference is not Prediction Error and
does not automatically modify Belief, Reality, or strategy.

Feedback has priority over stale Belief for current interpretation. It may
produce an Experience Record and Learning Candidate, but Learning does not
directly change an active Expectation.

## Attention and observation interface

Expectation may produce an Observation Requirement and Attention Request:

```text
Expectation
    ↓
Need Validation
    ↓
Attention Request
    ↓
Observation
    ↓
Feedback
```

Attention owns resource allocation. Expectation only identifies
discriminating Evidence, target observations, persistence, risk, and cost
candidates. Observation and Capability execution remain governed by their
existing contracts.

## Memory, Learning, and Brain interfaces

Memory records what occurred and preserves the related Expectation, so the
two are not conflated. Learning receives Feedback, Difference, and Experience
Record and may produce a Future Adjustment Candidate. No automatic strategy,
Belief, Goal, or Expectation modification is permitted.

Brain receives an Expectation Package containing current Understanding,
Expectation Candidates, supporting Evidence, Feedback Status, Difference,
Unknown, Risk, Conflict, and Provenance. Brain evaluates the package and
retains final judgment authority; Expectation does not make a Decision.

## Lifecycle

```text
Created → Active → Validated → Updated → Contradicted → Deprecated → Archived
```

Lifecycle transitions are candidate-based, time-aware, and provenance
preserving. A contradiction suspends or updates an expectation candidate; it
does not erase the historical expectation or force a new interpretation.

## B Route placeholder and explicit non-goals

Future B Route may consume an Expectation Snapshot and produce a Simulation
Expectation Candidate for comparison. This phase defines only a placeholder;
there is no B Simulation Runtime and no live Reality mutation.

This phase does not implement Prediction Runtime, World Model construction,
automatic future reasoning, automatic Belief modification, automatic Reality
modification, automatic Decision, Action Runtime, B Simulation Runtime,
model training, or hardware execution.

Contract keywords: Belief or Hypothesis source; Brain retains final judgment
authority; Simulation Expectation Candidate; automatic Reality modification;
Unknown is preserved.
Contract keyword: Brain retains final judgment authority.
