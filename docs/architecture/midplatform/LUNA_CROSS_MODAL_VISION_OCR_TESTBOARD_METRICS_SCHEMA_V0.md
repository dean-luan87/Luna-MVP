# Luna — CrossModal Vision OCR TestBoard Metrics Schema v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001`

## 目的

建立 TestBoard 统一 **metrics schema**（定义、口径、source map、collector 契约 stub）。**不产生 benchmark 数值、不跑 OCR。**

## 指标组（A–G）

- A OCR Output · B Case Outcome · C Risk Coverage · D Boundary · E Poster Layout · F Reference/Fusion · G Performance Placeholder

## 原则

- 不替代正式 Evaluation Platform；不模型准入；不写事实层
- `ocr_empty_text_count`：按 case_type 解释，空文本不默认等于失败
- Poster 指标区分 layout governance 与 OCR 执行

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_SCHEMA_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_SCHEMA_V0.md)

## 下一跳

**Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001** — 见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_COLLECTOR_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_METRICS_COLLECTOR_V0.md)

## 建议下一跳（Collector GO 后）

**Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001**
