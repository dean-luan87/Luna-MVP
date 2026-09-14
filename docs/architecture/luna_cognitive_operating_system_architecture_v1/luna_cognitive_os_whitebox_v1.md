# Luna Cognitive OS Whitebox v1

## Control questions

For every L1 subsystem, the audit must answer:

1. Who registers it?
2. Who owns its contract?
3. Who may write its state?
4. Which events may reach it?
5. What is its failure and recovery path?
6. Which L0 constraint blocks unsafe behavior?
7. Which L2/L4 interface consumes its output?

## Explicit non-authority

Cognitive OS is not Brain, Decision, Reality Reducer, Provider, Model Manager,
Hardware Manager, or Action Runtime. A flow node can route a candidate but
cannot approve a Decision. A recovery candidate can request a resume point but
cannot create a Goal or mutate Constitution.

## Review evidence

The phase verifier checks subsystem coverage, lifecycle fields, single-writer
state contracts, event lifecycle, trace fields, recovery ordering, admission
gates, and forbidden authority paths. Runtime execution is intentionally absent.

