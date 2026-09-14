# Luna — RealVideo OCR Reference Update v0

**Phase**：`Phase-RealVideo-OCR-Reference-Update-001`

## 目的

将 RealVideo ROI-to-OCR reference、gated submission、OCR evidence readonly consumer **并列更新**为 reference-only 索引。**不重新运行 OCR**，**不 fusion**，**不写事实层**。

## 原则

- 保留原 ROI-to-OCR reference（50 ROI refs）
- 保留 OCRRequest submission refs（10）
- 加入 OCR evidence refs（10）；`empty_text` 为有效 OCR 结果，**不得**解释为 `no_text_fact`
- 40 条 rejected ROI 仅保留引用，不生成 evidence
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/midplatform/realvideo_ocr_reference_update_v0.py`
- Runner：`tools/evaluation/midplatform/run_realvideo_ocr_reference_update_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_realvideo_ocr_reference_update_v0.py`

## 评测

[LUNA_EVALUATION_REALVIDEO_OCR_REFERENCE_UPDATE_V0.md](../evaluation/LUNA_EVALUATION_REALVIDEO_OCR_REFERENCE_UPDATE_V0.md)

## 建议下一跳

**Phase-RealVideo-OCR-Reference-Closure-001** — 见 [LUNA_REALVIDEO_OCR_REFERENCE_CLOSURE_V0.md](./LUNA_REALVIDEO_OCR_REFERENCE_CLOSURE_V0.md)。

**Phase-RealVideo-OCR-Text-Bearing-Sample-Planning-001** — 含字真实视频/帧样本测试计划（closure 后优先）。
