# Cognitive Primitive Layer Skeleton Contract v1

All five candidate types share `primitive_id`, `primitive_type`, source/context references, provenance, confidence, uncertainty, candidate status, and trace. They are fixed as `candidate_only=true` and `fact_status=not_fact`.

Forbidden input or schema fields are `fact_id`, `decision_id`, `action_id`, `state_write_target`, and `memory_target`. Skeleton flags declare all Runtime, external, database, Field Kernel, Reducer, Fact, Decision, Action, State, and Memory operations false.

