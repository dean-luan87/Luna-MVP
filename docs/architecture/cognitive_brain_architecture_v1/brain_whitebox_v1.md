# Brain Whitebox v1

## Authority questions

1. Who supplies Brain input? Global Cognitive State, relevant Evidence,
   Hypothesis/Belief/Expectation candidates, Option Candidates, and
   Constraint Candidates through governed interfaces.
2. Who owns Reality? Reality Workspace and Reducer; Brain receives state and
   does not write Reality.
3. Who owns Field, Self, Memory, Goal, and Attention? Their existing owners;
   Brain does not replace or mutate them.
4. Who evaluates Situation and Options? Brain emits evaluation candidates.
5. Who owns Value? Value Core; Brain treats Value as a constraint.
6. Who owns Drive? Drive Core; Brain treats Drive as influence.
7. Who owns final Decision authority? Brain retains final Decision authority,
   but its output remains a Decision Candidate until the Decision Boundary.
8. Who executes Action? Action Boundary and Runtime; Brain never executes.

## Allowed flow

```text
Global Cognitive State + Evidence + Hypothesis + Expectation Feedback
                       + Options + Constraints
                              ↓
                       Brain Context Package
                              ↓
State Interpretation → Situation Evaluation → Intent Alignment
                              ↓
Option Evaluation → Conflict Analysis → Decision Candidate
                              ↓
                         Decision Trace
```

## Negative paths

- Brain → Reality mutation: forbidden.
- Brain → Field mutation: forbidden.
- Brain → Memory ownership: forbidden.
- Brain → Goal mutation: forbidden.
- Brain → Attention allocation: forbidden.
- Brain → Capability/Provider/Model invocation: forbidden.
- Brain → Action execution: forbidden.
- Brain → automatic planning: forbidden.
- Brain → Prediction Runtime: forbidden.
- Brain → World Model: forbidden.
- Brain → B Simulation Runtime: forbidden.
- Learning → Brain modification: forbidden.
- Value → Brain replacement: forbidden; Value remains a constraint.

## Preserved fields

Every evaluation and Decision Candidate preserves Global Cognitive State,
Evidence, Options, Constraints, Intent, Goal, Task, Value, Drive, Hypothesis,
Expectation Feedback, Unknown, Risk, Conflict, Confidence, and Provenance.

Contract paths: Brain → Hypothesis or Belief resolution; Brain → Expectation update; Brain → Decision; Brain → automatic learning.
