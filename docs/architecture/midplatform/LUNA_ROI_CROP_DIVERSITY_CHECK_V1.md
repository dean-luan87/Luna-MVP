# Luna — ROI Crop Diversity Check v1

**Phase**：`Phase-ROI-Crop-Diversity-Check-v1-001`

## 目的

独立检查 12 条 ROI crop/OCR/semantic 链路的 bbox、frame、linebox、dimension、proposal 映射多样性；固化重复度与 reuse risk，为后续 BBox Expansion / Multiframe / Better Frame Extraction 提供依据。

## 边界

- Diversity check ≠ 事实判断；`fact_status=not_fact`；`write_allowed=false`
- Diversity score ≠ OCR accuracy；low diversity ≠ provider failure
- 不确认唯一 root cause；`root_cause_confirmed=false`
- 不运行 OCR、不生成新 crop、不抽取新帧、不写事实层

## 实现

- `capabilities/midplatform/roi_crop_diversity_check_v1.py`
- `tools/evaluation/midplatform/run_roi_crop_diversity_check_v1.py`
- `tools/evaluation/midplatform/verify_roi_crop_diversity_check_v1.py`

## 前置

- [LUNA_ROI_OCR_QUALITY_DIAGNOSIS_V1.md](./LUNA_ROI_OCR_QUALITY_DIAGNOSIS_V1.md)（已完成 smoke）

## 评测

[LUNA_EVALUATION_ROI_CROP_DIVERSITY_CHECK_V1.md](../evaluation/LUNA_EVALUATION_ROI_CROP_DIVERSITY_CHECK_V1.md)

## 建议下一 phase

- [LUNA_ROI_BBOX_EXPANSION_PROPOSAL_V1.md](./LUNA_ROI_BBOX_EXPANSION_PROPOSAL_V1.md)（已完成 smoke：4 expansion candidates）
- `ROI-Crop-Execution-DryRun-v2-BBoxExpansion`
- `Multiframe-Merge-Proposal-v1`
