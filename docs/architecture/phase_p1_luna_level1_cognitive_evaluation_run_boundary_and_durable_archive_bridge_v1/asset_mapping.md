# Asset Mapping

| Existing asset | Reuse decision | Evidence and boundary |
|---|---|---|
| `capabilities/evaluation/dataset_registry/types_v1.py` | Reuse as-is | `DatasetRegistryV1`, `DatasetSampleManifestV1`, annotation/benchmark refs; Evaluation Governance owner. |
| `capabilities/evaluation/dataset_registry/registration_v1.py` | Reuse as-is | Explicit registration only; rejects `_tmp_eval_inputs`, `_tmp_eval_out`, `_eval_out` auto-promotion. |
| `capabilities/evaluation/level1_field_cognition_suite/types_v1.py` | Reuse as-is | `Level1CognitiveTestCaseV1`, layered GT refs, assertions, failure attribution. |
| `level1_field_cognition_suite/composition_v1.py` | Reuse and wrap | Existing sample-to-case composition; this module adds registry membership validation without duplicating case semantics. |
| `a_route_cognitive_whitebox_foundation/types_v1.py` | Reuse as-is | `CognitiveWhiteBoxTraceV1`, `LunaCognitiveExecutionProfileV1`, `CognitiveFailureGapRefV1`. |
| `a_route_cognitive_whitebox_foundation/fixtures_v1.py` | Synthetic fixture only | Used only to prove attachment and validation; not real cognition evidence. |
| A-Route/FPO controlled engines | Readiness target only | Existing engines are synthetic/candidate-only or narrow provider precedents; no real general ingress is claimed. |
| `evaluation/common/evaluation_report_schema_v0.py` | Precedent/reference | Evaluation-only report, explicitly not White-box and not a durable archive. |
| Model Test Lens envelope/TestBoard | Reference surface | Candidate result visualization/protection; neither owns cognition nor archive semantics. |

No parallel Test Case, Trace, Profile, TestBoard, Dataset Manager, or cognition runtime was created.

