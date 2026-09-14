# Existing Asset Reuse Matrix

| Asset | Status | Owner / source of truth | Reuse or extension decision |
|---|---|---|---|
| `model_test_case_manifest_schema_v1.json` | Existing | Model Test Lens | Reuse for case identity and inputs; extend with dataset/sample/condition refs. |
| `model_test_result_envelope_schema_v1.json` | Existing | Model Test Lens | Reuse for candidate outputs, metrics, failure modes, and boundary flags. |
| `model_test_trace_schema_v1.json` | Existing | Model Test Lens | Reuse for stage trace; extend by reference to cognitive-cycle nodes. |
| `evaluation_report_schema_v0.py` | Existing | Evaluation Tools | Reuse for evaluation reports; add profile refs rather than a second report hierarchy. |
| `model_benchmark_record_schema_v1.json` | Existing | Model Governance evaluation surface | Reuse for model-scoped benchmark results; not dataset authority. |
| Model Test Lens | Existing | Model Test Lens | Read-only consumer/visualizer of evaluation artifacts; no UI work here. |
| TestBoard protocol | Existing | Test Governance | Reuse protected durable evidence requirement for every future run. |
| Human Correction Layer | Existing | Evaluation/review boundary | Reuse correction provenance; no automatic GT promotion. |
| Observation Demand/Request and Capability Requirement | Existing | FPO / Capability Governance | Reuse in execution traces; do not duplicate request types. |
| `EvidenceSufficiencyCandidateV1` / `NextCycleIngressCandidateV1` | Existing | A/FPO candidate boundary | Reuse for cognitive transitions and re-observation candidates. |
| Current World / Hypothesis candidates | Existing | Cognitive State Formation / A | Reuse candidate refs; never treat evaluation output as World Truth. |
| Model/Capability/Provider registries and bindings | Existing | respective canonical owners | Reference only. |
| RF-DETR Roboflow PoC | Existing | Provider/FPO integration | Use as first real provider evidence precedent, not as dataset source. |
| OCR Dataset Registry v0 | Existing | Evaluation/OCR | Domain precedent; extend conceptually, do not promote unchanged. |
| MUEP | Existing | Model Test Lens | Reuse metric layers; add object-detection vocabulary in a later bounded phase. |
| Cognitive trace / FPO trace replay | Partial | FPO / evaluation boundary | Reuse deterministic trace refs; no direct substitution for a unified profile. |
| Unified Execution Profile | Missing | Evaluation subsystem | New planning contract required; should reference existing records. |
| Cognitive Burden metrics | Missing | Evaluation subsystem | New derived evaluation metrics, not runtime policy. |
| Generic failure/gap taxonomy | Partial | MUEP + evaluation docs | Extend with Luna handoff/cognition categories. |
| Generic dataset registry | Missing | Evaluation subsystem | Planned from prior phase; not implemented here. |

## Source-of-truth rule

Model/Capability/Provider identity remains in their registries. TestBoard owns
durable test evidence. Dataset declarations, when implemented, belong to the
evaluation boundary. `_tmp_eval_out`, `_eval_out`, and RF-DETR summaries are
run evidence only.
