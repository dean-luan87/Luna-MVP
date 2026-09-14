# Luna OCR Lightweight Real Provider Adapter v0

**Phase**: `Phase-OCR-Lightweight-Real-Provider-Adapter-001`  
**判定目标**: **GO** 表示在 **单一轻量真实 provider（当前为 `rapidocr_candidate`）** 下，**feature flag 显式开启** 时可受控调用；**默认**仍为 stub；**不**启用 PaddleOCR runtime、**不**替换 RapidOCR、**不**改生产 routing、**不**进入 MidPlatform、**不**写 WorldModel。

## 前置（建议）

- `Phase-OCR-Real-Provider-Adapter-Selection-001` = GO  
- `Phase-OCR-Mainline-Minimal-Bridge-001` = GO  
- `Phase-OCR-ImageInput-Normalization-Pipeline-001` = GO  
- [LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md](./LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md)（治理文档）  
- OCR Input Size Governance（评测索引）

## 代码位置

| 文件 | 作用 |
|------|------|
| `capabilities/ocr_runtime/ocr_lightweight_provider_adapter_v0.py` | 轻量输入约束：`evaluate_lightweight_provider_input_pack_v0`、默认 **512px 边长上限**（`LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX`）。 |
| `capabilities/ocr_runtime/ocr_rapidocr_provider_adapter_v0.py` | `RapidOCRProviderAdapterV0`：`health_check` / `estimate_cost` / `run`（可选依赖 `rapidocr_onnxruntime` 或 `rapidocr`）。 |
| `capabilities/ocr_runtime/ocr_provider_registry_v0.py` | `rapidocr_candidate` 仅在 `LUNA_ENABLE_OCR_REAL_PROVIDER_V0` ∧ `LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0` 时 **enabled**。 |
| `capabilities/ocr_runtime/ocr_provider_selection_v0.py` | 结合 **input_pack** 与 **health** 选择 Rapid 或回退 stub；误配置（Paddle on 且 real off）仍硬拒绝。 |
| `capabilities/ocr_runtime/ocr_mainline_bridge_v0.py` | 调用后根据 `provider_result.real_provider_invoked` 回填 **audit.real_provider_invoked**。 |

## Feature flags

| 变量 | 默认 | 语义 |
|------|------|------|
| `LUNA_ENABLE_OCR_REAL_PROVIDER_V0` | `false` | 总开关：为 `false` 时 registry 不启用 Rapid。 |
| `LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0` | `false` | 轻量 Rapid 路径开关（与 real 同时为 true 才启用 registry 行）。 |
| `LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0` | `false` | 必须为 false 方走本阶段轻量路径；与 real 同时为 true 时 **不选 Rapid**（仅 stub），避免与 heavy 路径混淆。 |
| `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX` | `512` | 进入真实轻量 adapter 的 **单 unit** 最大宽高（**禁止**大图原尺寸直通）。 |
| `LUNA_OCR_RAPIDOCR_FORCE_UNAVAILABLE_V0` | `false` | 仅评测：强制 `health_check` 为 unavailable，验证回退 stub。 |

## 允许的 `input_pack`（单 unit）

- `full_image`、`downscaled_full_image`、`roi`（当前规范化管线主要产出前两者的单 unit）。  
- **拒绝**：`processing_policy.strategy == "tile"`、多 unit、`unit_type == "tile"`、边长超过 `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX`（超大图即便已 CONDITIONAL_ALLOW，只要 unit 仍为大尺寸即 **拒绝真实 provider**，回退 stub）。

## `run()` 输出（Rapid）

- `text_items[]`、`text_joined`、`duration_ms`、`provider_raw_ref`、`error`、`call_method=lightweight_runtime`、`real_provider_invoked`（仅在实际跑推理且未异常时为 true）。

## 评测

- Adapter 路径（含 A/B/C/D）：[LUNA_EVALUATION_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_SMOKE_V0.md)。  
- **非空文本**小图 smoke（GO / CONDITIONAL_GO）：[LUNA_EVALUATION_OCR_LIGHTWEIGHT_PROVIDER_TEXT_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_OCR_LIGHTWEIGHT_PROVIDER_TEXT_SMOKE_V0.md)（非 benchmark）。  
- **归一化大图 smoke**（`downscaled_full_image` → Rapid）：[LUNA_EVALUATION_OCR_LIGHTWEIGHT_PROVIDER_NORMALIZED_INPUT_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_OCR_LIGHTWEIGHT_PROVIDER_NORMALIZED_INPUT_SMOKE_V0.md)。

## 后续

- 将轻量上限与治理 `downscale_policy` 对齐（分环境调 `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX`）。  
- **PaddleOCR** 仅作为 Level-2 heavy 候选，待进程隔离与性能闸门成熟后再开独立 phase。
