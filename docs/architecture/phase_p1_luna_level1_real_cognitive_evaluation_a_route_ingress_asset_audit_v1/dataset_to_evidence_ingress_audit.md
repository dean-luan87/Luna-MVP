# Dataset to Evidence Ingress Audit

## Dataset and Case

Reusable canonical assets:

- `capabilities/evaluation/dataset_registry/types_v1.py`: registry, entry, sample, annotation/GT contracts.
- `dataset_registry/registration_v1.py`: explicit registration; rejects automatic promotion from `_tmp_eval_inputs`, `_tmp_eval_out`, and `_eval_out`.
- `capabilities/evaluation/level1_field_cognition_suite/composition_v1.py`: sample-to-case composition.
- `capabilities/evaluation/level1_cognitive_evaluation_run/run_boundary_v1.py`: membership and version/linkage validation.

Current status: evaluation-only. `registry_declaration_v1.json` contains no registered real dataset or sample. The case composer can consume a registered sample object, but no real sample-to-runtime ingress is proven.

## Input forms

| Input | Existing support | Conclusion |
|---|---|---|
| Live sensor/model/provider | Narrow raw-frame/RF-DETR precedents | Not a general case ingress. |
| Recorded evidence | Replay key/ref builders exist | Safer candidate for first bridge; cognition consumer not connected. |
| Synthetic evidence | Active observation and White-box fixtures | Supported for controlled verification only. |
| Evaluation-supplied evidence | Candidate/reference contracts exist | Must enter through Observation/Evidence owner, not semantic nodes. |

Dataset, Ground Truth, and evaluation assertions remain evaluation artifacts. They cannot be promoted to Luna World Truth.

