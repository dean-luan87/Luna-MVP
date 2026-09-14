# Luna — RealVideo OCR Reference Closure v0

**Phase**：`Phase-RealVideo-OCR-Reference-Closure-001`

## 目的

对 RealVideo OCR reference 链做 **closure**：聚合并验证 case registry → frame sample → ROI reference → gated submission → readonly consumer → reference update 的完整 lineage。**不新增能力**，**不重新 OCR**，**不 fusion**。

## 状态

- `realvideo_ocr_reference_status=closed_for_reference_evaluation`
- 非 fusion-ready / write-ready
- 全部 `fact_status=not_fact`；`write_allowed=false`

## 实现

- Capability：`capabilities/midplatform/realvideo_ocr_reference_closure_v0.py`
- Runner：`tools/evaluation/midplatform/run_realvideo_ocr_reference_closure_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_realvideo_ocr_reference_closure_v0.py`

## 评测

[LUNA_EVALUATION_REALVIDEO_OCR_REFERENCE_CLOSURE_V0.md](../evaluation/LUNA_EVALUATION_REALVIDEO_OCR_REFERENCE_CLOSURE_V0.md)

## 建议下一跳

**Phase-RealVideo-OCR-Text-Bearing-Sample-Planning-001** — 见 [LUNA_REALVIDEO_OCR_TEXT_BEARING_SAMPLE_PLANNING_V0.md](./LUNA_REALVIDEO_OCR_TEXT_BEARING_SAMPLE_PLANNING_V0.md)。

**Phase-RealVideo-Text-Bearing-FrameSample-Smoke-001** — 需先具备含字视频或 fixture。
