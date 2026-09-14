# Cognitive Observation Attention Selection Boundary Contract v1

## Allowed future inputs

Current Cognitive Context Reference, Observation Need Candidate, Survival Constraint Reference, Goal Reference, Field Reference, Information Gap Reference, provenance, and trace.

## Forbidden inputs and authority

Raw Observation, Model Result, Fact, State, Action, Command, Provider payload, Permission, and Reducer command are prohibited. Attention Selection cannot mutate Context, Field, State, Snapshot, Memory, Experience, Learning, Hive, or any Capability.

## Output boundary

Every future Attention Selection Candidate remains `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, and `not_memory=true`.
