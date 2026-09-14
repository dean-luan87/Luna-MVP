# Current Cognitive Context Model Definition v1

## Future candidate

`CurrentCognitiveContextCandidate` is a traceable candidate with:

- `current_field_reference`;
- `survival_context`;
- `task_context`;
- `attention_context`;
- `uncertainty_context`;
- `information_gap`;
- `temporal_scope`;
- `spatial_scope`;
- `experience_reference`; and
- `provenance` and trace.

It must remain candidate-only. The model holds references and explicit uncertainty; it does not duplicate Field State, Snapshot, Fact Store, Memory, or Decision state.

## Unknown condition

Context may expressly contain `unknown_field`, `unknown_identity`, and `partial_information`. Unknown Context is a valid cognitive condition, not failure and not a trigger for automatic completion.
