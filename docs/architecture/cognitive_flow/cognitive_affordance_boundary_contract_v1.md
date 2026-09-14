# Cognitive Affordance Boundary Contract v1

## Allowed candidate references

Field Representation/View, Primitive/Concept, Relationship, Situation, Context, Goal, Capability/Self Reference, Role Reference, Experience, provenance, and trace references may be read.

## Rejected inputs and effects

Decision result, Action command, permission, raw model/provider output, Fact Store authority, State handle, Reducer command, Memory mutation, Affordance Runtime, Action Planner, Behavior Executor, Permission Engine, Decision Runtime, Learning runtime, and Hive authority are outside this layer.

## Negative guards

- Affordance != Action.
- Affordance != Permission.
- Affordance != Decision.
- Affordance != Goal.
- Affordance != Identity.
- Situation != Affordance.
- Situation != Behavior.
- Role != Identity.
- Unknown Affordance != No Capability.
- Experience != Current Opportunity.
- Experience != Reality.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not behavior, not decision, not action, not permission, not goal, not identity, and not memory.
