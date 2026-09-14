# Cognitive Strategy Selection Boundary Contract v1

## Allowed future references

Current Context, Goal, Information Gap, Survival Constraint, Risk Candidate, Attention Candidate, provenance, and trace.

## Prohibited authority

Fact, Decision, Action, Permission, State Mutation, Reducer Command, Memory, Learning, Hive, Model Output, and Provider payload cannot enter as authority or leave as output.

Every future strategy output remains `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, and `not_memory=true`.

Unknown does not mean Failure; an Information Gap does not imply a requirement for complete information; Risk is not Fact; Confidence is not Authority; and Model Output cannot determine a strategy directly.
