# Cross-plane Evaluation Contract

## Join key

Cross-plane comparison joins immutable refs for:

`task_case + world_sample + condition + expected_observation_requirement +
capability + model/version + provider/binding version`.

## Attribution

- External Capability/Provider/Normalization failure: Plane B source failure.
- Observation planning, relevance, conflict, Sufficiency, re-observation,
  stopping, or owner failure: Plane A failure.
- Ambiguous attribution: unresolved candidate with both evidence and trace refs;
  never forced into a model score.

## Comparison outputs

The comparison may report how an implementation changes evidence quality,
cycles, burden, and goal completion. It cannot declare a benchmark winner to
be a preferred runtime model or infer Luna PASS from model PASS.
