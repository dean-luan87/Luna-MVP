# Luna — ROI BBox Expansion Proposal v1

**Phase**：`Phase-ROI-BBox-Expansion-Proposal-v1-001`

## 目的

基于 ROI Crop Diversity Check 与质量诊断结果，为单一低多样性 source bbox 生成多档 expansion proposal（small / medium / line_region / contextual），供下一轮 crop dry-run 使用。

## 边界

- Expansion proposal ≠ crop artifact ≠ OCR evidence ≠ 事实
- 原 bbox 必须保留；expansion 仅候选，不代表更好 ROI
- 不运行 OCR、不生成新 crop、不写事实层

## 实现

- `capabilities/midplatform/roi_bbox_expansion_proposal_v1.py`
- `tools/evaluation/midplatform/run_roi_bbox_expansion_proposal_v1.py`
- `tools/evaluation/midplatform/verify_roi_bbox_expansion_proposal_v1.py`

## 前置

- [LUNA_ROI_CROP_DIVERSITY_CHECK_V1.md](./LUNA_ROI_CROP_DIVERSITY_CHECK_V1.md)（已完成 smoke）

## 评测

[LUNA_EVALUATION_ROI_BBOX_EXPANSION_PROPOSAL_V1.md](../evaluation/LUNA_EVALUATION_ROI_BBOX_EXPANSION_PROPOSAL_V1.md)

## 建议下一 phase

- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V2_BBOX_EXPANSION.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V2_BBOX_EXPANSION.md)（已完成 smoke：4 expanded crops）
- `ROI-to-OCRRequest-Reference-v2-BBoxExpansion`
