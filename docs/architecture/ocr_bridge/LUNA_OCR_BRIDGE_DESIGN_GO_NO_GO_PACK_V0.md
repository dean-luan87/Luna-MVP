# LUNA OCR Bridge — Design Go/No-Go Pack v0 (Phase-OCRBridge-Design-001)

## GO

- `OcrEvidencePackV0` 合同骨架、证据类型、转发规则、校验器均已落地。
- 可从 OCR-007 产物生成 **design-only** `ocr_evidence_pack_example.json`。
- `verify_ocr_evidence_pack_contract_v0.py` verdict **GO**（在未被篡改的 eval 输出上）。
- `hard_audit` 清洁：`midplatform_invoked`、`scene_delta_invoked`、`world_context_invoked`、`runtime_integration` 等为 false。

## CONDITIONAL_GO

- 顶层与条目 `source_*_ref` 使用 **`eval:*` 占位**，主线实现需替换为真实 trace/ref。
- 默认 `reading_order_uncertain=true`，`fact_text_layer_candidates` 常为空 → 转发多为 `conditional_evidence`（预期保守）。

## NO_GO

- 将 `raw_text_joined` 作为 MidPlatform 唯一输入写入合同或文档。
- non-OCR / symbol/glyph 进入事实文本层或可写 raw 事实层。
- 工具链调用 MidPlatform / SceneDelta / WorldContext 或修改 OCR routing / 接 runtime。
