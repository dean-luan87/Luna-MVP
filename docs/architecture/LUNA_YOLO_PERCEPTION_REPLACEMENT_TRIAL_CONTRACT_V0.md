# LUNA — YOLO Shadow PerceptionEval Replacement Trial Contract v0 (Phase-ModelPerception-006)

## Contract scope
本 contract 仅约束 **replacement trial 输出**（离线评测产物），不产生任何 runtime 接入效力。

## Required signals (Perception-001 five)
Replacement trial 每条样本必须包含以下五类 signals（key 必须存在，且为 dict）：
- `object_stability_signal`
- `spatial_passability_signal`
- `risk_field_signal`
- `ocr_navigation_signal`
- `dynamic_event_signal`

### Minimum candidate-only constraints (hard)
每条样本必须满足：
- `allows_execute_now == false`（candidate-only）
- leakage counters 均为 0：
  - execute leakage
  - default-on leakage
  - release/retry/reopen leakage
  - side effects expansion

## Unsupported capability honesty (hard)
在 detection-first v0 中必须显式保持“不支持项”为不可用：
- `ocr_navigation_signal.status == "not_available"`
- `dynamic_event_signal.status == "not_available"`
- `spatial_passability_signal.depth_unavailable == true`
- `risk_field_signal.collision_risk_not_confirmed == true`

## Evidence boundary (hard)
每条样本必须保持：
- evidence_type == `phone_local_controlled_capture`
- controlled_live_stream == false
- phone_local_capture == true

并且 YOLO shadow 输出侧的边界声明必须保持：
- `evidence_type_preserved == true`
- `controlled_live_stream_false == true`

## Non-goals (explicit)
Replacement trial 不得被解释为：
- depth / OCR / dynamic / collision risk 已验证
- 真实导航能力
- 可进入 SceneTask/Fusion/Output
- 可执行任何导航动作

