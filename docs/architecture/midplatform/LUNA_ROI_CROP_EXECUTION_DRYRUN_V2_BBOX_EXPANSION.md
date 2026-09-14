# Luna — ROI Crop Execution DryRun v2 BBoxExpansion

**Phase**：`Phase-ROI-Crop-Execution-DryRun-v2-BBoxExpansion-001`

## 目的

消费 ROI BBox Expansion Proposal v1 的 4 个 expansion candidates，在已知帧 `f001620` 上 materialize 图像并生成 expanded ROI crop artifacts；不运行 OCR。

## 边界

- Expanded crop ≠ OCR evidence ≠ 事实
- 仅 `materialize_existing_scan_frame_index_only`；`new_frame_extracted=false`
- 保留 source_bbox、expanded_bbox、expansion_candidate_ref

## 实现

- `capabilities/midplatform/roi_crop_execution_dryrun_v2_bbox_expansion.py`
- `tools/evaluation/midplatform/run_roi_crop_execution_dryrun_v2_bbox_expansion.py`
- `tools/evaluation/midplatform/verify_roi_crop_execution_dryrun_v2_bbox_expansion.py`

## 前置

- [LUNA_ROI_BBOX_EXPANSION_PROPOSAL_V1.md](./LUNA_ROI_BBOX_EXPANSION_PROPOSAL_V1.md)（已完成 smoke）

## 评测

[LUNA_EVALUATION_ROI_CROP_EXECUTION_DRYRUN_V2_BBOX_EXPANSION.md](../evaluation/LUNA_EVALUATION_ROI_CROP_EXECUTION_DRYRUN_V2_BBOX_EXPANSION.md)

## 建议下一 phase

- [LUNA_ROI_TO_OCRREQUEST_REFERENCE_V2_BBOX_EXPANSION.md](./LUNA_ROI_TO_OCRREQUEST_REFERENCE_V2_BBOX_EXPANSION.md)（已完成 smoke：4 reference v2）
- `OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion`
