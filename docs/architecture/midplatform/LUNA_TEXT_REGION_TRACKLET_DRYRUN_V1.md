# Luna — Text Region Tracklet DryRun v1

**Phase**：`Phase-Text-Region-Tracklet-DryRun-v1-001`

## 目的

基于 6 个 better frame artifacts 与 multiframe region bbox，生成 **text-region tracklet candidate** dry-run：评估跨帧追踪条件（coverage / continuity / drift），**不是**真实 tracklet 或 OCR evidence。

## 边界

- 仅 `static_bbox_projection`（`projection_is_approximate=true`）；禁止 detector / text detector / OCR / crop
- same-frame blocker **不得**解除；`fact_status=not_fact`

## 实现

- `capabilities/midplatform/text_region_tracklet_dryrun_v1.py`
- `tools/evaluation/midplatform/run_text_region_tracklet_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_text_region_tracklet_dryrun_v1.py`

## 前置

- [LUNA_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md](./LUNA_BETTER_FRAME_EXTRACTION_DRYRUN_V1.md)

## 评测

[LUNA_EVALUATION_TEXT_REGION_TRACKLET_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_TEXT_REGION_TRACKLET_DRYRUN_V1.md)

## 建议下一 phase

- `OCRRequest-Gated-Submission-from-Multiframe-v1`（crop dry-run 见 [LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V1.md](./LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V1.md)）
