# Luna — MixedVideo OCR Scan LineBox Trace + Source Quality Gate v0

**Phase**：`Phase-MixedVideo-OCR-Scan-LineBox-Trace-SourceQualityGate-001`

## 架构原则

OCR 失败/误识别不只来自 provider，也来自 **输入源质量**。视角差、遮挡、运动模糊、压缩噪声、多招牌全帧混杂时，不应与高质量 ROI OCR **同权**进入 OCR evidence。

**先判断输入值不值得 OCR，再决定如何 OCR。**

## 目的

1. 将视频 scan 从 `ocr_preview` 字符串升级为 **line-level `text_items[]`**（`bbox_xyxy` / `confidence` / `line_index` / `frame timestamp` / `source_chain`）。
2. 建立 **OCR Source Quality Gate**（SQ_A–E），低质量输入不得与高质量输入同权进入 evidence。
3. 输出 **scan vs pack consistency**、全帧 OCR 风险、ROI crop 要求、scan observation vs evidence 政策。

## 边界

- **允许**：读取 mixed batch 产物；P0 轻量重扫；质量评分 / gate / eligibility matrix；trace / consistency 报告。
- **禁止**：MidPlatform fact、Scene Delta、WorldModel attach、导航、自动批准、改 routing、benchmark/provider 比较、把 scan 当事实。

## 实现

- Capability：`capabilities/midplatform/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0.py`
- Runner：`tools/evaluation/midplatform/run_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0.py`

## 技术说明

- P0 入选帧 OCR 使用 **顺序解码**（`CAP_PROP_POS_FRAMES` 在部分 codec 上不可靠）。
- `ocr_preview` 仅作 **display_text**；主 evidence 需 linebox + ROI OCR。
- `source_quality_grade` 为启发式，非最终质量分。

## 评测

[LUNA_EVALUATION_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_V0.md](../evaluation/LUNA_EVALUATION_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_V0.md)

## 建议下一跳

**OCR MidPlatform Gated Runtime Path Alignment**（见 [LUNA_OCR_MIDPLATFORM_GATED_RUNTIME_PATH_ALIGNMENT_V0.md](./LUNA_OCR_MIDPLATFORM_GATED_RUNTIME_PATH_ALIGNMENT_V0.md)）— SQ/readability gate 前置于 provider 调用。
