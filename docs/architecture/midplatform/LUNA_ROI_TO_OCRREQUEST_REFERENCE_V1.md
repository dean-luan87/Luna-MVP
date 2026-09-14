# Luna — ROI to OCRRequest Reference v1

**Phase**：`Phase-ROI-to-OCRRequest-Reference-v1-001`

## 目的

将 ROI Crop Rerun 产出的 **generated crop PNG**（smoke：12）转为标准 **OCRRequest reference / candidate**，为 `OCRRequest-Gated-Submission-from-ROI-v1` 准备输入。

## 核心原则

1. OCRRequest reference ≠ OCRRequest submission ≠ OCR evidence ≠ 事实
2. 仅消费 `crop_generation_status=generated` 且 `crop_file_path` 存在的 crop artifact
3. `metadata_only` / `deferred` 不进入 reference，仅写入 excluded report
4. 每条 reference 绑定 `crop_artifact_ref`、`source_chain` 与 gate metadata

## 边界（禁止）

- 不运行 OCR；不调用 RapidOCR / PaddleOCR / `ocr_mainline_bridge`
- 不提交 OCRRequest；不调用 Vision provider
- 不生成 Evidence Pack / Semantic Candidate
- 不写 MidPlatform fact / WorldModel；不做导航；不改 runtime routing

## 实现

- `capabilities/midplatform/roi_to_ocrrequest_reference_v1.py`
- `tools/evaluation/midplatform/run_roi_to_ocrrequest_reference_v1.py`
- `tools/evaluation/midplatform/verify_roi_to_ocrrequest_reference_v1.py`

## 前置

- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V1_RERUN_BETTER_FRAMES.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V1_RERUN_BETTER_FRAMES.md)
- [LUNA_BETTER_FRAME_SELECTION_RUNTIME_V1.md](./LUNA_BETTER_FRAME_SELECTION_RUNTIME_V1.md)

## 评测

[LUNA_EVALUATION_ROI_TO_OCRREQUEST_REFERENCE_V1.md](../evaluation/LUNA_EVALUATION_ROI_TO_OCRREQUEST_REFERENCE_V1.md)

## 建议下一 phase

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V1.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V1.md)（已完成 smoke：12 gated submission）
- `Evidence-Pack-Adapter-v2-ROIRef`
