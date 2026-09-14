# LUNA Evaluation Tools — OCR Eligibility Gate Simulator v0 (Phase-EvaluationTools-OCR-007)

## 定位

在 **Evaluation Tools / OCR Test Harness** 内，对 OCR-006 边界评测产物做 **离线门控仿真**：不重跑 OCR、不调用 provider、不写入 runtime/whitebox/主线路由。

## 实现入口

- 能力模块：`capabilities/evaluation/ocr/ocr_eligibility_gate_simulator_v0.py`
- CLI：`tools/evaluation/ocr/simulate_ocr_eligibility_gate_v0.py`
- Verifier：`tools/evaluation/ocr/verify_ocr_eligibility_gate_sim_v0.py`

## 输入

- `boundary_eval_root`：OCR-006 评测输出目录（含 `ocr_capability_boundary_map.json`、`ocr_capability_boundary_sample_matrix.json` 等）。
- `dataset_root`：OCR-006 数据集根目录（用于 manifest 可读性校验；仿真路由主要依赖 sample matrix）。

## 行为摘要

- 读取 boundary map 中的 A/B/C 三类 `content_type` 集合。
- 逐条对 sample matrix 中的样本做 **证据路由决策**（eligible / conditional / symbol / glyph / layout / rejected）。
- 汇总为 `ocr_evidence_routing_pack.json`，并计算门控前后 **False Text Risk**、**Eligibility Accuracy（proxy）** 及失真防控静态检查。

## 边界（硬约束）

- `runtime_integration=false`、`whitebox_integration=false`、`mainline_side_effect=false`。
- 不调用 OCR provider；不改变主线 OCR routing。
