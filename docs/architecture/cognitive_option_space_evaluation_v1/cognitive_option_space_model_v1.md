# Cognitive Option Space Model v1

## Purpose

Option Space is the governed set of possible paths formed from a Situation
Candidate. It is a candidate space, not an answer, recommendation, Decision,
Action, execution plan, or Prediction.

```text
Situation
 + Self Capability
 + Self State
 + Goal
 + Constraint
 + Unknown
        ↓
Option Candidate Space
        ↓
Evaluation Candidate
        ↓
Decision Candidate Package
        ↓
Brain Evaluation
```

Option Space must retain multiple materially different options when available.
For a road closure, candidates may include waiting, rerouting, finding another
entrance, or requesting help. No option is preferred merely because it was
generated first.

## Candidate structure

Each Option Candidate carries an identity, assumptions, expected benefit
candidate, Resource Cost, Risk Candidate, Capability Requirement, Unknown,
dependency, feasibility boundary, provenance, and confidence. Expected Benefit Candidate and Dependency are required. An option may be
infeasible under current Self Capability or Self State; it must remain visible
as rejected-by-constraint rather than being silently fabricated or executed.

## Generation boundary

Option sources are A Route, Brain Request, and Capability Feedback. A Provider
may provide evidence or a Capability Requirement, but Provider cannot generate
a behavior, select an option, create a Decision, or issue an Action. Experience
may supply an Option Prior; it cannot directly select a strategy.

## Evaluation boundary

Option Evaluation is a candidate comparison, not final value judgment. It
records Survival Impact, Goal Alignment, Capability Fit, Resource Cost, Risk,
Uncertainty, Experience Reference, and Confidence. Unknown remains explicit and
reduces confidence where relevant. Brain retains final Decision authority.

No Action, No Execution Runtime, No automatic execution, Provider Decision, Emotion,
Role, Social Runtime, B, or Prediction is implemented in this phase.
