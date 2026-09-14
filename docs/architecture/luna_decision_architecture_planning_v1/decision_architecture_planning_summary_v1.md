# Decision Architecture Planning Summary v1

## Summary

Decision Architecture Planning v1 defines a candidate-only governance layer that determines what can be selected now under Intent, Causal, Context, Field, Role, Permission, Safety, and Resource constraints. It explicitly forbids direct Action execution and Task creation.

## Key Freezes

- Canonical owner is Decision Governance.
- Legacy aliases do not create parallel authority.
- Decision Candidate is distinct from Action and Task.
- Hard constraints are prior to utility preference.
- Defer, Abstain, and Request-More-Evidence are first-class outcomes.
- Reversibility and human confirmation requirements are explicit.
- Decision to Action/Task output is candidate-only handoff.

## Evidence Completeness

- Provenance trace schema includes decision rationale, alternatives, rejected options, and state transitions.
- Minimum scenario suite covers 14 semantic cases required for future executable fixtures.

## Boundary Result

Planning-only boundaries are preserved:

- runtime_executed=false
- decision_execution=false
- action_triggered=false
- task_created=false
- database_write=false
- model_call=false
- source_mutation=false
