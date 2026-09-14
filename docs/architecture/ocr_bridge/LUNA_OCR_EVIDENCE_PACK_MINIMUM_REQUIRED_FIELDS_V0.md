# LUNA OCR Bridge — OcrEvidencePackV0 最小必填字段 v0 (Phase-OCRBridge-Review-001)

## Pack 顶层（最小集合）

| 字段 | 说明 |
|------|------|
| `pack_id` | 包实例标识 |
| `pack_version` | 固定语义版本，当前为 `ocr_evidence_pack_v0` |
| `source_image_ref` | 图像/帧来源引用（设计期 `eval:*` 占位） |
| `source_provider_ref` | OCR provider 追溯 |
| `source_quality_gate_ref` | 图像质量门追溯 |
| `source_layout_ref` | 版面/ROI 治理追溯 |
| `source_eligibility_gate_ref` | 适用域门控追溯 |
| `eligible_text_evidence` | 列表（可为空） |
| `conditional_text_evidence` | 列表 |
| `symbol_evidence` | 列表 |
| `glyph_evidence` | 列表 |
| `layout_evidence` | 列表 |
| `rejected_or_uncertain_evidence` | 列表 |
| `fact_text_layer_candidates` | 事实层候选（与 reading_order / 门控一致） |
| `must_not_enter_fact_text_layer` | 显式禁止进入事实层的证据 id 或其它标识 |
| `reading_order` | 全局阅读顺序元数据 |
| `uncertainty` | 包级不确定性 |
| `midplatform_contract` | 转发/事实层意图（设计期决策字段） |
| `hard_audit` | 集成与副作用审计（须全 false / navigation null） |

## 每条 evidence（跨类型最小）

| 字段 | 说明 |
|------|------|
| `evidence_id` | 稳定 id |
| `evidence_type` | `eligible_text` \| `conditional_text` \| `symbol` \| `glyph` \| `layout` \| `rejected_or_uncertain` |
| `should_enter_fact_text_layer` | 是否允许成为事实文本层候选（多数类型恒为 false） |
| `source_refs` | 至少包含可追溯的 `source_image_ref` / `provider_ref` / `quality_gate_ref` / `routing_ref` 等（实现阶段扩展） |

类型特有字段（如 `text`、`symbol_type`）在 `LUNA_OCR_EVIDENCE_TYPES_V0.md` 中定义；**本冻结文件只锁「最小交集」**。
