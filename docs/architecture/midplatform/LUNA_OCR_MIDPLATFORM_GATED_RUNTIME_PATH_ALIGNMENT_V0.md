# Luna — OCR MidPlatform Gated Runtime Path Alignment v0

**Phase**：`Phase-OCR-MidPlatform-Gated-Runtime-Path-Alignment-001`

## 问题

此前 mixed video/poster smoke 路径为：**OpenCV → 直接 RapidOCR → 事后组装 Pack/Gate 报告**。治理未在 provider 调用前生效。

## 目标路径

```
Frame / Image Input
→ InputCandidate
→ Source Quality Gate (SQ_A–E)
→ Readability Gate
→ ROI Crop / Scan Observation
→ OCRRequest Candidate
→ OCRRequest Gated Submission (ocr_mainline_bridge)
→ Provider
→ OCRTextEvidencePack (含 ocr_request_ref)
→ SemanticCandidate
```

**禁止**：`Frame → Direct RapidOCR → 事后补 gate`

## 边界

- 不追求 OCR 准确率；验证 **provider 调用发生在 gate 之后**
- 全帧 OCR 仅 **scan_observation**，不得作为主 Evidence Pack
- 不写 fact / WorldModel / Scene Delta；不改 routing

## 实现

- `capabilities/midplatform/ocr_midplatform_gated_runtime_path_alignment_v0.py`
- `tools/evaluation/midplatform/run_ocr_midplatform_gated_runtime_path_alignment_v0.py`
- `tools/evaluation/midplatform/verify_ocr_midplatform_gated_runtime_path_alignment_v0.py`

## 评测

[LUNA_EVALUATION_OCR_MIDPLATFORM_GATED_RUNTIME_PATH_ALIGNMENT_V0.md](../evaluation/LUNA_EVALUATION_OCR_MIDPLATFORM_GATED_RUNTIME_PATH_ALIGNMENT_V0.md)
