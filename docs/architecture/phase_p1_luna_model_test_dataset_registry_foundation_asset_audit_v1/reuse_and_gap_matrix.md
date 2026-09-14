# Reuse and Gap Matrix

| Concern | Existing asset | Decision | Gap / constraint |
|---|---|---|---|
| Dataset identity/lifecycle | OCR dataset registry v0 | Extend conceptually | Need generic modality/task/class/source/lifecycle fields. |
| Dataset sample identity | Model Test Case Manifest; OCR sample registry; local asset manifest | Reuse patterns, extend evaluation boundary | Need one cross-modal sample manifest and dataset-version link. |
| Media reference | `input_asset_refs`; local asset manifest; image/video/frame/timestamp fields | Reuse | Need normalization rules, not a second runtime media object. |
| Ground truth | OCR raw-text schemas; dry-run COCO/VOC/YOLO samples | Reuse as domain adapters | Need generic GT/annotation reference envelope with task-specific payload refs. |
| Benchmark definition | TestBoard matrix; MUEP schemas; model benchmark record | Extend | Need dataset/split/metric/reproducibility references; avoid a second result system. |
| Evaluation result | `EvaluationReportV0`; `ModelBenchmarkRecordV1`; Test Lens result envelope | Reuse directly | Ensure result points to dataset/sample/annotation versions. |
| Run trace | Model Test Trace; TestBoard protocol | Reuse directly | Preserve attempt identity and protected artifact refs. |
| Provenance | source refs, sha256, provider/model refs, TestBoard refs | Reuse directly | Need requiredness rules in future registry schema. |
| Human review | Human Correction Layer; evaluation human review docs | Reuse directly | Review/correction does not automatically become GT. |
| Object detection MUEP input | Model Test case `detection_tracking` | Extend in later phase | MUEP input enum lacks explicit object detection. |
| Provider/model declarations | Model/Capability/Provider registries and bindings | Reference only | No duplicate model/provider/capability records. |
| Long-lived storage | TestBoard durable evidence | Reuse for run evidence | TestBoard is not dataset registry or data lake. |
| Current Roboflow image | `_tmp_eval_inputs/roboflow_real_exit_v1` | Evidence/input only | Requires explicit dataset registration before dataset membership. |

## Minimum implementation gap

The smallest justified next implementation is an evaluation-only registry
with four new generic declarations:

1. dataset entry;
2. sample manifest;
3. annotation/ground-truth reference;
4. benchmark specification.

Existing Model Test Case, Evaluation Report, Model Benchmark Record, Test
Result Envelope, Trace, and TestBoard records should be referenced or
minimally extended instead of duplicated.

## What is explicitly not a gap to solve now

No runtime dataset loader, data lake, downloader, annotation generator,
training pipeline, model runner, or UI is required for the foundation audit.
