# Luna — Multiframe Crop Execution DryRun v1

**Phase**：`Phase-Multiframe-Crop-Execution-DryRun-v1-001`

## 目的

基于 Text Region Tracklet 的 **30 条 projected regions**，在 6 个 neighbor frame artifacts 上生成 **multiframe crop PNG** 与 metadata；**不**运行 OCR / OCRRequest / EP / Semantic / SV rerun。

## 边界

- `projection_is_approximate=true`；`detected_region=false`
- multiframe crop **不是** OCR evidence；**不是** detected text region
- `same_frame_blocker` **不得**解除；`fact_status=not_fact`

## 实现

- `capabilities/midplatform/multiframe_crop_execution_dryrun_v1.py`
- `tools/evaluation/midplatform/run_multiframe_crop_execution_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_multiframe_crop_execution_dryrun_v1.py`

## 前置

- [LUNA_TEXT_REGION_TRACKLET_DRYRUN_V1.md](./LUNA_TEXT_REGION_TRACKLET_DRYRUN_V1.md)
- [LUNA_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md](./LUNA_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md)

## 评测

[LUNA_EVALUATION_MULTIFRAME_CROP_EXECUTION_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_MULTIFRAME_CROP_EXECUTION_DRYRUN_V1.md)

## 建议下一 phase

- `Evidence-Pack-Adapter-v4-Multiframe`（OCR gated submission 见 [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md)）
