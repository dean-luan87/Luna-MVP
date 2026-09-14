# LUNA — YOLO × OCR Offline Bridge Regression v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-004** — 只读 Bridge-002 / Bridge-003 evidence roots 的回归验收与 closure 基线登记。

## Regression Inputs（只读）

- skeleton-root（Bridge-002）：`logs/yolo_ocr_offline_bridge_002_20260429_151332`
- evidence-root（Bridge-003）：`logs/yolo_ocr_offline_bridge_003_20260429_154500`

本阶段不生成新 evidence、不接 runtime、不接中台、不进入下游。

## Regression Tooling

1. `tools/run_yolo_ocr_bridge_regression_v0.py`
   - 输出到：`logs/yolo_ocr_bridge_regression_004_<timestamp>/`
   - 产物：
     - `yolo_ocr_bridge_regression_summary.json`
     - `yolo_ocr_bridge_regression_matrix.json`
     - `yolo_ocr_bridge_schema_matrix.json`
     - `yolo_ocr_bridge_boundary_summary.json`
     - `yolo_ocr_bridge_attribution_summary.json`
     - `regression_notes.md`

2. `tools/verify_yolo_ocr_bridge_regression_v0.py`
   - 对 regression output_root 做强门槛验证，并给出 verdict（GO / CONDITIONAL_GO / NO_GO）。

## Hard Gates（冻结）

同时满足（概念口径）：

- Bridge-002 root 可读
- Bridge-003 root 可读
- Bridge-002 verifier 通过
- Bridge-003 verifier 通过
- `proposal_generated_count > 0`
- `bridge_result_generated_count > 0`
- OCR source policy id 存在
- YOLO attribution 与 OCR attribution 存在
- governance leakage = 0
- `candidate_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`
- `downstream_invocation_count=0`
- trace/replay/whitebox 完整且非空
- 不修改 YOLO closed_v0 / OCR closed_v0（离线 bridge 证据只读）

## Sample Scale Limitation Register

本次 evidence-root 的真实解析规模较小（minimal evidence run）。
回归验收会把规模限制显式登记到 regression summary / notes，并在 closure 里给出 future branches。

