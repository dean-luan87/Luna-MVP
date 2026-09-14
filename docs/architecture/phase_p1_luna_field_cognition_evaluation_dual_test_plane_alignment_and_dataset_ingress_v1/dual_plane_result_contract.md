# Dual-plane Result Contract

Each future Cognitive Test Case has separate results:

- **Plane A**: Luna Cognitive Evaluation Result — process, cognition,
  sufficiency, gap, re-observation, stopping, and goal-completion candidate.
- **Plane B**: External Capability Fitness Observation — evidence usefulness,
  stability, uncertainty, latency/resource signals, and provider/normalization
  behavior.

Overall attribution is one of:

`LUNA_COGNITIVE`, `EXTERNAL_CAPABILITY`, `PROVIDER`, `NORMALIZATION`,
`DATASET_OR_GT`, `EVALUATION_INFRASTRUCTURE`, `UNRESOLVED`.

Attribution must link evidence and trace refs. Results are never collapsed into
a single model score and never mutate runtime policy.
