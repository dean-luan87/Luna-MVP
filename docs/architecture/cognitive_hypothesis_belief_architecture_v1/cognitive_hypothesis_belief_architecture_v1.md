# Cognitive Hypothesis and Belief Architecture v1

## Phase boundary

This phase defines how Luna forms temporary explanations when Reality is
incomplete, ambiguous, or conflicting. A Hypothesis Candidate is a
context-bound explanation proposal. A Belief Candidate is a more stable
reference candidate formed only after repeated, governed validation.

The intended information path is:

```text
Reality
    ↓
Evidence
    ↓
Hypothesis
    ↓
Field Understanding
    ↓
Situation
    ↓
Intent
    ↓
Goal
    ↓
Task
    ↓
Decision Boundary
```

The authority ordering is:

```text
Reality > Evidence > Hypothesis > Belief Candidate > Decision Context
```

This ordering means that neither a Hypothesis Candidate nor a Belief
Candidate can become Reality, overwrite Evidence, or make a Decision.

## Definitions and boundaries

**Hypothesis Candidate** is a temporary candidate explanation for an Unknown
or an observed pattern. It records what might explain current Evidence, not
what will happen in the future. Hypothesis is not Prediction, and this phase
does not define a Prediction Runtime.

**Belief Candidate** is a validated-pattern reference candidate. It can guide
future observation and Situation support, but it is not a fixed belief, a
Reality fact, a Field Rule, or a Decision. It remains revocable and
context-bound.

**Unknown** remains first-class. When Evidence is insufficient, Luna may keep
an Unknown without selecting a Hypothesis. Multiple Hypothesis Candidates
may coexist with separate confidence, support, contradiction, and
provenance.

## Hypothesis Candidate schema

Every Hypothesis Candidate contains:

```text
hypothesis_id
source_evidence
related_field
related_situation
candidate_explanation
confidence
uncertainty
supporting_evidence
contradicting_evidence
validation_status
lifecycle_state
```

The candidate also retains source type, time validity, Field context, rule
context, Experience reference, Human Feedback reference, Attention request
reference, Unknown, Risk, Constraint, and Provenance.

## Hypothesis sources

Four source classes are admitted:

1. **Evidence Driven** — direct or mediated Evidence suggests an explanation,
   such as a barrier suggesting a construction area.
2. **Field Rule Driven** — an existing Field Rule supplies a context-bound
   explanation candidate, such as movement toward a likely station exit.
3. **Experience Driven** — validated Experience supplies a reusable candidate,
   such as looking for a hidden entrance in a familiar building type.
4. **Human Feedback Driven** — user correction or clarification supplies a
   candidate that still requires Evidence and provenance.

No source is allowed to silently convert an explanation into a fact. Provider
and Model outputs enter as Evidence or Evidence Candidate only; they cannot
create a Decision, Reality, Field, or ungoverned Belief.

## Field and Situation binding

Hypothesis is always bound to an existing Field and Situation. The same
Evidence can have different meanings in different Fields: a warning sound in
a hospital may be equipment alarm evidence, while the same sound at home may
be an appliance notification. The binding package is:

```text
Hypothesis = Evidence + Field Context + Situation Context
```

Cross-Field transfer is a candidate only. A Hypothesis that cannot be
revalidated in the current Field remains Unknown or becomes a conflict; it
does not silently migrate.

## Confidence, support, and contradiction

Confidence is a candidate assessment, not truth. It must include its basis,
uncertainty, supporting Evidence, contradicting Evidence, source reliability,
Field validity, and calibration history. New Evidence can increase,
decrease, suspend, or revoke confidence.

When explanations conflict, the system records a Hypothesis Conflict with
all candidates, evidence, unknowns, tradeoffs, and provenance. It does not
force a selection. Brain Evaluation may accept, reject, defer, request more
Evidence, or keep multiple candidates active.

## Attention and validation loop

Hypothesis produces a validation requirement, not an observation execution:

```text
Hypothesis
    ↓
Validation Requirement
    ↓
Attention Request
    ↓
Observation
    ↓
Evidence Update
```

Attention owns resource allocation. Hypothesis only describes what Evidence
would discriminate among candidates, for example signs, crowd direction, or
door structure. Observation and Capability boundaries remain unchanged.

## Belief Candidate formation

The stability path is:

```text
Hypothesis Candidate
    ↓
Validated Pattern
    ↓
Belief Candidate
    ↓
Experience Reference
```

Belief Candidate admission requires repeated or high-impact validation,
current Field compatibility, contradiction review, confidence calibration,
and Governance admission. A single unconfirmed event cannot automatically
create a permanent Belief Candidate. Beliefs decay, can be contradicted,
deprecated, archived, or re-opened as Hypothesis Candidates.

Reality always overrides Belief Candidate. For example, a historical belief
that a shop opens at night must be suspended when current Evidence shows the
shop is closed.

## Learning, Memory, and Brain interfaces

Learning receives Validation Result and may produce Pattern or Future
Candidate updates. It does not directly solidify Belief or alter Reality.
Memory stores provenance-bearing references to Hypothesis, Validation, and
Belief Candidates; Memory does not override current Evidence.

Brain receives a Decision Context Package containing Reality, Evidence,
Hypothesis Candidates, Belief Candidates, Confidence, Unknown, Risk,
Conflict, and Provenance. Brain retains final judgment authority. A
Hypothesis or Belief Candidate is context for Brain, not a Decision.

## Lifecycle

Hypothesis lifecycle:

```text
Created → Candidate → Validated → Active Reference → Contradicted →
Deprecated → Archived
```

Belief Candidate lifecycle uses the same governed states but requires a
validated-pattern admission before Active Reference. Contradiction does not
delete history; it preserves the old candidate and creates an update or
replacement candidate with provenance.

## B Route placeholder and explicit non-goals

Future B Route may consume a Hypothesis Snapshot and produce a Simulation
Hypothesis Candidate for comparison. This phase defines only a placeholder;
there is no B Simulation Runtime and no live-state mutation.

This phase does not implement Prediction Runtime, World Model construction,
automatic belief solidification, Reality mutation, automatic Decision,
Action Runtime, B Simulation Runtime, model training, or hardware execution.

Contract keywords: Simulation Hypothesis Candidate; Unknown is first-class.
