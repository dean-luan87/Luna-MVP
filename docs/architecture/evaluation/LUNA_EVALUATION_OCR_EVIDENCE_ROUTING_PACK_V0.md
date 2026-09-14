# LUNA Evaluation Tools — OCR Evidence Routing Pack Schema v0 (Phase-EvaluationTools-OCR-007)

## 文件

- 主产物：`ocr_evidence_routing_pack.json`（由 `build_ocr_evidence_routing_pack_v0` 生成）。

## 顶层字段

| 字段 | 说明 |
|------|------|
| `routing_pack_id` | 本次 routing pack 标识 |
| `source_eval_root` | 来源 OCR-006 `boundary_eval_root` |
| `gate_version` | 固定为 `ocr_eligibility_gate_simulator_v0` |
| `eligible_text_evidence` | 可进入事实文本层的候选证据（仿真） |
| `conditional_text_evidence` | 条件域证据，**不得**直接作为唯一全局事实文本 |
| `symbol_evidence` / `glyph_evidence` / `layout_evidence` | 非纯事实文本分支 |
| `rejected_or_uncertain_evidence` | 拒识或需人工 |
| `summary` | 各类计数 |
| `runtime_integration` / `whitebox_integration` / `mainline_side_effect` | 必须为 `false` |

## 单条 evidence（概念）

每条含：`case_id`、`content_type`、`original_expected_route`、`ocr_raw_text`、`evidence_route`、`should_enter_fact_text_layer`、`uncertainty`、`source_metrics`（CER、中文 recall、garbled、空输出、图像质量门）。

## `icon_text_mix`

决策层可使用内部路由标签 `symbol_and_layout`；写入 pack 时拆为 **两条** 记录，分别进入 `symbol_evidence` 与 `layout_evidence`（同一 `case_id`）。
