# LUNA Evaluation Tools — OCR False Text Risk After Gate v0 (Phase-EvaluationTools-OCR-007)

## 报告文件

- `ocr_false_text_risk_after_gate_report.json`

## 语义

- **`false_text_risk_before`**：来自 OCR-006 `ocr_false_text_risk_report.json` 的 `false_text_risk_rate`（若缺失则为 `null`）。
- **`false_text_risk_after`**：仿真门控后，**non-OCR 域**样本中仍落入 `eligible_text_evidence` 的比例（evaluation proxy）。
- **`non_ocr_entered_eligible_text_count`**：必须为 **0** 方可视为本阶段失真防控目标达成（与 verifier 对齐）。

## 说明

本指标描述的是 **「评测离线门控是否阻断 non-OCR → 事实文本层」**，不是线上 OCR 引擎的真实误报率。
