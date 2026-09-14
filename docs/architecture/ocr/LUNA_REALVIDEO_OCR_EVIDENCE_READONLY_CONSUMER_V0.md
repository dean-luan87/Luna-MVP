# Luna — RealVideo OCR Evidence ReadOnly Consumer v0

**Phase**：`Phase-RealVideo-OCR-Evidence-ReadOnly-Consumer-001`

## 目的

只读消费 RealVideo **OCRRequest Gated Submission** 产出的 OCR evidence collection，构建 candidate / frame / roi / case 四类索引视图。

## 原则

- 只读 consumption；不重新运行 OCR
- `empty_text` 是有效 OCR 结果，不是 failure，也不是 no_text_fact
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/ocr_runtime/realvideo_ocr_evidence_readonly_consumer_v0.py`
- Runner：`tools/evaluation/ocr/run_realvideo_ocr_evidence_readonly_consumer_v0.py`
- Verifier：`tools/evaluation/ocr/verify_realvideo_ocr_evidence_readonly_consumer_v0.py`

## 评测

[LUNA_EVALUATION_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](../evaluation/LUNA_EVALUATION_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md)

## 建议下一跳

**Phase-RealVideo-OCR-Reference-Update-001** — 见 [LUNA_REALVIDEO_OCR_REFERENCE_UPDATE_V0.md](../midplatform/LUNA_REALVIDEO_OCR_REFERENCE_UPDATE_V0.md)（并列更新；仍不 fusion）。

**Phase-RealVideo-OCR-Reference-Closure-001** — 收口 reference 链。
