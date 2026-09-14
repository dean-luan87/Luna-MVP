# Luna — CrossModal Vision OCR Reference Only (RapidOCR) v0

**Phase**：`Phase-CrossModal-Vision-OCR-Reference-Only-002`

## 目的

使用 **RapidOCR read-only consumer** 产物重建 Vision–OCR **reference-only** 对齐，替换 v001 stub `MOCK_TEXT` 路径。

## 原则

- Reference Only；`empty_text=true` 为有效 real provider 结果。
- 不重新调用 RapidOCR；不写事实层；不融合。

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_RAPIDOCR_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_REFERENCE_ONLY_RAPIDOCR_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001**（见 [LUNA_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_V0.md)）；需配合 text-bearing sample 非空 OCR。
