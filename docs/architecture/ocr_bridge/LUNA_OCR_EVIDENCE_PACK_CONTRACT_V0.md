# LUNA OCR Bridge — OcrEvidencePack Contract v0 (Phase-OCRBridge-Design-001)

## 定位

定义未来 **OCR → MidPlatform** 侧应消费的 **`OcrEvidencePackV0`** JSON 合同（`pack_version: ocr_evidence_pack_v0`）。本阶段 **不接线**、不调用 MidPlatform、不写 runtime。

## 核心原则（合同层）

1. MidPlatform **不得**直接接收无结构的 `raw_text_joined` 作为唯一输入；仅允许 **结构化 `OcrEvidencePack`**（及未来与之对齐的序列化边界）。
2. OCR 层输出 **证据（evidence）**，不输出事实结论。
3. `fact_text_layer_candidates` 与 `must_not_enter_fact_text_layer` 显式分流；non-OCR 域不得标记为可进事实文本层。
4. 顶层 `source_*_ref` 与每条 evidence 的 `source_refs` 必须可追踪（设计期可用 `eval:*` 占位）。

## 每条 evidence 最小字段（Review-001 冻结）

与 `LUNA_OCR_EVIDENCE_PACK_MINIMUM_REQUIRED_FIELDS_V0.md` 对齐：`evidence_id`、`evidence_type`、`should_enter_fact_text_layer`、`source_refs`。

## 实现入口

- 合同骨架与 eval 映射：`capabilities/ocr_bridge/ocr_evidence_pack_contract_v0.py`
- 静态校验：`capabilities/ocr_bridge/ocr_evidence_pack_validator_v0.py`
- 设计示例生成：`tools/ocr_bridge/build_ocr_evidence_pack_from_eval_v0.py`

## `hard_audit`

所有集成类标志必须为 **false** / **null**（见 schema：`midplatform_invoked`、`scene_delta_invoked`、`world_context_invoked` 等）。
