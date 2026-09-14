# LUNA OCR Bridge — Fact Text Layer 准入策略 v0 (Phase-OCRBridge-Review-001)

## 总原则

- **仅** `eligible_text_evidence` 中的项，在满足下列 **全部** 强条件时，方可进入 **`fact_text_layer_candidates`**（表达「可成为事实文本的候选」，实现阶段仍须最终守卫）。
- **non-OCR 域**、**symbol**、**glyph**、**layout**、**conditional**、**rejected** 均 **不得** 以事实文本层唯一真值写入；**不得** 将 symbol/glyph 伪装为普通 text 事实。

---

## 强条件清单（eligible → fact 候选）

1. **适用域**：`source_refs.eval_content_type`（或实现期等价字段）表明属于 **OCR 合理输入域**（非 non-OCR taxonomy）。
2. **质量门**：`quality_gate` 为 **`GO`**（或经评审明确写进实现规范的窄化 `CONDITIONAL_GO` 规则）；**禁止** `NO_GO`。
3. **适用域门控**：存在可追溯的 **`source_eligibility_gate_ref` / 条目级 eligibility 引用**。
4. **阅读顺序**：`reading_order.reading_order_uncertain == false` 且 `global_reading_order_available == true`，且置信度达到实现阈值。
5. **失真**：无校验器定义的 distortion violation（与 OCR-007 / Bridge validator 对齐）。
6. **`should_enter_fact_text_layer`**：条目级为 **true** 且与上述一致。

---

## 显式禁止

- `reading_order_uncertain == true` 时 **`fact_text_layer_candidates` 必须为空**（设计期默认与保守实现一致）。
- **multi-panel**：不得跨 panel 拼接为 **单一全局事实字符串** 进入事实层；仅允许在 `layout_evidence` 的 **组内** 字段表达组级文本（仍非 MidPlatform 全局 raw 直通）。
