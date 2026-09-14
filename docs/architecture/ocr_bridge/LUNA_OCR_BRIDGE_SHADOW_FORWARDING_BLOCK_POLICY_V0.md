# LUNA OCR Bridge — Shadow Forwarding Block Policy v0

## 原则

Phase-OCRBridge-Implementation-001 **只证明** pack 结构与审计字段可运行；**不**执行 MidPlatform 转发。

## 强制字段（shadow 运行产物）

- `midplatform_forwarding_enabled`: **false**  
- `fact_text_layer_enabled`: **false**  
- `runtime_side_effect`: **false**

## 与 `ocr_evidence_pack_shadow_forwarding_block_report.json` 的关系

该报告记录 **本 phase 强制阻断** 的理由与 `missing_source_refs`（若有），与 `decide_midplatform_forwarding_v0` 的设计态结论 **独立**：即使校验通过，本 phase 仍 **不重写为可转发**。

## raw_text_joined

`layout_evidence` 等桶中的 `group_raw_text_joined` **仅**作证据组内展示字段；**不得**作为 MidPlatform 唯一输入（见 Review-001 冻结文档）。
