# Current Cognitive Context Candidate Skeleton Contract v1

## Input

The builder accepts declared references for Field, Field View, Primitive/Concept context, Survival, Attention Candidate, Task, Temporal/Spatial scope, provenance, and trace. It rejects raw model output, provider payload, Memory, Fact, Decision, Action, Reducer Command, and State mutation inputs.

## Output

The only output is `CurrentCognitiveContextCandidateV1` with fixed flags:

`candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, and `not_memory=true`.

Context is Luna's current way of facing an environment; it is not the Field and cannot modify Field or Field State. Context can reference Attention, but it does not own Attention authority. Language remains future expression-only and cannot mutate Context.

## Serialization

Canonical JSON uses sorted keys and compact separators. Serialization does not write to any store, invoke a provider, or enter Runtime.
