# Cognitive Value Evaluation Architecture Plan v1

## Position

Cognitive Value Evaluation Layer combines Mission Constraint, value evaluation, resource budget, and risk/reward balance as one candidate-only layer. Its flow is:

`Survival Constitution -> Mission Constraint -> Current Context -> Attention -> Information Value -> Strategy -> Reasoning/Hypothesis/Belief -> Cognitive Constraint -> Behavior Boundary -> Behavior Candidate -> Cognitive Value Evaluation -> Future Decision Candidate -> Future Action Candidate`.

It evaluates whether a current Behavior Candidate is worth possible cognitive, time, and future action resources. It does not select, permit, execute, learn, or mutate State.

## Authority order

`Survival Constitution > Mission Constraint > Cognitive Value Evaluation > Future Decision Candidate` is a constraint and evaluation order, not an execution order. Mission can affect candidate evaluation weights only within Survival constraints. It cannot override Survival, L0/L1 governance, Behavior Boundary, or Reducer authority.

## Planning boundary

No Runtime, policy/reward engine, Decision, Action, Permission, model/provider access, Field Kernel/Reducer integration, State mutation, Memory, Learning, Hive, or Library runtime behavior is authorized.
