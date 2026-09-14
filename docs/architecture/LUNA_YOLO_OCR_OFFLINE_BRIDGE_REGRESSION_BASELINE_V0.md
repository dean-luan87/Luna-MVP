# LUNA — YOLO × OCR Offline Bridge Regression Baseline v0

## Baseline Roots（冻结）

- skeleton-root（Bridge-002）：`logs/yolo_ocr_offline_bridge_002_20260429_151332`
  - verifier：`tools/verify_yolo_ocr_offline_bridge_v0.py`（需读入并通过）

- evidence-root（Bridge-003 最小真实证据）：`logs/yolo_ocr_offline_bridge_003_20260429_154500`
  - verifier：`tools/verify_yolo_ocr_bridge_evidence_run_v0.py`（需通过）

## Hard Requirements（冻结）

- governance leakage = 0
- candidate-only / raw-text-only flags 均满足
- trace/replay/whitebox 完整且非空
- source attribution（YOLO + OCR）完整
- OCR offline source policy id 存在且一致

## Allowed Drifts（允许波动）

- raw text 内容与 OCR candidate count
- latency 与检测数量（数量越大越好，但不是必须）

## Not Allowed Drifts（禁止波动）

- governance leakage 非 0
- attribution 缺失或 OCR policy id 缺失
- trace/replay/whitebox 缺失
- runtime / downstream / TTS / semantic summary / navigation 等越界触发

