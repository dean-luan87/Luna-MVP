# LUNA OCR Bridge — MidPlatform OCR 输入接口冻结 v0 (Phase-OCRBridge-Review-001)

## 冻结结论（规范级）

**MidPlatform 未来只能接收 `OcrEvidencePackV0`（`pack_version: ocr_evidence_pack_v0`），不得将无结构的 `raw_text_joined` 作为唯一 OCR 输入。**

本文件为 **接口评审冻结**，不产生 runtime 行为，不调用 MidPlatform。

---

## 写死原则（MidPlatform 侧）

1. **不接** `raw_text_joined` 作为 OCR 直通输入（不得把「整图拼接字符串」当作事实源）。
2. **不接** 无 **`source_refs`**（可追溯引用）的 OCR 文本证据。
3. **不接** 无 **quality gate**（质量门引用/结论可追溯）的 OCR 文本事实路径。
4. **不接** 无 **eligibility gate**（适用域门控可追溯）的 OCR 文本事实路径。
5. **不接** **reading order 不确定** 时的 **全局唯一事实文本**（不得把全局拼接当单一事实）。
6. **不接** 将 **symbol / glyph** 伪装成普通 **text** 事实的证据形态。
7. **可接** `forwarding_mode` 为 **`evidence_only` / `conditional_evidence`** 的包，用于高层判断，但 **不得写入事实文本层**。
8. **事实文本层** 仅允许 **`eligible_text_evidence`** 中满足 **强条件** 的项进入 **`fact_text_layer_candidates`** 所表达的候选集合（实现阶段须再经守卫，本阶段只冻结准入条件意图）。

---

## OCR Bridge 阶段边界

- **Design / Review**：仅 **design contract** 与文档冻结；**禁止**真实转发、**禁止**伪造 runtime `source_refs`。
- **Implementation**：单独阶段绑定真实 `image_frame_ref`、`trace_ref` 等（见 `LUNA_OCR_RUNTIME_SOURCE_REF_REQUIREMENTS_V0.md`）。

---

## 与 Evaluation Tools 的关系

OCR-007 产出的 routing pack 与 `eval:*` 示例 pack **仅为评审输入样例**，**不是** MidPlatform 或主线的运行时证据源。

## 治理权力边界（硬约束）

见 **`LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md`**：**MidPlatform has authority over OCR evidence interpretation**；**OCR provider has no authority to write facts**。
