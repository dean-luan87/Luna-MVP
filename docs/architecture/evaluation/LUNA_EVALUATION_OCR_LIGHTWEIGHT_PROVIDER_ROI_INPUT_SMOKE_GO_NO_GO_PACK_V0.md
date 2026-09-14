# Luna Evaluation — OCR Lightweight Provider ROI Input Smoke GO / NO_GO Pack v0

**Phase**: `Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001`  
**Verifier**: `tools/evaluation/ocr/verify_ocr_lightweight_provider_roi_input_smoke_v0.py`

## 语义边界

- **GO** 只表示：在合规 ROI input_pack 下 **RapidOCR 被选中并成功调用**，且 **`text_joined` 非空**、audit / coordinate_transform / bridge_pack 完整。  
- **不等于** OCR 质量验收、默认 provider、MidPlatform、整图/tile 真实 OCR、或 Paddle 可接入。

## GO

- 原图与 ROI 图产物存在；`input_units[0].unit_type == roi`；`bbox_in_original` 为合法 xyxy。  
- `coordinate_transform` 含 `offset_x`、`offset_y`（crop 原点）；`coordinate_transform_recorded == true`。  
- `original_image_used_directly != true`（真实 provider 不得整图直通）。  
- `selected_provider == rapidocr_candidate`；`real_provider_invoked == true`；`bridge_pack` 合法。  
- `paddleocr_invoked`、`rapidocr_replaced`、`ocr_routing_changed`、`midplatform_invoked`、`world_model_written` 等禁止项为 **false**（或缺失视为 false）。  
- `text_joined` 非空（且不为伪造：以主线 `ocr_evidence` 为准）。

## CONDITIONAL_GO

- Pack / bbox / transform / audit 合规，且 **RapidOCR 已调用** 但 **`text_joined` 为空**（依赖与图像内容导致空识别，不伪造文本）。  
- 或 **回退 `ocr_stub`**，但 `provider_selection_reason_codes` / `provider_unavailable_reason` 能解释（runtime 不可用、import、轻量 pack 拒绝等）。

## NO_GO

- 原图或 ROI 图缺失；unit 非 `roi`；缺少 bbox 或 offset 记录。  
- 整图直通真实 provider（`original_image_used_directly == true` 且与 ROI 语义冲突）。  
- PaddleOCR 被调用、routing 被改、Rapid 被替换、进入 MidPlatform / WorldModel、audit 禁止项为 true。  
- 选中 Rapid 但 `real_provider_invoked` 不为 true，或 bridge_pack 缺失。  
- Stub 回退但 **无**可解释 reason。  
- 伪造成功（例如宣称 Rapid 成功但 audit 与 `provider_result` 不一致——本 verifier 以落盘 JSON 一致性做静态检查）。
