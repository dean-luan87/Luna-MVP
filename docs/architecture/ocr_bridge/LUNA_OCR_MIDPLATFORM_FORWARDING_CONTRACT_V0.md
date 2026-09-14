# LUNA OCR Bridge — MidPlatform Forwarding Contract v0 (Phase-OCRBridge-Design-001)

## 转发模式

| 模式 | 含义 |
|------|------|
| `blocked` | 缺关键 ref、校验失败、non-OCR 进事实层、reading_order 不确定却存在 fact candidates、symbol/glyph raw/fact 违规等 |
| `evidence_only` | 仅 symbol/glyph/layout/rejected 等非「可进事实文本」路径 |
| `conditional_evidence` | 存在条件域或无法保证全局事实拼接安全时的保守转发 |
| `eligible_text_only` | 强条件：校验通过、reading_order 可用、存在合法 `fact_text_layer_candidates` 等（设计期默认偏保守，eval 导入常为 `conditional_evidence`） |

## 实现

- `capabilities/ocr_bridge/ocr_midplatform_forwarding_contract_v0.py` 中 `decide_midplatform_forwarding_v0`。
- 决策结果示例：`ocr_midplatform_forwarding_decision_example.json`（由 build 工具写出）。

**说明**：函数仅返回 JSON 决策，**不调用** MidPlatform。
