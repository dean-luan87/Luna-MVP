# Luna — ROI OCR Quality Diagnosis v1

**Phase**：`Phase-ROI-OCR-Quality-Diagnosis-v1-001`

## 目的

诊断 12 条 ROI OCR 全部为低信息重复文本「行」的原因，输出 hypothesis-only 质量诊断与修复路线；不运行 OCR、不生成新 crop、不写事实。

## 边界

- 诊断 ≠ Source Validation ≠ 事实；`root_cause_confirmed=false`
- 不声称 provider 失败；non_empty ≠ accuracy

## 实现

- `capabilities/midplatform/roi_ocr_quality_diagnosis_v1.py`
- `tools/evaluation/midplatform/run_roi_ocr_quality_diagnosis_v1.py`
- `tools/evaluation/midplatform/verify_roi_ocr_quality_diagnosis_v1.py`

## 前置

- [LUNA_SEMANTIC_CANDIDATE_V2_ROIAWARE.md](./LUNA_SEMANTIC_CANDIDATE_V2_ROIAWARE.md)

## 评测

[LUNA_EVALUATION_ROI_OCR_QUALITY_DIAGNOSIS_V1.md](../evaluation/LUNA_EVALUATION_ROI_OCR_QUALITY_DIAGNOSIS_V1.md)

## 建议下一 phase

- [LUNA_ROI_CROP_DIVERSITY_CHECK_V1.md](./LUNA_ROI_CROP_DIVERSITY_CHECK_V1.md)（已完成 smoke：`crop_diversity_low=true`）
- `ROI-BBox-Expansion-Proposal-v1`
- `Multiframe-Merge-Proposal-v1`
