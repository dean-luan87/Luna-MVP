# Luna 评测 — Vision Recognition Adapter Selection Smoke GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_vision_lightweight_recognition_adapter_selection_smoke_v0.py`  
**Phase**：`Phase-Vision-Lightweight-Recognition-Adapter-Selection-001`

## GO

- ROI 根下 **input pack** 存在；输出根下 **summary / registry_snapshot / selection_report / stub_result / candidate_matrix / audit** 齐全。  
- `input_units` 合计 **> 0**；stub **`items`** 数量 **> 0**。  
- `vision_provider_selection_report_v0`：`selected_provider=vision_stub`，`selected_provider_level=stub`，`real_provider_invoked=false`。  
- 每个 stub item 有 **`unit_id`**，且有 **`roi_id`** 或 **`source_unit_ref`**。  
- `vision_provider_registry_snapshot`：`schema_version=vision_provider_registry_v0`。  
- audit：`vision_provider_selection_executed=true`，`selected_provider=vision_stub`，`full_frame_direct_to_provider=false`，禁止类字段均为 **false**。

## CONDITIONAL_GO

- 无 **NO_GO** blockers，但存在 **soft_notes**（例如 `stub_result` 缺少显式 `synthetic=true`，或 matrix 行数与 units 不完全对齐等）。

## NO_GO

- **调用**或 audit 暗示 **YOLO / Supervision 主线 / VLM**（对应 `*_invoked` 非 false）。  
- **整帧直送** provider：`full_frame_direct_to_provider=true`。  
- **MidPlatform / Scene Delta / WorldModel / 导航 / OCR / AI interpretation** 被标记为已发生。  
- **audit 缺失**或关键产物缺失；`selected_provider` 非 `vision_stub`；stub **items** 为空。

## 一句话

本 smoke **只**验证 registry + selection + **stub** synthetic 结果链；**不**加载或调用任何真实视觉模型。
