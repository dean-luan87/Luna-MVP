# Cognitive Behavior Evaluation Architecture Plan v1

## Position

Behavior Evaluation Layer describes the comparative value profile of existing Behavior Candidates. It sits between candidate generation and a future, separately governed Decision layer:

`Behavior Boundary -> Behavior Candidate -> Behavior Evaluation Candidate -> Future Decision Candidate -> Future Action Candidate`.

It answers “what value, cost, uncertainty, risk exposure, and reversibility characteristics does each candidate have in the current context?” It never answers “select this candidate.”

## Input and output

Permitted inputs are traceable references to Behavior Boundary, Behavior Candidate, Survival, Current Cognitive Context, Field/Field View, Goal, Belief, Hypothesis, Information Value, Cognitive Constraint, Experience pattern, provenance, and trace. Output is a candidate-only evaluation record associated with exactly one Behavior Candidate.

## Responsibilities

| Layer | Responsibility | Excluded authority |
| --- | --- | --- |
| Behavior Boundary | Define constrained behavior space | Selection or execution |
| Behavior Candidate | Express possible behaviors | Comparative choice |
| Behavior Evaluation | Describe value/cost/risk/uncertainty profile | Decision, permission, action |
| Future Decision | Select from governed evaluation candidates | Execution and state mutation |
| Reducer | Sole State mutation authority | Evaluation or decision |

This phase is Planning Only. It authorizes no Runtime, policy engine, Decision, Action, permission, model/provider call, Field Kernel/Reducer integration, State mutation, Memory, Learning, Hive, or Library runtime.
