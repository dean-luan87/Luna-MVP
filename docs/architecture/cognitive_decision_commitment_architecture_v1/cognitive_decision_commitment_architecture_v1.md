# Cognitive Decision Commitment Architecture v1

## Phase boundary

This phase defines the controlled transition between a Brain-produced
Decision Candidate and an Action Request Candidate. Decision Commitment is a
reviewed qualification, not an Action, Plan, or execution.

```text
Brain
  ↓
Decision Candidate
  ↓
Decision Commitment
  ↓
Action Boundary
  ↓
Action Request Candidate
```

Decision Candidate answers “what may be the correct choice?” Decision
Commitment answers “is this choice currently fit to enter action preparation?”
The Action Boundary still owns permission, risk control, authorization, and
external execution isolation.

## Decision Commitment definition

Decision Commitment is a governed confirmation candidate for a Decision
Candidate. It is not a Plan and it is not an Action. It checks Reality freshness, Evidence sufficiency, Constitution,
Value, Safety, Governance, Intent alignment, Capability availability, timing,
resource requirements, expiration, and expected validation conditions.

Commitment does not execute, plan, call a Capability, control Hardware,
modify Reality, modify Goal, modify Value, or bypass Action Boundary.
It does not enter Model Runtime and does not make a model or hardware call.

## Decision Commitment Candidate schema

Every candidate contains:

```text
decision_commitment_id
source_decision_candidate
related_field
related_task
related_intent
supporting_evidence
confidence
risk_level
constraint_check
resource_requirement
expiration_condition
commitment_status
review_trace
```

It also preserves Reality freshness, Evidence sufficiency, Capability state,
Expectation, Unknown, Conflict, Human Override requirement, authorization
level, timing, and Provenance.

## Validation checks

1. **Reality Freshness Check** — current Reality remains compatible with the
   Decision Candidate; a new closure or hazard Evidence can invalidate it.
2. **Evidence Sufficiency Check** — the supporting Evidence meets the
   candidate’s validation condition or explicitly records an information gap.
3. **Constraint Check** — Constitution, Value, Safety, and Governance rules
   are not violated.
4. **Intent Alignment Check** — the candidate remains aligned with current
   Intent, Goal, Task, and Field context.
5. **Capability Availability Check** — required Capability state is available
   or degraded within an admitted threshold; this check does not invoke a
   Capability.

Failure of any check yields an Invalidated, Deferred, or More Evidence
Required candidate, not automatic execution.

## Lifecycle

```text
Created
   ↓
Candidate
   ↓
Reviewing
   ↓
Committed
   ↓
Executing Preparation
   ↓
Invalidated
   ↓
Expired
   ↓
Archived
```

`Executing Preparation` means that an Action Request Candidate may be formed
for the Action Boundary. It does not mean Action Execution. A commitment can
be invalidated before preparation when Evidence, Reality, Risk, Capability,
Intent, or authorization changes.

## Attention and Expectation

Commitment can emit a Validation Requirement and Attention Request when a
precondition is unresolved:

```text
Decision Commitment
  ↓
Validation Requirement
  ↓
Attention Request
  ↓
Evidence Update
  ↓
Maintain / Revise / Invalidate
```

Commitment does not allocate Attention. It binds an Expected Outcome or
Expectation condition so later Feedback can maintain, revise, or invalidate
the commitment.

## Evidence, Value, Capability, Memory, and Learning

Evidence has priority over stale Decision Commitment assumptions. Value is a
constraint, not a commitment-created preference. Capability contributes
state and availability only; no Capability is called by this phase.

Memory stores selected Decision Transitions, such as successful, erroneous,
or high-value decisions. Learning receives Decision Outcome and produces
Experience, Strategy, Pattern, or Future Candidates. Learning does not
automatically rewrite a Commitment, Value, Goal, or Strategy.

## Conflict and revision

Multiple Decision Commitments may coexist and produce a Conflict Candidate.
Supported conflict types are Intent Conflict, Goal Conflict, Value Conflict,
Role Conflict, Resource Conflict, and Time Conflict. Conflict is preserved
for Brain or Human Review; it is not silently resolved.

The revision loop is:

```text
Decision Candidate
  ↓
Commitment
  ↓
Feedback
  ↓
Revision Candidate
  ↓
New Commitment
```

Human Override is reserved as an interface for high-risk or uncertain
commitments. This phase defines the review contract only and does not
implement interaction.

## Action Boundary and explicit non-goals

The Action Boundary receives an Action Request Candidate, not a command. It
performs its own permission, risk, authorization, and external-world checks.
This phase does not perform Action Execution, Hardware Control, Model
Runtime, automatic planning, automatic execution, automatic Value or Goal
modification, B Simulation Runtime, Prediction Runtime, or any model or
hardware call.
The forbidden combined operation is automatic Value or Goal modification.
