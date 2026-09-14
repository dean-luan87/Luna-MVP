# Luna — CrossModal Vision OCR Fusion Candidate DryRun v0

**Phase**：`Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001`

## 目的

基于 **text-bearing** Vision ROI + RapidOCR reference，生成 Vision–OCR **fusion candidate** 草案（`dry_run_only`），不确认事实、不写任何事实层。

## 原则

- Fusion candidate **不是**事实；OCR 文本与 Vision ROI bbox 均 `not_fact`。
- 不重新调用 RapidOCR / PaddleOCR / YOLO / VLM；不调用 AI interpretation / 导航。
- `cross_modal_fusion_committed=false`；仅 no-write audit。

## 输入

| 根目录 | 作用 |
|--------|------|
| `vision_roi_text_bearing_ocr_sample_smoke_v0` | 含字 reference + submission + bridge pack |
| `cross_modal_vision_ocr_reference_only_rapidocr_smoke_v0` | RapidOCR reference-only 血缘（只读） |

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001**（见 [LUNA_CROSS_MODAL_FUSION_REVIEW_QUEUE_V0.md](./LUNA_CROSS_MODAL_FUSION_REVIEW_QUEUE_V0.md)）。
