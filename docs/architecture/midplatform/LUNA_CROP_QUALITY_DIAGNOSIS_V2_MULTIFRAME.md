# Luna — Crop Quality Diagnosis v2 Multiframe

**Phase**：`Crop-Quality-Diagnosis-v2-Multiframe-001`

## 目的

对 30 个 multiframe projection crop 与 30 个 empty OCR EP v4 做**输入侧质量诊断**（几何、bbox 类型、帧偏移、亮度/模糊、投影漂移、视觉存在性），输出 **hypothesis**（非 confirmed root cause）。

## 边界

- 不运行 OCR；不生成新 crop；不生成 EP / Semantic / SV rerun
- `empty OCR` 不是 no-text fact；`root_cause_confirmed=false`
- same-frame blocker 仍 active

## 实现

- `capabilities/midplatform/crop_quality_diagnosis_v2_multiframe.py`
- `tools/evaluation/midplatform/run_crop_quality_diagnosis_v2_multiframe.py`
- `tools/evaluation/midplatform/verify_crop_quality_diagnosis_v2_multiframe.py`

## 前置

- [LUNA_EVIDENCE_PACK_ADAPTER_V4_MULTIFRAME.md](./LUNA_EVIDENCE_PACK_ADAPTER_V4_MULTIFRAME.md)

## 评测

[LUNA_EVALUATION_CROP_QUALITY_DIAGNOSIS_V2_MULTIFRAME.md](../evaluation/LUNA_EVALUATION_CROP_QUALITY_DIAGNOSIS_V2_MULTIFRAME.md)

## 建议下一 phase

- `Text-Detector-DryRun-v1`（见 [LUNA_TEXT_DETECTOR_DRYRUN_V1.md](./LUNA_TEXT_DETECTOR_DRYRUN_V1.md)）
- `BBox-Adjustment-Proposal-v2-Multiframe`
