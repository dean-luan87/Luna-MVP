# Reality Context Projection Model v1

## Position

Reality Context Projection is the bridge from Reality Neural Operating Space to A
Route. It produces a bounded read model, not a Situation Engine.

```text
Reality Neural Operating Space
          ↓
Reality Context Projection
          ↓
       A Route Input Context
          ↓
   Situation Understanding
```

## Projection contents

The projection may include Observable State, State Change, Relevant Constraints,
Unknowns, Validity, and Provenance. It may select current facts using a declared
read scope or Attention Requirement, but selection is data relevance, not value
interpretation.

Example:

```json
{
  "observable_state": {"water_depth": "60cm"},
  "state_change": {"door": "closed_to_open_candidate"},
  "relevant_constraints": {"battery": "20%"},
  "unknowns": ["flow_speed", "exit_status"],
  "provenance": ["vision", "sensor", "user_input"]
}
```

## Interpretation boundary

The projection does not add risk, danger, recommendation, plan, prediction,
emotion, or Decision. `flow_unknown: true` is permitted; `risk: dangerous` is not.
`voice_pattern_change_candidate` is permitted; `user_is_sad` is not. Situation,
meaning, and choice remain in A Route, Brain, or Emotional Cognition according to
their contracts.
