# Asset Audit

## Phase

`Phase-P1-Luna-Model-Test-Dataset-Registry-Foundation-Asset-Audit-v1-001`

Canonical root: `/Users/luanlei/Desktop/Luna-Core`

This audit is static and read-only with respect to runtime, models, datasets,
network access, and evaluation execution.

## Scope and classification

Classification used in this audit:

- **A — canonical / reuse directly**: an existing contract or protected boundary.
- **B — canonical / extend**: an existing contract with a bounded gap.
- **C — useful precedent only**: informative but too narrow or planning-only.
- **D — generated evaluation artifact**: evidence of a run, never registry source-of-truth.
- **E — obsolete/conflicting**: historical or incompatible for the target foundation.

## Relevant assets

| Asset | Classification | Finding |
|---|---|---|
| `capabilities/evaluation/ocr/ocr_dataset_registry_v0.py` | C/B | The only explicit dataset registry; OCR-specific and evaluation-only. Reuse its source, GT-quality, lifecycle, and runtime-boundary conventions, not its schema as a universal registry. |
| `capabilities/evaluation/ocr/ocr_realworld_sample_registry_v0.py` | C/B | Strong sample/provenance/GT precedent; domain-specific. |
| `capabilities/midplatform/model_test_lens/schemas/model_test_case_manifest_schema_v1.json` | A/B | Reusable test-case manifest with `input_asset_refs`, model refs, source roots, and candidate-only boundary. Extend later with dataset/sample refs rather than creating a parallel case schema. |
| `capabilities/midplatform/model_test_lens/schemas/local_asset_import/local_test_asset_manifest_schema_v1.json` | A/C | Reusable local media-reference and safety boundary; it is an import manifest, not a durable dataset declaration. |
| `capabilities/midplatform/model_test_lens/schemas/model_test_result_envelope_schema_v1.json` | A | Reusable result/evidence envelope boundary; generated results remain evidence. |
| `capabilities/midplatform/model_test_lens/schemas/model_test_trace_schema_v1.json` | A | Reusable test trace and execution-flag contract. |
| `capabilities/midplatform/model_test_lens/human_correction/human_correction_types_v1.py` | A/C | Reusable correction provenance and review-state precedent; corrections do not become GT automatically. |
| `capabilities/evaluation/common/evaluation_report_schema_v0.py` | A/C | Generic evaluation report reference and metric/failure structure; not a dataset registry. |
| `capabilities/midplatform/model_manager/lifecycle/model_benchmark_record_schema_v1.json` | A/C | Model benchmark result record; candidate-only and not a benchmark/dataset catalog. |
| `capabilities/midplatform/model_manager/schemas/model_evaluation_profile_schema_v1.json` | C | Model evaluation profile, not dataset ownership. |
| `capabilities/midplatform/model_manager/registries/model_registry_v1.json` | A | Canonical model identity/version/declaration registry. Dataset records must reference it. |
| `capabilities/midplatform/model_manager/registries/capability_registry_v1.json` | A | Canonical capability and slot registry. Dataset task/capability refs must reference it. |
| `capabilities/midplatform/model_manager/registry/provider_registry_v1.json` | A | Canonical provider identity/binding registry. Dataset evaluation metadata may reference provider/model runs. |
| `capabilities/midplatform/model_manager/model_contract_repository/` | A | Canonical model contract/version/dependency/deployment references; must not be duplicated by dataset records. |
| `capabilities/test_board/test_board_protocol_v1.py` | A | Durable protected test evidence boundary. TestBoard records runs and artifacts; it is not dataset source-of-truth. |
| `docs/architecture/evaluation/` | A/C | Existing offline evaluation boundary: dataset manifests, GT, reports, failure bundles, and human review are allowed; runtime/mainline mutation is forbidden. |
| `capabilities/midplatform/cross_modal_vision_ocr_realvideo_case_registry_v0.py` | C | Useful media/case/provenance precedent; not a generic registry. |
| `capabilities/field_understanding/rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun/` | C | Useful license/source-chain/annotation admission precedent; dry-run evidence only. |
| `capabilities/test_assets/model_test_lens/` and `capabilities/test_assets/p1/` | C/D | Reusable local test inputs after explicit registration; current files are not a durable dataset registry. |
| `_tmp_eval_inputs/roboflow_real_exit_v1/` | C/D | User-provided input for the RF-DETR smoke; must remain an input/evidence asset until explicitly registered. |
| `_tmp_eval_out/` and `_eval_out/` | D | Generated run outputs, summaries, raw/normalized artifacts, and review evidence. Never canonical dataset or GT source. |
| `datasets/voice_output_governance_samples_v0/` | C | Dataset-like precedent for another domain; does not provide a perception registry. |
| `docs/architecture/roboflow_external_perception_provider_integration_asset_audit_v1.md` | E/C | Historical Roboflow audit. Reuse boundary principles, but supersede its older RF-DETR-missing claims with current declarations. |

## Existing answer by asset class

There is no generic cross-modal dataset registry, no generic benchmark
registry, and no one reusable ground-truth schema covering detection,
segmentation, OCR, depth, SLAM, audio, and multimodal observations.

There are reusable pieces: local media references, test-case manifests,
evaluation reports, TestBoard artifacts, OCR GT/sample schemas, human review
records, and model/capability/provider identity registries.

The repository therefore has enough precedent to extend the existing
evaluation boundary without creating a second model/provider/capability
system, but not enough to register long-lived datasets consistently.
